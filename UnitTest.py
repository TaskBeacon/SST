
from psychopy import visual
from TaskFunc import CountDown, ShowInstructions, SubjectInformation, RealTimeCountDown


win = visual.Window([1920, 1080], monitor="testMonitor", units="deg",
                    screen=1, color='white', fullscr=True, useFBO=True, gammaErrorPolicy='ignore')

win._monitorFrameRate = 60  # manually set FPS
CountDown(win)
RealTimeCountDown(win)

SubjectInformation()
ShowInstructions(win)
CountDown(win)

win.close()
