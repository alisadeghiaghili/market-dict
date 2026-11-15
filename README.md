# MarketDict

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

A modern bilingual (English & Persian) financial dictionary — **631 market & investing terms** across 14 domains, with real-time fuzzy search — paired with a stealth, polite Investopedia crawler that keeps the dataset fresh.

---

## Features

- **Bilingual Instant Search**: Real-time fuzzy search in both Persian and English with automatic Persian text normalization (`ی/ي`, `ک/ك`, zero-width non-joiners).
- **Side-by-Side Dual Language Display**: Full English definitions, Persian professional translations, and key takeaways for each term.
- **Audio Pronunciation**: Built-in voice pronunciation for English terms via the Web Speech API.
- **Interactive Alphabet & Category Filters**: Quickly explore terms by initial letter (`#`, `A-Z`) or financial domain (Corporate Finance, Accounting, Macroeconomics, Derivatives, etc.).
- **Local Favorites**: Bookmark terms for study sessions, persisted directly in local browser storage.
- **Dark / Light Mode**: Tailored user interface with responsive layout and glassmorphism styling.
- **Cloudflare-Tolerant Scraper**: Headless, silent crawler utilizing `curl_cffi` (Chrome TLS fingerprinting) with exponential backoff and polite rate limiting.

---

## Quick Start

### 1. Run Locally

```bash
# Clone the repository
git clone https://github.com/alisadeghiaghili/market-dict.git
cd market-dict

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
python app.py
```

Access the web interface at **`http://localhost:5000`**.

### 2. Run with Docker Compose

```bash
docker compose up -d --build
```

---

## Scraping Investopedia Terms

To refresh or expand the dictionary dataset directly from Investopedia:

```bash
# Extract curated terms from the dictionary landing page
python investopedia_scraper.py

# Extract all terms across all 27 alphabetical subpages
python investopedia_scraper.py --mode all

# Run quietly without terminal verbosity
python investopedia_scraper.py -q
```

---

## Production Deployment

For detailed production setup instructions using Docker or Gunicorn with Nginx and Systemd, refer to [DEPLOYMENT.md](DEPLOYMENT.md).

---

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Ali Sadeghi Aghili.
