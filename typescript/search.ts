// Websearch via the official TinyFish TS SDK.
// Run: npm run search   (or: npx tsx search.ts)
// Env: TINYFISH_API_KEY
import { TinyFish } from "@tiny-fish/sdk";

const client = new TinyFish(); // reads TINYFISH_API_KEY from env

const res = await client.search.query({
  query: "web automation tools",
  location: "US",
  // Optional extras:
  // purpose: "Find an open-source library for X in Node",
  // language: "en",
  // includeDomains: "github.com",
  // excludeDomains: "reddit.com",
  // domainType: "news",
  // recencyMinutes: 1440,
  // afterDate: "2024-01-01",
  // beforeDate: "2024-12-31",
});

console.log(`Query: ${res.query} (${res.total_results} results)\n`);
for (const r of res.results) {
  console.log(`${r.position}. ${r.title}`);
  console.log(`   ${r.url}\n`);
}
