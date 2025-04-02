from SST import *
# all
subdata = SubjectInformation()
win, kb, settings = Initialize(subdata)
trialSeq = GenTrialSeq(settings)
print(trialSeq.stop)
intro_test = (
        'You will perform a stop signal task. \n'
        'Press "q" for left arrow and "p" for right arrow as fast as possible! \n'
        'Sometimes the arrow color will turn red. \n'
        'If that happens, please withhold your response. \n'
        'Both fast responding and successful stopping are important. \n\n'
        'Press SPACE to continue.'
    )
ShowInstructions(win,intro_text=intro_test)
CountDown(win)
RunTask(win, kb, settings, trialSeq, subdata)
TerminateTask(win)