from psychopy import visual, event, core

def TerminateTask(win):
    outro = visual.TextStim(win, height=0.6, wrapWidth=25, color='black', pos=[0, 0])
    outro.text = "Thanks for your participation!"

    while not event.getKeys():
        outro.draw()
        win.flip()

    win.close()
    core.quit()
