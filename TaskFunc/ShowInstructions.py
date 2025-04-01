from psychopy import visual, event
def ShowInstructions(win):
    ins = visual.TextStim(win, height=.6, wrapWidth=25, color='black', pos=[0, 0])
    ins.text = (
        'You will perform a stop signal task. \n'
        'Press q to left arrow and p to right arrow as fast as possible! \n'
        'Sometimes arrow color will change into red. \n'
        'If that happens please withhold your response. \n'
        'Making fast responses and stopping are equally important! \n'
        'Press any key to continue'
    )

    while not event.getKeys():
        ins.draw()
        win.flip()