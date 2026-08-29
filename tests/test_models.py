# Copyright (c) 2026 Martial Systems LLC

import json
from pathlib import Path

from ecgap.config import (
    CENTERTON_ID,
    EAGLE_CREEK_ID,
    FALL_CREEK_CENTERTON_NORA_FC_RMSE_CFS,
    FALL_CREEK_ID,
    INDY_ID,
    LITTLE_EAGLE_ID,
    NORA_ID,
    NWM_CENTERTON_PERS_RMSE_CFS,
)

LIVE_REPORT = Path(__file__).resolve().parents[1] / "logs" / "nora_live" / "stage_c_report.json"
from ecgap.errors import LeakError
from ecgap.fixture import build_fixture
from ecgap.models import assert_features_clean, fit_pack


def test_fixture_eagle_beats_nora_fc() -> None:
    fit = fit_pack(build_fixture())
    assert fit["lag_days"] == 1
    assert fit["lag1_locked"] is True
    assert fit["predictor_sites"] == [NORA_ID, FALL_CREEK_ID, EAGLE_CREEK_ID]
    assert INDY_ID not in fit["predictor_sites"]
    assert CENTERTON_ID not in fit["predictor_sites"]
    assert LITTLE_EAGLE_ID not in fit["predictor_sites"]
    assert_features_clean(fit)
    skill = fit["skill"]
    assert skill["nora_fc_eagle"]["rmse_cfs"] < skill["nora_plus_fall_creek"]["rmse_cfs"]
    assert skill["nora_fc_eagle"]["coef_eagle_creek"] > 0.3
    assert skill["nwm_cited"]["source"] == "fa2e315"
    dirty = dict(fit)
    dirty["predictor_sites"] = [NORA_ID, FALL_CREEK_ID, EAGLE_CREEK_ID, INDY_ID]
    try:
        assert_features_clean(dirty)
        raise AssertionError("expected leak")
    except LeakError:
        pass


def test_live_two_feature_matches_fall_creek_citation() -> None:
    if not LIVE_REPORT.is_file():
        return
    report = json.loads(LIVE_REPORT.read_text(encoding="utf-8"))
    two = report["skill"]["nora_plus_fall_creek"]["rmse_cfs"]
    pers = report["skill"]["persistence_target"]["rmse_cfs"]
    three = report["skill"]["nora_fc_eagle"]["rmse_cfs"]
    assert abs(two - FALL_CREEK_CENTERTON_NORA_FC_RMSE_CFS) < 0.05
    assert abs(pers - NWM_CENTERTON_PERS_RMSE_CFS) < 0.05
    assert three < two
    assert report["nwm_citation"] == "fa2e315"
    assert report["fall_creek_citation"] == "962d503"
