from psychopy import visual, event, core
import numpy as np

def RunTask(win, kb, settings, trialseq, subdata):
    # Prepare stimuli
    fix = visual.TextStim(win, height=1, text="+", wrapWidth=10, color='black', pos=[0, 0])
    warning = visual.TextStim(win, text="TOO SLOW!!!", height=.6, wrapWidth=10, color='red', pos=[0, 0])
    BlockFeedback = visual.TextStim(win, height=.6, wrapWidth=25, color='black', pos=[0, 0])

    # Shortcuts
    LeftSSD = settings.initSSD
    RightSSD = settings.initSSD
    stairsize = settings.staircase
    keyList = settings.keyList
    left_key = settings.left_key
    right_key = settings.right_key

    # Block-level data container
    class blockdata:
        pass

    blockdata.arrow = []
    blockdata.resp = []
    blockdata.LeftSSD = []
    blockdata.RightSSD = []
    blockdata.RT = []
    blockdata.acc = []
    blockdata.DATA = []
    blockdata.GOidx = []
    blockdata.blockNum = []

    for i in range(len(trialseq.stop)):
        kb.clock.reset()
        kb.clearEvents()
        StopSignal = []

        # Select arrow and (if applicable) stop signal
        if trialseq.arrows[i] == 1:
            arrow = settings.Larrow
            if trialseq.stop[i] == 1:
                StopSignal = settings.LarrowSTOP
        else:
            arrow = settings.Rarrow
            if trialseq.stop[i] == 1:
                StopSignal = settings.RarrowSTOP

        trial_onset = core.getTime()

        # Fixation
        fix.draw()
        win.flip()
        core.wait(0.5)

        # GO stimulus
        arrow.draw()
        win.flip()
        arrow_onset = core.getTime()

        if trialseq.stop[i] == 0:
            blockdata.GOidx = np.hstack((blockdata.GOidx, 1))
            event.clearEvents()
            resp = event.waitKeys(maxWait=settings.arrowDuration, keyList=keyList)

            if resp:
                RT = core.getTime() - arrow_onset
                key = resp[0]
                if trialseq.arrows[i] == 1 and key == left_key:
                    acc = 1
                elif trialseq.arrows[i] == 2 and key == right_key:
                    acc = 1
                else:
                    acc = 0
            else:
                acc = -1
                RT = 0
                warning.draw()
                win.flip()
                core.wait(settings.trialDuration - (core.getTime() - trial_onset))

        else:
            blockdata.GOidx = np.hstack((blockdata.GOidx, 0))
            event.clearEvents()

            if trialseq.arrows[i] == 1:
                core.wait(LeftSSD / 1000)
            else:
                core.wait(RightSSD / 1000)

            StopSignal.draw()
            win.flip()
            arrow_onset = core.getTime()

            if trialseq.arrows[i] == 1:
                resp = event.waitKeys(maxWait=settings.arrowDuration - LeftSSD / 1000, keyList=keyList)
                if resp:
                    acc = 4
                    RT = core.getTime() - arrow_onset
                    LeftSSD = max(LeftSSD - stairsize, 0)
                else:
                    acc = 3
                    RT = 0
                    LeftSSD += stairsize
            else:
                resp = event.waitKeys(maxWait=settings.arrowDuration - RightSSD / 1000, keyList=keyList)
                if resp:
                    acc = 4
                    RT = core.getTime() - arrow_onset
                    RightSSD = max(RightSSD - stairsize, 0)
                else:
                    acc = 3
                    RT = 0
                    RightSSD += stairsize

        # Convert key response to numeric
        if resp and resp[0] == left_key:
            resp_code = 1
        elif resp and resp[0] == right_key:
            resp_code = 2
        else:
            resp_code = 0

        # Log data
        blockdata.RT = np.hstack((blockdata.RT, int(RT * 1000)))
        blockdata.arrow = np.hstack((blockdata.arrow, trialseq.arrows[i]))
        blockdata.resp = np.hstack((blockdata.resp, resp_code))
        blockdata.blockNum = np.hstack((blockdata.blockNum, trialseq.blocknum[i]))
        blockdata.acc = np.hstack((blockdata.acc, acc))
        blockdata.LeftSSD = np.hstack((blockdata.LeftSSD, LeftSSD))
        blockdata.RightSSD = np.hstack((blockdata.RightSSD, RightSSD))

        # ITI
        if acc != -1:
            fix.draw()
            win.flip()
            core.wait(2.5 - (core.getTime() - trial_onset))

        # End of block
        if trialseq.BlockEndIdx[i] == 1:
            STOPidx = blockdata.GOidx == 0
            MISSidx = blockdata.acc == -1
            RJTidx = STOPidx + MISSidx
            GOrtOnly = np.delete(blockdata.RT, np.where(RJTidx), 0)
            meanGOrt = np.mean(GOrtOnly)
            GOtrials = np.sum(blockdata.GOidx == 1)
            CorrectGO = np.sum(blockdata.acc == 1)
            STOPtrials = np.sum(blockdata.GOidx == 0)
            SuccesfulStop = np.sum(blockdata.acc == 3)

            BlockFeedback.text = f"End of Block #{trialseq.blocknum[i]}\n"
            BlockFeedback.text += f"Mean GO RT : {meanGOrt:.2f} ms\n"
            BlockFeedback.text += f"Accuracy : {CorrectGO / GOtrials * 100:.2f} %\n"
            BlockFeedback.text += f"p(STOP) : {SuccesfulStop / STOPtrials * 100:.2f} %\n"

            temp = np.hstack([
                blockdata.blockNum.reshape(-1, 1),
                abs(blockdata.GOidx - 1).reshape(-1, 1),
                blockdata.arrow.reshape(-1, 1),
                blockdata.resp.reshape(-1, 1),
                blockdata.LeftSSD.reshape(-1, 1),
                blockdata.RightSSD.reshape(-1, 1),
                blockdata.acc.reshape(-1, 1),
                blockdata.RT.reshape(-1, 1),
            ])

            if trialseq.blocknum[i] == 1:
                blockdata.DATA = temp
            else:
                blockdata.DATA = np.vstack([blockdata.DATA, temp])

            np.savetxt(settings.outfile, blockdata.DATA,
                       header="Block,TrialType,Arrow,Response,leftSSD,rightSSD,ACC,RT",
                       fmt='%4i', delimiter=',',
                       footer=','.join(subdata))

            # Show feedback
            while not event.getKeys():
                BlockFeedback.draw()
                win.flip()

            # Adaptive message
            if trialseq.blocknum[i] < settings.TotalBlocks:
                PerformanceFeedback = visual.TextStim(win, height=.6, wrapWidth=25, color='black', pos=[0, 0])
                stop_rate = SuccesfulStop / STOPtrials
                if stop_rate <= .45:
                    PerformanceFeedback.text = (
                        "You're fast, but not stopping well.\n"
                        "Focus more on stopping in the next block.\nThanks."
                    )
                elif stop_rate >= .55:
                    PerformanceFeedback.text = (
                        "You're stopping well, but responding slowly.\n"
                        "Try to respond faster in the next block.\nThanks."
                    )
                else:
                    PerformanceFeedback.text = "You're doing great!\nKeep it up!"

                while not event.getKeys():
                    PerformanceFeedback.draw()
                    win.flip()

                blockdata.arrow = []
                blockdata.resp = []
                blockdata.LeftSSD = []
                blockdata.RightSSD = []
                blockdata.RT = []
                blockdata.acc = []
                blockdata.GOidx = []
                blockdata.blockNum = []

                CountDown(win)
