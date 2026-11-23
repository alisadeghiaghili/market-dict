# Comprehensive MarketDict Setup & Installation Guide 🚀

> Official, step-by-step technical guide for setting up, running, testing, containerizing, and deploying **MarketDict** across all environments: Windows, Linux, macOS, Docker, Production Servers (Systemd + Gunicorn + Nginx), Model Context Protocol (MCP) servers, Static builds (PWA), and Mobile (Capacitor Android).

---

### 🌐 Documentation Languages / فهرست زبان‌ها:
- 🇮🇷 **[راهنمای جامع راه‌اندازی به زبان فارسی (SETUP_FA.md)](SETUP_FA.md)**
- 🇬🇧 **English Setup Guide (This Document)**
- 📖 **[REST API Reference (API.md)](API.md)**
- 🤖 **[MCP Server Documentation (MCP_DOCUMENTATION.md)](MCP_DOCUMENTATION.md)**
- 🚢 **[Production Deployment Architecture (DEPLOYMENT.md)](DEPLOYMENT.md)**
- ⚖️ **[Data Notice & Copyright (DATA_NOTICE.md)](DATA_NOTICE.md)**

---

## Table of Contents

1. [Architecture & Project Overview](#1-architecture--project-overview)
2. [Prerequisites & System Requirements](#2-prerequisites--system-requirements)
3. [Option 1: Local Development Quickstart](#3-option-1-local-development-quickstart)
   - [3.1. Clone Repository](#31-clone-repository)
   - [3.2. Setup Python Virtual Environment](#32-setup-python-virtual-environment)
   - [3.3. Install Dependencies](#33-install-dependencies)
   - [3.4. Run the Development Server](#34-run-the-development-server)
   - [3.5. Verify Health & Explore Web UI](#35-verify-health--explore-web-ui)
4. [Option 2: Docker & Docker Compose Containerization](#4-option-2-docker--docker-compose-containerization)
   - [4.1. One-Line Compose Execution](#41-one-line-compose-execution)
   - [4.2. Container Lifecycle & Monitoring](#42-container-lifecycle--monitoring)
   - [4.3. Manual Docker CLI Build](#43-manual-docker-cli-build)
5. [Option 3: Enterprise Linux Production Deployment](#5-option-3-enterprise-linux-production-deployment)
   - [5.1. System Preparation](#51-system-preparation)
   - [5.2. Systemd Service Unit Configuration](#52-systemd-service-unit-configuration)
   - [5.3. Nginx Reverse Proxy Setup](#53-nginx-reverse-proxy-setup)
   - [5.4. SSL/TLS Certificate with Let's Encrypt](#54-ssltls-certificate-with-lets-encrypt)
6. [Option 4: Model Context Protocol (MCP) Server Setup](#6-option-4-model-context-protocol-mcp-server-setup)
   - [6.1. MCP Server Test Suite](#61-mcp-server-test-suite)
   - [6.2. Claude Desktop Integration](#62-claude-desktop-integration)
   - [6.3. Cursor IDE & Google Antigravity Integration](#63-cursor-ide--google-antigravity-integration)
   - [6.4. Remote SSE Network Transport](#64-remote-sse-network-transport)
7. [Option 5: Static Build & Offline Progressive Web App (PWA)](#7-option-5-static-build--offline-progressive-web-app-pwa)
   - [7.1. Generate 100% Static Build](#71-generate-100-static-build)
   - [7.2. Serve & Install Offline PWA](#72-serve--install-offline-pwa)
8. [Option 6: Native Android Mobile App (Capacitor 6)](#8-option-6-native-android-mobile-app-capacitor-6)
   - [8.1. Mobile Prerequisites](#81-mobile-prerequisites)
   - [8.2. Install Dependencies](#82-install-dependencies)
   - [8.3. Sync & Build APK](#83-sync--build-apk)
9. [Configuration & Environment Variables](#9-configuration--environment-variables)
10. [Automated Verification & Test Suite](#10-automated-verification--test-suite)
11. [Troubleshooting & Frequently Asked Questions (FAQ)](#11-troubleshooting--frequently-asked-questions-faq)
12. [Security & Compliance](#12-security--compliance)

---

## 1. Architecture & Project Overview

**MarketDict** is a production-ready bilingual financial dictionary platform featuring:
- **6,108 enriched financial terms** across **32 taxonomy categories**.
- **44 quantitative financial formulas** rendered with mathematical KaTeX.
- Real-time bilingual fuzzy search with automatic Persian text normalization (`ی/ي`, `ک/ك`, zero-width non-joiners).
- Production REST API v1 with interactive Swagger UI and OpenAPI 3.0 specification.
- Native Model Context Protocol (MCP) server for LLMs and AI coding assistants.
- Fully offline Progressive Web App (PWA) and Capacitor-powered Android application.

### Key File Map:
```
Market-Dict/
├── app.py                      # Flask web application and HTTP entrypoint
├── api_v1.py                   # REST API v1 engine with OpenAPI 3.0 specs & Swagger UI
├── mcp_server.py               # Native Model Context Protocol (MCP) server (stdio/SSE)
├── categories_engine.py        # 32-category taxonomy engine & text classifier
├── polite_fetcher.py           # Ethical web scraper honoring robots.txt and Crawl-delay
├── build_static.py             # Generates standalone serverless static build in dist/
├── sw.js / manifest.json       # Service worker & PWA manifest for offline caching
├── marketdict_client.py        # Zero-dependency official Python client SDK
├── MarketDictClient.cs         # Official C# / .NET client SDK
├── capacitor.config.json       # Capacitor 6 configuration for Android builds
├── Dockerfile                  # Production container definition (Python 3.11-slim)
├── docker-compose.yml          # Container orchestration service definition
├── requirements.txt            # Python dependencies
├── test_*.py                   # 72 automated offline test cases
└── bilingual_dictionary.json   # 6,108-term enriched bilingual database
```

---

## 2. Prerequisites & System Requirements

### Hardware Requirements:
- **CPU**: 1 core minimum (2+ cores recommended for production or Docker builds)
- **RAM**: 1 GB minimum (2 GB recommended)
- **Disk**: 500 MB free storage

### Software Requirements:
- **Python**: Python 3.10+ (tested on Python 3.11 and 3.12)
- **Package Manager**: `pip`
- **Version Control**: `git`
- *(Optional - for containerization)*: Docker Engine 24+ & Docker Compose v2+
- *(Optional - for mobile build)*: Node.js 18+ LTS, npm, Java JDK 17, Android Studio

---

## 3. Option 1: Local Development Quickstart

### 3.1. Clone Repository
```bash
git clone https://github.com/alisadeghiaghili/market-dict.git
cd market-dict
```

---

### 3.2. Setup Python Virtual Environment

#### On Windows (PowerShell or CMD):
```powershell
# Create virtual environment
python -m venv .venv

# Activate in PowerShell:
.venv\Scripts\Activate.ps1

# Or activate in classic Command Prompt:
.venv\Scripts\activate.bat
```

> 💡 **PowerShell Tip**: If you encounter an `ExecutionPolicy` error on Windows, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process RemoteSigned
> ```

#### On Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3.3. Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3.4. Run the Development Server
```bash
python app.py
```

By default, the server listens on all network interfaces on port `5000`:
```text
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

#### Custom Host / Port:
```bash
# Custom port
python app.py --port 5050

# Bind to localhost only
python app.py --host 127.0.0.1 --port 5000
```

---

### 3.5. Verify Health & Explore Web UI

Once started, navigate to:

| Target | URL | Description |
| :--- | :--- | :--- |
| **Web Interface** | `http://localhost:5000` | Instant search, alphabetical filters, formulas, dark/light mode |
| **Swagger UI** | `http://localhost:5000/docs` | Interactive REST API explorer |
| **OpenAPI Spec** | `http://localhost:5000/api/v1/openapi.json` | Machine-readable OpenAPI 3.0.3 specification |
| **Health Check** | `http://localhost:5000/api/v1/health` | System status, uptime, term count, database state |
| **Statistics** | `http://localhost:5000/api/stats` | Aggregated term, letter, formula, and category counts |

Quick verification with cURL:
```bash
curl -s http://localhost:5000/api/v1/health
```

---

## 4. Option 2: Docker & Docker Compose Containerization

### 4.1. One-Line Compose Execution
```bash
docker compose up -d --build
```
This automatically compiles the Python 3.11 image, sets up Gunicorn with 3 workers, and serves the app on `http://localhost:5000`.

---

### 4.2. Container Lifecycle & Monitoring

```bash
# Check container status
docker compose ps

# Follow live container logs
docker compose logs -f web

# Stop container
docker compose stop

# Restart container
docker compose restart

# Stop and remove containers
docker compose down
```

---

### 4.3. Manual Docker CLI Build
```bash
# Build Docker image
docker build -t marketdict:latest .

# Run container
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

## 5. Option 3: Enterprise Linux Production Deployment

For production deployments on Ubuntu 22.04 LTS / Debian 12 / RHEL, use **Gunicorn** managed by **Systemd** behind an **Nginx** reverse proxy with SSL termination.

### 5.1. System Preparation
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip nginx certbot python3-certbot-nginx git

# Setup directory
sudo mkdir -p /opt/market-dict
cd /opt
sudo git clone https://github.com/alisadeghiaghili/market-dict.git market-dict
cd market-dict

# Virtual environment
sudo python3 -m venv .venv
sudo /opt/market-dict/.venv/bin/pip install --upgrade pip
sudo /opt/market-dict/.venv/bin/pip install -r requirements.txt

# Permissions
sudo chown -R www-data:www-data /opt/market-dict
```

---

### 5.2. Systemd Service Unit Configuration

Create `/etc/systemd/system/market-dict.service`:
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

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now market-dict
sudo systemctl status market-dict
```

---

### 5.3. Nginx Reverse Proxy Setup

Create `/etc/nginx/sites-available/market-dict`:
```nginx
server {
    listen 80;
    server_name marketdict.internal.yourcompany.com;

    client_max_body_size 10M;

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

    access_log /var/log/nginx/market_dict_access.log;
    error_log /var/log/nginx/market_dict_error.log;
}
```

Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/market-dict /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### 5.4. SSL/TLS Certificate with Let's Encrypt
```bash
sudo certbot --nginx -d marketdict.internal.yourcompany.com
```

---

## 6. Option 4: Model Context Protocol (MCP) Server Setup

MarketDict includes a native **Model Context Protocol (MCP)** server (`mcp_server.py`) enabling AI assistants (such as **Claude Desktop**, **Cursor IDE**, and **Google Antigravity**) to search terms, query formulas, and explore categories.

### 6.1. MCP Server Test Suite
Verify local MCP operation:
```bash
python test_mcp_server.py
```

---

### 6.2. Claude Desktop Integration

Edit your Claude Desktop configuration file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the server using absolute python paths:

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "C:\\path\\to\\Market-Dict\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\Market-Dict\\mcp_server.py"]
    }
  }
}
```

Restart Claude Desktop. The 9 MarketDict financial tools will appear in the 🛠️ Tools panel.

---

### 6.3. Cursor IDE & Google Antigravity Integration

The repository includes a ready-to-use configuration file: [`mcp_config.json`](mcp_config.json):
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

### 6.4. Remote SSE Network Transport
Run MCP as an SSE server accessible across the network:
```bash
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"
```
Client SSE endpoint: `http://<server-ip>:8000/sse`

---

## 7. Option 5: Static Build & Offline Progressive Web App (PWA)

### 7.1. Generate 100% Static Build
```bash
python build_static.py
```
This generates the standalone build in the `dist/` directory, including:
- Data sharded into lightweight JSON files under `dist/data/`
- Full offline search capability via Service Worker (`sw.js`) and Web Manifest (`manifest.json`)
- `.nojekyll` file for compatibility with static file hosts.

---

### 7.2. Serve & Install Offline PWA
```bash
python -m http.server --directory dist 8080
```
Open `http://localhost:8080`. Once loaded, click the "Install" button in your browser to install MarketDict as an offline desktop or mobile app.

---

## 8. Option 6: Native Android Mobile App (Capacitor 6)

### 8.1. Mobile Prerequisites
- Node.js 18+ or 20+ LTS
- Android Studio with Android SDK 33+
- Java JDK 17

---

### 8.2. Install Dependencies
Install dependencies with `--legacy-peer-deps` (required for text-to-speech plugin compatibility):
```bash
npm install --legacy-peer-deps
```

---

### 8.3. Sync & Build APK
```bash
# 1. Compile static web assets
npm run build:static

# 2. Sync assets with native Android project
npx cap sync android

# 3. Open in Android Studio
npx cap open android
```

In Android Studio:
- Select **Build > Build Bundle(s) / APK(s) > Build APK(s)**
- The output APK is generated at `android/app/build/outputs/apk/debug/app-debug.apk`.

---

## 9. Configuration & Environment Variables

| Variable | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `PORT` | Integer (e.g. `5000`) | `5000` | HTTP listening port |
| `HOST` | IP Address (e.g. `0.0.0.0`) | `0.0.0.0` | Network interface to bind |
| `FLASK_ENV` | `production`, `development` | `production` | Flask runtime environment |
| `PROXY_HEADERS` | `true`, `false` | `false` / `true` (Docker) | Enable reverse proxy header processing |
| `FORWARDED_ALLOW_IPS` | Comma-separated IPs or `*` | `*` | Trusted upstream reverse proxy IP addresses |

---

## 10. Automated Verification & Test Suite

MarketDict includes **72 offline automated tests** covering 100% of the core functionality.

Run the entire test suite:
```bash
python -m pytest -v
```

Run specific test modules:
```bash
# REST API endpoints (29 tests)
python -m pytest test_api.py -v

# Categorization and Persian normalization (11 tests)
python -m pytest test_categories_engine.py -v

# Model Context Protocol tools & resources (11 tests)
python -m pytest test_mcp_server.py -v

# Ethical scraper & polite fetcher (9 tests)
python -m pytest test_polite_fetcher.py -v

# Formula parser and LaTeX extraction (1 test)
python -m pytest test_enrich_sharpe.py -v

# Internal term auto-linker (6 tests)
python -m pytest test_linker.py -v

# Translation and link tag preservation (5 tests)
python -m pytest test_tr_link.py -v
```

---

## 11. Troubleshooting & Frequently Asked Questions (FAQ)

### 1. Error: `Address already in use` (Port 5000 busy)
- **Fix**: Change port using `--port 5050` or terminate the occupying process:
  - Windows: `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`
  - Linux/macOS: `sudo lsof -i :5000` then `sudo kill -9 <PID>`

### 2. Error: `Execution of scripts is disabled on this system` (PowerShell)
- **Fix**: Enable local script execution:
  ```powershell
  Set-ExecutionPolicy -Scope Process RemoteSigned
  ```

### 3. Error: `npm ERR! ERESOLVE could not resolve`
- **Fix**: Use `--legacy-peer-deps`:
  ```bash
  npm install --legacy-peer-deps
  ```

### 4. Error: Claude Desktop cannot connect to MCP server
- **Fix**: Ensure you provide the full absolute path to the `.venv` Python executable in `claude_desktop_config.json`.

---

## 12. Security & Compliance

- **Source Code**: Apache 2.0 License ([LICENSE](LICENSE) and [NOTICE](NOTICE)).
- **Dictionary Data**: Third-party copyrighted data not licensed for redistribution or public internet hosting. Deploy strictly behind authentication on internal company networks. See [DATA_NOTICE.md](DATA_NOTICE.md).
