# MarketDict MCP Server — Complete Bilingual Documentation
# مستندات جامع و دو زبانه سرور پروتکل زمینه مدل (MCP) برای MarketDict

> **Language / زبان:**
> - 🇮🇷 [بخش اول: راهنمای جامع فارسی (Persian Documentation)](#-بخش-اول-راهنمای-جامع-فارسی)
> - 🇬🇧 [Part 2: Complete English Documentation (مستندات انگلیسی)](#-part-2-complete-english-documentation)

---

```
  ┌───────────────────────────────────────────────────────────────┐
  │                        AI Clients                             │
  │   Claude Desktop  │  Cursor IDE  │  Antigravity  │  Cline    │
  └───────────────────────────────┬───────────────────────────────┘
                                  │ JSON-RPC (stdio / SSE)
                                  ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                  MarketDict MCP Server                        │
  │                      (mcp_server.py)                          │
  │   9 Tools   │   3 Resources   │   2 Prompts   │  Cache Index  │
  └───────┬───────────────────────┬───────────────────────┬───────┘
          │                       │                       │
          ▼                       ▼                       ▼
  ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
  │ SQLite Index  │       │ Formula DB    │       │  28 Taxonomy  │
  │ 6,108 Terms   │       │ 44 Math LaTeX │       │  Categories   │
  └───────────────┘       └───────────────┘       └───────────────┘
```

---

# 🇮🇷 بخش اول: راهنمای جامع فارسی

## ۱. مقدمه و معماری سیستم

**پروتکل زمینه مدل (Model Context Protocol یا به اختصار MCP)** یک استاندارد باز و نوین است که به مدل‌های زبانی بزرگ (LLM) و دستیاران هوش مصنوعی اجازه می‌دهد به صورت امن، دوطرفه و بلادرنگ به ابزارها، پایگاه‌های داده و منابع محلی متصل شوند.

سرور **MarketDict MCP** پلی میان هوش مصنوعی (نظیر Claude، Cursor، Antigravity و Cline) و پایگاه داده ۶,۱۰۸ واژه‌ای MarketDict برقرار می‌کند. این سرور مزایای زیر را فراهم می‌سازد:

- 🚀 **پاسخ‌دهی آنی (زیر ۱ میلی‌ثانیه)** با بهره‌گیری از نمایه باینری حافظه (RAM) و پایگاه داده SQLite در حالت WAL.
- 🔤 **جستجوی هوشمند فازی دو زبانه** با نرمال‌سازی تخصصی متون فارسی (یکسان‌سازی حروف `ی/ي`، `ک/ك`، اعراب‌زدایی و مدیریت نیم‌فاصله).
- 📐 **فرمول‌های ریاضی استاندارد LaTeX** با تشریح دقیق متغیرها به دو زبان فارسی و انگلیسی.
- 🏷️ **طبقه‌بندی ساختاریافته در ۳۲ دسته مالی** (ارز دیجیتال، ابزارهای مشتقه، مدیریت سبد دارایی، اقتصاد کلان و...).
- 🔒 **۱۰۰٪ محلی، آفلاین و خصوصی** بدون ارسال هیچ‌گونه دیتایی به سرورهای خارجی.

---

## ۲. پیش‌نیازها و نصب

برای اجرای سرور MCP به **پایتون نسخه ۳.۱۰ به بالا** نیاز دارید.

### مرحله ۱: نصب پکیج‌های مورد نیاز
```bash
# نصب پکیج رسمی MCP
pip install mcp>=1.0.0

# یا نصب تمام وابستگی‌های پروژه
pip install -r requirements.txt
```

### مرحله ۲: اجرای آزمون خودکار صحت عملکرد
پروژه مجهز به یک فایل تست جامع است که سلامت تمامی ابزارها، منابع و پرامپت‌ها را بررسی می‌کند:
```bash
python test_mcp_server.py
```
در صورت موفقیت‌آمیز بودن، پیام زیر را مشاهده خواهید کرد:
```text
============================================================
ALL TESTS PASSED SUCCESSFULLY! 🚀
============================================================
```

---

## ۳. راهنمای اتصال کلاینت‌های هوش مصنوعی (گام‌به‌گام)

### ۳.۱. اتصال به Claude Desktop

فایل کانفیگ کلود را بر اساس سیستم‌عامل خود باز کنید:
- **ویندوز**: `%APPDATA%\Claude\claude_desktop_config.json`
- **مک (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **لینوکس**: `~/.config/Claude/claude_desktop_config.json`

محتوای زیر را به کلید `mcpServers` اضافه کنید:

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

> 💡 **نکته ویندوز:** اگر از محیط مجازی (`.venv`) استفاده می‌کنید، به جای `"python"` آدرس کامل مفسر پایتون را وارد کنید (مانند: `C:/Users/IME/Desktop/Projects/Market-Dict/.venv/Scripts/python.exe`). پس از ویرایش فایل، Claude Desktop را ری‌استارت کنید. آیکون 🔨 (چکش) در نوار ورودی چت ظاهر خواهد شد.

---

### ۳.۲. اتصال به Cursor IDE

در ادیتور Cursor می‌توانید به دو روش عمل کنید:

#### روش اول: از طریق رابط کاربری (UI)
1. وارد بخش تنظیمات شوید: **Cursor Settings** -> **Features** -> **MCP**.
2. روی دکمه **+ Add New MCP Server** کلیک کنید.
3. مقادیر را مطابق زیر تنظیم نمایید:
   - **Name**: `marketdict`
   - **Type**: `command`
   - **Command**: `python c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py`
4. دکمه Refresh را بزنید؛ چراغ وضعیت سبز شده و تعداد ۹ ابزار شناسایی می‌شود.

#### روش دوم: از طریق فایل کانفیگ پروژه
فایلی به نام `.cursor/mcp.json` در ریشه پروژه بسازید:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "mcp_server.py"
      ]
    }
  }
}
```

---

### ۳.۳. اتصال به Google Antigravity

در محیط Antigravity، می‌توانید سرور را به صورت سراسری یا ویژه پروژه فعال کنید:
- **کانفیگ سراسری**: `~/.gemini/config/mcp_config.json`
- **کانفیگ اختصاصی پروژه**: `.agents/mcp_config.json` یا استفاده از [mcp_config.json](file:///c:/Users/IME/Desktop/Projects/Market-Dict/mcp_config.json) موجود در ریشه پروژه:

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### ۳.۴. اتصال به اکستنشن‌های VS Code (مانند Cline، Roo Code و Continue)

در اکستنشن Cline یا Roo Code:
1. روی آیکون افزونه در نوار کناری کلیک کنید.
2. به تب **MCP Servers** بروید.
3. در فایل `cline_mcp_settings.json` کانفیگ زیر را قرار دهید:

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": ["c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"],
      "disabled": false,
      "autoApprove": [
        "search_terms",
        "suggest_terms",
        "get_term_details",
        "get_financial_formula",
        "list_categories"
      ]
    }
  }
}
```

