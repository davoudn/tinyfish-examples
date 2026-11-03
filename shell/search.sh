#!/usr/bin/env bash
# Websearch via raw cURL.
# Requires: curl, jq, TINYFISH_API_KEY
set -euo pipefail

: "${TINYFISH_API_KEY:?Set TINYFISH_API_KEY first (see ../.env.example)}"

curl -sS -G "https://api.search.tinyfish.ai" \
  --data-urlencode "query=web automation tools" \
  --data-urlencode "location=US" \
  # Optional extras (uncomment as needed):
  # --data-urlencode "purpose=Find an open-source library for X" \
  # --data-urlencode "include_domains=github.com" \
  # --data-urlencode "exclude_domains=reddit.com" \
  # --data-urlencode "domain_type=news" \
  # --data-urlencode "recency_minutes=1440" \
  # --data-urlencode "after_date=2024-01-01" \
  # --data-urlencode "before_date=2024-12-31" \
  -H "X-API-Key: $TINYFISH_API_KEY" \
  | jq .
