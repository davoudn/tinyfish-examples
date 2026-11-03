// Pipeline: websearch → webfetch top 5 results.
// Run: npm run pipeline   (or: npx tsx pipeline.ts)
// Env: TINYFISH_API_KEY
import { TinyFish } from "@tiny-fish/sdk";

const client = new TinyFish(); // reads TINYFISH_API_KEY from env

// 1) Websearch — last 3 days, with an intent hint
const search = await client.search.query({
  query: "latest Bun release notes",
  purpose: "Summarize the most recent Bun release",
  recencyMinutes: 4320, // 3 * 24 * 60
});
const topUrls = search.results.slice(0, 5).map((r) => r.url);
console.log(`Found ${search.results.length} results; fetching top ${topUrls.length}\n`);

// 2) Webfetch — full page content as markdown
const pages = await client.fetch.getContents({
  urls: topUrls,
  format: "markdown",
  purpose: "Extract release notes content",
});

for (const page of pages.results) {
  console.log(`## ${page.title}`);
  console.log(`   ${page.url}`);
  console.log(page.text.slice(0, 300), "\n");
}

for (const err of pages.errors) {
  console.error(`FAILED: ${err.url} — ${err.error}`);
}
