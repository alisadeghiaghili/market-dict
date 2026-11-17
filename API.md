# MarketDict REST API Documentation 📈

> High-performance bilingual (English & Persian) Financial Terms REST API providing instant fuzzy search, 6,108 market terms across 32 domains, KaTeX mathematical formulas, and autocomplete suggestions.

---

### 🌐 Language / زبان مستندات:
- 🇮🇷 **[مستندات کامل به زبان فارسی (Persian Documentation)](API_FA.md)**
- 🇬🇧 **[Comprehensive English Reference Guide (English Documentation)](API_EN.md)**
- 📖 **[Interactive Swagger UI Explorer](http://localhost:5000/docs)**
- 📄 **[OpenAPI 3.0.3 Specification JSON](http://localhost:5000/api/v1/openapi.json)**

---

## 📌 Overview

- **Base URL (Local)**: `http://localhost:5000/api/v1`
- **Interactive Swagger Docs**: [`http://localhost:5000/docs`](http://localhost:5000/docs) (or [`/api/v1/docs`](http://localhost:5000/api/v1/docs))
- **OpenAPI 3.0.3 Spec**: `http://localhost:5000/api/v1/openapi.json`
- **Authentication**: **None (Open Access)**
- **CORS**: Fully enabled (`Access-Control-Allow-Origin: *`) for web applications, mobile apps, bots, and browser extensions.
- **Python Client SDK**: Included out-of-the-box in [`marketdict_client.py`](marketdict_client.py).

---

## 🚀 Quick Start

### Python SDK (Zero external dependencies)

```python
from marketdict_client import MarketDict

client = MarketDict("http://localhost:5000/api/v1")

# 1. Search financial terms in Persian or English
results = client.search(query="نسبت شارپ", limit=5)
for term in results["data"]:
    print(f"{term['term_en']} ({term['term_fa']}) - {term['category_icon']} {term['category_fa']}")

# 2. Get full term details with LaTeX formula
sharpe = client.get_term("sharperatio")
print(sharpe["formula"]["formula_en"])

# 3. Autocomplete prefix suggestions (<5ms)
suggestions = client.suggest("bit", limit=3)

# 4. Financial Term of the Day
random_term = client.get_random(has_deep=True)
print(random_term["term_en"], "-", random_term["definition_fa"])
```

### C# / .NET SDK (Compatible with .NET 6, 7, 8, 9 & .NET Standard)

Add [`MarketDictClient.cs`](MarketDictClient.cs) to your project (zero NuGet packages required):

```csharp
using MarketDict;

using var client = new MarketDictClient("http://localhost:5000/api/v1");

// 1. Search financial terms in Persian or English
var results = await client.SearchTermsAsync(query: "نسبت شارپ", limit: 5);
foreach (var term in results.Data)
{
    Console.WriteLine($"{term.TermEn} ({term.TermFa}) - {term.CategoryIcon} {term.CategoryFa}");
}

// 2. Get full term details with LaTeX formula
var sharpe = await client.GetTermAsync("sharperatio");
Console.WriteLine(sharpe.Formula?.FormulaEn);

// 3. Fast autocomplete suggestions (<5ms)
var suggestions = await client.SuggestAsync("bit", limit: 3);

// 4. Financial Term of the Day
var dailyTerm = await client.GetRandomTermAsync(hasDeep: true);
Console.WriteLine($"{dailyTerm.TermEn} - {dailyTerm.DefinitionFa}");
```

### JavaScript / TypeScript (`fetch`)

```javascript
// Search terms
const response = await fetch('http://localhost:5000/api/v1/terms?q=inflation&limit=5');
const { data, pagination } = await response.json();
console.log(`Found ${pagination.total} terms:`, data);

// Autocomplete suggestions
const suggestions = await fetch('http://localhost:5000/api/v1/suggest?q=cap')
  .then(res => res.json());
console.log(suggestions.data);
```

### cURL

```bash
# Health check
curl -s http://localhost:5000/api/v1/health

# Search terms in English or Persian
curl -s "http://localhost:5000/api/v1/terms?q=Sharpe&limit=2"

# Retrieve full details of a term
curl -s http://localhost:5000/api/v1/terms/sharperatio
```

---

## 📑 Response Standards

### Success Envelope
By default, all responses follow this standard envelope:

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
  }
}
```

> **Tip**: Add `?raw=true` to any request to bypass the envelope and receive the data array or object directly.

### Error Envelope
When an error occurs, the API returns standard HTTP status codes (400, 404, 500) and a descriptive JSON body:

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

## 🛠️ Endpoints Reference

### 1. System & Health

#### `GET /api/v1/health` (or `/api/v1/ping`)
Returns system status, version, uptime, and database metrics.

**Response:**
```json
{
  "status": "success",
  "data": {
    "service": "MarketDict API",
    "version": "1.0.0",
    "status": "healthy",
    "uptime_seconds": 182.4,
    "total_terms": 6108,
    "total_categories": 32,
    "total_letters": 27,
    "database": "sqlite_wal_active",
    "cache_status": "hot"
  }
}
```

#### `GET /api/v1/stats`
Returns dictionary content statistics.

---

### 2. Financial Terms

#### `GET /api/v1/terms`
Bilingual fuzzy search and filtering across all 6,108 terms.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `q` | string | `""` | Search query in English or Persian (fuzzy scoring + text normalization) |
| `letter` | string | - | Initial letter filter (`#`, `A` to `Z`) |
| `category` | string | - | Category slug (e.g. `crypto`, `derivatives`) or Persian name |
| `has_deep` | boolean | - | Filter only comprehensive terms with detailed subsections (`true`/`false`) |
| `has_formula` | boolean | - | Filter terms that feature mathematical formulas (`true`/`false`) |
| `sort` | string | `relevance` | Sort field: `relevance` (if `q`), `term_en`, `term_fa`, `id` |
| `order` | string | `asc` | Sort direction: `asc` or `desc` |
| `page` | integer | `1` | Page number |
| `limit` | integer | `20` | Items per page (max 100) |
| `fields` | string | - | Comma-separated field projection (e.g. `id,slug,term_en,term_fa`) |
| `raw` | boolean | `false` | Return plain array without envelope |

**Example Request:**
```bash
curl -s "http://localhost:5000/api/v1/terms?category=crypto&limit=2&fields=id,slug,term_en,term_fa"
```

---

#### `GET /api/v1/terms/{identifier}`
Lookup complete term details by **numeric ID** (e.g. `461`), **slug** (e.g. `sharperatio`), or clean title.

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
    "definition_fa": "نسبت شارپ معیاری برای اندازه‌گیری عملکرد یک سرمایه‌گذاری با تعدیل ریسک است...",
    "takeaways_en": [ ... ],
    "takeaways_fa": [ ... ],
    "bottom_line_en": "...",
    "bottom_line_fa": "...",
    "sections": [ ... ],
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

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `count` | integer | `1` | Number of random terms (1 to 10) |
| `category` | string | - | Filter pool by category |
| `has_deep` | boolean | - | Restrict pool to deeply enriched terms |

**Example:**
```bash
curl -s "http://localhost:5000/api/v1/terms/random?count=3"
```

---

#### `POST /api/v1/terms/batch` (or `GET /api/v1/terms/batch?ids=...`)
Retrieve multiple terms in a single round-trip.

**POST Body:**
```json
{
  "identifiers": ["sharperatio", 461, "cagr", "ebitda"]
}
```

---

### 3. Autocomplete / Instant Suggestions

#### `GET /api/v1/suggest` (or `/api/v1/autocomplete`)
Ultra-fast prefix search designed for search inputs, typeaheads, and mobile keyboards (<5ms latency).

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `q` | string | **required** | Query prefix (English or Persian) |
| `limit` | integer | `10` | Max suggestions (1 to 30) |

**Response:**
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

### 4. Categories & Taxonomy

#### `GET /api/v1/categories`
Returns all 32 financial categories with English and Persian names, emojis, term counts, and sub-resource URLs.

#### `GET /api/v1/categories/{category_id}`
Returns metadata for a single category (e.g. `crypto`, `derivatives`, `accounting`).

#### `GET /api/v1/categories/{category_id}/terms`
Paginated terms in that category (supports `page`, `limit`, `sort`, `fields`).

---

### 5. Alphabetical Browsing

#### `GET /api/v1/letters`
List all letters (`#`, `A` through `Z`) with term counts.

#### `GET /api/v1/letters/{letter}/terms`
Paginated terms starting with that letter.

---

### 6. Quantitative Financial Formulas

#### `GET /api/v1/formulas`
Returns all 44 financial metrics that include mathematical LaTeX formulas:
- Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio
- CAPM, Jensen's Alpha, Beta
- Black-Scholes Model, Put-Call Parity
- Break-Even Point (BEP), Accounting Equation, D/E Ratio, DSCR, WACC, EBIT/EBITDA
- CAGR, EPS, P/E, Dividend Payout, NAV, Free Cash Flow, etc.

Each item includes both **English & Persian LaTeX equations** and variable explanations.

---

## 💻 Integration Examples

### 1. Telegram / Discord Bot Integration (Python)

```python
import telebot
from marketdict_client import MarketDict

bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_TOKEN")
api = MarketDict("http://localhost:5000/api/v1")

@bot.message_handler(commands=['term'])
def handle_term(message):
    query = message.text.replace('/term', '').strip()
    if not query:
        bot.reply_to(message, "لطفاً عبارت مورد نظر را بنویسید:\nمثال: /term Sharpe")
        return

    results = api.search(query=query, limit=1)
    if not results["data"]:
        bot.reply_to(message, "❌ اصطلاحی یافت نشد.")
        return

    term = results["data"][0]
    reply = (
        f"📚 *{term['term_en']}* ({term['term_fa']})\n"
        f"🏷️ دسته‌بندی: {term['category_fa']}\n\n"
        f"{term['definition_fa']}\n\n"
        f"🔗 منبع: {term['url']}"
    )
    bot.reply_to(message, reply, parse_mode="Markdown")

bot.polling()
```

### 2. Browser Extension / Frontend Widget (Vanilla JS)

```javascript
async function searchFinancialTerms(keyword) {
  const url = `http://localhost:5000/api/v1/suggest?q=${encodeURIComponent(keyword)}&limit=5`;
  const res = await fetch(url);
  const json = await res.json();
  return json.data; // [{ id, slug, term_en, term_fa, category }]
}
```

### 3. ASP.NET Core Dependency Injection & Minimal API (C#)

```csharp
// Program.cs
using MarketDict;

var builder = WebApplication.CreateBuilder(args);

// Register MarketDictClient via IHttpClientFactory
builder.Services.AddHttpClient<MarketDictClient>(client =>
{
    client.BaseAddress = new Uri("http://localhost:5000/api/v1");
});

var app = builder.Build();

// Minimal API endpoint proxying financial search
app.MapGet("/api/financial-search", async (string q, MarketDictClient dict) =>
{
    var results = await dict.SearchTermsAsync(query: q, limit: 10);
    return Results.Ok(results.Data);
});

// Financial Word of the Day endpoint
app.MapGet("/api/term-of-the-day", async (MarketDictClient dict) =>
{
    var term = await dict.GetRandomTermAsync(hasDeep: true);
    return Results.Ok(term);
});

app.Run();
```

---

## 📄 License
Licensed under the [Apache License 2.0](LICENSE).
