from psyflow import BlockUnit,StimBank, StimUnit,SubInfo,TaskSettings,TriggerSender,load_config,count_down
import pandas as pd
from psychopy.visual import Window
from psychopy.hardware import keyboard
from psychopy import logging, core
from functools import partial
import serial
from src import run_trial,Controller, generate_valid_conditions

# 1. Load config
cfg = load_config()

# 2. Collect subject info
subform = SubInfo(cfg['subform_config'])
subject_data = subform.collect()

# 3. Load task settings
settings = TaskSettings.from_dict(cfg['task_config'])
settings.add_subinfo(subject_data)

# 4. setup triggers
settings.triggers = cfg['trigger_config']
ser = serial.serial_for_url("loop://", baudrate=115200, timeout=1)
trigger_sender = TriggerSender(
    trigger_func=lambda code: ser.write([1, 225, 1, 0, (code)]),
    post_delay=0,
    on_trigger_start=lambda: ser.open() if not ser.is_open else None,
    on_trigger_end=lambda: ser.close()
)

# 5. Set up window & input
win = Window(size=settings.size, fullscr=settings.fullscreen, screen=1,
             monitor=settings.monitor, units=settings.units, color=settings.bg_color,
             gammaErrorPolicy='ignore')
kb = keyboard.Keyboard()
settings.frame_time_seconds =win.monitorFramePeriod
settings.win_fps = win.getActualFrameRate()

# 6. Set up logging
logging.setDefaultClock(core.Clock())
logging.LogFile(settings.log_file, level=logging.DATA, filemode='a')
logging.console.setLevel(logging.INFO)

# 7. Setup stimulus bank
stim_bank = StimBank(win,cfg['stim_config']).preload_all()
# stim_bank.preview_all() 

# 8. Setup controller across blocks
controller = Controller.from_dict(cfg['controller_config'])

# 9. Start experiment
StimUnit(win, 'instruction_text').add_stim(stim_bank.get('instruction_text')).wait_and_continue()
all_data = []
for block_i in range(settings.total_blocks):
    count_down(win, 3, color='white')
    # 8. setup block
    block = BlockUnit(
        block_id=f"block_{block_i}",
        block_idx=block_i,
        settings=settings,
        window=win,
        keyboard=keyboard
    ).generate_conditions(func=generate_valid_conditions)\
    .on_start(lambda b: trigger_sender.send(settings.triggers.get("block_onset")))\
    .on_end(lambda b: trigger_sender.send(settings.triggers.get("block_end")))\
    .run_trial(partial(run_trial, stim_bank=stim_bank, controller=controller, trigger_sender=trigger_sender))\
    .to_dict(all_data)\
    
    # get block data and statistics
    # Separate go and stop trials
    go_trials = block.get_trial_data(key='condition', pattern='go', match_type='startswith')
    stop_trials = block.get_trial_data(key='condition', pattern='stop', match_type='startswith')

    # --- For go trials ---
    num_go = len(go_trials)
    num_go_hit = sum(trial.get('go_hit', False) for trial in go_trials)
    go_hit_rate = num_go_hit / num_go if num_go > 0 else 0

    # --- For stop trials ---
    num_stop = len(stop_trials)
    # Correct stop success definition
    num_stop_success = sum(
        (not trial.get('go_ssd_key_press', False)) and 
        (not trial.get('stop_unit_key_press', False)) 
        for trial in stop_trials
    )
    stop_success_rate = num_stop_success / num_stop if num_stop > 0 else 0

    # show block break screen and statistics
    StimUnit(win, 'block').add_stim(stim_bank.get_and_format('block_break', 
                                                             block_num=block_i+1,
                                                             total_blocks=settings.total_blocks,
                                                             go_accuracy=go_hit_rate,
                                                             stop_accuracy=stop_success_rate)).wait_and_continue()
# end of experiment
StimUnit(win, 'block').add_stim(stim_bank.get('good_bye')).wait_and_continue(terminate=True)
    
# 10. Save data
df = pd.DataFrame(all_data)
df.to_csv(settings.res_file, index=False)
settings.save_to_json()

# 11. Close everything
win.close()
core.quit()



