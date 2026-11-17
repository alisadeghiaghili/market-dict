# MarketDict

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Deploy to GitHub Pages](https://github.com/alisadeghiaghili/market-dict/actions/workflows/deploy.yml/badge.svg)](https://github.com/alisadeghiaghili/market-dict/actions/workflows/deploy.yml)
[![Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-emerald?logo=github)](https://alisadeghiaghili.github.io/market-dict/)

A modern bilingual (English & Persian) financial dictionary — **6,108 market & investing terms** across 14 domains with real-time fuzzy search, KaTeX mathematical formulas, and internal term cross-linking — deployed as a zero-latency static web app on GitHub Pages and paired with an Investopedia enrichment pipeline.

👉 **Live Demo:** [https://alisadeghiaghili.github.io/market-dict/](https://alisadeghiaghili.github.io/market-dict/)

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
- **Cloudflare-Tolerant Scraper**: Headless, silent crawler utilizing `curl_cffi` (Chrome TLS fingerprinting) with exponential backoff and polite rate limiting.

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

---

## Scraping Investopedia Terms

The scraper traverses all 27 alphabetical subpages (`#`, `A` through `Z`) to discover and extract all financial terms across the entire dictionary, capturing complete definitions, key takeaways, and full Table of Contents sections.

```bash
# Scrape all 27 alphabetical subpages (#, A-Z) with full definitions, takeaways, and sections
python investopedia_scraper.py

# Scrape specific letter categories (e.g. A, B, and C)
python investopedia_scraper.py --letters a,b,c

# Fast catalog extraction (extract all 6,106+ term URLs and titles without body content)
python investopedia_scraper.py --no-details

# High-concurrency extraction with custom output filename
python investopedia_scraper.py --workers 16 -o full_investopedia_dictionary

# Run quietly in the background
python investopedia_scraper.py -q
```

---

## Production Deployment

For detailed production setup instructions using Docker or Gunicorn with Nginx and Systemd, refer to [DEPLOYMENT.md](DEPLOYMENT.md).

---

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Ali Sadeghi Aghili.