---

## ۴. مرجع کامل ابزارها (Tools Reference)

سرور MarketDict دارای **۹ ابزار تخصصی** است:

### ۱. `search_terms`
جستجوی فازی و رتبه‌بندی‌شده در میان ۶,۱۰۸ واژه تخصصی با اولویت‌بندی عنوان، تطابق پیشوندی، دسته‌بندی و توضیحات.

- **پارامترها:**
  - `query` (رشته، اجباری): کلمه یا عبارت مورد جستجو به فارسی یا انگلیسی (مانند `"تورم"`, `"sharpe ratio"`, `"اوراق قرضه"`).
  - `category` (رشته، اختیاری): فیلتر بر اساس نام یا شناسه دسته (مانند `"ارزهای دیجیتال و بلاک‌چین"`, `"crypto"`, `"derivatives"`).
  - `letter` (رشته، اختیاری): فیلتر بر اساس حرف اول انگلیسی (`"A"` تا `"Z"` یا `"#"`).
  - `limit` (عدد صحیح، پیش‌فرض ۱۰، سقف ۵۰): تعداد موارد بازگشتی در هر صفحه.
  - `page` (عدد صحیح، پیش‌فرض ۱): شماره صفحه جهت صفحه‌بندی.

- **نمونه خروجی:**
```json
{
  "query": "تورم",
  "total": 37,
  "page": 1,
  "limit": 2,
  "has_more": true,
  "terms": [
    {
      "id": 2690,
      "slug": "inflation",
      "term_en": "Inflation",
      "term_fa": "تورم",
      "letter": "I",
      "category": "اقتصاد کلان و سیاست پولی",
      "category_en": "Macroeconomics & Monetary Policy",
      "definition_en": "Inflation is the rate of increase in prices over a given period of time...",
      "definition_fa": "تورم نرخ افزایش قیمت‌ها در یک دوره زمانی معین است...",
      "takeaways_en": ["Inflation is the rate at which prices increase over time..."],
      "takeaways_fa": ["تورم نرخی است که قیمت‌ها در طول زمان با آن افزایش می‌یابند..."],
      "has_deep_content": true,
      "has_formula": false,
      "url": "https://www.investopedia.com/terms/i/inflation.asp"
    }
  ]
}
```

