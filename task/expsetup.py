from psychopy import visual
from psychopy.hardware import keyboard
from psychopy.visual import ShapeStim
from types import SimpleNamespace
from datetime import datetime
from psyflow.seedcontrol import setup_seed_for_settings

def exp_setup(subdata):
    """
    Initializes window, stimuli, experiment settings, and keyboard.

    Args:
        subdata (list): Subject info including ID.
    Returns:
        win (visual.Window): The PsychoPy window object.
        kb (keyboard.Keyboard): Keyboard input handler.
        settings (SimpleNamespace): Experimental settings and stimuli.
    """
    win = visual.Window(
        size=[1920, 1080],
        monitor="testMonitor",
        units="deg",
        screen=1,
        color="white",
        fullscr=True,
        gammaErrorPolicy='ignore'  # avoid gamma ramp errors
    )

    # Define settings
    settings = SimpleNamespace()
    settings.TotalBlocks = 2
    settings.TotalTrials = 20
    settings.TrialsPerBlock = settings.TotalTrials // settings.TotalBlocks

    # random seed
    settings = setup_seed_for_settings(settings, subdata, mode="indiv") # each sub will have a unique seed

    # Arrow vertices
    LarrowVert = [(0.2,0.05),(0.2,-0.05),(0,-0.05),(0,-0.1),(-.2,0),(0,0.1),(0,0.05)]
    RarrowVert = [(-0.2,0.05),(-0.2,-0.05),(0,-0.05),(0,-0.1),(.2,0),(0,0.1),(0,0.05)]
    UparrowVert = [(-0.05,-0.2),(0.05,-0.2),(0.05,0),(0.1,0),(0,0.2),(-0.1,0),(-0.05,0)]  # Centered vertical arrow

    # Arrow stimuli
    settings.Larrow = ShapeStim(win, vertices=LarrowVert, fillColor='black', size=8, lineColor=None)
    settings.Rarrow = ShapeStim(win, vertices=RarrowVert, fillColor='black', size=8, lineColor=None)
    settings.LarrowSTOP = ShapeStim(win, vertices=LarrowVert, fillColor='red', size=8, lineColor=None)
    settings.RarrowSTOP = ShapeStim(win, vertices=RarrowVert, fillColor='red', size=8, lineColor=None)
    settings.UparrowSTOP = ShapeStim(win, vertices=UparrowVert, fillColor='black', size=8, lineColor=None)
    
    settings.twoArrows = False  # set True to enable both arrows
    if settings.twoArrows:
        settings.arrowTypes = [1, 2]  # 1 = left, 2 = right
    else:
        settings.arrowTypes = [2]     # only right arrow
    
    # set stop type: 
    settings.useUpArrowStop = False  # if True, show ↑ instead of red ←/→ for stop signal
    

    # Timing and staircase
    settings.initSSD = 200
    settings.staircase = 50
    settings.arrowDuration = 1
    settings.trialDuration = 3

    # Keyboard settings
    settings.left_key = 'q'
    settings.right_key = 'p'
    settings.keyList = [settings.left_key, settings.right_key]
    
    # File naming
    dt_string = datetime.now().strftime("%H%M%d%m")
    settings.outfile = f"Subject{subdata[0]}_{dt_string}.csv"

    kb = keyboard.Keyboard()

    return win, kb, settings
