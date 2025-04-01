import numpy as np
import random
from types import SimpleNamespace
import warnings

def GenTrialSeq(settings):
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
        arrows = generate_arrow_sequence(rstims)

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


def generate_valid_rstims(n_trials):
    """Generates a valid stop/go sequence with constraints."""
    sflag = False
    while not sflag:
        rstims = np.repeat([0, 0, 1], n_trials // 3)
        random.shuffle(rstims)
        rstims = rstims[:n_trials]

        if any(rstims[:3]):  # first 3 trials can't be stop
            continue

        check = [sum(rstims[i:i+5]) for i in range(n_trials - 4)]
        if max(check) >= 5:
            continue
        sflag = True
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

