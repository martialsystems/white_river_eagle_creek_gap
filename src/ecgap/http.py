# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
import time
from http.client import IncompleteRead
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ecgap.config import USER_AGENT
from ecgap.errors import FetchError


def get_bytes(url: str, *, timeout: int = 90, attempts: int = 6) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    last: BaseException | None = None
    for i in range(attempts):
        try:
            with urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                if not body:
                    raise FetchError(f"GET empty or 404: {url}")
                return body
        except HTTPError as exc:
            last = exc
            if int(getattr(exc, "code", 0) or 0) == 404:
                raise FetchError(f"GET empty or 404: {url}") from exc
            if int(getattr(exc, "code", 0) or 0) < 500 or i == attempts - 1:
                raise FetchError(f"GET failed: {url}: {exc}") from exc
            time.sleep(min(2 ** i, 16))
        except (URLError, TimeoutError, ConnectionError, IncompleteRead) as exc:
            last = exc
            if i == attempts - 1:
                raise FetchError(f"GET failed: {url}: {exc}") from exc
            time.sleep(min(2 ** i, 16))
    raise FetchError(f"GET failed: {url}: {last}") from last


def get_json(url: str, *, timeout: int = 90) -> dict[str, Any]:
    raw = get_bytes(url, timeout=timeout)
    doc = json.loads(raw.decode("utf-8"))
    if not isinstance(doc, dict):
        raise FetchError(f"JSON object required: {url}")
    return doc
