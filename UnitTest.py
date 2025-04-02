from psychopy import visual, core
from psyflow.screenflow import  *
from task.expsetup import exp_setup
from task.trialcontrol import generate_trial_seq
from task.expcontrol import exp_run

# CountDown test
win = visual.Window([1920, 1080], monitor="testMonitor", units="deg",
                    screen=1, color='white', fullscr=True, useFBO=True, gammaErrorPolicy='ignore')
# win._monitorFrameRate = 60  # manually set FPS
show_static_countdown(win)
show_realtime_countdown(win)
win.close()

# ShowInstructions test
win = visual.Window([1920, 1080], monitor="testMonitor", units="deg",
                    screen=1, color='white', fullscr=True, useFBO=True, gammaErrorPolicy='ignore')
show_instructions(win, intro_text="This is a test")
win.close()


subdata = ['102', '20', 'Male', 'Caucasian']    

# Initialize test
win, kb, settings = exp_setup(subdata)
win.close()
core.quit()

# GenTrialSeq test
trialSeq = generate_trial_seq(settings)
exp_run(win, kb, settings, trialSeq, subdata)
show_goodbye(win)


