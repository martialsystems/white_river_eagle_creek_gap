# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class QPack:
    """Daily 00060. Features are Nora, Fall Creek, Eagle Creek. Centerton is the label."""

    dates: np.ndarray
    nora_cfs: np.ndarray
    fall_creek_cfs: np.ndarray
    eagle_creek_cfs: np.ndarray
    centerton_cfs: np.ndarray
    source: str = "fixture"
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def n_days(self) -> int:
        return int(self.dates.shape[0])
