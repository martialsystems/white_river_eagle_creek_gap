# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from ecgapforge.graphs._common import binary_graph

_FLAGS = ("lag_as_wet_mask", "flood_warning", "feet_invert", "closed_reach")


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v = [k for k in _FLAGS if state.get(k)]
    if int(state.get("n_figures") or 0) > 2:
        v.append("figure_cap")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="ecgap.claim_bans", evaluate=_evaluate, extra=[*_FLAGS, "n_figures"])
