# مستندات جامع و راهنمای کامل REST API دیکشنری مالی (MarketDict) 📈

> راهنمای مرجع و رسمی توسعه‌دهندگان برای استفاده از API دیکشنری مالی دو‌زبانه (انگلیسی و فارسی) MarketDict شامل ۶,۱۰۸ اصطلاح مالی، ۳۲ دسته‌بندی تخصصی، ۴۴ فرمول محاسباتی لاتک (LaTeX) و موتور جستجوی هوشمند فازی.

---

## فهرست مطالب

1. [معرفی و اصول طراحی](#۱-معرفی-و-اصول-طراحی)
2. [آدرس‌های پایه و مستندات تعاملی](#۲-آدرسهای-پایه-و-مستندات-تعاملی)
3. [احراز هویت و امنیت](#۳-احراز-هویت-و-امنیت)
4. [سیاست CORS و دسترسی بین‌مبدأ](#۴-سیاست-cors-و-دسترسی-بینمبدأ)
5. [ساختار و استاندارد پاسخ‌ها](#۵-ساختار-و-استاندارد-پاسخها)
6. [فهرست کامل اندپوینت‌ها و متدها](#۶-فهرست-کامل-اندپوینت‌ها-و-متدها)
   - [۶.۱. وضعیت سیستم و آمار (System & Stats)](#۶۱-وضعیت-سیستم-و-آمار)
   - [۶.۲. جستجو و مدیریت اصطلاحات (Terms)](#۶۲-جستجو-و-مدیریت-اصطلاحات)
   - [۶.۳. تکمیل خودکار جستجو (Autocomplete / Suggest)](#۶۳-تکمیل-خودکار-جستجو)
   - [۶.۴. دسته‌بندی‌های مالی (Categories)](#۶۴-دسته‌بندی‌های-مالی)
   - [۶.۵. فهرست حروف الفبا (Letters)](#۶۵-فهرست-حروف-الفبا)
   - [۶.۶. فرمول‌های محاسباتی مالی (Formulas)](#۶۶-فرمول‌های-محاسباتی-مالی)
   - [۶.۷. دریافت دسته‌ای اصطلاحات (Batch Terms)](#۶۷-دریافت-دسته‌ای-اصطلاحات)
7. [مدل‌های داده و اسکیماها (Data Schemas)](#۷-مدل‌های-داده-و-اسکیماها)
8. [نمونه کدها در زبان‌های مختلف](#۸-نمونه-کدها-در-زبان‌های-مختلف)
   - [۸.۱. پایتون (Python SDK)](#۸۱-پایتون-python-sdk)
   - [۸.۲. سی‌شارپ (C# / .NET SDK)](#۸۲-سی‌شارپ-c--net-sdk)
   - [۸.۳. جاوااسکریپت و تایپ‌اسکریپت (JavaScript / TypeScript)](#۸۳-جاوااسکریپت-و-تایپ‌اسکریپت)
   - [۸.۴. دستورات cURL](#۸۴-دستورات-curl)
9. [سناریوهای کاربردی و ایده‌های پیاده‌سازی](#۹-سناریوهای-کاربردی-و-ایده‌های-پیاده‌سازی)
10. [کدهای خطا و عیب‌یابی](#۱۰-کدهای-خطا-و-عیب‌یابی)

---

## ۱. معرفی و اصول طراحی

سرویس MarketDict یک پایگاه دانش جامع و دو‌زبانه مالی است. این API برای ارائه خدمات به:
- اپلیکیشن‌های موبایل (Android / iOS / Flutter / React Native)
- سامانه‌های وب و وبلاگ‌های اقتصادی
- ربات‌های معاملاتی (Trading Bots) و دستیاران الگوریتمی
- ربات‌های پیام‌رسان (Telegram، Discord، بله، ایتا)
- افزونه‌های مرورگر و ابزارهای اکسل/گوگل‌شیتس

طراحی شده است. تمام فرآیندهای جستجو دارای **نرمال‌سازی خودکار متن فارسی** (یکسان‌سازی `ی/ي`، `ک/ك`، حذف حرکات و اعراب، یکپارچه‌سازی نیم‌فاصله‌ها) می‌باشند.

---

## ۲. آدرس‌های پایه و مستندات تعاملی

| محیط | آدرس پایه (Base URL) | نوع سرویس |
| :--- | :--- | :--- |
| **سرور محلی توسعه** | `http://localhost:5000/api/v1` | سرویس زنده Flask + دیتابیس SQLite WAL |
| **مستندات تعاملی Swagger** | `http://localhost:5000/docs` یا `/api/v1/docs` | رابط گرافیکی تست زنده متدها |
| **مشخصات ماشین‌خوان OpenAPI** | `http://localhost:5000/api/v1/openapi.json` | سند رسمی OpenAPI 3.0.3 |
| **نسخه ایستا** | `dist/api/v1/` (خروجی `python build_static.py`) | اسنپ‌شات‌های JSON فقط برای میزبانی داخلی؛ [DATA_NOTICE.md](DATA_NOTICE.md) را ببینید |

---

## ۳. احراز هویت و امنیت

- **نوع دسترسی**: **کاملاً آزاد و رایگان (Open Access)**
- **نیاز به API Key**: **خیر**. برای استفاده از هیچ‌یک از اندپوینت‌ها نیاز به توکن، کلید یا لاگین نیست.
- **محدودیت نرخ (Rate Limiting)**: محدودیتی اعمال نشده است، اما برای حفظ پایداری سیستم پیشنهاد می‌شود در درخواست‌های متوالی فاصله‌گذاری معقول رعایت گردد.

---

## ۴. سیاست CORS و دسترسی بین‌مبدأ

تمامی مسیرهای API به طور پیش‌فرض دارای هدرهای کامل CORS هستند:
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS, HEAD
Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With, Accept
X-API-Version: 1.0.0
```
بنابراین می‌توانید مستقیماً از داخل مرورگر یا هر دامنه دیگری بدون مواجهه با خطای CORS از API استفاده کنید. درخواست‌های Preflight از نوع `OPTIONS` نیز پاسخ وضعیت `204 No Content` دریافت می‌کنند.

---

## ۵. ساختار و استاندارد پاسخ‌ها

### ۵.۱. ساختار استاندارد پاسخ موفق (Envelope)
به طور پیش‌فرض، همه پاسخ‌های موفق ساختار یکپارچه زیر را دارند:

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

> **نکته مهم (پارامتر `raw=true`)**: اگر می‌خواهید پاسخ بدون پوشش (Envelope) و مستقیماً به شکل آرایه یا شیء JSON برگردد، کافی است پارامتر `raw=true` را در انتهای URL قرار دهید.

### ۵.۲. ساختار استاندارد پاسخ خطا
در صورت بروز هرگونه خطا (یافت نشدن، پارامتر نامعتبر و غیره)، پاسخ با کد وضعیت HTTP مناسب (مانند 400، 404، 500) و ساختار زیر ارسال می‌شود:

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

## ۶. فهرست کامل اندپوینت‌ها و متدها

### ۶.۱. وضعیت سیستم و آمار

#### `GET /api/v1/health` (یا `/api/v1/ping`)
بررسی سلامت سرویس، وضعیت کش حافظه و دیتابیس SQLite.

- **پارامترها**: ندارد
- **نمونه پاسخ:**
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
آمار دقیق و تعداد آیتم‌های پایگاه دانش دیکشنری.

- **نمونه پاسخ:**
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

### ۶.۲. جستجو و مدیریت اصطلاحات

#### `GET /api/v1/terms`
موتور جستجو و فیلتر جامع اصطلاحات مالی با صفحه‌بندی.

**پارامترهای Query:**

| نام پارامتر | نوع | پیش‌فرض | توضیحات |
| :--- | :---: | :---: | :--- |
| `q` | `string` | `""` | عبارت مورد جستجو به فارسی یا انگلیسی (فازی و هوشمند) |
| `category` | `string` | - | فیلتر بر اساس اسلاگ دسته‌بندی (`crypto`) یا نام فارسی آن |
| `letter` | `string` | - | فیلتر بر اساس حرف اول انگلیسی (`#` یا `A` تا `Z`) |
| `has_deep` | `boolean` | - | فقط اصطلاحات دارای مقالات تفصیلی چند‌بخشی (`true`/`false`) |
| `has_formula` | `boolean` | - | فقط اصطلاحات دارای فرمول ریاضیاتی لاتک (`true`/`false`) |
| `sort` | `string` | `relevance` | فیلد مرتب‌سازی: `relevance` (اگر q ارسال شود)، `term_en`، `term_fa`، `id` |
| `order` | `string` | `asc` | جهت مرتب‌سازی: `asc` (صعودی) یا `desc` (نزولی) |
| `page` | `integer` | `1` | شماره صفحه (شروع از ۱) |
| `limit` | `integer` | `20` | تعداد نتایج در هر صفحه (حداکثر ۱۰۰) |
| `fields` | `string` | - | انتخاب فیلدهای دلخواه با کاما جهت صرفه‌جویی در پهنای باند |
| `raw` | `boolean` | `false` | بازگرداندن آرایه خام بدون Envelope |

**نمونه فراخوانی:**
```bash
curl -s "http://localhost:5000/api/v1/terms?q=شارپ&limit=2"
```

---

#### `GET /api/v1/terms/{identifier}`
دریافت جزئیات کامل و غنی اصطلاح بر اساس **شناسه عددی** (مثل `461`)، **اسلاگ** (مثل `sharperatio`) یا عنوان انگلیسی.

- **پارامتر Path**:
  - `identifier`: شناسه عددی اصطلاح یا نام اسلاگ آن
- **پارامترهای اختیاری Query**:
  - `fields`: فیلدهای مورد نظر
  - `raw`: مقدار `true` برای دریافت شیء خام

**نمونه خروجی:**
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
دریافت یک یا چند اصطلاح به صورت تصادفی (بسیار مناسب برای قابلیت «اصطلاح مالی روز»، بات‌ها و کارت‌های آموزشی).

**پارامترهای Query:**
- `count`: تعداد موارد تصادفی (۱ تا ۱۰، پیش‌فرض: ۱)
- `category`: محدود کردن انتخاب تصادفی به دسته‌بندی خاص
- `has_deep`: انتخاب فقط از میان اصطلاحات غنی‌شده جامع (`true`/`false`)

---

### ۶.۳. تکمیل خودکار جستجو (Autocomplete / Suggest)

#### `GET /api/v1/suggest` (یا `/api/v1/autocomplete`)
اندپوینت فوق‌سریع (<5 میلی‌ثانیه) طراحی‌شده برای اینپوت‌های جستجو، Typeahead و کیبوردهای موبایل.

**پارامترهای Query:**
- `q` (**اجباری**): پیشوند یا بخشی از واژه به فارسی یا انگلیسی
- `limit` (اختیاری): حداکثر پیشنهادات (۱ تا ۳۰، پیش‌فرض: ۱۰)

**نمونه خروجی:**
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

### ۶.۴. دسته‌بندی‌های مالی (Categories)

#### `GET /api/v1/categories`
فهرست کامل ۳۲ حوزه تخصصی مالی به همراه آیکون، نام انگلیسی، نام فارسی، تعداد اصطلاحات و لینک دسترسی.

#### `GET /api/v1/categories/{category_id}`
دریافت مشخصات و آمار یک دسته‌بندی بر اساس شناسه (مانند `crypto`، `quant_math`، `derivatives`، `accounting`) یا نام فارسی آن.

#### `GET /api/v1/categories/{category_id}/terms`
اصطلاحات موجود در یک دسته‌بندی به همراه صفحه‌بندی (پشتیبانی از `page`، `limit`، `sort`، `fields`).

---

### ۶.۵. فهرست حروف الفبا (Letters)

#### `GET /api/v1/letters`
فهرست تمامی حروف الفبا (`#` و `A` تا `Z`) همراه با تعداد اصطلاحات هر حرف.

#### `GET /api/v1/letters/{letter}/terms`
اصطلاحاتی که با حرف مورد نظر شروع می‌شوند (پشتیبانی از `page` و `limit`).

---

### ۶.۶. فرمول‌های محاسباتی مالی (Formulas)

#### `GET /api/v1/formulas`
فهرست ۴۴ نسبت و فرمول استاندارد مالی و محاسباتی با کدهای ریاضیاتی KaTeX/LaTeX به دو زبان انگلیسی و فارسی.

فرمول‌های پشتیبانی‌شده شامل:
- نسبت شارپ (Sharpe Ratio)، سورتینو (Sortino)، ترینور (Treynor)، ضریب اطلاعات (Information Ratio)
- مدل CAPM، آلفای جنسن (Jensen's Alpha)، بتا (Beta)
- نقطه سربه‌سر (BEP)، معادله اصلی حسابداری، نسبت بدهی به حقوق صاحبان سهام (D/E)
- نسبت پوشش بدهی (DSCR)، سود قبل از بهره و مالیات (EBIT/EBITDA)
- رشد مرکب سالانه (CAGR)، سود هر سهم (EPS)، نسبت قیمت به درآمد (P/E)، ارزش خالص دارایی (NAV)
- فرمول‌های تحلیل تکنیکال (MACD) و توزیع نرمال آماری

---

### ۶.۷. دریافت دسته‌ای اصطلاحات (Batch Terms)

#### `POST /api/v1/terms/batch`
دریافت همزمان چندین اصطلاح در یک درخواست جهت کاهش درخواست‌های رفت و برگشت شبکه.

**بدنه درخواست (JSON Body):**
```json
{
  "identifiers": ["sharperatio", "461", "cagr", "ebitda"]
}
```

**پاسخ:**
```json
{
  "status": "success",
  "data": [ ... فهرست اشیاء کامل اصطلاحات یافت‌شده ... ],
  "meta": {
    "requested": 4,
    "found": 4,
    "missing": []
  }
}
```

> همچنین متد `GET /api/v1/terms/batch?ids=sharperatio,461,cagr` نیز به صورت Query String پشتیبانی می‌شود.

---

## ۷. مدل‌های داده و اسکیماها

### شیء `TermSummary` (خلاصه اصطلاح)
```typescript
interface TermSummary {
  id: number;                 // شناسه منحصر‌به‌فرد عددی
  slug: string;               // شناسه متنی آدرس
  term_en: string;            // عنوان انگلیسی
  term_fa: string;            // عنوان تخصصی فارسی
  letter: string;             // حرف الفبای انگلیسی (A-Z, #)
  category: string;           // عنوان فارسی دسته‌بندی
  category_id: string;        // شناسه انگلیسی دسته‌بندی (مانند crypto)
  category_fa: string;        // عنوان دسته‌بندی به فارسی
  category_en: string;        // عنوان دسته‌بندی به انگلیسی
  category_icon: string;      // ایموجی یا آیکون دسته‌بندی
  definition_fa: string;      // خلاصه تعریف به زبان فارسی (حداکثر ۳۵۰ کاراکتر)
  definition_en: string;      // خلاصه تعریف به زبان انگلیسی (حداکثر ۳۵۰ کاراکتر)
  has_deep: boolean;          // آیا اصطلاح دارای مقاله کامل چندبخشی است؟
  has_formula: boolean;       // آیا دارای فرمول ریاضیاتی است؟
  url: string;                // آدرس مرجع در Investopedia
}
```

### شیء `TermDetail` (جزئیات کامل اصطلاح)
شامل کلیه فیلدهای `TermSummary` به همراه:
- `takeaways_en` / `takeaways_fa`: آرایه‌ای از نکات کلیدی و چکیده مقاله
- `bottom_line_en` / `bottom_line_fa`: نتیجه‌گیری نهایی
- `sections`: آرایه‌ای از بخش‌های مقاله شامل `title_en`, `title_fa`, `paragraphs_en`, `paragraphs_fa`, `items_en`, `items_fa`
- `formula`: شیء فرمول شامل `formula_en` و `formula_fa` به قالب LaTeX

---

## ۸. نمونه کدها در زبان‌های مختلف

### ۸.۱. پایتون (Python SDK)

فایل آماده [`marketdict_client.py`](marketdict_client.py) در ریشه پروژه قرار دارد و بدون نیاز به نصب هیچ پکیج اضافی (صرفاً با کتابخانه استاندارد پایتون) کار می‌کند:

```python
from marketdict_client import MarketDict

# ایجاد کلاینت با آدرس پایه
client = MarketDict(base_url="http://localhost:5000/api/v1")

# ۱. جستجوی اصطلاحات مالی به فارسی یا انگلیسی
results = client.search(query="نسبت شارپ", limit=5)
for term in results["data"]:
    print(f"📌 {term['term_en']} ({term['term_fa']}) - {term['category_icon']} {term['category_fa']}")

# ۲. دریافت جزئیات اصطلاح به همراه فرمول ریاضیاتی
sharpe = client.get_term("sharperatio")
print("تعریف:", sharpe["definition_fa"][:150])
if sharpe.get("formula"):
    print("فرمول لاتک:", sharpe["formula"]["formula_en"])

# ۳. تکمیل خودکار جستجو برای اینپوت زنده
suggestions = client.suggest("bit", limit=5)
for s in suggestions:
    print(f"👉 [{s['id']}] {s['term_en']} -> {s['term_fa']}")

# ۴. دریافت اصطلاح تصادفی روز
daily = client.get_random(has_deep=True)
print("اصطلاح تصادفی امروز:", daily["term_en"], "->", daily["term_fa"])
```

---

### ۸.۲. سی‌شارپ (C# / .NET SDK)

فایل آماده [`MarketDictClient.cs`](MarketDictClient.cs) را در پروژه سی‌شارپ خود قرار دهید (سازگار با .NET 6، 7، 8، 9، دات‌نت استاندارد و فریم‌ورک):

```csharp
using System;
using System.Threading.Tasks;
using MarketDict;

class Program
{
    static async Task Main()
    {
        using var client = new MarketDictClient("http://localhost:5000/api/v1");

        // ۱. جستجوی اصطلاحات
        var searchResult = await client.SearchTermsAsync(query: "نسبت شارپ", limit: 3);
        foreach (var term in searchResult.Data)
        {
            Console.WriteLine($"📌 {term.TermEn} ({term.TermFa}) - {term.CategoryIcon} {term.CategoryFa}");
        }

        // ۲. دریافت جزئیات اصطلاح و فرمول ریاضی
        var termDetail = await client.GetTermAsync("sharperatio");
        Console.WriteLine($"تعریف: {termDetail.DefinitionFa}");
        if (termDetail.Formula != null)
        {
            Console.WriteLine($"فرمول: {termDetail.Formula.FormulaEn}");
        }

        // ۳. تکمیل خودکار (Autocomplete)
        var suggestions = await client.SuggestAsync("bit", limit: 4);
        foreach (var s in suggestions)
        {
            Console.WriteLine($"👉 [{s.Id}] {s.TermEn} -> {s.TermFa}");
        }
    }
}
```

#### نحوه ثبت در ASP.NET Core با تزریق وابستگی (Dependency Injection):
```csharp
// Program.cs
builder.Services.AddHttpClient<MarketDictClient>(c =>
{
    c.BaseAddress = new Uri("http://localhost:5000/api/v1");
});
```

---

### ۸.۳. جاوااسکریپت و تایپ‌اسکریپت

#### با استفاده از `fetch` در فرانت‌اند یا Node.js:
```javascript
// ۱. جستجوی اصطلاحات
async function searchTerms(query) {
  const url = `http://localhost:5000/api/v1/terms?q=${encodeURIComponent(query)}&limit=5`;
  const response = await fetch(url);
  const { data, pagination } = await response.json();
  console.log(`تعداد کل نتایج: ${pagination.total}`, data);
}

// ۲. تکمیل خودکار جستجو برای اینپوت باکس
async function getSuggestions(prefix) {
  const res = await fetch(`http://localhost:5000/api/v1/suggest?q=${encodeURIComponent(prefix)}&limit=5`);
  const json = await res.json();
  return json.data; // [{ id, slug, term_en, term_fa, category }]
}

// ۳. دریافت فرمول‌های مالی
async function getFinancialFormulas() {
  const res = await fetch('http://localhost:5000/api/v1/formulas');
  const json = await res.json();
  return json.data;
}
```

---

### ۸.۴. دستورات cURL

```bash
# بررسی وضعیت سلامت
curl -s http://localhost:5000/api/v1/health

# دریافت آمار دیتابیس
curl -s http://localhost:5000/api/v1/stats

# جستجوی اصطلاحات با کلمه 'تورم'
curl -s "http://localhost:5000/api/v1/terms?q=%D8%AA%D9%88%D8%B1%D9%85&limit=3"

# دریافت اصطلاح با شناسه عددی
curl -s http://localhost:5000/api/v1/terms/461

# دریافت یک اصطلاح تصادفی
curl -s http://localhost:5000/api/v1/terms/random

# دریافت فهرست ۳۲ دسته‌بندی مالی
curl -s http://localhost:5000/api/v1/categories

# دریافت ۴۴ فرمول محاسباتی ریاضی
curl -s http://localhost:5000/api/v1/formulas
```

---

## ۹. سناریوهای کاربردی و ایده‌های پیاده‌سازی

1. **ربات تلگرام یا پیام‌رسان‌های داخلی**:
   ارسال دستوراتی مثل `/term شارپ` یا ارسال خودکار «اصطلاح مالی روز» در ساعت مشخص با استفاده از متد `/api/v1/terms/random`.
2. **افزونه مرورگر Chrome / Firefox**:
   با انتخاب هر کلمه انگلیسی مالی در سایت‌های خبری (مثل بلومبرگ یا یاهو فایننس)، پنجره پاپ‌آپ افزونه بلافاصله معنی و تعریف فارسی را از `/api/v1/terms/{slug}` لود کند.
3. **ماشین‌حساب‌های مالی و ابزارهای تحلیل کمی**:
   نمایش دقیق فرمول لاتک و متغیرهای آن در کنار ابزار محاسبه نسبت‌های مالی از طریق `/api/v1/formulas`.
4. **جعبه جستجوی وب‌سایت‌های اقتصادی**:
   اتصال ایونت `input` فیلد سرچ به اندپوینت `/api/v1/suggest` برای ارائه تایپ‌اهید زیر ۵ میلی‌ثانیه.

---

## ۱۰. کدهای خطا و عیب‌یابی

| کد وضعیت HTTP | عنوان خطا | علت و راه‌حل |
| :---: | :--- | :--- |
| **`200 OK`** | موفق | درخواست با موفقیت پردازش شد. |
| **`204 No Content`** | پاسخ پرفلایت CORS | برای درخواست‌های `OPTIONS` پیش‌پرواز مرورگر ارسال می‌شود. |
| **`400 Bad Request`** | درخواست نامعتبر | پارامتر ارسالی اشتباه است (مثلاً مقداردهی غیراستاندارد به `page`). |
| **`404 Not Found`** | یافت نشد | اصطلاح یا دسته‌بندی با شناسه یا اسلاگ ارسالی وجود ندارد. |
| **`500 Internal Error`** | خطای سرور | خطای داخلی سرور؛ لاگ‌های سرور را بررسی کنید. |

---

## 📄 مجوز استفاده
این پروژه و API تحت لایسنس **[Apache License 2.0](LICENSE)** به صورت متن‌باز منتشر شده است.
حق نشر (c) ۲۰۲۶ علی صادقی عقیلی.
