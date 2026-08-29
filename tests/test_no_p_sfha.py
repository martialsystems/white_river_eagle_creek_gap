# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_FORBIDDEN = ("p_sfha_calibrated", "indiana_flood_completion", "import p_sfha")


def test_src_does_not_import_p_sfha() -> None:
    hits = []
    for path in (REPO / "src").rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for token in _FORBIDDEN:
            if token in text:
                hits.append(f"{path.name}:{token}")
    assert hits == []
