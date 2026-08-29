# Copyright (c) 2026 Martial Systems LLC
"""NWIS only. No NWM. No 2026 overlay. Empty or late Eagle Creek 00060 stops."""

from __future__ import annotations

from datetime import date
from typing import Any

import numpy as np

from ecgap.config import (
    CENTERTON_ID,
    EAGLE_CREEK_ID,
    EAGLE_CREEK_NAME,
    FALL_CREEK_ID,
    LIVE_END,
    LIVE_START,
    NORA_ID,
)
from ecgap.errors import FetchError
from ecgap.nwis import fetch_four
from ecgap.pack import QPack


def _starts_late(values: np.ndarray, dates: np.ndarray, start: date) -> bool:
    ok = np.isfinite(values)
    if not ok.any():
        return False
    first = dates[int(np.flatnonzero(ok)[0])]
    return first > np.datetime64(start.isoformat())


def fetch_live(*, start: date = LIVE_START, end: date = LIVE_END, get_json_fn=None) -> tuple[QPack, dict[str, Any]]:
    series = fetch_four(start=start, end=end, get_json_fn=get_json_fn)
    dates = np.arange(np.datetime64(start.isoformat()), np.datetime64(end.isoformat()) + np.timedelta64(1, "D"))

    def align(site: str) -> np.ndarray:
        m = series[site]
        return np.array([m.get(d, np.nan) for d in dates], dtype=float)

    nora = align(NORA_ID)
    fc = align(FALL_CREEK_ID)
    eagle = align(EAGLE_CREEK_ID)
    cent = align(CENTERTON_ID)
    if not np.isfinite(eagle).any():
        raise FetchError(f"Eagle Creek 00060 is empty at {EAGLE_CREEK_ID} {EAGLE_CREEK_NAME}")
    if _starts_late(eagle, dates, start):
        raise FetchError(
            f"Eagle Creek 00060 starts late at {EAGLE_CREEK_ID} {EAGLE_CREEK_NAME}"
        )
    if not np.isfinite(nora).any():
        raise FetchError("Nora 00060 has no overlap")
    if not np.isfinite(fc).any():
        raise FetchError("Fall Creek 00060 has no overlap")
    if not np.isfinite(cent).any():
        raise FetchError("Centerton 00060 has no overlap")
    pack = QPack(
        dates=dates,
        nora_cfs=nora,
        fall_creek_cfs=fc,
        eagle_creek_cfs=eagle,
        centerton_cfs=cent,
        source="nwis_dv_00060",
        extra={
            "eagle_creek_id": EAGLE_CREEK_ID,
            "eagle_creek_name": EAGLE_CREEK_NAME,
            "sites": [NORA_ID, FALL_CREEK_ID, EAGLE_CREEK_ID, CENTERTON_ID],
        },
    )
    return pack, {"sites": pack.extra["sites"], "n_days": pack.n_days, "eagle_creek_name": EAGLE_CREEK_NAME}
