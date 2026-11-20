# Deployment Guide - MarketDict

This document outlines standard production deployment strategies for **MarketDict**, including Docker containerization, Systemd service setup, and Nginx reverse proxy configuration.

> **Internal deployments only.** The dictionary data contains third-party copyrighted content that is not licensed for redistribution. Deploy behind authentication on an internal network, never on a public website. See [DATA_NOTICE.md](DATA_NOTICE.md).

---

## Architecture Overview

```
                      ┌────────────────────────┐
                      │   Internet / Clients   │
                      └───────────┬────────────┘
                                  │ HTTPS (443)
                                  ▼
                      ┌────────────────────────┐
                      │   Nginx Reverse Proxy  │
                      └───────────┬────────────┘
                                  │ Proxy Pass (5000)
                                  ▼
                      ┌────────────────────────┐
                      │  Gunicorn WSGI Server  │
                      │  (app:app / 3 Workers) │
                      └────────────────────────┘
```

---

## Option 1: Docker & Docker Compose (Recommended)

### 1. Requirements
- Docker Engine 24.0+
- Docker Compose v2+

### 2. Quick Start
Build and run the containerized application in detached mode:

```bash
docker compose up -d --build
```

Check running container status:
```bash
docker compose ps
docker compose logs -f
```

The application is accessible at `http://localhost:5000`.

---

## Option 2: Linux Host Deployment (Systemd + Gunicorn + Nginx)

### 1. Prepare Environment
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip nginx certbot python3-certbot-nginx

# Setup project directory
cd /opt
sudo git clone https://github.com/alisadeghiaghili/market-dict.git
cd market-dict

# Virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Systemd Service
Create service file `/etc/systemd/system/market-dict.service`:

```ini
[Unit]
Description=MarketDict Bilingual Financial Web App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/market-dict
Environment="PATH=/opt/market-dict/.venv/bin"
ExecStart=/opt/market-dict/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 --timeout 120 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo chown -R www-data:www-data /opt/market-dict
sudo systemctl daemon-reload
sudo systemctl enable --now market-dict
sudo systemctl status market-dict
```

### 3. Configure Nginx Reverse Proxy
Create `/etc/nginx/sites-available/market-dict`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```

Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/market-dict /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Enable SSL Certificate (Let's Encrypt)
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## Reverse Proxy Configuration & CLI Flags

MarketDict supports full reverse proxy integration (e.g. Nginx, Traefik, Caddy, Cloudflare) for both the **Flask Web App & REST API (`app.py`)** and the **MCP Server (`mcp_server.py`)**.

### Command Line Flags

Both servers accept standard reverse proxy flags:

| Flag | Type / Format | Default | Description |
| :--- | :--- | :--- | :--- |
| `--host` | `TEXT` | `0.0.0.0` (app) / `127.0.0.1` (mcp) | Host IP address to bind to (also via `$HOST`) |
| `--port` | `INTEGER` | `5000` (app) / `8000` (mcp) | Port number to bind to (also via `$PORT`) |
| `--proxy-headers` / `--no-proxy-headers` | `BOOLEAN` | `False` (app) / `True` (mcp) | Enable processing of `X-Forwarded-*` headers |
| `--forwarded-allow-ips` | `TEXT` | `*` | Comma-separated list of trusted proxy IPs or `*` (also via `$FORWARDED_ALLOW_IPS`) |

### Example Usages

#### 1. Flask Web App & REST API (`app.py`)
```bash
# Run behind Nginx listening on port 5000, trusting localhost
python app.py --host 0.0.0.0 --port 5000 --proxy-headers --forwarded-allow-ips "127.0.0.1,10.0.0.1"

# Or trust all upstream reverse proxies (Docker / Kubernetes / Cloudflare)
python app.py --host 0.0.0.0 --port 5000 --proxy-headers --forwarded-allow-ips "*"
```

#### 2. MCP Server (`mcp_server.py`)
```bash
# Run MCP server with SSE transport behind reverse proxy
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"

# Run with Streamable HTTP transport
python mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "127.0.0.1"
```

#### 3. Via Environment Variables
You can also enable reverse proxy behavior globally without CLI flags:
```bash
export PROXY_HEADERS=true
export FORWARDED_ALLOW_IPS="*"
python app.py
# or
gunicorn --bind 0.0.0.0:5000 --forwarded-allow-ips "*" app:app
```

---

## Verification & Health Check

Query the health check / stats endpoint:
```bash
curl http://localhost:5000/api/stats
```
Expected response:
```json
{
  "total_terms": 631,
  "total_categories": 14,
  "total_letters": 27,
  "deep_enriched_count": 57
}
```
