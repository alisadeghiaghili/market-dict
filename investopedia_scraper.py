#!/usr/bin/env python3
"""
=============================================================================
Investopedia Financial Terms Dictionary Scraper (Deep Content Edition)
=============================================================================
Target: https://www.investopedia.com/financial-term-dictionary-4769738

Key Features:
- Silent & Stealth: Uses curl_cffi with Chrome 124 TLS/JA3/JA4 fingerprinting
  to bypass Cloudflare WAF silently and headless without any browser popups.
- Full Content Extraction:
  * Lead Definition (introductory definition paragraphs)
  * Key Takeaways (all bullet points from callouts)
  * Complete In-Depth Sections (Formulas, Calculations, Examples, Pros/Cons,
    Comparisons, FAQs, and 'The Bottom Line')
- Graceful & Resilient:
  * Automatic retry with exponential backoff & jitter for network/rate limits.
  * Polite randomized rate limiting between requests to avoid server throttling.
  * Signal handling (Ctrl+C / SIGINT) ensures partial results are safely saved.
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
            self.logger.warning("curl_cffi not found. Using standard urllib fallback.")

    def _setup_signals(self):
        def handle_signal(sig, frame):
            self.logger.warning("\n[!] Interrupt signal received (Ctrl+C). Gracefully finishing and saving collected data...")
            self.interrupted = True

        signal.signal(signal.SIGINT, handle_signal)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, handle_signal)

    def _sleep_polite(self):
        delay = random.uniform(self.config.delay_min, self.config.delay_max)
        time.sleep(delay)

    def fetch_page(self, url: str) -> Optional[str]:
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
                    response = self.session.get(url, headers=headers, timeout=self.config.timeout)
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
                    self.logger.warning(f"HTTP {status_code} on {url}. Retrying in {backoff:.1f}s...")
                    time.sleep(backoff)
                    backoff *= self.config.backoff_factor
                    retries += 1
                else:
                    self.logger.error(f"HTTP {status_code} for {url}. Skipping.")
                    return None

            except Exception as e:
                self.logger.warning(f"Network error on {url}: {e}. Retrying in {backoff:.1f}s...")
                time.sleep(backoff)
                backoff *= self.config.backoff_factor
                retries += 1

        return None

    def parse_hub_page(self, html: str) -> Tuple[List[Dict], Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        hub_terms = []
        letter_links = {}
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
        import re
        soup = BeautifulSoup(html, "html.parser")
        letter_terms = []

        anchors = soup.find_all("a", class_=re.compile(r"dictionary-(?:top\d+|list).*__list"))
        if not anchors:
            main = soup.find("main") or soup.find("article") or soup
            anchors = [a for a in main.find_all("a", href=True) if "/terms/" in a["href"]]

        for a in anchors:
            term_title = a.get_text(strip=True)
            term_url = a.get("href", "").strip()
            if term_url.startswith("/"):
                term_url = "https://www.investopedia.com" + term_url

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

    def parse_full_term_content(self, html: str) -> Dict:
        """
        Extracts ALL useful information from a term page:
        1. Lead definition (paragraphs before first heading)
        2. Key takeaways (all bullet points)
        3. All in-depth sections (Heading, Paragraphs, Lists, Examples, Bottom line)
        """
        import re
        soup = BeautifulSoup(html, "html.parser")

        # 1. Meta description
        meta_desc = ""
        m = soup.find("meta", attrs={"name": "description"})
        if m and m.get("content"):
            meta_desc = m["content"].strip()

        body = soup.find("div", class_="article-body-content") or soup.find("div", id="article-body_1-0") or soup

        # 2. Key Takeaways
        takeaways = []
        callout = soup.find(class_=re.compile(r"universal-callout|whatyouneedtoknow|key-takeaways"))
        if callout:
            for li in callout.find_all("li"):
                txt = li.get_text(strip=True)
                if txt and len(txt) > 5:
                    takeaways.append(txt)

        # 3. Lead Definition
        lead_paragraphs = []
        for p in body.find_all("p", recursive=True):
            if p.find_parent(class_=re.compile(r"callout|recirc|newsletter|author|ad-")):
                continue
            txt = p.get_text(strip=True)
            if len(txt) > 25 and not any(skip in txt for skip in ["Get personalized", "Investopedia /", "Fact checked by"]):
                lead_paragraphs.append(txt)
                if len(lead_paragraphs) >= 2:
                    break

        lead_definition = "\n\n".join(lead_paragraphs) if lead_paragraphs else meta_desc

        # 4. Detailed Sections
        sections = []
        current_sec = None
        bottom_line = ""

        for el in body.children:
            if not hasattr(el, "name") or not el.name:
                continue

            h = el if el.name in ["h2", "h3"] else el.find(["h2", "h3"])
            if h:
                htxt = h.get_text(strip=True)
                if any(skip in htxt.lower() for skip in ["related articles", "article sources", "trending", "newsletter", "key takeaways"]):
                    continue
                if current_sec and (current_sec["paragraphs"] or current_sec["items"]):
                    sections.append(current_sec)
                current_sec = {"title": htxt, "paragraphs": [], "items": []}

            if current_sec:
                ps = el.find_all("p") if el.name != "p" else [el]
                for p in ps:
                    ptxt = p.get_text(strip=True)
                    if ptxt and len(ptxt) > 20 and not any(skip in ptxt for skip in ["Get personalized", "Investopedia /", "Fact checked by"]):
                        if "bottom line" in current_sec["title"].lower():
                            bottom_line += ptxt + " "
                        current_sec["paragraphs"].append(ptxt)

                lis = el.find_all("li")
                for li in lis:
                    litxt = li.get_text(strip=True)
                    if litxt and len(litxt) > 5 and len(litxt) < 300:
                        current_sec["items"].append(litxt)

        if current_sec and (current_sec["paragraphs"] or current_sec["items"]):
            sections.append(current_sec)

        return {
            "meta_description": meta_desc,
            "definition": lead_definition,
            "key_takeaways": takeaways,
            "sections": sections,
            "bottom_line": bottom_line.strip()
        }

    def fetch_term_detail(self, term_dict: Dict) -> Dict:
        url = term_dict["url"]
        self._sleep_polite()
        html = self.fetch_page(url)
        if not html:
            term_dict["definition"] = ""
            term_dict["key_takeaways"] = []
            term_dict["sections"] = []
            term_dict["bottom_line"] = ""
            return term_dict

        details = self.parse_full_term_content(html)
        term_dict.update(details)
        return term_dict

    def run(self) -> List[Dict]:
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
                self.logger.info(f"[{idx}/{len(letters_order)}] Scraping letter '{letter_key}'...")
                self._sleep_polite()

                sub_html = self.fetch_page(letter_url)
                if not sub_html:
                    continue

                sub_terms = self.parse_letter_page(sub_html, letter_key)
                self.terms.extend(sub_terms)

        if self.config.max_terms:
            self.terms = self.terms[:self.config.max_terms]

        if self.config.fetch_details and not self.interrupted:
            total = len(self.terms)
            self.logger.info(f"Fetching complete in-depth content (definition, takeaways, full sections) for {total} terms...")
            for idx, item in enumerate(self.terms, 1):
                if self.interrupted:
                    break
                self.logger.info(f"[{idx}/{total}] Scraping full details: {item['term']}")
                self.fetch_term_detail(item)

        self.logger.info(f"Scraping completed! Total unique terms: {len(self.terms)}")
        self.save_results()
        return self.terms

    def save_results(self):
        if not self.terms:
            return

        prefix = self.config.output_prefix

        if self.config.export_json:
            json_filename = f"{prefix}.json"
            try:
                with open(json_filename, "w", encoding="utf-8") as f:
                    json.dump(self.terms, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Saved {len(self.terms)} terms to JSON: [ {json_filename} ]")
            except Exception as e:
                self.logger.error(f"Failed to write JSON: {e}")

        if self.config.export_csv:
            csv_filename = f"{prefix}.csv"
            try:
                keys = ["letter", "term", "url", "slug", "source"]
                if self.config.fetch_details:
                    keys += ["definition", "key_takeaways", "bottom_line"]

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


def parse_arguments() -> ScraperConfig:
    parser = argparse.ArgumentParser(
        description="Deep, accurate, graceful & silent scraper for Investopedia Financial Terms Dictionary."
    )
    parser.add_argument("--mode", choices=["hub", "all"], default="hub")
    parser.add_argument("-o", "--output", default="investopedia_terms")
    parser.add_argument("--format", choices=["json", "csv", "both"], default="both")
    parser.add_argument("--with-details", action="store_true", help="Fetch complete definitions, takeaways, and full in-depth sections for every term.")
    parser.add_argument("--delay-min", type=float, default=0.8)
    parser.add_argument("--delay-max", type=float, default=2.0)
    parser.add_argument("--max-terms", type=int, default=None)
    parser.add_argument("-q", "--quiet", action="store_true")

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
