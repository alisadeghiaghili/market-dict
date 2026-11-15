# Deployment Guide - MarketDict

This document outlines standard production deployment strategies for **MarketDict**, including Docker containerization, Systemd service setup, and Nginx reverse proxy configuration.

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

## Verification & Health Check

Query the health check / stats endpoint:
```bash
curl http://localhost:5000/api/stats
```
Expected response:
```json
{
  "featured_count": 46,
  "total_categories": 46,
  "total_letters": 27,
  "total_terms": 631
}
```