---

### ۲. `suggest_terms`
پیش‌بینی و تکمیل خودکار با سرعت رعدآسا (زیر ۵ میلی‌ثانیه) برای تایپ تعاملی و پیشنهاد سریع واژگان.

- **پارامترها:**
  - `prefix` (رشته، اجباری): حروف اولیه به فارسی یا انگلیسی (مانند `"infl"`, `"بیت"`, `"shar"`).
  - `limit` (عدد صحیح، پیش‌فرض ۸، سقف ۲۰): حداکثر تعداد پیشنهادات.

- **نمونه خروجی:**
```json
[
  {
    "slug": "sharperatio",
    "term_en": "Sharpe Ratio",
    "term_fa": "Sharpe نسبت",
    "category": "صندوق‌ها و مدیریت سبد دارایی",
    "category_en": "Mutual Funds & Portfolio Management"
  },
  {
    "slug": "share-certificate",
    "term_en": "Share Certificate",
    "term_fa": "سهم Certificate (Share Certificate)",
    "category": "بورس، اوراق بهادار و تحلیل بازار",
    "category_en": ""
  }
]
```

---

### ۳. `get_term_details`
دریافت دایره‌المعارفی اصطلاح به همراه متن کامل تعریف دو زبانه، نکات کلیدی (Takeaways)، نتیجه‌گیری نهایی (Bottom Line)، سرفصل‌های تشریحی و فرمول‌های محاسباتی.

- **پارامترها:**
  - `term_identifier` (رشته، اجباری): اسلاگ (`"sharpe-ratio"`), نام انگلیسی (`"Sharpe Ratio"`), نام فارسی (`"نسبت شارپ"`), یا شناسه عددی (`2690`).

- **نمونه خروجی:**
```json
{
  "found": true,
  "id": 4892,
  "slug": "sharperatio",
  "term_en": "Sharpe Ratio",
  "term_fa": "Sharpe نسبت",
  "letter": "S",
  "category": "صندوق‌ها و مدیریت سبد دارایی",
  "category_en": "Mutual Funds & Portfolio Management",
  "definition_en": "The Sharpe ratio compares the return of an investment with its risk...",
  "definition_fa": "نسبت شارپ بازده یک سرمایه‌گذاری را با ریسک آن مقایسه می‌کند...",
  "takeaways_en": [
    "The Sharpe ratio adjusts a portfolio's past performance for risk."
  ],
  "takeaways_fa": [
    "نسبت شارپ عملکرد گذشته سبد سرمایه‌گذاری را برای ریسک تعدیل می‌کند."
  ],
  "has_formula": true,
  "formula": {
    "formula_en": "$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$",
    "formula_fa": "$$\\text{نسبت شارپ} = \\frac{R_p - R_f}{\\sigma_p}$$"
  },
  "has_deep_content": true,
  "sections": [
    {
      "title_en": "What Is the Sharpe Ratio?",
      "title_fa": "نسبت شارپ چیست؟",
      "paragraphs_en": ["..."],
      "paragraphs_fa": ["..."],
      "items_en": [],
      "items_fa": []
    }
  ],
  "investopedia_url": "https://www.investopedia.com/terms/s/sharperatio.asp"
}
```

---

