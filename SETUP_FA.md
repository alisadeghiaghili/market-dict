# راهنمای جامع و گام‌به‌گام راه‌اندازی دیکشنری مالی (MarketDict) 🚀

> این سند مرجع رسمی و بسیار دقیق برای نصب، راه‌اندازی، بیلد، آزمایش و استقرار پروداکشن پروژه **MarketDict** در انواع سیستم‌عامل‌ها (ویندوز، لینوکس، مک‌اواس)، محیط‌های کانتینری (Docker)، سرورهای پروداکشن (Nginx + Gunicorn + Systemd)، سرور پروتکل زمینه مدل (MCP) و تولید نسخه‌های استاتیک (PWA) و موبایل (Capacitor Android) است.

---

### 🌐 زبان‌ها و مستندات مرتبط / Documentation Index:
- 🇮🇷 **راهنمای فارسی راه‌اندازی (همین سند)**
- 🇬🇧 **[English Setup Guide (SETUP_EN.md)](SETUP_EN.md)**
- 📖 **[مستندات REST API به فارسی (API_FA.md)](API_FA.md)**
- 🤖 **[مستندات سرور MCP به فارسی (MCP_FA.md)](MCP_FA.md)**
- 🚢 **[مستندات استقرار سازمانی (DEPLOYMENT.md)](DEPLOYMENT.md)**
- ⚖️ **[نکات حقوقی داده‌ها (DATA_NOTICE.md)](DATA_NOTICE.md)**

---

## فهرست مطالب

