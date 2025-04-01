from psychopy import visual, event
def ShowInstructions(win):
    ins = visual.TextStim(win, height=.6, wrapWidth=25, color='black', pos=[0, 0])
    ins.text = (
        'You will perform a stop signal task. \n'
        'Press "q" for left arrow and "p" for right arrow as fast as possible! \n'
        'Sometimes the arrow color will turn red. \n'
        'If that happens, please withhold your response. \n'
        'Both fast responding and successful stopping are important. \n\n'
        'Press SPACE to continue.'
    )

    while not event.getKeys(keyList=['space']):
        ins.draw()
        win.flip()