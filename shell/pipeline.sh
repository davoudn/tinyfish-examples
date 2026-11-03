#!/usr/bin/env bash
# Pipeline: websearch → webfetch top 3 results, chained with jq.
# Requires: curl, jq, TINYFISH_API_KEY
set -euo pipefail

: "${TINYFISH_API_KEY:?Set TINYFISH_API_KEY first (see ../.env.example)}"

# 1) Search
SEARCH_JSON=$(curl -sS -G "https://api.search.tinyfish.ai" \
  --data-urlencode "query=latest Bun release notes" \
  --data-urlencode "location=US" \
  -H "X-API-Key: $TINYFISH_API_KEY")

TOP_URLS=$(echo "$SEARCH_JSON" | jq -c '[.results[:3][].url]')
echo "Fetching: $TOP_URLS" >&2

# 2) Fetch
curl -sS -X POST https://api.fetch.tinyfish.ai \
  -H "X-API-Key: $TINYFISH_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --argjson urls "$TOP_URLS" '{urls: $urls, format: "markdown"}')" \
  | jq .
