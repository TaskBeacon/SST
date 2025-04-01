import numpy as np
import random
def SetupSeed(settings, subdata, mode="indiv"):
    """
    Sets up random seed strategy for trial sequence generation.

    Args:
        settings (SimpleNamespace): Settings object to update.
        subdata (list): Subject info, where subdata[0] is subject ID.
        mode (str): Randomization mode.
            - "random": no seed at all (fully random every time)
            - "same": fixed seed shared by all participants
            - "indiv": per-subject seed based on subject ID
    """
    if mode == "random":
        settings.GeneralSeed = None
        settings.blockSeed = None
        print("[INFO] Trial sequence mode: fully random (no seed).")

    else:
        # Assign general seed based on mode
        if mode == "same":
            settings.GeneralSeed = 123
            print("[INFO] Trial sequence mode: same for all participants.")
        elif mode == "indiv":
            settings.GeneralSeed = int(subdata[0])
            print(f"[INFO] Trial sequence mode: individualized. Seed = {settings.GeneralSeed}")
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'random', 'same', or 'indiv'.")

        # Apply global seed
        random.seed(settings.GeneralSeed)
        np.random.seed(settings.GeneralSeed)

        # Generate per-block seeds for fine-grained control
        settings.blockSeed = np.random.randint(0, 100000, size=settings.TotalBlocks)
        print(f"[INFO] Per-block seeds: {settings.blockSeed}")
    return settings
