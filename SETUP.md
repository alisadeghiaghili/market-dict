# MarketDict Setup & Installation Guide 🚀
# راهنمای جامع راه‌اندازی و نصب دیکشنری مالی (MarketDict)

> Official setup, running, containerization, and deployment guide for MarketDict across Windows, Linux, macOS, Docker, MCP, and Mobile environments.

---

### 🌐 Select Language / انتخاب زبان مستندات:

- 🇮🇷 **[راهنمای بسیار دقیق و جامع به زبان فارسی (Persian Setup Guide)](SETUP_FA.md)**
- 🇬🇧 **[Comprehensive Technical Setup Guide in English (English Setup Guide)](SETUP_EN.md)**

---

## ⚡ Quick Start (TL;DR)

### 1. Local Python Environment (Windows / Linux / macOS)
```bash
# Clone and enter repo
git clone https://github.com/alisadeghiaghili/market-dict.git
cd market-dict

# Setup virtual environment
python -m venv .venv
# Activate:
source .venv/bin/activate       # On Linux / macOS
.venv\Scripts\Activate.ps1      # On Windows PowerShell

# Install requirements
pip install -r requirements.txt

# Run server (Flask + REST API + Swagger UI)
python app.py
```
👉 Access Web App: [http://localhost:5000](http://localhost:5000)  
👉 Interactive Swagger API Docs: [http://localhost:5000/docs](http://localhost:5000/docs)  
👉 System Health Check: [http://localhost:5000/api/v1/health](http://localhost:5000/api/v1/health)

---

### 2. Docker & Docker Compose
```bash
docker compose up -d --build
```
Check running container:
```bash
docker compose ps
docker compose logs -f
```

---

### 3. Model Context Protocol (MCP) Server for AI
Test MCP tools and resources:
```bash
python test_mcp_server.py
```
For Claude Desktop or Cursor IDE, add `mcp_server.py` as configured in [mcp_config.json](mcp_config.json).  
See [MCP_DOCUMENTATION.md](MCP_DOCUMENTATION.md) for full setup instructions.

---

### 4. Standalone Offline PWA Build
```bash
python build_static.py
python -m http.server --directory dist 8080
```

---

### 5. Automated Test Suite (72 Offline Tests)
```bash
python -m pytest -v
```

---

## 📚 Detailed Documentation

For full step-by-step instructions including production **Systemd**, **Nginx Reverse Proxy**, **Let's Encrypt SSL**, **Capacitor Android APK builds**, and complete **Troubleshooting**, please read:
- 🇮🇷 **[SETUP_FA.md](SETUP_FA.md)** (راهنمای فارسی)
- 🇬🇧 **[SETUP_EN.md](SETUP_EN.md)** (English Guide)
