# Data Notice

The Apache License 2.0 in [`LICENSE`](LICENSE) covers the **source code** of
this repository only. It does **not** cover the dictionary content, and no
licence of any kind is granted for that content.

## Third-party content

The following files contain, or are derived from, text published on
Investopedia (<https://www.investopedia.com>), which is owned by its publisher
and protected by copyright:

| File | Content |
|------|---------|
| `bilingual_dictionary.json` | Term definitions, key takeaways, article sections and "bottom line" summaries, plus Persian translations of that text |
| `all_investopedia_terms_catalog.json` | Term titles and URLs |
| `investopedia_terms.json`, `investopedia_terms.csv` | Scraped term entries |
| `market_dict.db`, `dist/`, `cache_index.pkl` | Generated from the files above |

The Persian translations are derivative works of the original English text and
carry the same restrictions.

All rights in this content remain with its owners. It is kept here for
internal, non-commercial reference only. Do not republish, redistribute,
sublicense or deploy it to a public website, and do not use it to train
models, unless you hold the rights to do so.

Each entry keeps its source `url`, so the original article can always be
consulted directly.

## What is original to this project

- The application, API, MCP server and pipeline code (Apache License 2.0).
- The formula registry in `formula_registry.py` and the category taxonomy in
  `categories_engine.py`.

## Fetching new content

The enrichment scripts fetch pages through `polite_fetcher.py`. It identifies
itself honestly, honours `robots.txt` and `Crawl-delay`, rate-limits requests,
and stops when a site refuses automated access. Complying with robots.txt does
not grant any right to the content: before running the scripts, check the
source site's terms of use, and do not run them against a site whose terms
prohibit automated collection.

## Takedown

If you own content in this repository and want it removed, open an issue on
the repository and it will be removed promptly.