### ۴. `get_financial_formula`
بازیابی مستقیم فرمول ریاضی استاندارد LaTeX به همراه تشریح نام و نماد متغیرها به زبان انگلیسی و فارسی. این ابزار از اسامی مخفف (مانند `roe`, `roa`, `wacc`, `ebit`, `fcf`, `d/e`, `cagr`) نیز پشتیبانی می‌کند.

- **پارامترها:**
  - `term` (رشته، اجباری): نام، اسلاگ یا مخفف فرمول (مانند `"ebit"`, `"roe"`, `"cagr"`, `"sharpe-ratio"`, `"breakevenanalysis"`).

- **نمونه خروجی:**
```json
{
  "found": true,
  "key": "ebit",
  "term_info": {
    "term_en": "Earnings Before Interest and Taxes (EBIT)",
    "term_fa": "EBIT (سود قبل از بهره و مالیات)",
    "category": "حسابداری و صورت‌های مالی",
    "url": "https://www.investopedia.com/terms/e/ebit.asp"
  },
  "formula_latex_en": "$$\\text{EBIT} = \\text{Revenue} - \\text{COGS} - \\text{Operating Expenses}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &\\text{Revenue} = \\text{Total sales} \\\\ &\\text{COGS} = \\text{Cost of Goods Sold} \\end{aligned}$$",
  "formula_latex_fa": "$$\\text{سود قبل از بهره و مالیات (EBIT)} = \\text{درآمد فروش} - \\text{بهای تمام‌شده} - \\text{هزینه‌های عملیاتی}$$"
}
```

---

### ۵. `list_all_formulas`
کاتالوگ کامل کلیه فرمول‌های محاسباتی موجود در پایگاه داده.

- **پارامترها:**
  - `query` (رشته، اختیاری): فیلتر جستجو بر اساس کلمه کلیدی در فرمول‌ها.

---

### ۶. `list_categories`
فهرست کامل ۳۲ حوزه و دسته‌بندی موضوعی بازارهای مالی همراه با عنوان انگلیسی، عنوان فارسی، ایموجی اختصاصی و تعداد اصطلاحات هر دسته.

- **پارامترها:** ندارد.
- **نمونه خروجی:**
```json
[
  {
    "id": "management",
    "name_fa": "مدیریت کسب‌وکار و استراتژی",
    "name_en": "Business Strategy & Management",
    "icon": "💡",
    "count": 1029
  },
  {
    "id": "accounting",
    "name_fa": "حسابداری و صورت‌های مالی",
    "name_en": "Financial Accounting & Reporting",
    "icon": "📑",
    "count": 604
  },
  {
    "id": "stocks",
    "name_fa": "بازار سهام و معاملات",
    "name_en": "Stock Market & Equities Trading",
    "icon": "📈",
    "count": 488
  }
]
```

---

### ۷. `list_letters`
فهرست حروف الفبای انگلیسی (`#` و `A` تا `Z`) و تعداد اصطلاحات اختصاص‌یافته به هر حرف.

---

### ۸. `get_random_term`
دریافت یک اصطلاح تصادفی برای سناریوهایی نظیر اصطلاح روز، ربات‌های شبکه‌های اجتماعی، کوییزهای مالی یا مطالعات دوره‌ای.

- **پارامترها:**
  - `category` (رشته، اختیاری): محدود کردن انتخاب به یک دسته موضوعی خاص.
  - `only_deep_enriched` (بولین، پیش‌فرض `true`): فیلتر کردن تنها اصطلاحاتی که مقاله کامل و سرفصل‌های تشریحی دارند.

---

### ۹. `get_dictionary_stats`
دریافت آمارهای کلیدی از کل مخزن لغت‌نامه.

- **نمونه خروجی:**
```json
{
  "total_terms": 6108,
  "total_categories": 32,
  "total_letters": 27,
  "deep_enriched_count": 6108,
  "total_formulas": 44,
  "languages": ["English", "Persian"]
}
```

---

## ۵. مرجع منابع داده (Resources Reference)

منابع MCP به مدل اجازه می‌دهند داده‌های ایستا یا ساخت‌یافته را مستقیماً مانند فایل مطالعه کند:

