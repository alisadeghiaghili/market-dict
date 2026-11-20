# MarketDict REST API Comprehensive Reference Guide 📈

> Official developer documentation for the MarketDict Bilingual (English & Persian) Financial Terms REST API, featuring 6,108 financial terms, 32 financial taxonomy categories, 44 KaTeX/LaTeX mathematical formulas, and an ultra-fast fuzzy search engine.

---

## Table of Contents

1. [Introduction & Architecture](#1-introduction--architecture)
2. [Base URLs & Interactive Documentation](#2-base-urls--interactive-documentation)
3. [Authentication & Security](#3-authentication--security)
4. [CORS Policy & Cross-Origin Access](#4-cors-policy--cross-origin-access)
5. [Response Standards & Envelope Format](#5-response-standards--envelope-format)
6. [Complete Endpoints Reference](#6-complete-endpoints-reference)
   - [6.1 System Status & Statistics](#61-system-status--statistics)
   - [6.2 Terms Search & Details](#62-terms-search--details)
   - [6.3 Autocomplete & Suggestions](#63-autocomplete--suggestions)
   - [6.4 Financial Categories](#64-financial-categories)
   - [6.5 Alphabetical Browsing](#65-alphabetical-browsing)
   - [6.6 Quantitative Formulas](#66-quantitative-formulas)
   - [6.7 Batch Operations](#67-batch-operations)
7. [Data Models & Schemas](#7-data-models--schemas)
8. [Code Examples Across Languages](#8-code-examples-across-languages)
   - [8.1 Python SDK](#81-python-sdk)
   - [8.2 C# / .NET SDK](#82-c--net-sdk)
   - [8.3 JavaScript / TypeScript](#83-javascript--typescript)
   - [8.4 cURL Commands](#84-curl-commands)
9. [Real-World Recipes & Use Cases](#9-real-world-recipes--use-cases)
10. [Error Codes & Troubleshooting](#10-error-codes--troubleshooting)

---

## 1. Introduction & Architecture

MarketDict provides a high-performance knowledge base of global financial terminology paired with professional Persian translations, definitions, key takeaways, and mathematical formula specifications.

The API is specifically engineered for:
- Mobile Applications (iOS, Android, Flutter, React Native)
- Web Frontends & Financial Dashboards
- Trading Bots & Algorithmic Execution Systems
- Chatbots & Messengers (Telegram, Discord, Slack)
- Browser Extensions & Spreadsheet Integrations (Excel, Google Sheets)

All text search operations feature **intelligent text normalization** for Persian (unifying `ي/ی`, `ك/ک`, zero-width non-joiners, and diacritics removal) and case-insensitive English indexing.

---

## 2. Base URLs & Interactive Documentation

| Environment | Base URL | Description |
| :--- | :--- | :--- |
| **Local Development** | `http://localhost:5000/api/v1` | Live Flask server backed by SQLite (WAL mode) and in-memory indexes |
| **Interactive Swagger UI** | `http://localhost:5000/docs` (or `/api/v1/docs`) | Interactive browser-based API explorer with "Try it out" buttons |
| **OpenAPI 3.0.3 Spec** | `http://localhost:5000/api/v1/openapi.json` | Formal machine-readable OpenAPI specification |
| **Serverless Static Build** | `dist/api/v1/` (output of `python build_static.py`) | Pre-rendered static snapshots for internal hosting only; see [DATA_NOTICE.md](DATA_NOTICE.md) |

---

## 3. Authentication & Security

- **Access Level**: **100% Open Access**
- **API Keys / Tokens**: **None required**. No sign-up, authorization headers, or registration needed.
- **Rate Limits**: Unrestricted for normal application usage.

---

## 4. CORS Policy & Cross-Origin Access

The API ships with unrestricted Cross-Origin Resource Sharing (CORS) headers on all routes:
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS, HEAD
Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With, Accept
X-API-Version: 1.0.0
```
This enables zero-configuration integration in single-page apps (SPAs), webviews, and server-side runtimes. Preflight `OPTIONS` requests receive an automatic `204 No Content` response.

---

## 5. Response Standards & Envelope Format

### 5.1 Success Envelope
All successful requests return a JSON object with this standard envelope:

```json
{
  "status": "success",
  "data": { ... },
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 6108,
    "total_pages": 306,
    "has_next": true,
    "has_prev": false,
    "next_page": 2,
    "prev_page": null
  },
  "meta": {
    "timestamp": 1731845000.0,
    "version": "1.0.0"
  }
}
```

> **Pro Tip (`raw=true` parameter)**: Pass `raw=true` in the query string to bypass the wrapper envelope and receive the data array or object directly.

### 5.2 Error Envelope
When a request fails, a structured error payload accompanied by standard HTTP status codes (400, 404, 500) is returned:

```json
{
  "status": "error",
  "error": {
    "code": 404,
    "message": "Term 'xyz' not found",
    "details": "No financial term matched the identifier 'xyz'."
  }
}
```

---

## 6. Complete Endpoints Reference

### 6.1 System Status & Statistics

#### `GET /api/v1/health` (or `/api/v1/ping`)
Service health check, uptime, cache status, and database connectivity.

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "service": "MarketDict API",
    "version": "1.0.0",
    "status": "healthy",
    "uptime_seconds": 128.5,
    "total_terms": 6108,
    "total_categories": 32,
    "total_letters": 27,
    "database": "sqlite_wal_active",
    "cache_status": "hot"
  }
}
```

#### `GET /api/v1/stats`
Statistical metrics on vocabulary size, categorized distribution, and formulas.

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "total_terms": 6108,
    "total_categories": 32,
    "total_letters": 27,
    "deep_enriched_count": 3125,
    "formulas_count": 44,
    "languages": ["fa", "en"]
  }
}
```

---

### 6.2 Terms Search & Details

#### `GET /api/v1/terms`
Bilingual fuzzy search and filtering across 6,108 financial terms with pagination and field projection.

**Query Parameters:**

| Parameter | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `q` | `string` | `""` | Search query in English or Persian (fuzzy scoring) |
| `category` | `string` | - | Category slug (e.g. `crypto`, `derivatives`) or Persian name |
| `letter` | `string` | - | Initial letter filter (`#`, `A` through `Z`) |
| `has_deep` | `boolean` | - | Filter terms with comprehensive multi-section articles (`true`/`false`) |
| `has_formula` | `boolean` | - | Filter terms containing LaTeX mathematical formulas (`true`/`false`) |
| `sort` | `string` | `relevance` | Sort field: `relevance` (default when `q` is given), `term_en`, `term_fa`, `id` |
| `order` | `string` | `asc` | Sort direction: `asc` or `desc` |
| `page` | `integer` | `1` | Page number (1-based) |
| `limit` | `integer` | `20` | Items per page (max 100) |
| `fields` | `string` | - | Comma-separated field projection (e.g. `id,slug,term_en,term_fa`) |
| `raw` | `boolean` | `false` | Return bare JSON array without pagination envelope |

**Example Request:**
```bash
curl -s "http://localhost:5000/api/v1/terms?category=crypto&limit=2&fields=id,slug,term_en,term_fa"
```

---

#### `GET /api/v1/terms/{identifier}`
Retrieve complete term details by **numeric ID** (e.g. `461`), **slug** (e.g. `sharperatio`), or exact title.

- **Path Parameter**:
  - `identifier`: Integer ID, slug, or title.
- **Query Parameters**:
  - `fields`: Comma-separated field list
  - `raw`: `true` to return data object without envelope

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "id": 461,
    "slug": "sharperatio",
    "term_en": "Sharpe Ratio",
    "term_fa": "نسبت شارپ",
    "letter": "S",
    "category": "روش‌های کمی و ریاضیات مالی",
    "category_id": "quant_math",
    "category_en": "Quantitative Methods & Financial Math",
    "category_icon": "📐",
    "definition_en": "The Sharpe ratio compares the return of an investment with its risk...",
    "definition_fa": "نسبت شارپ معیاری برای ارزیابی بازده سرمایه‌گذاری نسبت به ریسک آن است...",
    "takeaways_en": [ ... ],
    "takeaways_fa": [ ... ],
    "bottom_line_en": "...",
    "bottom_line_fa": "...",
    "sections": [
      {
        "title_en": "What Is the Sharpe Ratio?",
        "title_fa": "نسبت شارپ چیست؟",
        "paragraphs_en": [ ... ],
        "paragraphs_fa": [ ... ]
      }
    ],
    "formula": {
      "formula_en": "$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$",
      "formula_fa": "$$\\text{نسبت شارپ} = \\frac{R_p - R_f}{\\sigma_p}$$"
    },
    "url": "https://www.investopedia.com/terms/s/sharperatio.asp"
  }
}
```

---

#### `GET /api/v1/terms/random`
Get one or more randomly selected terms.

**Query Parameters:**
- `count`: Number of terms to retrieve (1 to 10, default: 1).
- `category`: Restrict random pool to a specific category.
- `has_deep`: Restrict pool to deeply enriched terms (`true`/`false`).

---

### 6.3 Autocomplete & Suggestions

#### `GET /api/v1/suggest` (or `/api/v1/autocomplete`)
High-speed autocomplete endpoint (<5ms response time) designed for search inputs, typeaheads, and mobile applications.

**Query Parameters:**
- `q` (**Required**): Search prefix (min 1 character).
- `limit` (Optional): Maximum suggestions (1 to 30, default: 10).

**Response Example:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 461,
      "slug": "sharperatio",
      "term_en": "Sharpe Ratio",
      "term_fa": "نسبت شارپ",
      "category": "روش‌های کمی و ریاضیات مالی"
    }
  ]
}
```

---

### 6.4 Financial Categories

#### `GET /api/v1/categories`
List all 32 financial categories with English/Persian names, emoji icons, term counts, and sub-resource endpoints.

#### `GET /api/v1/categories/{category_id}`
Retrieve metadata and metrics for a specific category using its slug (`crypto`, `quant_math`, `derivatives`) or Persian name.

#### `GET /api/v1/categories/{category_id}/terms`
Paginated terms belonging to this category (supports `page`, `limit`, `sort`, `fields`).

---

### 6.5 Alphabetical Browsing

#### `GET /api/v1/letters`
List all letters (`#` and `A` to `Z`) with term counts.

#### `GET /api/v1/letters/{letter}/terms`
Paginated terms starting with the requested letter.

---

### 6.6 Quantitative Formulas

#### `GET /api/v1/formulas`
Returns all 44 financial metrics that feature KaTeX/LaTeX mathematical formulas:
- Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio
- Capital Asset Pricing Model (CAPM), Jensen's Alpha, Beta
- Break-Even Point (BEP), Accounting Equation, Debt-to-Equity (D/E), DSCR
- Operating Earnings (EBIT/EBITDA), WACC
- Compound Annual Growth Rate (CAGR), Earnings Per Share (EPS), P/E Ratio, Net Asset Value (NAV)
- Technical Analysis (MACD) and Statistical Distributions

Each entry contains both **English & Persian LaTeX equations** along with variable definitions.

---

### 6.7 Batch Operations

#### `POST /api/v1/terms/batch`
Retrieve multiple terms in a single HTTP request to minimize network round-trips.

**Request Body (JSON):**
```json
{
  "identifiers": ["sharperatio", "461", "cagr", "ebitda"]
}
```

**Response Example:**
```json
{
  "status": "success",
  "data": [ ... array of resolved term detail objects ... ],
  "meta": {
    "requested": 4,
    "found": 4,
    "missing": []
  }
}
```

> **Query String Alternative**: `GET /api/v1/terms/batch?ids=sharperatio,461,cagr` is also supported.

---

## 7. Data Models & Schemas

### `TermSummary` Interface
```typescript
interface TermSummary {
  id: number;                 // Unique integer identifier
  slug: string;               // URL-friendly identifier
  term_en: string;            // English term name
  term_fa: string;            // Persian translation
  letter: string;             // Alphabetical bucket ('A'-'Z', '#')
  category: string;           // Category name in Persian
  category_id: string;        // Normalized category slug (e.g. 'crypto')
  category_fa: string;        // Category name in Persian
  category_en: string;        // Category name in English
  category_icon: string;      // Category emoji icon
  definition_fa: string;      // Persian definition preview (up to 350 chars)
  definition_en: string;      // English definition preview (up to 350 chars)
  has_deep: boolean;          // Whether full multi-section article exists
  has_formula: boolean;       // Whether mathematical formula exists
  url: string;                // Source Investopedia URL
}
```

### `TermDetail` Interface
Extends `TermSummary` with:
- `takeaways_en` / `takeaways_fa`: Bullet-point key takeaways
- `bottom_line_en` / `bottom_line_fa`: Article conclusion
- `sections`: Structured array of subsections (`title_en`, `title_fa`, `paragraphs_en`, `paragraphs_fa`, `items_en`, `items_fa`)
- `formula`: LaTeX math object (`formula_en`, `formula_fa`)

---

## 8. Code Examples Across Languages

### 8.1 Python SDK

Use [`marketdict_client.py`](marketdict_client.py) with zero external dependencies:

```python
from marketdict_client import MarketDict

client = MarketDict("http://localhost:5000/api/v1")

# 1. Bilingual Search
res = client.search(query="نسبت شارپ", limit=5)
for term in res["data"]:
    print(f"📌 {term['term_en']} ({term['term_fa']}) - {term['category_icon']} {term['category_fa']}")

# 2. Term Details with LaTeX Formula
sharpe = client.get_term("sharperatio")
print(sharpe["definition_fa"][:150])
if sharpe.get("formula"):
    print("Formula LaTeX:\n", sharpe["formula"]["formula_en"])

# 3. Fast Autocomplete
for s in client.suggest("bit", limit=4):
    print(f"👉 [{s['id']}] {s['term_en']} -> {s['term_fa']}")

# 4. Random Term of the Day
random_term = client.get_random(has_deep=True)
print("Term of the Day:", random_term["term_en"])
```

---

### 8.2 C# / .NET SDK

Drop [`MarketDictClient.cs`](MarketDictClient.cs) directly into any .NET 6/7/8/9, .NET Standard, or Framework project:

```csharp
using System;
using System.Threading.Tasks;
using MarketDict;

class Program
{
    static async Task Main()
    {
        using var client = new MarketDictClient("http://localhost:5000/api/v1");

        // 1. Search Terms
        var results = await client.SearchTermsAsync(query: "نسبت شارپ", limit: 3);
        foreach (var term in results.Data)
        {
            Console.WriteLine($"📌 {term.TermEn} ({term.TermFa}) - {term.CategoryIcon} {term.CategoryFa}");
        }

        // 2. Term Detail with LaTeX
        var term = await client.GetTermAsync("sharperatio");
        Console.WriteLine($"Definition: {term.DefinitionFa}");
        if (term.Formula != null)
        {
            Console.WriteLine($"LaTeX: {term.Formula.FormulaEn}");
        }

        // 3. Autocomplete
        var suggestions = await client.SuggestAsync("bit", limit: 4);
        foreach (var s in suggestions)
        {
            Console.WriteLine($"👉 [{s.Id}] {s.TermEn} -> {s.TermFa}");
        }
    }
}
```

#### ASP.NET Core Dependency Injection:
```csharp
builder.Services.AddHttpClient<MarketDictClient>(client =>
{
    client.BaseAddress = new Uri("http://localhost:5000/api/v1");
});
```

---

### 8.3 JavaScript / TypeScript

```javascript
// 1. Search Terms
async function searchTerms(query) {
  const url = `http://localhost:5000/api/v1/terms?q=${encodeURIComponent(query)}&limit=5`;
  const res = await fetch(url);
  const { data, pagination } = await res.json();
  console.log(`Found ${pagination.total} terms:`, data);
}

// 2. Instant Autocomplete
async function getSuggestions(prefix) {
  const res = await fetch(`http://localhost:5000/api/v1/suggest?q=${encodeURIComponent(prefix)}&limit=5`);
  const { data } = await res.json();
  return data;
}

// 3. Quantitative Formulas
async function getFormulas() {
  const res = await fetch('http://localhost:5000/api/v1/formulas');
  const { data } = await res.json();
  return data;
}
```

---

### 8.4 cURL Commands

```bash
# Health Check
curl -s http://localhost:5000/api/v1/health

# Statistics
curl -s http://localhost:5000/api/v1/stats

# Search by English or Persian Keyword
curl -s "http://localhost:5000/api/v1/terms?q=inflation&limit=3"

# Lookup by Integer ID
curl -s http://localhost:5000/api/v1/terms/461

# Get Random Term
curl -s http://localhost:5000/api/v1/terms/random

# List All 32 Categories
curl -s http://localhost:5000/api/v1/categories

# List All 44 Quantitative Formulas
curl -s http://localhost:5000/api/v1/formulas
```

---

## 9. Real-World Recipes & Use Cases

1. **Telegram / Discord Financial Bots**:
   Deploy interactive `/term <query>` commands or automated daily broadcast messages utilizing `/api/v1/terms/random`.
2. **Browser Search Extension**:
   Highlight any financial terminology on Bloomberg, Financial Times, or Reuters and pop up full Persian definitions fetched via `/api/v1/terms/{slug}`.
3. **Quantitative Calculator Tools**:
   Render rich mathematical formulas and variable descriptions side-by-side with user calculation forms using `/api/v1/formulas`.
4. **Live Search Typeahead Widgets**:
   Bind browser `input` events directly to `/api/v1/suggest` for ultra-responsive search dropdowns.

---

## 10. Error Codes & Troubleshooting

| HTTP Status | Meaning | Resolution |
| :---: | :--- | :--- |
| **`200 OK`** | Request Succeeded | Normal response. |
| **`204 No Content`** | CORS Preflight Response | Returned automatically for browser `OPTIONS` preflight requests. |
| **`400 Bad Request`** | Invalid Parameters | Check query string parameters (e.g. invalid `page` or `limit` format). |
| **`404 Not Found`** | Resource Missing | No financial term or category matches the requested identifier. |
| **`500 Internal Error`** | Server Error | Check application server logs. |

---

## 📄 License
MarketDict and its REST API are released under the open-source **[Apache License 2.0](LICENSE)**.
Copyright (c) 2026 Ali Sadeghi Aghili.
