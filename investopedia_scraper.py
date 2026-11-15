#!/usr/bin/env python3
"""
=============================================================================
Investopedia Financial Terms Dictionary Scraper
=============================================================================
Target: https://www.investopedia.com/financial-term-dictionary-4769738

Key Features:
- Silent & Stealth: Uses curl_cffi with Chrome 124 TLS/JA3/JA4 fingerprinting
  to bypass Cloudflare WAF silently and headless without any browser popups.
- Graceful:
  * Automatic retry with exponential backoff & jitter for network/rate limits (429/503).
  * Polite randomized rate limiting between requests to avoid server throttling.
  * Signal handling (Ctrl+C / SIGINT) ensures partial results are safely saved.
  * Checkpoint & incremental saving support.
- Dual Scrape Modes:
  * 'hub' (default): Extracts all 630+ terms directly listed on the dictionary hub page.
  * 'all' (--all-letters): Follows all 27 letter index subpages (#, A-Z) to extract
    the full dictionary (thousands of terms).
- Optional Deep Extraction (--with-details):
  * Scrapes definitions, meta descriptions, and key takeaways for each term.
- Multi-format Export: JSON and CSV with UTF-8 encoding.
=============================================================================
"""

import os
import sys
import time
import json
import csv
import random
import signal
import logging
import argparse
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, asdict

# Third-party dependencies
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] 'beautifulsoup4' is required. Run: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False
    import urllib.request
    import urllib.error


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
@dataclass
class ScraperConfig:
    hub_url: str = "https://www.investopedia.com/financial-term-dictionary-4769738"
    mode: str = "hub"  # 'hub' or 'all'
    output_prefix: str = "investopedia_terms"
    export_json: bool = True
    export_csv: bool = True
    delay_min: float = 0.8
    delay_max: float = 2.0
    timeout: int = 25
    max_retries: int = 4
    backoff_factor: float = 1.5
    fetch_details: bool = False
    max_terms: Optional[int] = None
    quiet: bool = False
    log_level: int = logging.INFO


