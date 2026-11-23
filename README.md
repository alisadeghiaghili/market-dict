# MarketDict

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![CI Verification](https://github.com/alisadeghiaghili/market-dict/actions/workflows/ci.yml/badge.svg)](https://github.com/alisadeghiaghili/market-dict/actions/workflows/ci.yml)
[![MCP](https://img.shields.io/badge/MCP-Enabled-purple)](MCP_DOCUMENTATION.md)
[![Latest Release](https://img.shields.io/github/v/release/alisadeghiaghili/market-dict?color=emerald)](https://github.com/alisadeghiaghili/market-dict/releases)
[![Changelog](https://img.shields.io/badge/Changelog-Keep%20a%20Changelog-orange.svg)](CHANGELOG.md)

A modern bilingual (English & Persian) financial dictionary — **6,108 market & investing terms** across 14 domains with real-time fuzzy search, KaTeX mathematical formulas, and internal term cross-linking — available as a web app, a static build, a REST API and an MCP server for internal use.

> **Data notice.** The Apache 2.0 licence covers the code only. The dictionary content is derived from third-party copyrighted material and is not licensed for redistribution or public hosting. See [DATA_NOTICE.md](DATA_NOTICE.md).

---

## Features

- **Bilingual Instant Search**: Real-time fuzzy search in both Persian and English with automatic Persian text normalization (`ی/ي`, `ک/ك`, zero-width non-joiners).
- **Side-by-Side Dual Language Display**: Full English definitions, Persian professional translations, and key takeaways for each term.
- **Audio Pronunciation**: Built-in voice pronunciation for English terms via the Web Speech API.
- **Interactive Alphabet & Category Filters**: Quickly explore terms by initial letter (`#`, `A-Z`) or financial domain (Corporate Finance, Accounting, Macroeconomics, Derivatives, etc.).
- **Local Favorites**: Bookmark terms for study sessions, persisted directly in local browser storage.
- **Dark / Light Mode**: Tailored user interface with responsive layout and glassmorphism styling.
- **RESTful Developer API**: Production-grade versioned API (`/api/v1`) with full CORS support, OpenAPI 3.0 specification, interactive Swagger UI (`/docs`), and zero-dependency SDKs for Python and C# (.NET).
- **Model Context Protocol (MCP) Server**: Native MCP integration with 9 tools, 3 resources, and 2 prompts for Claude Desktop, Cursor, Antigravity, and AI agents.
- **Transparent Enrichment Pipeline**: All fetching goes through `polite_fetcher.py`, which identifies itself honestly, honours `robots.txt` and `Crawl-delay`, rate-limits per host, and stops when a site refuses automated access.

---

## REST API for Developers & Applications 🚀

MarketDict provides a full-featured REST API with CORS enabled so third-party apps, trading bots, mobile apps, web widgets, and Telegram/Discord bots can consume the financial dictionary.

- 📖 **Interactive Swagger UI**: [http://localhost:5000/docs](http://localhost:5000/docs)
- 📄 **OpenAPI 3.0.3 Spec**: [http://localhost:5000/api/v1/openapi.json](http://localhost:5000/api/v1/openapi.json)
- 📚 **Full Documentation**: See [API.md](API.md)

### Key Endpoints:
- `GET /api/v1/terms?q=...` — Fuzzy bilingual search & filter (by letter, category, formulas, deep sections)
- `GET /api/v1/terms/{id_or_slug}` — Full definition, takeaways, sections, and LaTeX formulas
- `GET /api/v1/terms/random` — Financial term of the day (widgets, bots, daily quotes)
- `GET /api/v1/suggest?q=...` — Ultra-fast autocomplete prefix search (<5ms)
- `GET /api/v1/categories` — 32 financial categories with icons and counts
- `GET /api/v1/formulas` — 44 quantitative finance formulas with LaTeX equations
- `POST /api/v1/terms/batch` — Batch retrieval of multiple terms in one request
- `GET /api/v1/health` — System status, uptime, and database metrics

### Python Client SDK:
```python
from marketdict_client import MarketDict

client = MarketDict("http://localhost:5000/api/v1")

# Search terms in English or Persian
results = client.search("نسبت شارپ", limit=5)

# Full term detail with formula
term = client.get_term("sharperatio")
print(term["formula"]["formula_en"])

# Random term of the day
daily_term = client.get_random(has_deep=True)
```

### C# (.NET) Client SDK:
Add [`MarketDictClient.cs`](MarketDictClient.cs) to any .NET 6/7/8/9, .NET Standard, or Framework project:
```csharp
using MarketDict;

using var client = new MarketDictClient("http://localhost:5000/api/v1");

// Search terms in English or Persian
var results = await client.SearchTermsAsync(query: "نسبت شارپ", limit: 5);

// Full term detail with LaTeX formula
var term = await client.GetTermAsync("sharperatio");
Console.WriteLine(term.Formula?.FormulaEn);

// Autocomplete prefix suggestions (<5ms)
var suggestions = await client.SuggestAsync("bit", limit: 3);
```

---

## Model Context Protocol (MCP) Server 🤖

MarketDict includes a production-ready **MCP server** (`mcp_server.py`) enabling AI assistants (such as **Claude Desktop**, **Cursor**, **Google Antigravity**, and **Cline**) to directly search financial terms, retrieve LaTeX mathematical formulas, fetch bilingual definitions, and explore taxonomies in real-time.

- 📖 **Complete Bilingual Documentation (FA/EN)**: See [MCP_DOCUMENTATION.md](MCP_DOCUMENTATION.md)
- 🚀 **Quick Setup Guide**: See [MCP_GUIDE.md](MCP_GUIDE.md)
- ⚙️ **Included Configuration**: [mcp_config.json](mcp_config.json)

### Quick Configuration:
Add to your `claude_desktop_config.json` or Antigravity's `mcp_config.json`:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

### Key MCP Tools:
- `search_terms` — Search 6,108 terms with bilingual fuzzy matching and Persian normalization
- `suggest_terms` — Prefix autocomplete search (<5ms)
- `get_term_details` — Full term info (definitions, takeaways, LaTeX formulas, deep sections)
- `get_financial_formula` — Standardized LaTeX equations (Sharpe, WACC, ROE, EBIT, CAPM, etc.)
- `list_all_formulas` — List all 44+ registered quantitative financial formulas
- `list_categories` — 32 financial taxonomy categories with term counts
- `get_random_term` — Random financial term discovery (filter by category or deep content)

Test the server with:
```bash
python test_mcp_server.py
```

---

## Quick Start

### 1. Run Locally

```bash
# Clone the repository
git clone https://github.com/alisadeghiaghili/market-dict.git
cd market-dict

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
python app.py
```

Access the web interface at **`http://localhost:5000`**.

### 2. Run with Docker Compose

```bash
docker compose up -d --build
```

### 3. Run Behind a Reverse Proxy (Nginx / Cloudflare / Traefik)

Both `app.py` and `mcp_server.py` natively support reverse proxy headers:

```bash
# Run Web App & REST API behind reverse proxy
python app.py --host 0.0.0.0 --port 5000 --proxy-headers --forwarded-allow-ips "*"

# Run MCP Server with SSE transport behind reverse proxy
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"
```

---

## Enrichment Pipeline

> Check the source site's terms of use before running the scraper. Honouring `robots.txt` does not grant any right to the content, and the scraper must not be run against a site whose terms prohibit automated collection. See [DATA_NOTICE.md](DATA_NOTICE.md).

The scraper traverses all 27 alphabetical subpages (`#`, `A` through `Z`) to discover and extract all financial terms across the entire dictionary, capturing complete definitions, key takeaways, and full Table of Contents sections.

```bash
# Scrape all 27 alphabetical subpages (#, A-Z) with full definitions, takeaways, and sections
python investopedia_scraper.py

# Scrape specific letter categories (e.g. A, B, and C)
python investopedia_scraper.py --letters a,b,c

# Fast catalog extraction (extract all 6,106+ term URLs and titles without body content)
python investopedia_scraper.py --no-details

# Custom output filename and a slower request rate (seconds between requests)
python investopedia_scraper.py --min-delay 5 -o full_investopedia_dictionary

# Run quietly in the background
python investopedia_scraper.py -q
```

---

## Production Deployment

For detailed production setup instructions using Docker or Gunicorn with Nginx and Systemd, refer to [DEPLOYMENT.md](DEPLOYMENT.md).

---

## License

The **source code** is licensed under the **Apache License 2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

The **dictionary data** is not covered by that licence and no licence is granted for it. See [DATA_NOTICE.md](DATA_NOTICE.md).

Copyright (c) 2026 Ali Sadeghi Aghili.
