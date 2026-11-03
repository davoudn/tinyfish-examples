// Webfetch via the official TinyFish TS SDK.
// Run: npm run fetch   (or: npx tsx fetch.ts)
// Env: TINYFISH_API_KEY
import { TinyFish } from "@tiny-fish/sdk";

const client = new TinyFish(); // reads TINYFISH_API_KEY from env

const res = await client.fetch.getContents({
  urls: ["https://example.com", "https://tinyfish.ai"],
  format: "markdown", // or "html" / "json"
  // Optional extras:
  // purpose: "Compare pricing tiers across vendors",
  // links: true,
  // imageLinks: true,
  // perUrlTimeoutMs: 45_000,
  // includeSelectors: ["article"],
  // excludeSelectors: [".comments"],
});

for (const page of res.results) {
  console.log(`## ${page.title} (${page.url})`);
  console.log(page.text.slice(0, 500), "\n");
}

// Per-URL failures — the request itself still returns 200.
for (const err of res.errors) {
  console.error(`FAILED: ${err.url} — ${err.error}`);
}
