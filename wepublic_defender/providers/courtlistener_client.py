"""
CourtListener API client with simple caching.

Environment variables:
- COURTLISTENER_TOKEN: API token (optional but recommended)
- COURTLISTENER_USER_AGENT: Custom UA string (recommended)

Cache:
- .wepublic_defender/cache/courtlistener/<hash>.json
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests


BASE_URL = os.getenv("COURTLISTENER_BASE_URL", "https://www.courtlistener.com/api")
CACHE_DIR = Path.cwd() / ".wepublic_defender" / "cache" / "courtlistener"


def _headers() -> Dict[str, str]:
    ua = os.getenv("COURTLISTENER_USER_AGENT", "WePublicDefender/0.1 (+https://example.com)")
    token = os.getenv("COURTLISTENER_TOKEN")
    h = {"User-Agent": ua}
    if token:
        h["Authorization"] = f"Token {token}"
    return h


def _cache_key(url: str, params: Dict[str, Any]) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    m = hashlib.sha256()
    m.update(url.encode("utf-8"))
    m.update(json.dumps(params, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    return CACHE_DIR / f"{m.hexdigest()}.json"


def _get(path: str, params: Dict[str, Any], *, use_cache: bool = True) -> Dict[str, Any]:
    url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    ck = _cache_key(url, params)
    if use_cache and ck.exists():
        return json.loads(ck.read_text(encoding="utf-8"))

    r = requests.get(url, headers=_headers(), params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    try:
        ck.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return data


def search_opinions(query: str, *, page_size: int = 10, jurisdiction: Optional[str] = None, court: Optional[str] = None, order_by: str = "dateFiled desc") -> Dict[str, Any]:
    """Search opinions via the /search/ endpoint.

    Note: CourtListener search syntax supports quoted phrases and fields (e.g., cite:"410 U.S. 113").
    """
    params: Dict[str, Any] = {"q": query, "page_size": page_size, "order_by": order_by}
    if jurisdiction:
        params["jurisdiction"] = jurisdiction
    if court:
        params["court"] = court
    return _get("search/", params)


def get_opinion_by_citation(citation: str) -> Dict[str, Any]:
    """Resolve a citation using a targeted search query.

    Tries exact citation search first, falls back to general search.
    """
    # Try exact citation field search
    q = f'citation:"{citation}"'
    res = search_opinions(q, page_size=5)
    if res.get("count", 0) > 0:
        return res
    # Fallback to general query
    return search_opinions(citation, page_size=5)


def get_opinion_detail(opinion_url: str) -> Dict[str, Any]:
    """Fetch the full opinion JSON given its API URL."""
    # opinion_url is usually absolute, but we normalize just in case
    if opinion_url.startswith("http"):
        path = opinion_url.replace(BASE_URL.rstrip("/"), "").lstrip("/")
    else:
        path = opinion_url
    return _get(path, {})


def get_cluster_detail(cluster_url: str) -> Dict[str, Any]:
    if cluster_url.startswith("http"):
        path = cluster_url.replace(BASE_URL.rstrip("/"), "").lstrip("/")
    else:
        path = cluster_url
    return _get(path, {})

