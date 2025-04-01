from TaskFunc import *
# all
subdata = SubjectInformation()
win, kb, settings = Initialize(subdata)
trialSeq = GenTrialSeq(settings)
print(trialSeq.stop)
ShowInstructions(win)
CountDown(win)
RunTask(win, kb, settings, trialSeq, subdata)
TerminateTask(win)