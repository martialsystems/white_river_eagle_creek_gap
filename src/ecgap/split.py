# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from ecgap.config import HOLDOUT_START, TRAIN_END
from ecgap.errors import SplitError

TRAIN_END64 = np.datetime64(TRAIN_END.isoformat())
HOLDOUT_START64 = np.datetime64(HOLDOUT_START.isoformat())


def as_day(dates: np.ndarray) -> np.ndarray:
    return np.asarray(dates).astype("datetime64[D]")


def temporal_masks(dates: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    d = as_day(dates)
    return d <= TRAIN_END64, d >= HOLDOUT_START64


def assert_temporal(dates: np.ndarray, train: np.ndarray, holdout: np.ndarray) -> None:
    d = as_day(dates)
    train = np.asarray(train, dtype=bool)
    holdout = np.asarray(holdout, dtype=bool)
    if not train.any() or not holdout.any():
        raise SplitError("train or holdout is empty")
    if np.any(train & holdout):
        raise SplitError("train and holdout overlap")
    if np.any(d[train] >= HOLDOUT_START64):
        raise SplitError("holdout dates in train")
    if d[train].max() >= d[holdout].min():
        raise SplitError("not a temporal split")
    if np.any((d >= np.datetime64("2026-08-01")) & (d <= np.datetime64("2026-08-31")) & train):
        raise SplitError("August 2026 in train")
