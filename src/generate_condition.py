import random
import numpy as np
from typing import List, Optional

def generate_valid_conditions(
    n_trials: int,
    condition_labels: Optional[List[str]] = None,
    stop_ratio: float = 0.25,
    max_stop_run: int = 4,
    min_go_start: int = 3,
    seed: Optional[int] = None
) -> np.ndarray:
    """
    As before, but uses a local RNG so the global random state is untouched.
    """
    # 1) Prepare labels
    if condition_labels is None:
        condition_labels = ['go_left', 'go_right', 'stop_left', 'stop_right']
    go_labels   = [lbl for lbl in condition_labels if lbl.startswith('go')]
    stop_labels = [lbl for lbl in condition_labels if lbl.startswith('stop')]

    # 2) Compute how many of each
    n_stop = int(round(n_trials * stop_ratio))
    n_go   = n_trials - n_stop

    base_go,     rem_go     = divmod(n_go,   len(go_labels))
    base_stop,   rem_stop   = divmod(n_stop, len(stop_labels))

    counts = {}
    for i, lbl in enumerate(go_labels):
        counts[lbl] = base_go   + (1 if i < rem_go   else 0)
    for i, lbl in enumerate(stop_labels):
        counts[lbl] = base_stop + (1 if i < rem_stop else 0)

    # 3) Build the flat trial list
    trial_list = []
    for lbl, cnt in counts.items():
        trial_list.extend([lbl] * cnt)

    # 4) Create a local RNG
    rng = random.Random(seed)

    # 5) Shuffle & enforce constraints
    while True:
        rng.shuffle(trial_list)

        # a) First few must be go
        if any(not lbl.startswith('go') for lbl in trial_list[:min_go_start]):
            continue

        # b) No more than max_stop_run stops in any 5-trial window
        violation = False
        for i in range(n_trials - 4):
            window = trial_list[i:i+5]
            if sum(lbl.startswith('stop') for lbl in window) > max_stop_run:
                violation = True
                break
        if violation:
            continue

        break

    return np.array(trial_list, dtype=object)
