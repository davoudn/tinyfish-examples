#!/usr/bin/env python3
"""TinyFish Search + Fetch API — raw HTTP, no SDK required.

Requires:  pip install requests
Env var:   TINYFISH_API_KEY
"""

import os
import sys

import requests

API_KEY = os.environ.get("TINYFISH_API_KEY")
HEADERS = {"X-API-Key": API_KEY} if API_KEY else {}

SEARCH_URL = "https://api.search.tinyfish.ai"
FETCH_URL = "https://api.fetch.tinyfish.ai"


def search(query: str, location: str = "US", language: str | None = None, **params) -> dict:
    """Websearch — GET https://api.search.tinyfish.ai

    Extra params can be passed through, e.g. include_domains="github.com",
    recency_minutes=1440, domain_type="news", purpose="...".
    """
    if language:
        params["language"] = language
    params.update({"query": query, "location": location})
    resp = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch(urls: list[str], fmt: str = "markdown", **kwargs) -> dict:
    """Webfetch — POST https://api.fetch.tinyfish.ai

    Up to 10 URLs per call (fetched in parallel). Per-URL failures appear in
    the returned "errors" list, the HTTP response is still 200.

    Extra options: links=True, image_links=True, per_url_timeout_ms=45000,
    include_selectors=["article"], exclude_selectors=[".comments"], purpose="...".
    """
    body = {"urls": urls[:10], "format": fmt, **kwargs}
    resp = requests.post(FETCH_URL, json=body, headers=HEADERS, timeout=120)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if not API_KEY:
        sys.exit("Set TINYFISH_API_KEY first (see .env.example)")

    # ── Websearch ─────────────────────────────────────────────
    s = search("web automation tools")
    print(f"Query: {s['query']} ({s['total_results']} results)\n")
    for r in s["results"]:
        print(f"  {r['position']}. {r['title']}")
        print(f"     {r['url']}\n")

    # ── Webfetch (top 3 search results) ───────────────────────
    top_urls = [r["url"] for r in s["results"][:3]]
    f = fetch(top_urls)

    for page in f["results"]:
        print(f"## {page['title']} ({page['url']})")
        print(page["text"][:500], "\n")

    for err in f["errors"]:
        print(f"FAILED: {err['url']} — {err['error']}\n")


if __name__ == "__main__":
    main()