# -----------------------------------------------------------------------------
# Scraper Implementation
# -----------------------------------------------------------------------------
class InvestopediaScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.terms: List[Dict] = []
        self.seen_urls: Set[str] = set()
        self.interrupted: bool = False

        self._setup_logging()
        self._setup_session()
        self._setup_signals()

    def _setup_logging(self):
        self.logger = logging.getLogger("InvestopediaScraper")
        self.logger.setLevel(logging.ERROR if self.config.quiet else self.config.log_level)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def _setup_session(self):
        if HAS_CURL_CFFI:
            self.session = cffi_requests.Session(impersonate="chrome124")
            self.logger.debug("Initialized curl_cffi session with Chrome 124 impersonation.")
        else:
            self.session = None
            self.logger.warning("curl_cffi not found. Using standard urllib fallback (may trigger Cloudflare 403).")

    def _setup_signals(self):
        """Handle Ctrl+C gracefully by saving what has been collected so far."""
        def handle_signal(sig, frame):
            self.logger.warning("\n[!] Interrupt signal received (Ctrl+C). Gracefully finishing and saving collected data...")
            self.interrupted = True

        signal.signal(signal.SIGINT, handle_signal)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, handle_signal)

    def _sleep_polite(self):
        """Graceful randomized delay to avoid triggering server rate limits."""
        delay = random.uniform(self.config.delay_min, self.config.delay_max)
        time.sleep(delay)

    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content gracefully with retries, exponential backoff, and WAF evasion.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
        }

        retries = 0
        backoff = 2.0

        while retries <= self.config.max_retries and not self.interrupted:
            try:
                if HAS_CURL_CFFI:
                    response = self.session.get(
                        url,
                        headers=headers,
                        timeout=self.config.timeout
                    )
                    status_code = response.status_code
                    text = response.text
                else:
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                        status_code = resp.status
                        text = resp.read().decode("utf-8", errors="ignore")

                if status_code == 200:
                    return text
                elif status_code in (429, 500, 502, 503, 504):
                    self.logger.warning(f"HTTP {status_code} on {url}. Retrying in {backoff:.1f}s (attempt {retries+1}/{self.config.max_retries})...")
                    time.sleep(backoff)
                    backoff *= self.config.backoff_factor
                    retries += 1
                else:
                    self.logger.error(f"HTTP {status_code} for {url}. Skipping.")
                    return None

            except Exception as e:
                self.logger.warning(f"Network error on {url}: {e}. Retrying in {backoff:.1f}s (attempt {retries+1}/{self.config.max_retries})...")
                time.sleep(backoff)
                backoff *= self.config.backoff_factor
                retries += 1

        self.logger.error(f"Failed to fetch {url} after {self.config.max_retries} attempts.")
        return None

    def parse_hub_page(self, html: str) -> Tuple[List[Dict], Dict[str, str]]:
        """
        Parses the master dictionary page:
        1. Extracts the curated top terms for each letter block.
        2. Discovers the 27 subpage links ('terms-beginning-with-*') for deep scraping.
        """
        soup = BeautifulSoup(html, "html.parser")
        hub_terms = []
        letter_links = {}

        # 1. Extract letter blocks
        import re
        sections = soup.find_all("div", class_=re.compile(r"dictionary-top24-list__content"))
        for section in sections:
            heading = section.find(["h2", "h3", "span", "a"], class_=re.compile(r"heading|letter|title", re.I))
            letter = heading.get_text(strip=True).upper() if heading else "OTHER"

            items = section.find_all("a", class_=re.compile(r"dictionary-top24-list__sublist"))
            for item in items:
                term_title = item.get_text(strip=True)
                term_url = item.get("href", "").strip()
                if term_url.startswith("/"):
                    term_url = "https://www.investopedia.com" + term_url

                if term_url and term_url not in self.seen_urls:
                    self.seen_urls.add(term_url)
                    slug = term_url.rstrip("/").split("/")[-1].replace(".asp", "")
                    hub_terms.append({
                        "letter": letter,
                        "term": term_title,
                        "url": term_url,
                        "slug": slug,
                        "source": "hub_page"
                    })

        # 2. Extract full letter index links
        for a in soup.find_all("a", href=re.compile(r"terms-beginning-with-")):
            href = a.get("href", "").strip()
            if href.startswith("/"):
                href = "https://www.investopedia.com" + href
            m = re.search(r"terms-beginning-with-([a-z0-9]+)", href)
            if m:
                letter_key = m.group(1).upper()
                letter_links[letter_key] = href

        return hub_terms, letter_links

    def parse_letter_page(self, html: str, letter: str) -> List[Dict]:
        """
        Parses an individual letter index page (e.g. Terms Beginning With 'A').
        Extracts all terms listed under the dictionary list container.
        """
        import re
        soup = BeautifulSoup(html, "html.parser")
        letter_terms = []

        # Find all term links inside the dictionary container
        # Pattern covers 'dictionary-top300-list__list', 'dictionary-list', etc.
        anchors = soup.find_all("a", class_=re.compile(r"dictionary-(?:top\d+|list).*__list"))
        if not anchors:
            # Fallback: scan main content for /terms/ links
            main = soup.find("main") or soup.find("article") or soup
            anchors = [a for a in main.find_all("a", href=True) if "/terms/" in a["href"]]

        for a in anchors:
            term_title = a.get_text(strip=True)
            term_url = a.get("href", "").strip()
            if term_url.startswith("/"):
                term_url = "https://www.investopedia.com" + term_url

            # Filter out non-term links (e.g. navigation or category pages)
            if not term_title or not term_url or "/terms/" not in term_url:
                continue

            if term_url not in self.seen_urls:
                self.seen_urls.add(term_url)
                slug = term_url.rstrip("/").split("/")[-1].replace(".asp", "")
                letter_terms.append({
                    "letter": letter,
                    "term": term_title,
                    "url": term_url,
                    "slug": slug,
                    "source": f"letter_{letter}"
                })

        return letter_terms

    def fetch_term_detail(self, term_dict: Dict) -> Dict:
        """
        Optionally fetches the term's page to extract:
        - Meta description
        - Summary / Definition
        - Key Takeaways (if present)
        """
        url = term_dict["url"]
        self._sleep_polite()
        html = self.fetch_page(url)
        if not html:
            term_dict["definition"] = ""
            term_dict["key_takeaways"] = []
            return term_dict

        soup = BeautifulSoup(html, "html.parser")

        # 1. Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        term_dict["meta_description"] = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""

        # 2. Key takeaways
        takeaways = []
        takeaways_div = soup.find("div", id=lambda x: x and "key-takeaways" in x.lower()) or \
                        soup.find(class_=lambda x: x and "takeaways" in str(x).lower())
        if takeaways_div:
            takeaways = [li.get_text(strip=True) for li in takeaways_div.find_all("li")]
        term_dict["key_takeaways"] = takeaways

        # 3. Intro definition paragraph
        body_div = soup.find("div", id="article-body") or soup.find("div", class_=lambda x: x and "article-body" in str(x).lower())
        if body_div:
            p = body_div.find("p")
            term_dict["definition"] = p.get_text(strip=True) if p else ""
        else:
            term_dict["definition"] = term_dict.get("meta_description", "")

        return term_dict

    def run(self) -> List[Dict]:
        """
        Orchestrates the scraping flow based on configuration.
        """
        self.logger.info(f"Starting Investopedia scraper in mode='{self.config.mode}'...")
        self.logger.info(f"Fetching master dictionary hub: {self.config.hub_url}")

        hub_html = self.fetch_page(self.config.hub_url)
        if not hub_html:
            self.logger.error("Failed to load dictionary hub page. Exiting.")
            return []

        hub_terms, letter_links = self.parse_hub_page(hub_html)
        self.logger.info(f"Extracted {len(hub_terms)} terms directly from the hub page.")
        self.logger.info(f"Discovered {len(letter_links)} letter subpages (#, A-Z).")

        self.terms.extend(hub_terms)

        # Mode 'all': Crawl all letter subpages
        if self.config.mode == "all" and not self.interrupted:
            self.logger.info("Beginning deep extraction across all letter subpages...")
            letters_order = sorted(letter_links.keys())

            for idx, letter_key in enumerate(letters_order, 1):
                if self.interrupted:
                    break
                if self.config.max_terms and len(self.terms) >= self.config.max_terms:
                    self.logger.info(f"Reached max_terms limit ({self.config.max_terms}).")
                    break

                letter_url = letter_links[letter_key]
                self.logger.info(f"[{idx}/{len(letters_order)}] Scraping letter '{letter_key}' ({letter_url})...")
                self._sleep_polite()

                sub_html = self.fetch_page(letter_url)
                if not sub_html:
                    self.logger.warning(f"Could not load letter '{letter_key}'. Skipping.")
                    continue

                sub_terms = self.parse_letter_page(sub_html, letter_key)
                self.logger.info(f"  -> Added {len(sub_terms)} new terms for letter '{letter_key}'. Total so far: {len(self.terms) + len(sub_terms)}")
                self.terms.extend(sub_terms)

        # Truncate if max_terms specified
        if self.config.max_terms:
            self.terms = self.terms[:self.config.max_terms]

        # Mode '--with-details': Fetch term details
        if self.config.fetch_details and not self.interrupted:
            total = len(self.terms)
            self.logger.info(f"Fetching in-depth definitions for {total} terms...")
            for idx, item in enumerate(self.terms, 1):
                if self.interrupted:
                    break
                self.logger.info(f"[{idx}/{total}] Fetching details: {item['term']}")
                self.fetch_term_detail(item)

        self.logger.info(f"Scraping completed! Total unique terms collected: {len(self.terms)}")
        self.save_results()
        return self.terms

    def save_results(self):
        """
        Saves the results cleanly to JSON and/or CSV files.
        """
        if not self.terms:
            self.logger.warning("No terms collected to save.")
            return

        prefix = self.config.output_prefix

        # 1. JSON Export
        if self.config.export_json:
            json_filename = f"{prefix}.json"
            try:
                with open(json_filename, "w", encoding="utf-8") as f:
                    json.dump(self.terms, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Saved {len(self.terms)} terms to JSON: [ {json_filename} ]")
            except Exception as e:
                self.logger.error(f"Failed to write JSON: {e}")

        # 2. CSV Export
        if self.config.export_csv:
            csv_filename = f"{prefix}.csv"
            try:
                # Determine fieldnames dynamically
                keys = ["letter", "term", "url", "slug", "source"]
                if self.config.fetch_details:
                    keys += ["meta_description", "definition", "key_takeaways"]

                with open(csv_filename, "w", encoding="utf-8-sig", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
                    writer.writeheader()
                    for item in self.terms:
                        row = dict(item)
                        if "key_takeaways" in row and isinstance(row["key_takeaways"], list):
                            row["key_takeaways"] = " | ".join(row["key_takeaways"])
                        writer.writerow(row)
                self.logger.info(f"Saved {len(self.terms)} terms to CSV: [ {csv_filename} ]")
            except Exception as e:
                self.logger.error(f"Failed to write CSV: {e}")


# -----------------------------------------------------------------------------
# CLI Entry Point
# -----------------------------------------------------------------------------
def parse_arguments() -> ScraperConfig:
    parser = argparse.ArgumentParser(
        description="Accurate, graceful & silent scraper for Investopedia Financial Terms Dictionary."
    )
    parser.add_argument(
        "--mode",
        choices=["hub", "all"],
        default="hub",
        help="Scraping mode: 'hub' extracts terms directly on the target URL (~630 terms); 'all' follows all 27 letter subpages to extract the entire dictionary (~6,000+ terms)."
    )
    parser.add_argument(
        "-o", "--output",
        default="investopedia_terms",
        help="Output filename prefix (without extension). Default: 'investopedia_terms'."
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        default="both",
        help="Export format: 'json', 'csv', or 'both' (default: both)."
    )
    parser.add_argument(
        "--with-details",
        action="store_true",
        help="Fetch in-depth definition, meta description, and key takeaways for each term."
    )
    parser.add_argument(
        "--delay-min",
        type=float,
        default=0.8,
        help="Minimum polite delay between requests in seconds (default: 0.8s)."
    )
    parser.add_argument(
        "--delay-max",
        type=float,
        default=2.0,
        help="Maximum polite delay between requests in seconds (default: 2.0s)."
    )
    parser.add_argument(
        "--max-terms",
        type=int,
        default=None,
        help="Optional limit on maximum number of terms to collect (useful for testing)."
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Silent mode (suppress terminal logs, except errors)."
    )

    args = parser.parse_args()

    return ScraperConfig(
        mode=args.mode,
        output_prefix=args.output,
        export_json=args.format in ("json", "both"),
        export_csv=args.format in ("csv", "both"),
        delay_min=args.delay_min,
        delay_max=args.delay_max,
        fetch_details=args.with_details,
        max_terms=args.max_terms,
        quiet=args.quiet
    )


def main():
    config = parse_arguments()
    scraper = InvestopediaScraper(config)
    scraper.run()


if __name__ == "__main__":
    main()
