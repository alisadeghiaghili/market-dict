# MarketDict

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Deploy to GitHub Pages](https://github.com/alisadeghiaghili/market-dict/actions/workflows/deploy.yml/badge.svg)](https://github.com/alisadeghiaghili/market-dict/actions/workflows/deploy.yml)
[![Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-emerald?logo=github)](https://alisadeghiaghili.github.io/market-dict/)

A modern bilingual (English & Persian) financial dictionary — **6,108 market & investing terms** across 14 domains with real-time fuzzy search, KaTeX mathematical formulas, and internal term cross-linking — deployed as a zero-latency static web app on GitHub Pages and paired with an Investopedia enrichment pipeline.

👉 **Live Demo:** [https://alisadeghiaghili.github.io/market-dict/](https://alisadeghiaghili.github.io/market-dict/)

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

The scraper traverses all 27 alphabetical subpages (`#`, `A` through `Z`) to discover and extract all financial terms across the entire dictionary, capturing complete definitions, key takeaways, and full Table of Contents sections.

```bash
# Scrape all 27 alphabetical subpages (#, A-Z) with full definitions, takeaways, and sections
python investopedia_scraper.py

# Scrape specific letter categories (e.g. A, B, and C)
python investopedia_scraper.py --letters a,b,c

# Fast catalog extraction (extract all 6,106+ term URLs and titles without body content)
python investopedia_scraper.py --no-details

# High-concurrency extraction with custom output filename
python investopedia_scraper.py --workers 16 -o full_investopedia_dictionary

# Run quietly in the background
python investopedia_scraper.py -q
```

---

## Production Deployment

For detailed production setup instructions using Docker or Gunicorn with Nginx and Systemd, refer to [DEPLOYMENT.md](DEPLOYMENT.md).

---

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Ali Sadeghi Aghili.
