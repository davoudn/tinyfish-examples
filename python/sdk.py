#!/usr/bin/env python3
"""TinyFish Search + Fetch via the official Python SDK.

Requires:  pip install tinyfish
Env var:   TINYFISH_API_KEY (read automatically by the SDK)
"""

from tinyfish import TinyFish

client = TinyFish()

# ── Websearch ─────────────────────────────────────────────────
results = client.search.query(query="web automation tools", location="US")
# Optional extras:
#   purpose="Find an open-source library for X",
#   include_domains="github.com",
#   exclude_domains="reddit.com",
#   domain_type="news",
#   recency_minutes=1440,
#   after_date="2024-01-01", before_date="2024-12-31",
#   page=1,

for r in results.results:
    print(r.position, r.title, "→", r.url)

top_urls = [r.url for r in results.results[:3]]

# ── Webfetch (1–10 URLs per call, parallel server-side) ───────
pages = client.fetch.get_contents(
    urls=top_urls,
    format="markdown",  # or "html" / "json"
    # Optional extras:
    #   purpose="Extract release notes content",
    #   links=True,
    #   per_url_timeout_ms=45_000,
    #   include_selectors=["article"],
    #   exclude_selectors=[".comments"],
)
for page in pages.results:
    print(f"\n## {page.title}")
    print(f"   {page.url}")
    print(page.text[:500], "\n")

# Per-URL failures — the request itself still succeeds.
for err in pages.errors:
    print(f"FAILED: {err.url} — {err.error}")
