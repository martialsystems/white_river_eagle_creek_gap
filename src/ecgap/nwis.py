# Copyright (c) 2026 Martial Systems LLC
"""NWIS daily 00060. Empty Eagle Creek stops the tree."""

from __future__ import annotations

from datetime import date
from typing import Any

import numpy as np

from ecgap.config import CENTERTON_ID, EAGLE_CREEK_ID, FALL_CREEK_ID, NORA_ID, NWIS_DV_URL
from ecgap.errors import FetchError
from ecgap.http import get_json


def parse_dv_q(doc: dict[str, Any]) -> dict[np.datetime64, float]:
    blob = doc.get("value") if isinstance(doc.get("value"), dict) else doc
    out: dict[np.datetime64, float] = {}
    for ts in (blob or {}).get("timeSeries") or []:
        var = ((ts.get("variable") or {}).get("variableCode") or [{}])[0]
        if str(var.get("value") or "") != "00060":
            continue
        for rec in ((ts.get("values") or [{}])[0]).get("value") or []:
            stamp = str(rec.get("dateTime") or "")[:10]
            try:
                val = float(rec.get("value"))
            except (TypeError, ValueError):
                continue
            if stamp and np.isfinite(val):
                out[np.datetime64(stamp)] = val
    return out


def fetch_q(*, site: str, start: date, end: date, get_json_fn=None) -> dict[np.datetime64, float]:
    getter = get_json_fn or get_json
    doc = getter(NWIS_DV_URL.format(site=site, start=start.isoformat(), end=end.isoformat()))
    series = parse_dv_q(doc)
    if not series:
        raise FetchError(f"NWIS daily 00060 is empty for {site}")
    return series


def fetch_four(*, start: date, end: date, get_json_fn=None) -> dict[str, dict[np.datetime64, float]]:
    return {
        NORA_ID: fetch_q(site=NORA_ID, start=start, end=end, get_json_fn=get_json_fn),
        FALL_CREEK_ID: fetch_q(site=FALL_CREEK_ID, start=start, end=end, get_json_fn=get_json_fn),
        EAGLE_CREEK_ID: fetch_q(site=EAGLE_CREEK_ID, start=start, end=end, get_json_fn=get_json_fn),
        CENTERTON_ID: fetch_q(site=CENTERTON_ID, start=start, end=end, get_json_fn=get_json_fn),
    }
