import numpy as np
import random
from types import SimpleNamespace
import warnings


def generate_trial_seq(settings):
    """
    Generates trial sequence for stop-signal task.

    Args:
        settings (SimpleNamespace): Experiment parameters.

    Returns:
        trialseq (SimpleNamespace): Contains blocknum, stop signal flags, arrow directions, and block-end indices.
    """
    TotalBlocks = settings.TotalBlocks
    TotalTrials = settings.TotalTrials
    TrialsPerBlock = settings.TrialsPerBlock
    arrowTypes = settings.arrowTypes

    ALLrstims = np.zeros(TotalTrials, dtype=int)
    ALLarrows = np.zeros(TotalTrials, dtype=int)
    ALLblocknum = np.zeros(TotalTrials, dtype=int)
    ALLblockEndIdx = np.zeros(TotalTrials, dtype=int)

    for block_i in range(TotalBlocks):
        block_start = block_i * TrialsPerBlock
        block_end = (block_i + 1) * TrialsPerBlock
        blocknum = np.full(TrialsPerBlock, block_i + 1, dtype=int)
        blockEndIdx = np.zeros(TrialsPerBlock, dtype=int)
        blockEndIdx[-1] = 1
        if settings.blockSeed is not None:
            block_seed = int(settings.blockSeed[block_i])
            random.seed(block_seed)
            np.random.seed(block_seed)
        # Create a valid stop-signal sequence
        rstims = generate_valid_rstims(TrialsPerBlock)

        # Generate arrow directions
        arrows = generate_arrow_sequence(rstims, arrowTypes)

        # Fill into block-level arrays
        ALLrstims[block_start:block_end] = rstims
        ALLarrows[block_start:block_end] = arrows
        ALLblocknum[block_start:block_end] = blocknum
        ALLblockEndIdx[block_start:block_end] = blockEndIdx

    if not (len(ALLrstims) == len(ALLblocknum) == len(ALLarrows) == TotalTrials):
        warnings.warn("Trial sequence size mismatch!")

    # Return as structured object
    trialseq = SimpleNamespace()
    trialseq.blocknum = ALLblocknum
    trialseq.BlockEndIdx = ALLblockEndIdx
    trialseq.stop = ALLrstims
    trialseq.arrows = ALLarrows

    return trialseq


def generate_valid_rstims(n_trials, stop_ratio=1/3, max_stop_run=4, min_go_start=3):
    """
    Generate a valid sequence of GO (0) and STOP (1) trials.

    Args:
        n_trials (int): Total number of trials.
        stop_ratio (float): Proportion of stop trials (default = 1/3).
        max_stop_run (int): Max number of stop trials allowed in any 5-trial window.
        min_go_start (int): First N trials must be all GO trials.

    Returns:
        np.ndarray: Array of 0s (GO) and 1s (STOP), length == n_trials
    """
    n_stop = int(n_trials * stop_ratio)
    n_go = n_trials - n_stop

    sflag = False
    attempt = 0
    while not sflag:
        attempt += 1
        # Step 1: Create initial array with exact GO/STOP counts
        trial_types = [0] * n_go + [1] * n_stop
        random.shuffle(trial_types)
        rstims = np.array(trial_types)

        # Step 2: Constraint 1 — First few trials must be GO
        if np.any(rstims[:min_go_start]):
            continue

        # Step 3: Constraint 2 — Max number of stop trials in any sliding window
        window_sums = [sum(rstims[i:i+5]) for i in range(n_trials - 4)]
        if any(w > max_stop_run for w in window_sums):
            continue

        sflag = True  # passed all checks

    return rstims


def generate_arrow_sequence(rstims, arrowTypes):
    """Assigns randomized arrow directions"""
    n_trials = len(rstims)
    arrows = np.zeros(n_trials, dtype=int)

    stop_idx = np.where(rstims == 1)[0]
    go_idx = np.where(rstims == 0)[0]

    arrows_stop = np.tile(arrowTypes, len(stop_idx) // len(arrowTypes))
    arrows_go = np.tile(arrowTypes, len(go_idx) // len(arrowTypes))

    np.random.shuffle(arrows_stop)
    np.random.shuffle(arrows_go)

    for i, idx in enumerate(stop_idx):
        arrows[idx] = arrows_stop[i]
    for i, idx in enumerate(go_idx):
        arrows[idx] = arrows_go[i]

    return arrows
