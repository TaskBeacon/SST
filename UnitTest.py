from psychopy import visual, core
from TaskFunc import *

# CountDown test
win = visual.Window([1920, 1080], monitor="testMonitor", units="deg",
                    screen=1, color='white', fullscr=True, useFBO=True, gammaErrorPolicy='ignore')
# win._monitorFrameRate = 60  # manually set FPS
CountDown(win)
RealTimeCountDown(win)
win.close()

# ShowInstructions test
win = visual.Window([1920, 1080], monitor="testMonitor", units="deg",
                    screen=1, color='white', fullscr=True, useFBO=True, gammaErrorPolicy='ignore')
ShowInstructions(win)
win.close()

# SubjectInformation test
subdata = SubjectInformation()
subdata = ['102', '20', 'Male', 'Caucasian']    

# Initialize test
win, kb, settings = Initialize(subdata)
win.close()
core.quit()

# GenTrialSeq test
trialSeq = GenTrialSeq(settings)
RunTask(win, kb, settings, trialSeq, subdata)
TerminateTask(win)


