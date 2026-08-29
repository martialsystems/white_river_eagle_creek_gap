# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from ecgapforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from ecgapforge.gate import require_claims, require_fetch, require_no_p_sfha, require_split
from ecgapforge.product_laws import laws


def test_laws() -> None:
    require_no_p_sfha(thread_id="t.p")
    with pytest.raises(LawBlockedError):
        require_no_p_sfha(p_sfha_feature=True, thread_id="t.p.bad")
    require_split(thread_id="t.s")
    with pytest.raises(LawBlockedError):
        require_split(lag1_locked=False, thread_id="t.s.lag")
    with pytest.raises(LawBlockedError):
        require_split(indy_predictor=True, thread_id="t.s.indy")
    require_fetch(nwis_ok=True, eagle_creek_ok=True, eagle_creek_on_time=True, thread_id="t.f")
    with pytest.raises(LawBlockedError):
        require_fetch(nwis_ok=True, eagle_creek_ok=True, eagle_creek_on_time=True, nwm_repull=True, thread_id="t.f.nwm")
    with pytest.raises(LawBlockedError):
        require_fetch(nwis_ok=True, eagle_creek_ok=False, eagle_creek_on_time=True, thread_id="t.f.empty")
    with pytest.raises(LawBlockedError):
        require_fetch(nwis_ok=True, eagle_creek_ok=True, eagle_creek_on_time=False, thread_id="t.f.late")
    require_claims(n_figures=2, thread_id="t.c")
    with pytest.raises(LawBlockedError):
        require_claims(n_figures=3, thread_id="t.c.fig")
    assert {row["id"] for row in laws()} == {
        "ecgap.no_p_sfha",
        "ecgap.temporal_split",
        "ecgap.fetch_nwis",
        "ecgap.claim_bans",
    }
