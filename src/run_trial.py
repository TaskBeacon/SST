from functools import partial
from psyflow import TrialUnit
from .controller import Controller  # your simple 1-up/1-down SSTControllerSimple

def run_trial(
    win,
    kb,
    settings,
    condition: str,           # 'go' or 'stop'
    stim_bank: dict,          # must contain 'fixation': ShapeStim
    controller: Controller,   # 1-up/1-down controller managing ssd
    trigger_bank: dict,       # dict of trigger codes
    trigger_sender=None,
    
):
    """
    Single SST trial:
      - fixation → go (or go→stop) → record acc/RT → update ssd on stop trials
    Returns:
      trial_data dict with fields 'condition','acc','rt','response', + timing/triggers.
    """
    trial_data = {'condition': condition}
    make_unit = partial(TrialUnit, win=win, triggersender=trigger_sender)
    go_stim   = stim_bank.get('go')
    stop_stim = stim_bank.get('stop')
    fix_stim  = stim_bank.get('fixation')
    # 1) Fixation (500 ms)
    make_unit(unit_label='fixation') \
        .add_stim(fix_stim) \
        .show(
            duration=settings.fixation_duration,
            onset_trigger=trigger_bank.get('fixation_onset')
        ) \
        .to_dict(trial_data)



    # 2) Go trial branch
    if condition == 'go':
        go_unit = make_unit(unit_label='go') \
            .add_stim(go_stim) \
            .capture_response(
                keys=settings.key_list,
                duration=settings.go_duration,
                onset_trigger=trigger_bank.get('go_onset'),
                response_trigger=trigger_bank.get('key_press'),
                timeout_trigger=trigger_bank.get('no_response'),
                terminate_on_response=True
            )
        go_unit.to_dict(trial_data)

        resp = go_unit.get_state('response', [])
        rt   = go_unit.get_state('rt', 0)
        trial_data['response'] = resp
        trial_data['rt']       = rt
        trial_data['acc']      = 1   if resp else -1

    # 3) Stop trial branch
    else:
        # 3a) Phase 1: present go_stim for ssd, do NOT terminate on presses
        ssd     = controller.get_ssd()
        go_unit = make_unit(unit_label='go_ssd') \
            .add_stim(go_stim) \
            .capture_response(
                keys=settings.key_list,
                duration=ssd,
                onset_trigger=trigger_bank.get('go_onset'),
                response_trigger=trigger_bank.get('key_press'),
                timeout_trigger=trigger_bank.get('no_response'),
                terminate_on_response=False
            )
        go_unit.to_dict(trial_data)
        resp1 = go_unit.get_state('response', [])
        rt1   = go_unit.get_state('rt', 0)

        # 3b) Phase 2: switch immediately to stop_stim for remaining time
        rem = settings.go_duration - ssd
        stop_unit = make_unit(unit_label='stop') \
            .add_stim(stop_stim) \
            .capture_response(
                keys=settings.key_list,
                duration=rem,
                onset_trigger=trigger_bank.get('stop_onset'),
                response_trigger=trigger_bank.get('key_press'),
                timeout_trigger=trigger_bank.get('no_response'),
                terminate_on_response=True
            )
        stop_unit.to_dict(trial_data)
        resp2 = stop_unit.get_state('response', [])

        # 3c) Determine success/failure
        failed_stop = bool(resp1 or resp2)
       
        # 3d) Update ssd staircase (+/- settings.staircase)
        controller.update(success=not failed_stop)

    return trial_data