| آدرس منبع (URI) | شرح داده |
| :--- | :--- |
| `marketdict://stats` | خلاصه آمار دیکشنری در قالب JSON |
| `marketdict://categories` | فهرست ساختاریافته ۳۲ دسته‌بندی و تعداد کلمات |
| `marketdict://formulas` | کاتالوگ تمام فرمول‌های ثبت‌شده در رجیستری |
| `marketdict://terms/{slug}` | دیتای کامل شیء JSON برای یک اصطلاح معین بر اساس اسلاگ (مثلاً `marketdict://terms/sharperatio`) |

---

## ۶. الگوهای پرامپت (Prompt Templates)

سرور MarketDict دارای دو قالب پرامپت آماده برای مدل‌های زبانی است:

### ۱. `explain_financial_term`
تولید یک پرامپت ساختاریافته برای آموزش و کالبدشکافی یک مفهوم مالی:
- **پارامترها:**
  - `term` (رشته، اجباری): نام مفهوم (مثلاً `"Sharpe Ratio"`, `"تورم"`).
  - `language` (رشته، پیش‌فرض `"bilingual"`): زبان پاسخ (`"fa"`, `"en"` یا `"bilingual"`).
  - `target_audience` (رشته، پیش‌فرض `"general"`): سطح مخاطب (`"beginner"`, `"general"`, `"advanced"`, `"student"`).

### ۲. `compare_financial_terms`
ایجاد پرامپت تحلیلی و مقایسه‌ای میان دو مفهوم مالی با جدول مقایسه، سناریوهای کاربرد و تمایزات فرمولی:
- **پارامترها:** `term1`, `term2`, `language`.

---

## ۷. مدهای مختلف راه‌اندازی و CLI

سرور را می‌توان به حالت‌های گوناگون اجرا کرد:

```bash
# مد پیش‌فرض: ارتباط Stdio (برای دستیارهای محلی)
python mcp_server.py

# مد شبکه و سرور وب با استفاده از SSE:
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000

# مد Streamable HTTP (استاندارد نوین MCP):
python mcp_server.py --transport streamable-http --host 127.0.0.1 --port 8000
```

---

## ۸. سوالات متداول و عیب‌یابی (FAQ)

### ۱. خطای شناسایی نشدن پایتون در Claude Desktop
- **علت:** ممکن است `python` در متغیر محیطی `PATH` سیستم قرار نداشته باشد.
- **راه حل:** در فایل کانفیگ JSON، به جای `"python"` مسیر کامل فایل اجرایی را بگذارید، مثلاً:
  `"command": "C:\\Users\\IME\\AppData\\Local\\Python\\pythoncore-3.15-64\\python.exe"`

### ۲. نمایش نادرست حروف فارسی در ویندوز
- **علت:** عدم تنظیم انکودینگ UTF-8 در پایپ استریم کنسول ویندوز.
- **راه حل:** در کلید `"env"` کانفیگ MCP، مقدار `"PYTHONIOENCODING": "utf-8"` را قرار دهید (در فایل‌های نمونه اعمال شده است).

### ۳. آیا سرور نیاز دارد که وب‌سرور فلسک (`python app.py`) همیشه روشن باشد؟
- **خیر!** سرور `mcp_server.py` کاملاً خودکفا بوده و مستقیماً با SQLite و فایل ایندکس باینری کار می‌کند و نیازی به اجرای سرور وب ندارد.

---
---

# 🇬🇧 Part 2: Complete English Documentation

## 1. Overview & Architecture

The **Model Context Protocol (MCP)** is an open standard designed by Anthropic and the open-source community that enables Large Language Models (LLMs) to seamlessly access tools, data stores, and context providers with safety and low latency.

The **MarketDict MCP Server** connects AI applications (Claude Desktop, Cursor IDE, Google Antigravity, Cline, Continue, etc.) directly to the MarketDict bilingual financial dictionary database.

### Key Highlights:
- ⚡ **Sub-millisecond Retrieval**: In-memory binary cache combined with SQLite WAL-mode indexing for instantaneous responses.
- 🌐 **6,108 Financial Terms**: Complete bilingual coverage in English and Persian.
- 📐 **LaTeX Mathematical Formulas**: 44+ standardized financial math formulas with comprehensive variable explanations.
- 🏷️ **32 Taxonomy Domains**: Spanning Cryptocurrency, Derivatives, Corporate Finance, Quantitative Analysis, Real Estate, and more.
- 🔒 **100% Offline & Private**: Zero cloud dependency; all queries execute locally on your machine.

