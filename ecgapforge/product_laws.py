# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from ecgapforge.graphs.claim_bans import build_graph as claim_bans
    from ecgapforge.graphs.fetch_nwis import build_graph as fetch_nwis
    from ecgapforge.graphs.no_p_sfha import build_graph as no_p_sfha
    from ecgapforge.graphs.temporal_split import build_graph as temporal_split

    return [
        {
            "id": "ecgap.no_p_sfha",
            "build": no_p_sfha,
            "state": {"p_sfha_feature": False, "p_sfha_label": False, "p_sfha_figure": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "ecgap.temporal_split",
            "build": temporal_split,
            "state": {"temporal_ok": True, "lag1_locked": True, "indy_predictor": False, "invented_tributary": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "ecgap.fetch_nwis",
            "build": fetch_nwis,
            "state": {
                "nwis_ok": True,
                "eagle_creek_ok": True,
                "eagle_creek_on_time": True,
                "nwm_repull": False,
                "invented_tributary": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "ecgap.claim_bans",
            "build": claim_bans,
            "state": {
                "lag_as_wet_mask": False,
                "flood_warning": False,
                "feet_invert": False,
                "closed_reach": False,
                "n_figures": 2,
            },
            "allow_decisions": ["allow"],
        },
    ]
