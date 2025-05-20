from typing import Dict, List, Optional
from psychopy import logging

class Controller:
    """
    Controller dynamically adjusts the stop‐signal delay (ssd) based on stop‐trial performance,
    aiming to hit a specified stop‐success rate (defaults to 50%).
    """

    def __init__(
        self,
        initial_ssd: float = 0.25,
        min_ssd: float = 0.05,
        max_ssd: float = 0.5,
        step: float = 0.05,
        target_success: float = 0.5,
        condition_specific: bool = False,
        enable_logging: bool = True
    ):
        self.initial_ssd    = initial_ssd
        self.min_ssd        = min_ssd
        self.max_ssd        = max_ssd
        self.step           = step
        self.target_success = target_success
        self.condition_specific = condition_specific
        self.enable_logging = enable_logging

        # keyed by stim ('left'/'right') or None if pooling
        self.ssds      : Dict[Optional[str], float] = {}
        self.histories : Dict[Optional[str], List[bool]] = {}

    @classmethod
    def from_dict(cls, config: dict) -> "Controller":
        allowed = {
            "initial_ssd": 0.25,
            "min_ssd":     0.05,
            "max_ssd":     0.5,
            "step":        0.05,
            "target_success": 0.5,
            "condition_specific": False,
            "enable_logging": True
        }
        extra = set(config) - set(allowed)
        if extra:
            raise ValueError(f"[Controller] Unsupported keys: {extra}")
        params = {k: config.get(k, default) for k, default in allowed.items()}
        return cls(**params)

    def _key(self, stim: Optional[str]) -> Optional[str]:
        return stim if self.condition_specific else None

    def get_ssd(self, stim: Optional[str] = None) -> float:
        key = self._key(stim)
        if key not in self.ssds:
            self.ssds[key] = self.initial_ssd
            self.histories[key] = []
        return self.ssds[key]

    def update(self, success: bool, stim: Optional[str] = None):
        """
        Call after each stop trial.
        `success=True` means the subject successfully stopped (no response).
        """
        key = self._key(stim)
        if key not in self.ssds:
            # initialize on first use
            self.ssds[key] = self.initial_ssd
            self.histories[key] = []

        self.histories[key].append(success)
        rate = sum(self.histories[key]) / len(self.histories[key])
        old = self.ssds[key]

        if rate > self.target_success:
            new = min(self.max_ssd, old + self.step)
        else:
            new = max(self.min_ssd, old - self.step)

        self.ssds[key] = new

        if self.enable_logging:
            label = f"[{stim}]" if stim else ""
            logging.data(
                f"[Controller]{label} Trials:{len(self.histories[key])} "
                f"Success:{rate:.0%} ssd:{old:.3f}→{new:.3f}"
            )

    def describe(self):
        print("=== SST Controller Status ===")
        for k, hist in self.histories.items():
            label = f"[{k}]" if k else "[all]"
            rate = sum(hist)/len(hist)
            ssd = self.ssds[k]
            print(f"{label} success {rate:.2%} over {len(hist)} trials → ssd {ssd:.3f}s")


import random
import numpy as np
from typing import List, Optional

def generate_sst_conditions(
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
