# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from ecgapforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if not state.get("nwis_ok"):
        v.append("nwis_empty")
    if not state.get("eagle_creek_ok"):
        v.append("eagle_creek_empty")
    if not state.get("eagle_creek_on_time"):
        v.append("eagle_creek_late")
    if state.get("nwm_repull"):
        v.append("nwm_repull")
    if state.get("invented_tributary"):
        v.append("invented_tributary")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="ecgap.fetch_nwis",
        evaluate=_evaluate,
        extra=["nwis_ok", "eagle_creek_ok", "eagle_creek_on_time", "nwm_repull", "invented_tributary"],
    )
