# Copyright (c) 2026 Martial Systems LLC
"""Nora plus Fall Creek plus an independent Eagle Creek pulse routed into Centerton."""

from __future__ import annotations

from datetime import date

import numpy as np

from ecgap.pack import QPack

FIXTURE_START = date(2016, 10, 1)
FIXTURE_END = date(2020, 12, 31)
NORA_SCALE = 1.05
FC_SCALE = 0.85
EC_SCALE = 1.10


def build_fixture(*, seed: int = 11) -> QPack:
    rng = np.random.default_rng(seed)
    dates = np.arange(
        np.datetime64(FIXTURE_START.isoformat()),
        np.datetime64(FIXTURE_END.isoformat()) + np.timedelta64(1, "D"),
    )
    n = dates.shape[0]
    y = dates.astype("datetime64[Y]")
    doy = (dates - y).astype("timedelta64[D]").astype(int) + 1
    seasonal = 500 + 280 * np.sin(2 * np.pi * (doy - 50) / 365.25)
    nora = np.zeros(n)
    fc = np.zeros(n)
    eagle = np.zeros(n)
    nora[0] = seasonal[0]
    fc[0] = 0.25 * seasonal[0]
    eagle[0] = 0.18 * seasonal[0]
    for t in range(1, n):
        shared = rng.gamma(2.0, 70.0) if rng.random() < 0.06 else 0.0
        fc_only = rng.gamma(2.2, 90.0) if rng.random() < 0.07 else 0.0
        ec_only = rng.gamma(2.4, 120.0) if rng.random() < 0.09 else 0.0
        nora[t] = max(90.0, 0.72 * nora[t - 1] + 0.22 * seasonal[t] + shared + rng.normal(0, 18))
        fc[t] = max(20.0, 0.55 * fc[t - 1] + 0.08 * seasonal[t] + 0.15 * shared + fc_only + rng.normal(0, 12))
        eagle[t] = max(15.0, 0.50 * eagle[t - 1] + 0.06 * seasonal[t] + 0.10 * shared + ec_only + rng.normal(0, 10))
    cent = np.zeros(n)
    for t in range(n):
        n_src = nora[t - 1] if t else nora[0]
        f_src = fc[t - 1] if t else fc[0]
        e_src = eagle[t - 1] if t else eagle[0]
        extra = rng.gamma(1.3, 40.0) if rng.random() < 0.08 else rng.normal(0, 28)
        cent[t] = max(150.0, NORA_SCALE * n_src + FC_SCALE * f_src + EC_SCALE * e_src + extra)
    return QPack(
        dates=dates,
        nora_cfs=nora,
        fall_creek_cfs=fc,
        eagle_creek_cfs=eagle,
        centerton_cfs=cent,
        source="fixture",
        extra={"nora_scale": NORA_SCALE, "fc_scale": FC_SCALE, "ec_scale": EC_SCALE},
    )
