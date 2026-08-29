# Copyright (c) 2026 Martial Systems LLC

from datetime import date

import numpy as np
import pytest

from ecgap.config import EAGLE_CREEK_ID, LIVE_START
from ecgap.errors import FetchError
from ecgap.fetch import _starts_late, fetch_live
from ecgap.nwis import parse_dv_q


def test_parse_dv() -> None:
    doc = {
        "value": {
            "timeSeries": [
                {
                    "variable": {"variableCode": [{"value": "00060"}]},
                    "values": [{"value": [{"dateTime": "2019-07-01T00:00:00.000", "value": "80"}]}],
                }
            ]
        }
    }
    assert parse_dv_q(doc)[np.datetime64("2019-07-01")] == 80.0


def test_empty_eagle_creek_stops(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(**kwargs):
        del kwargs
        raise FetchError(f"NWIS daily 00060 is empty for {EAGLE_CREEK_ID}")

    monkeypatch.setattr("ecgap.fetch.fetch_four", boom)
    with pytest.raises(FetchError, match="empty"):
        fetch_live(start=date(2019, 7, 1), end=date(2019, 7, 2))


def test_starts_late_detects_gap() -> None:
    dates = np.array([np.datetime64("2016-10-01"), np.datetime64("2016-10-02"), np.datetime64("2016-10-03")])
    late = np.array([np.nan, np.nan, 10.0])
    on_time = np.array([10.0, 11.0, 12.0])
    assert bool(_starts_late(late, dates, LIVE_START))
    assert not bool(_starts_late(on_time, dates, LIVE_START))


def test_late_eagle_creek_stops(monkeypatch: pytest.MonkeyPatch) -> None:
    from ecgap.config import CENTERTON_ID, FALL_CREEK_ID, NORA_ID

    def late_four(*, start, end, get_json_fn=None):
        del get_json_fn
        days = np.arange(np.datetime64(start.isoformat()), np.datetime64(end.isoformat()) + np.timedelta64(1, "D"))
        stem = {d: 100.0 for d in days}
        eagle = {d: 40.0 for d in days if d > np.datetime64(start.isoformat())}
        return {NORA_ID: stem, FALL_CREEK_ID: dict(stem), EAGLE_CREEK_ID: eagle, CENTERTON_ID: dict(stem)}

    monkeypatch.setattr("ecgap.fetch.fetch_four", late_four)
    with pytest.raises(FetchError, match="starts late"):
        fetch_live(start=date(2016, 10, 1), end=date(2016, 10, 10))
