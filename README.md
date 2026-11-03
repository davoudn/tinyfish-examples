# TinyFish — Web Search & Web Fetch Examples

Complete, runnable examples for the [TinyFish](https://tinyfish.ai) **Search API** and **Fetch API**,
outside of OpenCode.

## Endpoints

| Product | Method + URL                                        | Auth                      |
| ------- | --------------------------------------------------- | ------------------------- |
| Search  | `GET  https://api.search.tinyfish.ai`               | `X-API-Key` header        |
| Fetch   | `POST https://api.fetch.tinyfish.ai`                | `X-API-Key` header        |

**Free tier:** ~12,000 searches/day and ~1,000 fetched URLs/day. Beyond that a positive wallet
balance is required.

## Folder layout

```
tinyfish-examples/
├── README.md              ← you are here
├── .env.example           ← copy to .env and add your key
├── .gitignore
├── requirements.txt       ← Python deps
├── python/
│   ├── raw_http.py        ← Search + Fetch with plain `requests` (no SDK)
│   ├── sdk.py             ← Search + Fetch with the official Python SDK
│   └── pipeline.py        ← Search → fetch top results (SDK)
├── typescript/
│   ├── package.json
│   ├── search.ts          ← Search with the official TS SDK
│   ├── fetch.ts           ← Fetch with the official TS SDK
│   └── pipeline.ts        ← Search → fetch top results (TS SDK)
└── shell/
    ├── search.sh          ← raw cURL search
    ├── fetch.sh           ← raw cURL fetch
    └── pipeline.sh        ← search → fetch top 3, chained with jq
```

## 1. Setup

Get an API key from <https://agent.tinyfish.ai/api-keys>, then:

```bash
export TINYFISH_API_KEY="your_api_key_here"
```

### Python

```bash
pip install -r requirements.txt   # requests (raw_http.py)
pip install tinyfish              # official SDK (sdk.py, pipeline.py)
```

### TypeScript

```bash
cd typescript
npm install                      # installs @tiny-fish/sdk, tsx, typescript
```

### Shell

Requires `curl` and `jq`.

## 2. Run the examples

```bash
# Python
python python/raw_http.py        # search + fetch, no SDK
python python/sdk.py             # search + fetch, official SDK
python python/pipeline.py        # search → fetch top 5

# TypeScript
cd typescript
npm run search
npm run fetch
npm run pipeline

# Shell
./shell/search.sh
./shell/fetch.sh
./shell/pipeline.sh
```

## 3. Search API reference

`GET https://api.search.tinyfish.ai`

### Query parameters

| Parameter          | Type   | Notes                                                                 |
| ------------------ | ------ | --------------------------------------------------------------------- |
| `query`            | string | **Required.** 1–2000 chars.                                            |
| `purpose`          | string | Optional intent hint, ≤2000 chars, improves ranking.                   |
| `location`         | string | Country code for geo-targeting (e.g. `US`). Defaults to `US`.          |
| `language`         | string | Language code (e.g. `en`). Auto-resolves with `location`.              |
| `include_domains`  | string | Comma-separated domains to restrict results to.                        |
| `exclude_domains`  | string | Comma-separated domains to exclude.                                    |
| `domain_type`      | string | `web` (default) \| `news` \| `research_paper`.                         |
| `after_date`       | string | `YYYY-MM-DD`. Not usable with `recency_minutes`.                       |
| `before_date`      | string | `YYYY-MM-DD`. Not usable with `recency_minutes`.                       |
| `recency_minutes`  | int    | Freshness window, `1`–`5256000` (10 years).                            |
| `pub_year_min`     | int    | `0`–`9999`, `research_paper` only.                                     |
| `pub_year_max`     | int    | `0`–`9999`, `research_paper` only.                                     |
| `page`             | int    | `0`–`10`, pagination (0-based).                                        |
| `include_thumbnails` | bool | Return `thumbnail_url` per result when available.                     |

Rules:

- Don't combine `recency_minutes` with `after_date`/`before_date`.
- `research_paper` ignores date/recency filters — use `pub_year_min`/`pub_year_max`.
- `site:` / `-site:` in the query still work but are deprecated; prefer the
  `include_domains` / `exclude_domains` parameters.

### Search response

```json
{
  "query": "web automation tools",
  "results": [
    {
      "position": 1,
      "site_name": "tinyfish.ai",
      "title": "TinyFish — AI Web Automation Platform",
      "snippet": "Automate any website with natural language instructions...",
      "url": "https://tinyfish.ai"
    }
  ],
  "total_results": 10,
  "page": 0
}
```

## 4. Fetch API reference

`POST https://api.fetch.tinyfish.ai` — renders JavaScript-heavy pages in a real browser and
returns clean extracted content.

### Request body

| Field                          | Type    | Notes                                                        |
| ------------------------------ | ------- | ------------------------------------------------------------ |
| `urls`                         | string[] | **Required.** 1–10 URLs, fetched in parallel.                |
| `purpose`                      | string  | Optional intent hint, ≤2000 chars.                           |
| `format`                       | string  | `markdown` (default) \| `html` \| `json`.                    |
| `links`                        | bool    | Extract outbound links per page.                             |
| `image_links`                  | bool    | Extract image URLs per page.                                 |
| `iframe_links`                 | bool    | Extract iframe URLs.                                         |
| `page_metadata`                | bool    | Include extra page metadata.                                 |
| `ttl`                          | int     | Cache TTL in seconds (`0` = no caching).                     |
| `per_url_timeout_ms`           | int     | `1`–`110000`, per-URL timeout budget.                        |
| `if_none_match`                | string  | Conditional request (ETag).                                  |
| `if_modified_since`            | string  | Conditional request (HTTP date).                             |
| `include_etag_and_last_modified` | bool   | Return caching headers.                                      |
| `include_selectors`            | string[] | Only extract these CSS selectors (boilerplate removal off). |
| `exclude_selectors`            | string[] | Strip these before extraction (applied first).               |

### Fetch response

```json
{
  "results": [
    {
      "url": "https://example.com",
      "final_url": "https://example.com/",
      "title": "Example Domain",
      "description": "Page meta description",
      "language": "en",
      "format": "markdown",
      "text": "# Example Domain\n\n...",
      "author": "Jane Doe",
      "published_date": "2026-01-15",
      "latency_ms": 1430.4
    }
  ],
  "errors": [
    { "url": "https://invalid.example.com", "error": "bot_blocked" }
  ]
}
```

**Important:** per-URL failures do **not** fail the request — the response is still HTTP 200.
Always check `errors[]`.

### Per-URL error codes

| Code               | Meaning                                            |
| ------------------ | -------------------------------------------------- |
| `target_http_error`| Non-2xx status other than 404/410 (see `status`).  |
| `page_not_found`   | 404 or 410 (see `status`).                         |
| `target_unreachable` | Connection / TLS / DNS failure.                  |
| `timeout`          | Request timed out.                                 |
| `proxy_error`      | Proxy tunnel failure.                              |
| `bot_blocked`      | Bot-challenge page detected (e.g. Cloudflare).     |
| `empty_content`    | Page loaded but no extractable text.               |
| `login_required`   | Redirected to a login/account wall.                |

### API-level error codes (non-2xx)

`MISSING_API_KEY`, `INVALID_API_KEY`, `INVALID_INPUT`, `UNAUTHORIZED`, `FORBIDDEN`,
`NOT_FOUND`, `RATE_LIMIT_EXCEEDED`, `SERVICE_BUSY`, `TIMEOUT`, `INTERNAL_ERROR`,
`INSUFFICIENT_CREDITS`, `CONTENT_POLICY_VIOLATION`, `SITE_BLOCKED`, `TASK_FAILED`,
`MAX_STEPS_EXCEEDED`, `CANCELLED`.

## 5. Which API when?

- **Search** — you need ranked web results with titles, snippets, and URLs.
- **Fetch** — you already have URLs and want clean, extracted page content.
- Typical flow: Search first, then Fetch the top N URLs.

## Docs

- Search API: <https://docs.tinyfish.ai/search-api>
- Fetch API:  <https://docs.tinyfish.ai/fetch-api>
- Full reference: <https://docs.tinyfish.ai/api-reference>
# tinyfish-examples
