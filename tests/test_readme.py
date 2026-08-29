# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from ecgap.claims import scan_text
from ecgap.config import EAGLE_CREEK_ID, EAGLE_CREEK_NAME, QUESTION

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    assert EAGLE_CREEK_ID in text
    assert EAGLE_CREEK_NAME in text
    assert "03352500" in text
    assert "03351000" in text
    assert "03354000" in text
    assert "fa2e315" in text
    assert "8e4fdca" in text
    assert "962d503" in text
    assert "1,607" in text
    assert "1,734" in text
    assert "1,795" in text
    assert "823" in text
    assert "00060" in text
    assert "p_sfha" in text
    assert "03353451" in text
    assert "explains Centerton" not in text
    assert scan_text(text) == []
    assert "—" not in text
    assert "What it is not" not in text