---

## 2. Requirements & Installation

### Requirements:
- Python 3.10 or higher.
- `mcp>=1.0.0` (Official Model Context Protocol SDK).

### Step 1: Install Dependencies
```bash
# Install the official MCP package
pip install mcp>=1.0.0

# Or install repository dependencies
pip install -r requirements.txt
```

### Step 2: Run Verification Test Suite
```bash
python test_mcp_server.py
```
Expected output:
```text
============================================================
ALL TESTS PASSED SUCCESSFULLY! 🚀
============================================================
```

---

## 3. Client Configuration Guides

### 3.1. Claude Desktop Setup

Locate your Claude Desktop configuration file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the `marketdict` server under the `mcpServers` object:

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

> **Tip:** If you use a virtual environment, specify the full path to the virtualenv python binary (e.g., `C:/Users/IME/Desktop/Projects/Market-Dict/.venv/Scripts/python.exe`). Restart Claude Desktop to activate the tools.

---

### 3.2. Cursor IDE Setup

#### Option A: Via Settings UI
1. Open **Cursor Settings** -> **Features** -> **MCP**.
2. Click **+ Add New MCP Server**.
3. Fill in the fields:
   - **Name**: `marketdict`
   - **Type**: `command`
   - **Command**: `python c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py`
4. Click Save and Refresh. You will see a green status indicator and 9 tools discovered.

#### Option B: Via Workspace Config
Create `.cursor/mcp.json` at the root of your project:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "mcp_server.py"
      ]
    }
  }
}
```

---

### 3.3. Google Antigravity Setup

Configure MarketDict in your Antigravity environment:
- **Global Config**: `~/.gemini/config/mcp_config.json`
- **Project Config**: `.agents/mcp_config.json` or the included [mcp_config.json](file:///c:/Users/IME/Desktop/Projects/Market-Dict/mcp_config.json):

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### 3.4. VS Code Extensions (Cline, Roo Code, Continue)

In your VS Code extension settings (e.g. `cline_mcp_settings.json`):
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "disabled": false,
      "autoApprove": [
        "search_terms",
        "suggest_terms",
        "get_term_details",
        "get_financial_formula",
        "list_categories"
      ]
    }
  }
}
```

---

## 4. MCP Tools Reference

The MarketDict MCP Server exposes **9 dedicated tools**:

### 1. `search_terms`
Search through 6,108 terms with bilingual fuzzy search, Persian normalization, category filtering, and pagination.

- **Parameters:**
  - `query` (string, required): Search query in English or Persian (e.g., `"inflation"`, `"تورم"`, `"sharpe ratio"`).
  - `category` (string, optional): Filter by category name or ID (e.g., `"crypto"`, `"derivatives"`, `"ارزهای دیجیتال"`).
  - `letter` (string, optional): Filter by alphabetical letter (`"A"`-`"Z"` or `"#"`).
  - `limit` (integer, default 10, max 50): Number of items per page.
  - `page` (integer, default 1): Page index for pagination.

- **Example Output:**
```json
{
  "query": "inflation",
  "total": 34,
  "page": 1,
  "limit": 1,
  "has_more": true,
  "terms": [
    {
      "id": 2690,
      "slug": "inflation",
      "term_en": "Inflation",
      "term_fa": "تورم",
      "letter": "I",
      "category": "اقتصاد کلان و سیاست پولی",
      "category_en": "Macroeconomics & Monetary Policy",
      "definition_en": "Inflation is the rate of increase in prices over a given period of time...",
      "definition_fa": "تورم نرخ افزایش قیمت‌ها در یک دوره زمانی معین است...",
      "has_deep_content": true,
      "has_formula": false,
      "url": "https://www.investopedia.com/terms/i/inflation.asp"
    }
  ]
}
```

---

### 2. `suggest_terms`
Ultra-fast prefix search designed for instant auto-completion (<5ms).

- **Parameters:**
  - `prefix` (string, required): Prefix string (e.g., `"infl"`, `"shar"`, `"بیت"`).
  - `limit` (integer, default 8, max 20): Maximum number of suggestions.

