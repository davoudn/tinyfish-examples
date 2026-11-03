#!/usr/bin/env bash
# Webfetch via raw cURL.
# Requires: curl, jq, TINYFISH_API_KEY
set -euo pipefail

: "${TINYFISH_API_KEY:?Set TINYFISH_API_KEY first (see ../.env.example)}"

# Up to 10 URLs per call, fetched in parallel server-side.
curl -sS -X POST https://api.fetch.tinyfish.ai \
  -H "X-API-Key: $TINYFISH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "urls": ["https://example.com", "https://tinyfish.ai"],
        "format": "markdown",
        "links": false,
        "per_url_timeout_ms": 45000
      }' \
  | jq .
