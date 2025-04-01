from psychopy import visual, core
def CountDown(win, start=3, interval=1.0):
    countdown_text = visual.TextStim(win, height=0.6, wrapWidth=10, color='black', pos=[0, 0])
    
    for i in range(start, 0, -1):
        countdown_text.text = f'Task will begin in {i} s'
        countdown_text.draw()
        win.flip()
        core.wait(interval)


def RealTimeCountDown(win, duration=3):
    countdown_text = visual.TextStim(win, height=0.6, wrapWidth=10, color='black', pos=[0, 0])
    timer = core.Clock()
    
    while timer.getTime() < duration:
        time_left = duration - timer.getTime()
        countdown_text.text = f'Task will begin in {int(time_left) + 1} s'  # +1 to avoid displaying '0 s'
        countdown_text.draw()
        win.flip()
