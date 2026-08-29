# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from ecgapforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if not state.get("temporal_ok"):
        v.append("not_temporal")
    if not state.get("lag1_locked"):
        v.append("lag_not_locked")
    if state.get("indy_predictor"):
        v.append("indy_predictor")
    if state.get("invented_tributary"):
        v.append("invented_tributary")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="ecgap.temporal_split",
        evaluate=_evaluate,
        extra=["temporal_ok", "lag1_locked", "indy_predictor", "invented_tributary"],
    )
