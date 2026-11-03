#!/usr/bin/env python3
"""Pipeline: search the web, then fetch the top results.

Requires:  pip install tinyfish
Env var:   TINYFISH_API_KEY (read automatically by the SDK)
"""

from tinyfish import TinyFish

client = TinyFish()

QUERY = "latest Bun release notes"
PURPOSE = "Summarize the most recent Bun release for a changelog"

# 1) Websearch — last 3 days, with an intent hint
search = client.search.query(
    query=QUERY,
    purpose=PURPOSE,
    recency_minutes=4320,  # 3 * 24 * 60
)
top_urls = [r.url for r in search.results[:5]]
print(f"Found {len(search.results)} results; fetching top {len(top_urls)}\n")

# 2) Webfetch — full page content as markdown
pages = client.fetch.get_contents(
    urls=top_urls,
    format="markdown",
    purpose="Extract release notes content",
)

for page in pages.results:
    print(f"## {page.title}")
    print(f"   {page.url}")
    print(page.text[:300], "\n")

for err in pages.errors:
    print(f"FAILED: {err.url} — {err.error}")