1. [معرفی و معماری اجزای پروژه](#۱-معرفی-و-معماری-اجزای-پروژه)
2. [پیش‌نیازهای نرم‌افزاری و سخت‌افزاری](#۲-پیش‌نیازهای-نرم‌افزاری-و-سخت‌افزاری)
3. [روش اول: راه‌اندازی محلی برای توسعه (Local Development)](#۳-روش-اول-راه‌اندازی-محلی-برای-توسعه-local-development)
   - [۳.۱. دریافت سورس‌کد (Clone)](#۳۱-دریافت-سورس‌کد-clone)
   - [۳.۲. ساخت و فعال‌سازی محیط مجازی پایتون (Virtualenv)](#۳۲-ساخت-و-فعال‌سازی-محیط-مجازی-پایتون-virtualenv)
   - [۳.۳. نصب کتابخانه‌های پیش‌نیاز](#۳۳-نصب-کتابخانه‌های-پیش‌نیاز)
   - [۳.۴. اجرای وب‌اپلیکیشن و API](#۳۴-اجرای-وب‌اپلیکیشن-و-api)
   - [۳.۵. بررسی سلامت و دسترسی به صفحات](#۳۵-بررسی-سلامت-و-دسترسی-به-صفحات)
4. [روش دوم: راه‌اندازی با داکر و داکر کامپوز (Docker & Docker Compose)](#۴-روش-دوم-راه‌اندازی-با-داکر-و-داکر-کامپوز-docker--docker-compose)
   - [۴.۱. اجرای سریع تک‌دستوری](#۴۱-اجرای-سریع-تک‌دستوری)
   - [۴.۲. مدیریت و نظارت کانتینر](#۴۲-مدیریت-و-نظارت-کانتینر)
   - [۴.۳. ساخت دستی با داکر CLI](#۴۳-ساخت-دستی-با-داکر-cli)
5. [روش سوم: استقرار عملیاتی روی سرور لینوکس (Production Linux Deployment)](#۵-روش-سوم-استقرار-عملیاتی-روی-سرور-لینوکس-production-linux-deployment)
   - [۵.۱. ساخت سرویس سیستمی Systemd](#۵۱-ساخت-سرویس-سیستمی-systemd)
   - [۵.۲. پیکربندی وب‌سرور معکوس Nginx](#۵۲-پیکربندی-وب‌سرور-معکوس-nginx)
   - [۵.۳. فعال‌سازی رمزنگاری و SSL رایگان (Let's Encrypt)](#۵۳-فعال‌سازی-رمزنگاری-و-ssl-رایگان-lets-encrypt)
6. [روش چهارم: راه‌اندازی و اتصال سرور MCP برای هوش مصنوعی](#۶-روش-چهارم-راه‌اندازی-و-اتصال-سرور-mcp-برای-هوش-مصنوعی)
   - [۶.۱. تست و اجرای سرور MCP](#۶۱-تست-و-اجرای-سرور-mcp)
   - [۶.۲. اتصال به Claude Desktop](#۶۲-اتصال-به-claude-desktop)
   - [۶.۳. اتصال به Cursor IDE و Antigravity](#۶۳-اتصال-به-cursor-ide-و-antigravity)
   - [۶.۴. اجرای تحت شبکه با پروتکل SSE](#۶۴-اجرای-تحت-شبکه-با-پروتکل-sse)
7. [روش پنجم: تولید بیلد استاتیک و وب‌اپلیکیشن آفلاین (Static Site & PWA)](#۷-روش-پنجم-تولید-بیلد-استاتیک-و-وب‌اپلیکیشن-آفلاین-static-site--pwa)
   - [۷.۱. ساخت خروجی ایستا](#۷۱-ساخت-خروجی-ایستا)
   - [۷.۲. میزبانی و استفاده در حالت آفلاین](#۷۲-میزبانی-و-استفاده-در-حالت-آفلاین)
8. [روش ششم: ساخت اپلیکیشن موبایل اندروید با Capacitor](#۸-روش-ششم-ساخت-اپلیکیشن-موبایل-اندروید-با-capacitor)
   - [۸.۱. پیش‌نیازهای محیط موبایل](#۸۱-پیش‌نیازهای-محیط-موبایل)
   - [۸.۲. نصب وابستگی‌های Node و خازنی](#۸۲-نصب-وابستگی‌های-node-و-خازنی)
   - [۸.۳. همگام‌سازی و تولید APK](#۸۳-همگام‌سازی-و-تولید-apk)
9. [متغیرهای محیطی و پارامترهای خط فرمان (CLI & Environment Variables)](#۹-متغیرهای-محیطی-و-پارامترهای-خط-فرمان-cli--environment-variables)
10. [اجرای آزمون‌های خودکار و تضمین کیفیت (Testing & QA)](#۱۰-اجرای-آزمون‌های-خودکار-و-تضمین-کیفیت-testing--qa)
11. [راهنمای جامع رفع اشکال و سوالات متداول (Troubleshooting & FAQ)](#۱۱-راهنمای-جامع-رفع-اشکال-و-سوالات-متداول-troubleshooting--faq)
12. [نکات امنیتی و رعایت قوانین مالکیت داده‌ها](#۱۲-نکات-امنیتی-و-رعایت-قوانین-مالکیت-داده‌ها)

---

## ۱. معرفی و معماری اجزای پروژه

پروژه **MarketDict** یک سکوی جامع فرهنگ اصطلاحات مالی دو زبانه (انگلیسی و فارسی) است که شامل **۶,۱۰۸ اصطلاح مالی**، **۳۲ حوزه بازار و طبقه‌بندی موضوعی**، **۴۴ فرمول مالی پیاده‌سازی شده با لاتک (KaTeX)** و پیوندهای داخلی میان اصطلاحات است.

### ساختار اجزا و فایل‌های کلیدی:

```
Market-Dict/
├── app.py                      # سرور وب اپلیکیشن Flask و ارائه‌دهنده روت‌های اصلی
├── api_v1.py                   # موتور REST API v1 با مشخصات کامل OpenAPI 3.0.3 و Swagger UI
├── mcp_server.py               # سرور استاندارد Model Context Protocol (ابزارها، منابع و پرامپت‌ها)
├── categories_engine.py        # موتور تاکسونومی و طبقه‌بندی ۳۲ گانه حوزه‌های مالی
├── polite_fetcher.py           # کلاینت اخلاقی وب با رعایت کامل robots.txt و تاخیر درخواست‌ها
├── build_static.py             # اسکریپت بیلد نسخه ۱۰۰٪ استاتیک و شاردینگ JSON در پوشه dist/
├── sw.js / manifest.json       # سرویس‌ورکر و مانیفست وب‌اپلیکیشن پیش‌رونده (PWA) با قابلیت کش آفلاین
├── marketdict_client.py        # کلاینت رسمی و بدون وابستگی پایتون (Python SDK)
├── MarketDictClient.cs         # کلاینت رسمی C# / .NET SDK
├── capacitor.config.json       # پیکربندی خروجی بومی اندروید و وب با Capacitor 6
├── Dockerfile                  # تصویر استاندارد کانتینر سبک پایتون (Python 3.11 slim)
├── docker-compose.yml          # فایل ارکستراسیون کانتینر
├── requirements.txt            # فهرست وابستگی‌های پایتون
├── test_*.py                   # سوئیت آزمون‌های خودکار و کاملاً آفلاین (۷۲ تست کامل)
└── bilingual_dictionary.json   # پایگاه داده غنی‌شده اصطلاحات دو زبانه
```

---

## ۲. پیش‌نیازهای نرم‌افزاری و سخت‌افزاری

### حداقل سخت‌افزار پیشنهادی:
- **پردازنده (CPU)**: حداقل ۱ هسته (برای محیط عملیاتی ۲ هسته یا بیشتر)
- **حافظه رم (RAM)**: حداقل ۱ گیگابایت (۲ گیگابایت برای کامپایل داکر و اجرای سریع آزمون‌ها)
- **فضای دیسک**: حداقل ۵۰۰ مگابایت فضای خالی

### نیازمندی‌های نرم‌افزاری:
- **پایتون**: Python 3.10 یا بالاتر (نسخه‌های 3.11 و 3.12 شدیداً پیشنهاد می‌شود)
- **مدیر بسته‌ها**: `pip` به‌روز
- **سیستم کنترل نسخه**: `git`
- *(اختیاری جهت کانتینرسازی)*: Docker Engine 24+ و Docker Compose v2+
- *(اختیاری جهت ساخت نسخه موبایل Android)*:
  - Node.js نسخه 18 یا 20 LTS به همراه npm
  - Java JDK 17
  - Android Studio و Android SDK Platform 33+

---

## ۳. روش اول: راه‌اندازی محلی برای توسعه (Local Development)

این سریع‌ترین روش برای اجرای برنامه روی رایانه شخصی (ویندوز، مک، لینوکس) است.

### ۳.۱. دریافت سورس‌کد (Clone)
ابتدا ترمینال یا PowerShell را باز کرده و مخزن را کلون کنید:

```bash
git clone https://github.com/alisadeghiaghili/market-dict.git
cd market-dict
```

---

### ۳.۲. ساخت و فعال‌سازی محیط مجازی پایتون (Virtualenv)

ایجاد محیط مجازی مجزا مانع از تداخل وابستگی‌های پکیج‌ها با سیستم‌عامل می‌شود:

#### در ویندوز (PowerShell / Command Prompt):
```powershell
# ساخت محیط مجازی به نام .venv
python -m venv .venv

# فعال‌سازی در PowerShell:
.venv\Scripts\Activate.ps1

# یا فعال‌سازی در CMD سنتی:
.venv\Scripts\activate.bat
```

> 💡 **نکته در خصوص ویندوز**: اگر در اجرای اسکریپت فعال‌سازی در PowerShell با خطای `Execution Policy` مواجه شدید، دستور زیر را در همان پنجره PowerShell اجرا کنید:
> ```powershell
> Set-ExecutionPolicy -Scope Process RemoteSigned
> ```

#### در لینوکس و مک‌اواس (Linux / macOS):
```bash
# ساخت محیط مجازی
python3 -m venv .venv

# فعال‌سازی محیط
source .venv/bin/activate
```

پس از فعال‌سازی موفق، عبارت `(.venv)` در ابتدای خط فرمان نمایش داده خواهد شد.

---

### ۳.۳. نصب کتابخانه‌های پیش‌نیاز

مطمئن شوید که pip به‌روز است و سپس پکیج‌های پروژه را نصب کنید:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

بسته‌های اصلی نصب‌شده شامل:
- `Flask`: فریم‌ورک وب و API
- `gunicorn`: سرور وب WSGI برای محیط‌های لینوکسی
- `uvicorn`: سرور ASGI پرسرعت
- `beautifulsoup4`: پردازش و استخراج ساختار HTML
- `mcp`: کیت رسمی پروتکل زمینه مدل (Model Context Protocol)
- `edge-tts`: ماژول تلفظ صوتی متن به گفتار

---

### ۳.۴. اجرای وب‌اپلیکیشن و API

برای اجرای مستقیم سرور در محیط توسعه:

```bash
python app.py
```

به صورت پیش‌فرض سرور روی پورت `5000` و آدرس تمام کارت‌های شبکه (`0.0.0.0`) شروع به شنود می‌کند:

```text
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

#### اجرای با پورت یا هاست دلخواه:
```bash
# اجرا روی پورت سفارشی (مثلاً 5050)
python app.py --port 5050

# اجرا فقط روی لوکال‌هاست (عدم دسترسی از سایر سیستم‌های شبکه)
python app.py --host 127.0.0.1 --port 5000
```

---

### ۳.۵. بررسی سلامت و دسترسی به صفحات

پس از راه‌اندازی، آدرس‌های زیر در مرورگر در دسترس شما خواهند بود:

| بخش | آدرس مرورگر / کلاینت | توضیحات |
| :--- | :--- | :--- |
| **رابط وب اصلی** | `http://localhost:5000` | جستجوی تعاملی، فیلتر حروف، دسته‌بندی‌ها و حالت تیره/روشن |
| **داکیومنت سواگر تعاملی** | `http://localhost:5000/docs` | محیط آزمون زنده و مستندات گرافیکی متدهای REST API |
| **اسکیما و سند OpenAPI 3** | `http://localhost:5000/api/v1/openapi.json` | مشخصات رسمی JSON برای تولید کلاینت در زبان‌های مختلف |
| **بررسی سلامت سیستم (Health)** | `http://localhost:5000/api/v1/health` | بازگرداندن وضعیت سرویس، زمان فعالیت (uptime) و متریک‌ها |
| **آمار کلی پایگاه دانش** | `http://localhost:5000/api/stats` | تعداد کل اصطلاحات (۶,۱۰۸)، فرمول‌ها، دسته‌ها و حروف |

تست سلامت سریع با ابزار `curl`:
```bash
curl -s http://localhost:5000/api/v1/health
```
نمونه پاسخ:
```json
{
  "status": "healthy",
  "version": "1.1.1",
  "uptime_seconds": 12.4,
  "total_terms": 6108,
  "database": "connected"
}
```

---

## ۴. روش دوم: راه‌اندازی با داکر و داکر کامپوز (Docker & Docker Compose)

کانتینرسازی ساده‌ترین و پایدارترین روش برای اجرای ایزوله بدون نیاز به نصب دستی پایتون و پکیج‌ها بر روی سیستم میزبان است.

### ۴.۱. اجرای سریع تک‌دستوری

در ریشه پروژه که فایل‌های `Dockerfile` و `docker-compose.yml` قرار دارند، دستور زیر را اجرا کنید:

```bash
docker compose up -d --build
```

این دستور به صورت خودکار:
1. تصویر سبک پایتون ۳.۱۱ را دریافت می‌کند.
2. پکیج‌های مورد نیاز را نصب می‌نماید.
3. کدها و فایل‌های داده را درون کانتینر کپی می‌کند.
4. سرور را به کمک Gunicorn با ۳ Worker بهینه روی پورت ۵۰۰۰ بالا می‌آورد.

---

### ۴.۲. مدیریت و نظارت کانتینر

#### بررسی وضعیت اجرای کانتینر:
```bash
docker compose ps
```

#### مشاهده زنده لاگ‌های خروجی:
```bash
docker compose logs -f web
```

#### متوقف‌سازی کانتینر:
```bash
docker compose stop
```

#### راه‌اندازی مجدد یا خاموش کردن کامل و پاکسازی:
```bash
# راه‌اندازی مجدد
docker compose restart

# حذف کانتینر و شبکه‌ها
docker compose down
```

---

### ۴.۳. ساخت دستی با داکر CLI (بدون Compose)

اگر نمی‌خواهید از docker-compose استفاده کنید:

```bash
# ساخت ایمیج با برچسب marketdict:latest
docker build -t marketdict:latest .

# اجرای کانتینر روی پورت ۵۰۰۰
docker run -d \
  --name marketdict-app \
  -p 5000:5000 \
  --restart unless-stopped \
  -e PORT=5000 \
  -e PROXY_HEADERS=true \
  -e FORWARDED_ALLOW_IPS="*" \
  marketdict:latest
```

---

## ۵. روش سوم: استقرار عملیاتی روی سرور لینوکس (Production Linux Deployment)

برای محیط‌های عملیاتی سازمانی (Ubuntu 22.04 LTS / Debian 12 / RHEL)، توصیه می‌شود از ترکیب **Gunicorn** به عنوان WSGI Server، **Systemd** به عنوان ناظر فرآیند و **Nginx** به عنوان Reverse Proxy و لایه SSL استفاده نمایید.

```
                  ┌─────────────────────────────────────────┐
                  │          کاربران و کلاینت‌ها            │
                  └────────────────────┬────────────────────┘
                                       │ HTTPS (Port 443)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │           Nginx Reverse Proxy           │
                  │       (SSL Termination, Gzip, Cache)    │
                  └────────────────────┬────────────────────┘
                                       │ HTTP Unix Sock / 127.0.0.1:5000
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │             Gunicorn WSGI               │
                  │   (3-5 Workers, Auto-Restart via systemd)│
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │         MarketDict Flask App            │
                  │    SQLite WAL Engine (6,108 Terms)      │
                  └─────────────────────────────────────────┘
```

### ۵.۱. نصب ابزارهای پایه روی سرور
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip nginx certbot python3-certbot-nginx git
```

### ۵.۲. راه‌اندازی سورس‌کد در مسیر استاندارد `/opt`
```bash
sudo mkdir -p /opt/market-dict
cd /opt
sudo git clone https://github.com/alisadeghiaghili/market-dict.git market-dict
cd market-dict

# ساخت محیط مجازی
sudo python3 -m venv .venv
sudo /opt/market-dict/.venv/bin/pip install --upgrade pip
sudo /opt/market-dict/.venv/bin/pip install -r requirements.txt

# اعطای دسترسی به کاربر سرویس‌دهنده وب www-data
sudo chown -R www-data:www-data /opt/market-dict
```

---

### ۵.۳. ساخت سرویس سیستمی Systemd

یک فایل سرویس سیستمی به آدرس `/etc/systemd/system/market-dict.service` بسازید:

```bash
sudo nano /etc/systemd/system/market-dict.service
```

محتوای زیر را داخل آن قرار دهید:

```ini
[Unit]
Description=MarketDict Production Web Application and REST API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/market-dict
Environment="PATH=/opt/market-dict/.venv/bin"
Environment="PROXY_HEADERS=true"
Environment="FORWARDED_ALLOW_IPS=127.0.0.1,::1"
ExecStart=/opt/market-dict/.venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --forwarded-allow-ips "127.0.0.1,::1" \
    --access-logfile /var/log/market-dict-access.log \
    --error-logfile /var/log/market-dict-error.log \
    app:app

Restart=always
RestartSec=5
KillSignal=SIGQUIT

[Install]
WantedBy=multi-user.target
```

فعال‌سازی و شروع به کار سرویس:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now market-dict
sudo systemctl status market-dict
```

---

### ۵.۴. پیکربندی وب‌سرور معکوس Nginx

فایل تنظیمات سایت Nginx را ایجاد کنید:

```bash
sudo nano /etc/nginx/sites-available/market-dict
```

تنظیمات کامل با فشرده‌سازی و هدایت هدرها:

```nginx
server {
    listen 80;
    server_name marketdict.internal.yourcompany.com; # دامنه داخلی شبکه سازمانی شما

    client_max_body_size 10M;

    # فشرده‌سازی خودکار جهت افزایش سرعت لود کاربران
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
    }

    # لاگ‌های اختصاصی
    access_log /var/log/nginx/market_dict_access.log;
    error_log /var/log/nginx/market_dict_error.log;
}
```

لینک کردن و ری‌لود انجین‌اکس:
```bash
sudo ln -s /etc/nginx/sites-available/market-dict /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### ۵.۵. فعال‌سازی رمزنگاری و SSL رایگان (Let's Encrypt)

برای اخذ و تمدید خودکار گواهینامه معتبر HTTPS:

```bash
sudo certbot --nginx -d marketdict.internal.yourcompany.com
```

ابزار Certbot به صورت خودکار فایل کانفیگ Nginx را به‌روزرسانی کرده و تایمر تمدید دوره‌ای را فعال می‌سازد.

---

## ۶. روش چهارم: راه‌اندازی و اتصال سرور MCP برای هوش مصنوعی

پروژه دارای سرور بومی **Model Context Protocol (MCP)** در فایل `mcp_server.py` است که امکان اتصال مستقیم پایگاه دانش ۶,۱۰۸ اصطلاحی را به ابزارهایی چون **Claude Desktop**، **Cursor IDE**، **Google Antigravity** و سایر ایجنت‌های هوش مصنوعی فراهم می‌آورد.

### ۶.۱. تست و اجرای سرور MCP

جهت اعتبارسنجی اجرای محلی سرور MCP:

```bash
python test_mcp_server.py
```
در صورت موفقیت‌آمیز بودن، تمام آزمون‌های مربوط به رجیستری ابزارها (`search_terms`, `get_financial_formula`, `suggest_terms` و...) تأیید می‌شوند.

---

### ۶.۲. اتصال به Claude Desktop

فایل پیکربندی کلود دسکتاپ را باز کنید:
- **ویندوز**: `%APPDATA%\Claude\claude_desktop_config.json`
- **مک‌اواس**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **لینوکس**: `~/.config/Claude/claude_desktop_config.json`

تنظیمات زیر را داخل بخش `mcpServers` اضافه نمایید (مسیر مفسر پایتون محیط مجازی و مسیر سورس‌پروژه را جایگزین کنید):

#### در ویندوز:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "C:\\Users\\YourUser\\Desktop\\Projects\\Market-Dict\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourUser\\Desktop\\Projects\\Market-Dict\\mcp_server.py"
      ]
    }
  }
}
```

#### در لینوکس / مک‌اواس:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "/opt/market-dict/.venv/bin/python",
      "args": [
        "/opt/market-dict/mcp_server.py"
      ]
    }
  }
}
```

پس از ذخیره فایل، برنامه Claude Desktop را کاملاً بسته و مجدداً باز نمایید. آیکون چکش (🛠️ Tools) در چت پدیدار شده و ۹ ابزار مالی MarketDict آماده پاسخ‌گویی خواهند بود.

---

### ۶.۳. اتصال به Cursor IDE و Antigravity

در محیط‌های توسعه هوشمند مانند Cursor یا Antigravity، فایل کانفیگ پروژه به صورت آماده در ریشه با نام `mcp_config.json` قرار دارد:

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
می‌توانید در تنظیمات **Features > MCP Servers** در Cursor، نوع سرور را `command` و دستور را `python mcp_server.py` قرار دهید.

---

### ۶.۴. اجرای تحت شبکه با پروتکل SSE

اگر می‌خواهید سرور MCP را روی یک ماشین سرور اجرا کرده و کلاینت‌ها از راه دور به آن متصل شوند:

```bash
# اجرا با ترنسپورت SSE روی پورت 8000
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"
```
آدرس اندپوینت SSE برای اتصال کلاینت‌ها: `http://<server-ip>:8000/sse`

---

## ۷. روش پنجم: تولید بیلد استاتیک و وب‌اپلیکیشن آفلاین (Static Site & PWA)

پروژه شامل یک اسکریپت بیلد اختصاصی (`build_static.py`) است که کل پایگاه دانش را به یک وب‌اپلیکیشن ۱۰۰٪ مستقل از بک‌اند پایتون تبدیل کرده و در پوشه `dist/` ذخیره می‌کند.

### ۷.۱. ساخت خروجی ایستا

در خط فرمان محیط مجازی دستور زیر را اجرا کنید:

```bash
python build_static.py
```

برای پاکسازی بیلد قبلی و ساخت کاملاً تازه:
```bash
python build_static.py --clean
```

این اسکریپت فرآیندهای زیر را انجام می‌دهد:
- تولید فایل `index.html` ایستا با تمامی استایل‌ها و اسکریپت‌ها
- شاردینگ داده‌های حجیم دیکشنری به بخش‌های سبک بر اساس حروف الفبا و شناسه‌ها در `dist/data/`
- کپی کردن فایل‌های کمکی، آیکون‌ها، فونت‌ها و کتابخانه‌های KaTeX
- ایجاد فایل‌های `manifest.json` و `sw.js` برای قابلیت نصب وب‌اپلیکیشن (PWA)
- افزودن فایل `.nojekyll` جهت سازگاری با سیستم‌های میزبانی فایل ایستا

---

### ۷.۲. میزبانی و استفاده در حالت آفلاین

پوشه `dist/` تولید شده می‌تواند توسط هر وب‌سرور ساده‌ای میزبانی شود:

```bash
# تست محلی پوشه dist با سرور پایتون:
python -m http.server --directory dist 8080
```
آدرس `http://localhost:8080` را در مرورگر باز کنید. پس از اولین بازگشایی، کش سرویس‌ورکر فعال شده و اپلیکیشن حتی در صورت قطع اینترنت به صورت آفلاین پاسخگوی جستجوها خواهد بود.

> ⚠️ **یادآوری حقوقی مهم**: دیتای موجود در دیکشنری طبق قوانین کپی‌رایت مندرج در [DATA_NOTICE.md](DATA_NOTICE.md) تنها مجاز به میزبانی در سرورها و شبکه‌های داخلی (Internal Deployment) است و نباید روی وب‌سایت‌های عمومی منتشر شود.

---

## ۸. روش ششم: ساخت اپلیکیشن موبایل اندروید با Capacitor

پروژه دارای پیکربندی یکپارچه با فریم‌ورک **Capacitor 6** است که خروجی وب استاتیک را به یک اپلیکیشن بومی با کارایی بالا (Native Android APK) تبدیل می‌کند.

### ۸.۱. پیش‌نیازهای محیط موبایل
1. نصب **Node.js LTS** (نسخه ۱۸ یا ۲۰)
2. نصب **Android Studio** به همراه Android SDK Platform 33+ و Android SDK Build-Tools
3. متغیر محیطی `ANDROID_HOME` به مسیر SDK اندروید سیستم شما اشاره کند.

---

### ۸.۲. نصب وابستگی‌های Node و خازنی

با توجه به سازگاری افزونه Text-to-Speech با نگارش Capacitor 6، پکیج‌ها باید حتماً با فلگ `--legacy-peer-deps` نصب شوند:

```bash
npm install --legacy-peer-deps
```

---

### ۸.۳. همگام‌سازی و تولید APK

```bash
# ۱. تولید فایل‌های استاتیک در پوشه dist
npm run build:static

# ۲. همگام‌سازی فایل‌های وب به پروژه نیتیو اندروید
npx cap sync android

# ۳. باز کردن پروژه در Android Studio
npx cap open android
```

در نرم‌افزار اندروید استودیو:
- از منوی **Build > Build Bundle(s) / APK(s) > Build APK(s)** را انتخاب کنید.
- فایل خروجی `app-debug.apk` در مسیر `android/app/build/outputs/apk/debug/` تولید می‌شود و آماده نصب بر روی گوشی‌های اندرویدی خواهد بود.

---

## ۹. متغیرهای محیطی و پارامترهای خط فرمان (CLI & Environment Variables)

برنامه به طور کامل از استاندارد ۱۲-Factor پشتیبانی کرده و از طریق خط فرمان یا متغیرهای سیستمی قابل پیکربندی است:

### جدول متغیرهای محیطی:

| نام متغیر محیطی | مقادیر معتبر | مقدار پیش‌فرض | توضیحات |
| :--- | :--- | :--- | :--- |
| `PORT` | عدد صحیح (مثلاً `5000`, `8080`) | `5000` | پورت شنود وب‌اپلیکیشن و API |
| `HOST` | آدرس IP (مثلاً `0.0.0.0`, `127.0.0.1`) | `0.0.0.0` | رابط شبکه برای بایند شدن سرور |
| `FLASK_ENV` | `production`, `development` | `production` | وضعیت محیط اجرای فلسک |
| `PROXY_HEADERS` | `true`, `false` | `false` (در app) / `true` (در داکر) | پردازش هدرهای پروکسی (`X-Forwarded-*`) |
| `FORWARDED_ALLOW_IPS` | لیست IP با کاما یا `*` | `*` | آی‌پی‌های مجاز پروکسی‌های معکوس بالادست |

### پارامترهای خط فرمان `app.py`:
```bash
python app.py --host 0.0.0.0 --port 5000 --proxy-headers --forwarded-allow-ips "127.0.0.1"
```

### پارامترهای خط فرمان `mcp_server.py`:
```bash
python mcp_server.py --transport [stdio|sse|streamable-http] --host 0.0.0.0 --port 8000
```

---

## ۱۰. اجرای آزمون‌های خودکار و تضمین کیفیت (Testing & QA)

پروژه شامل یک مجموعه تست جامع و آفلاین شامل **۷۲ آزمون کامل** است که تمام عملکردهای REST API، اعتبارسنجی داده‌ها، فرمول‌ها، دسته‌بندی‌ها و پروتکل MCP را می‌سنجد.

### اجرای کامل سوئیت تست‌ها:
```bash
python -m pytest -v
```

### اجرای تست‌های تفکیکی بر اساس ماژول:
```bash
# تست‌های مربوط به REST API و کلیه اندپوینت‌ها (29 تست)
python -m pytest test_api.py -v

# تست‌های موتور طبقه‌بندی و نرمال‌سازی فارسی (11 تست)
python -m pytest test_categories_engine.py -v

# تست‌های ابزارها و منابع سرور MCP (11 تست)
python -m pytest test_mcp_server.py -v

# تست‌های کلاینت اخلاقی وب و کراول مودبانه (9 تست)
python -m pytest test_polite_fetcher.py -v

# تست‌های فرمول‌های ریاضی و استخراج لاتک (1 تست)
python -m pytest test_enrich_sharpe.py -v

# تست‌های سیستم پیونددهی خودکار اصطلاحات (6 تست)
python -m pytest test_linker.py -v

# تست‌های اعتبارسنجی ترجمه و ساختار لینک‌ها (5 تست)
python -m pytest test_tr_link.py -v
```

---

## ۱۱. راهنمای جامع رفع اشکال و سوالات متداول (Troubleshooting & FAQ)

### ۱. خطای `Address already in use` یا `WinError 10048` (پورت ۵۰۰۰ اشغال است):
- **علت**: سرویس دیگری (مانند AirPlay در مک یا سرویس دیگر پایتون در ویندوز/لینوکس) پورت ۵۰۰۰ را در دست دارد.
- **راه حل**:
  - در پایتون می‌توانید پورت را تغییر دهید:
    ```bash
    python app.py --port 5050
    ```
  - یا در ویندوز فرآیند اشغال‌کننده پورت را پیدا و متوقف کنید:
    ```powershell
    netstat -ano | findstr :5000
    taskkill /PID <PID_NUMBER> /F
    ```
  - در لینوکس / مک:
    ```bash
    sudo lsof -i :5000
    sudo kill -9 <PID>
    ```

### ۲. خطای `Script Execution Policy` در PowerShell ویندوز:
- **علت**: سیاست‌های پیش‌فرض امنیتی ویندوز مانع اجرای اسکریپت‌های ناشناخته می‌شود.
- **راه حل**:
  دستور زیر را در پاورشل وارد نمایید:
  ```powershell
  Set-ExecutionPolicy -Scope Process RemoteSigned
  ```

### ۳. خطای `peer dependency conflict` در زمان اجرای `npm install`:
- **علت**: نیازمندی افزونه Text-to-Speech موبایل برای سازگاری با هسته Capacitor 6.
- **راه حل**:
  همیشه از فلگ مربوطه استفاده کنید:
  ```bash
  npm install --legacy-peer-deps
  ```

### ۴. خطای در دسترس نبودن یا مسدود بودن فایل SQLite:
- **علت**: عدم دسترسی Write در محیط‌هایی که فایل دیتابیس در مالکیت کاربر دیگر است.
- **راه حل**:
  در لینوکس مالکیت پوشه را به کاربری که برنامه را اجرا می‌کند انتقال دهید:
  ```bash
  sudo chown -R $USER:$USER .
  # یا در محیط عملیاتی:
  sudo chown -R www-data:www-data /opt/market-dict
  ```

### ۵. عدم شناسایی سرور MCP در Claude Desktop:
- **علت**: Claude Desktop نمی‌تواند دستور `python` را در مسیر عمومی پیدا کند یا پکیج‌های محیط مجازی در دسترس آن نیستند.
- **راه حل**:
  در فایل کانفیگ `claude_desktop_config.json`، به جای کلمه `python` ساده، مسیر مطلق فایل اجرایی مفسر پایتون موجود در پوشه `.venv` را قرار دهید (مانند `C:\\Users\\...\\.venv\\Scripts\\python.exe` یا `/opt/market-dict/.venv/bin/python`).

---

## ۱۲. نکات امنیتی و رعایت قوانین مالکیت داده‌ها

1. **پروانه سورس‌کد (Apache 2.0)**:
   تمامی کدهای توسعه‌داده شده در این مخزن تحت مجوز متن‌باز Apache 2.0 منتشر شده‌اند (فایل [LICENSE](LICENSE) و [NOTICE](NOTICE)).
2. **پایگاه داده اصطلاحات و محتوا**:
   محتوای متنی دیکشنری از سایت‌های شخص ثالث استخراج و غنی‌سازی شده است و تحت مالکیت معنوی مؤلفین اصلی قرار دارد. بازنشر عمومی، فروش یا توزیع تجاری این داده‌ها مجاز نمی‌باشد. این پایگاه صرفاً برای استفاده‌های داخلی سازمانی، تحقیقاتی، علمی و ارزیابی طراحی گردیده است.
3. **امنیت در سطح شبکه**:
   توصیه می‌شود هنگام استقرار سرور در محیط‌های عملیاتی، دسترسی به پورت ۵۰۰۰ مستقیماً از اینترنت مسدود شده و تنها از طریق Reverse Proxy امن و فایروال محلی (UFW / iptables) اجازه تبادل ترافیک داده شود.

---

### 🎉 تبریک! سیستم MarketDict شما با موفقیت راه‌اندازی و آماده بهره‌برداری است.
برای ارسال بازخورد، گزارش باگ یا ثبت درخواست ویژگی جدید به بخش Issues در مخزن گیت‌هاب مراجعه فرمایید.
