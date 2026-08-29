# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from ecgap.claims import require_clean
from ecgap.config import MAX_FIGURES
from ecgap.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def write_hydrograph(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    ho = fit["holdout"]
    dates = [datetime.strptime(str(x)[:10], "%Y-%m-%d") for x in ho["dates"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(dates, ho["centerton_cfs"], color="#222222", lw=1.4, label="Centerton 00060")
    ax.plot(
        dates,
        ho["persistence_cfs"],
        color="#7a7a7a",
        lw=1.0,
        ls="--",
        label="Centerton 00060 lag 1 d",
    )
    ax.plot(
        dates,
        ho["nora_plus_fc_cfs"],
        color="#b36b00",
        lw=1.1,
        label="Nora + Fall Creek lag 1 d",
    )
    ax.plot(
        dates,
        ho["nora_fc_eagle_cfs"],
        color="#1b6ca8",
        lw=1.2,
        label="Nora + Fall Creek + Eagle Creek",
    )
    ax.set_ylabel("USGS daily mean 00060 (cfs)")
    ax.set_title(title, fontsize=10)
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.text(0.5, 0.02, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.16, top=0.88, left=0.12, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_contributions(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ho = fit["holdout"]
    stem = ho["nora_contrib_cfs"] + ho["fc_contrib_cfs"]
    eagle = ho["eagle_contrib_cfs"]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.scatter(stem, eagle, s=8, c="#1b6ca8", alpha=0.45, linewidths=0)
    ax.axhline(0.0, color="#888888", lw=0.6)
    ax.axvline(0.0, color="#888888", lw=0.6)
    ax.set_xlabel("Nora + Fall Creek lag-1 contribution (cfs)")
    ax.set_ylabel("Eagle Creek lag-1 contribution (cfs)")
    ax.set_title(title, fontsize=10)
    fig.text(0.5, 0.02, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.16, top=0.88, left=0.16, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any]) -> list[Path]:
    three = fit["skill"]["nora_fc_eagle"]
    cn = float(three["coef_nora"])
    cf = float(three["coef_fall_creek"])
    ce = float(three["coef_eagle_creek"])
    paths = [
        write_hydrograph(
            log_dir / "hydrograph.png",
            fit=fit,
            title="Centerton holdout: USGS daily mean 00060",
            subtitle="Observed Centerton 00060, lag 1 d, Nora+Fall Creek, Nora+Fall Creek+Eagle Creek. cfs.",
        ),
        write_contributions(
            log_dir / "contributions.png",
            fit=fit,
            title="Holdout contributions at Centerton",
            subtitle=(
                f"OLS {cn:.2f} Nora, {cf:.2f} Fall Creek, {ce:.2f} Eagle Creek. "
                "Not a routing mass balance."
            ),
        ),
    ]
    _cap(len(paths))
    return paths
