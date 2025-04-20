# sst_controller.py

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