---

### 3. `get_term_details`
Retrieve comprehensive bilingual information for any financial term.

- **Parameters:**
  - `term_identifier` (string, required): Term slug (`"sharpe-ratio"`), English title (`"Sharpe Ratio"`), Persian title (`"نسبت شارپ"`), or ID (`4892`).

- **Returned Fields:**
  - Full English & Persian definitions.
  - Bulleted English & Persian Key Takeaways.
  - Bottom Line / Conclusion in both languages.
  - Associated mathematical LaTeX formula (if registered).
  - Deep article sections with paragraphs and sub-items.
  - Canonical Investopedia source URL.

---

### 4. `get_financial_formula`
Retrieve standardized LaTeX equations for quantitative finance metrics.

- **Parameters:**
  - `term` (string, required): Term name, acronym, or slug (e.g., `"sharpe-ratio"`, `"roe"`, `"roa"`, `"ebit"`, `"wacc"`, `"cagr"`, `"dscr"`, `"debtequityratio"`).

- **Returned Fields:**
  - `formula_latex_en`: English LaTeX equation with variable definitions.
  - `formula_latex_fa`: Persian translated LaTeX equation with localized definitions.

---

### 5. `list_all_formulas`
Catalog of all 44 registered quantitative finance formulas.

- **Parameters:**
  - `query` (string, optional): Keyword filter.

---

### 6. `list_categories`
List all 32 financial taxonomy categories with icons, English names, Persian names, and term counts.

---

### 7. `list_letters`
List all alphabetical index letters (`#`, `A` to `Z`) with term counts.

---

### 8. `get_random_term`
Retrieve a random term for daily concepts, study quizzes, or exploration.

- **Parameters:**
  - `category` (string, optional): Restrict to a specific category.
  - `only_deep_enriched` (boolean, default `true`): Restrict to multi-section comprehensive articles.

---

### 9. `get_dictionary_stats`
Returns high-level statistics of the entire database.

---

## 5. MCP Resources Reference

Clients can read and mount MarketDict knowledge resources directly:

| Resource URI | Description |
| :--- | :--- |
| `marketdict://stats` | High-level dictionary metrics and statistics (JSON). |
| `marketdict://categories` | Complete taxonomy of all 32 financial domains (JSON). |
| `marketdict://formulas` | Full registry of mathematical formulas (JSON). |
| `marketdict://terms/{slug}` | Complete JSON representation of a specific financial term. |

---

## 6. MCP Prompt Templates Reference

Interactive prompt templates for LLMs:

### 1. `explain_financial_term`
Generates a CFA-grade prompt instructing the LLM to explain a concept utilizing the verified definition, formulas, and takeaways from MarketDict.
- **Arguments**: `term`, `language` (`"bilingual"`, `"fa"`, or `"en"`), `target_audience` (`"beginner"`, `"general"`, `"advanced"`, `"student"`).

### 2. `compare_financial_terms`
Generates a structured prompt comparing two financial concepts side-by-side with reference data for both terms.
- **Arguments**: `term1`, `term2`, `language`.

---

## 7. CLI Usage & Transport Modes

```bash
# Standard stdio mode (Default for local desktop assistants)
python mcp_server.py

# SSE transport mode (For web or networked clients)
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000

# Streamable HTTP mode (MCP 2025/2026 specification)
python mcp_server.py --transport streamable-http --host 127.0.0.1 --port 8000
```

---

## 8. Troubleshooting & FAQ

#### Q: How do I test if the MCP server is communicating correctly over stdio?
Run the test suite:
```bash
python test_mcp_server.py
```
Or execute an interactive stdio test using python to send a JSON-RPC `initialize` handshake.

#### Q: Does `mcp_server.py` require the Flask server (`python app.py`) to be active?
**No.** `mcp_server.py` accesses `market_dict.db` and the in-memory cache directly with sub-millisecond query execution. It does not require any background web server.

#### Q: How are non-English characters handled?
The server automatically applies Persian text normalization (`ی/ي`, `ک/ك`, ZWNJ removal, and diacritic stripping) so that both formal Persian and user-typed variations match accurately.
