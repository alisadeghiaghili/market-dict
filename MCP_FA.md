# مستندات جامع سرور پروتکل زمینه مدل (MCP) برای MarketDict 🤖

> راهنمای تخصصی اتصال دستیاران هوش مصنوعی (**Claude Desktop**, **Cursor IDE**, **Google Antigravity**, **Cline**) به پایگاه دانش مالی دو زبانه MarketDict.

---

## فهرست مطالب

1. [معرفی و معماری](#۱-معرفی-و-معماری)
2. [پیش‌نیازها و نصب](#۲-پیش‌نیازها-و-نصب)
3. [راهنمای راه‌اندازی کلاینت‌ها](#۳-راهنمای-راه‌اندازی-کلاینت‌ها)
   - [Claude Desktop](#۳۱-اتصال-به-claude-desktop)
   - [Cursor IDE](#۳۲-اتصال-به-cursor-ide)
   - [Google Antigravity](#۳۳-اتصال-به-google-antigravity)
   - [اکستنشن‌های VS Code](#۳۴-اتصال-به-اکستنشن‌های-vs-code)
4. [مرجع کامل ابزارها (Tools Reference)](#۴-مرجع-کامل-ابزارها-tools-reference)
5. [مرجع منابع داده (Resources Reference)](#۵-مرجع-منابع-داده-resources-reference)
6. [الگوهای پرامپت (Prompts Reference)](#۶-الگوهای-پرامپت-prompts-reference)
7. [خط فرمان و حالت‌های شبکه (CLI & Transports)](#۷-خط-فرمان-و-حالت‌های-شبکه-cli--transports)
8. [سوالات متداول و رفع اشکال (FAQ)](#۸-سوالات-متداول-و-رفع-اشکال-faq)

---

## ۱. معرفی و معماری

**پروتکل زمینه مدل (Model Context Protocol یا MCP)** یک استاندارد باز است که امکان اتصال امن، استاندارد و دوطرفه میان مدل‌های زبانی بزرگ (LLM) و داده‌های محلی را فراهم می‌سازد.

سرور **MarketDict MCP** با بهره‌گیری از نمایه باینری حافظه و موتور SQLite WAL به مدل هوش مصنوعی اجازه می‌دهد بدون نیاز به فراخوانی اینترنت، مستقیماً به اطلاعات مالی دسترسی داشته باشد:

```
  ┌───────────────────────────────────────────────────────────────┐
  │                        کلاینت‌های AI                           │
  │   Claude Desktop  │  Cursor IDE  │  Antigravity  │  Cline    │
  └───────────────────────────────┬───────────────────────────────┘
                                  │ ارتباط دوطرفه JSON-RPC (stdio / SSE)
                                  ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                  MarketDict MCP Server                        │
  │                      (mcp_server.py)                          │
  │   ۹ ابزار عملیاتی  │  ۳ منبع داده   │   ۲ پرامپت آماده       │
  └───────┬───────────────────────┬───────────────────────┬───────┘
          │                       │                       │
          ▼                       ▼                       ▼
  ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
  │  بانک اطلاعات  │       │ رجیستری فرمول  │       │  طبقه‌بندی     │
  │  ۶,۱۰۸ اصطلاح  │       │ ۴۴ فرمول لاتک │       │  ۳۲ حوزه بازار │
  └───────────────┘       └───────────────┘       └───────────────┘
```

### ویژگی‌های کلیدی:
- ⚡ **سرعت پردازش زیر میلی‌ثانیه**: اجرای تمام کوئری‌ها بر روی نمایه محلی بدون تاخیر شبکه.
- 🔤 **موتور جستجوی فازی فارسی و انگلیسی**: مجهز به سیستم نرمال‌سازی کلمات فارسی (`ی/ي`، `ک/ك`، اعراب‌زدایی، نیم‌فاصله).
- 📐 **فرمول‌های ریاضی استاندارد LaTeX**: به همراه تعریف دقیق متغیرها به فارسی و انگلیسی.
- 🔒 **۱۰۰٪ آفلاین و امن**: بدون هیچ‌گونه نیاز به اینترنت و بدون ردیابی یا ارسال داده به بیرون.

---

## ۲. پیش‌نیازها و نصب

- **پایتون**: نسخه ۳.۱۰ یا بالاتر

```bash
# نصب پکیج رسمی MCP
pip install mcp>=1.0.0

# اجرای تست جامع سرور
python test_mcp_server.py
```

---

## ۳. راهنمای راه‌اندازی کلاینت‌ها

### ۳.۱. اتصال به Claude Desktop

فایل کانفیگ کلود را در مسیر زیر باز کنید:
- **ویندوز**: `%APPDATA%\Claude\claude_desktop_config.json`
- **مک**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **لینوکس**: `~/.config/Claude/claude_desktop_config.json`

کانفیگ زیر را در بخش `mcpServers` درج نمایید:
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
*سپس نرم‌افزار Claude Desktop را ببندید و مجدداً باز کنید.*

---

### ۳.۲. اتصال به Cursor IDE

- **روش اول (رابط کاربری)**: وارد **Cursor Settings** -> **Features** -> **MCP** شده، روی **Add New MCP Server** کلیک کنید:
  - **Name**: `marketdict`
  - **Type**: `command`
  - **Command**: `python c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py`
- **روش دوم (فایل کانفیگ)**: فایل `.cursor/mcp.json` را در ریشه پروژه بسازید:
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

---

### ۳.۳. اتصال به Google Antigravity

در فایل کانفیگ سراسری `~/.gemini/config/mcp_config.json` یا کانفیگ پروژه `.agents/mcp_config.json`:
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

### ۳.۴. اتصال به اکستنشن‌های VS Code (Cline / Roo Code / Continue)

در فایل `cline_mcp_settings.json`:
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

| نام ابزار | پارامترها | توضیحات عملکرد |
| :--- | :--- | :--- |
| **`search_terms`** | `query` (اجباری)، `category`، `letter`، `limit=10`، `page=1` | جستجوی فازی و پیشرفته در ۶,۱۰۸ واژه با پشتیبانی کامل از زبان فارسی و انگلیسی. |
| **`suggest_terms`** | `prefix` (اجباری)، `limit=8` | تکمیل خودکار کلمات بر اساس حروف تایپ شده با سرعت کمتر از ۵ میلی‌ثانیه. |
| **`get_term_details`** | `term_identifier` (اسلاگ، نام انگلیسی، نام فارسی یا شناسه عددی) | دریافت دایره‌المعارفی اصطلاح به همراه تعاریف کامل، نکات کلیدی، سرفصل‌ها و فرمول. |
| **`get_financial_formula`** | `term` (نام مفهوم یا مخفف مانند `sharpe`, `roe`, `ebit`, `wacc`) | فرمول استاندارد LaTeX ریاضی و تشریح متغیرها به زبان انگلیسی و فارسی. |
| **`list_all_formulas`** | `query` (اختیاری) | نمایش تمام ۴۴ فرمول محاسباتی ثبت‌شده در سیستم. |
| **`list_categories`** | ندارد | فهرست کامل ۳۲ حوزه و دسته‌بندی موضوعی بازارهای مالی همراه با آیکون و تعداد کلمات. |
| **`list_letters`** | ندارد | دسته‌بندی الفبایی کلمات بر اساس حروف انگلیسی (`#` و `A` تا `Z`). |
| **`get_random_term`** | `category`، `only_deep_enriched=true` | دریافت یک اصطلاح تصادفی (برای یادگیری، آزمون یا مفهوم روزانه). |
| **`get_dictionary_stats`** | ندارد | دریافت آمار تفکیکی دیتابیس (تعداد کل، دسته‌بندی‌ها، مقالات تشریحی). |

---

## ۵. مرجع منابع داده (Resources Reference)

- **`marketdict://stats`**: دیتای JSON شامل مشخصات آماری مخزن.
- **`marketdict://categories`**: ساختار JSON از ۳۲ دسته‌بندی و تعداد هرکدام.
- **`marketdict://formulas`**: کاتالوگ فرمول‌های مالی به صورت داده مستقیم.
- **`marketdict://terms/{slug}`**: متن کامل ساختار JSON برای یک اصطلاح معین (مثلاً `marketdict://terms/sharperatio`).

---

## ۶. الگوهای پرامپت (Prompts Reference)

- **`explain_financial_term`**:
  - پارامترها: `term` (نام مفهوم), `language` (`"fa"`, `"en"`, `"bilingual"`), `target_audience` (`"beginner"`, `"general"`, `"advanced"`, `"student"`).
  - خروجی: پرامپت مهندسی‌شده حرفه‌ای با تزریق تعاریف رسمی و فرمول برای تدریس بدون نقص مفهوم مالی.
- **`compare_financial_terms`**:
  - پارامترها: `term1`, `term2`, `language`.
  - خروجی: پرامپت تحلیلی مقایسه‌ای برای جدول تفاوت‌ها و شباهت‌های دو مفهوم.

---

## ۷. خط فرمان، حالت‌های شبکه و ریورس پروکسی (CLI & Reverse Proxy)

```bash
# ارتباط استاندارد ورودی/خروجی (کلاینت‌های دسکتاپ محلی):
python mcp_server.py

# راه‌اندازی تحت شبکه با پروتکل SSE:
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000

# راه‌اندازی با پروتکل مدرن Streamable HTTP:
python mcp_server.py --transport streamable-http --host 127.0.0.1 --port 8000

# راه‌اندازی پشت ریورس پروکسی (Nginx / Cloudflare / Traefik / Caddy):
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"
```

### فلگ‌های خط فرمان:
- `--host`: تعیین آدرس IP بایند سرور (پیش‌فرض: `127.0.0.1` یا `$HOST`)
- `--port`: پورت اتصال (پیش‌فرض: `8000` یا `$PORT`)
- `--proxy-headers` / `--no-proxy-headers`: فعال/غیرفعال‌سازی پردازش هدرهای پروکسی (`X-Forwarded-*`) (پیش‌فرض: `True`)
- `--forwarded-allow-ips`: فهرست IPهای مجاز و مورد اعتماد ریورس پروکسی یا `*` (پیش‌فرض: `*` یا `$FORWARDED_ALLOW_IPS`)

---

## ۸. سوالات متداول و رفع اشکال (FAQ)

### ۱. آیا برای کارکرد MCP نیاز است سرور وب فلسک روشن باشد؟
خیر، سرور MCP به صورت مستقل مستقیماً به فایل بانک اطلاعاتی SQLite و ایندکس محلی متصل است و هیچ نیازی به اجرای `app.py` ندارد.

### ۲. چگونه از سازگاری حروف فارسی اطمینان حاصل کنیم؟
سرور به صورت خودکار تمام متن‌ها را نرمال‌سازی می‌کند. همچنین برای جلوگیری از به هم ریختگی کاراکترها در ویندوز، مقدار `"PYTHONIOENCODING": "utf-8"` در بخش `env` کانفیگ گنجانده شده است.
