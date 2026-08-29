# Copyright (c) 2026 Martial Systems LLC

from ecgap.claims import scan_text
from ecgap.config import QUESTION


def test_question_and_bans() -> None:
    assert scan_text(QUESTION) == []
    assert "lag_wet" in scan_text("lag-scatter is a wet mask")
    assert "nwm_repull" in scan_text("re-pulling NWM")
    assert "little_as_eagle" in scan_text("03353600 is Eagle Creek")
    assert "centerton_closed" in scan_text("Eagle Creek explains Centerton")
    assert "feet_invert" in scan_text("inverting Nora Q to feet")
