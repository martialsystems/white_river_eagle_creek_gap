# Copyright (c) 2026 Martial Systems LLC
"""Lag-1 Nora, Fall Creek, Eagle Creek. Label is Centerton. Lag frozen at 1."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.linear_model import LinearRegression

from ecgap.config import (
    BELOW_RESERVOIR_ID,
    CENTERTON_ID,
    EAGLE_CREEK_ID,
    FALL_CREEK_ID,
    INDY_ID,
    LAG_DAYS,
    LITTLE_EAGLE_ID,
    NORA_ID,
    NWM_CENTERTON_RMSE_CFS,
    NWM_CITATION,
    ZIONSVILLE_ID,
)
from ecgap.errors import LeakError, SplitError
from ecgap.pack import QPack
from ecgap.split import assert_temporal, temporal_masks


def rmse(y: np.ndarray, yhat: np.ndarray) -> float:
    e = np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float)
    ok = np.isfinite(e)
    return float(np.sqrt(np.mean(e[ok] * e[ok]))) if ok.any() else float("nan")


def mae(y: np.ndarray, yhat: np.ndarray) -> float:
    e = np.abs(np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float))
    ok = np.isfinite(e)
    return float(np.mean(e[ok])) if ok.any() else float("nan")


def _lag(arr: np.ndarray, k: int) -> np.ndarray:
    if k < 0:
        raise SplitError("negative lag is a future leak")
    src = np.asarray(arr, dtype=float)
    if k == 0:
        return src.copy()
    out = np.full(arr.shape, np.nan, dtype=float)
    out[k:] = src[:-k]
    return out


def _verdict(three_rmse: float, two_rmse: float, pers_rmse: float) -> str:
    if three_rmse < two_rmse and three_rmse < pers_rmse:
        return "eagle_beats_nora_fc_and_persistence"
    if three_rmse < two_rmse:
        return "eagle_beats_nora_fc_not_persistence"
    return "nora_plus_fall_creek_enough"


def fit_pack(pack: QPack) -> dict[str, Any]:
    nora = np.asarray(pack.nora_cfs, dtype=float)
    fc = np.asarray(pack.fall_creek_cfs, dtype=float)
    eagle = np.asarray(pack.eagle_creek_cfs, dtype=float)
    cent = np.asarray(pack.centerton_cfs, dtype=float)
    train_all, hold_all = temporal_masks(pack.dates)
    assert_temporal(pack.dates, train_all, hold_all)
    nora_l1 = _lag(nora, LAG_DAYS)
    fc_l1 = _lag(fc, LAG_DAYS)
    eagle_l1 = _lag(eagle, LAG_DAYS)
    pers = _lag(cent, LAG_DAYS)
    if LAG_DAYS != 1:
        raise SplitError("lag is locked at 1 calendar day")
    ok = (
        np.isfinite(nora_l1)
        & np.isfinite(fc_l1)
        & np.isfinite(eagle_l1)
        & np.isfinite(cent)
        & np.isfinite(pers)
    )
    train, hold = train_all & ok, hold_all & ok
    if not train.any() or not hold.any():
        raise SplitError("no valid rows after lag")
    x_two = np.column_stack([nora_l1, fc_l1])
    x_three = np.column_stack([nora_l1, fc_l1, eagle_l1])
    lr_two = LinearRegression()
    lr_two.fit(x_two[train], cent[train])
    lr_three = LinearRegression()
    lr_three.fit(x_three[train], cent[train])
    yhat_two = lr_two.predict(x_two[hold])
    yhat_three = lr_three.predict(x_three[hold])
    y_ho, pers_ho = cent[hold], pers[hold]
    skill = {
        "persistence_target": {"rmse_cfs": rmse(y_ho, pers_ho), "mae_cfs": mae(y_ho, pers_ho)},
        "nora_plus_fall_creek": {
            "rmse_cfs": rmse(y_ho, yhat_two),
            "mae_cfs": mae(y_ho, yhat_two),
            "coef_nora": float(lr_two.coef_[0]),
            "coef_fall_creek": float(lr_two.coef_[1]),
            "intercept": float(lr_two.intercept_),
            "lag_days": LAG_DAYS,
        },
        "nora_fc_eagle": {
            "rmse_cfs": rmse(y_ho, yhat_three),
            "mae_cfs": mae(y_ho, yhat_three),
            "coef_nora": float(lr_three.coef_[0]),
            "coef_fall_creek": float(lr_three.coef_[1]),
            "coef_eagle_creek": float(lr_three.coef_[2]),
            "intercept": float(lr_three.intercept_),
            "lag_days": LAG_DAYS,
        },
        "nwm_cited": {"rmse_cfs": NWM_CENTERTON_RMSE_CFS, "source": NWM_CITATION},
    }
    return {
        "lag_days": LAG_DAYS,
        "lag1_locked": True,
        "skill": skill,
        "verdict": _verdict(
            skill["nora_fc_eagle"]["rmse_cfs"],
            skill["nora_plus_fall_creek"]["rmse_cfs"],
            skill["persistence_target"]["rmse_cfs"],
        ),
        "predictor_sites": [NORA_ID, FALL_CREEK_ID, EAGLE_CREEK_ID],
        "label_sites": [CENTERTON_ID],
        "holdout": {
            "dates": pack.dates[hold],
            "centerton_cfs": y_ho,
            "persistence_cfs": pers_ho,
            "nora_plus_fc_cfs": yhat_two,
            "nora_fc_eagle_cfs": yhat_three,
            "nora_contrib_cfs": float(lr_three.coef_[0]) * nora_l1[hold],
            "fc_contrib_cfs": float(lr_three.coef_[1]) * fc_l1[hold],
            "eagle_contrib_cfs": float(lr_three.coef_[2]) * eagle_l1[hold],
            "intercept": skill["nora_fc_eagle"]["intercept"],
        },
    }


def assert_features_clean(fit: dict[str, Any]) -> None:
    preds = list(fit.get("predictor_sites") or [])
    banned = {INDY_ID, CENTERTON_ID, LITTLE_EAGLE_ID, ZIONSVILLE_ID, BELOW_RESERVOIR_ID}
    hit = banned.intersection(preds)
    if hit:
        raise LeakError(f"banned site in X: {sorted(hit)}")
    need = {NORA_ID, FALL_CREEK_ID, EAGLE_CREEK_ID}
    if need.difference(preds):
        raise LeakError("Nora, Fall Creek Millersville, and Eagle Creek Indianapolis must be the features")
    if fit.get("lag_days") != 1 or not fit.get("lag1_locked"):
        raise SplitError("lag is locked at 1 calendar day")
