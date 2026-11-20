#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Investopedia Financial Terms Dictionary Scraper (Full Alphabet Edition)
=============================================================================
Target: https://www.investopedia.com/financial-term-dictionary-4769738

Traverses every letter page (#, A through Z) to discover and extract all
financial terms across the entire dictionary, capturing complete definitions,
key takeaways, and full Table of Contents sections.

Features:
- Transparent fetching: all requests go through polite_fetcher.PoliteFetcher,
  which identifies the tool honestly, honours robots.txt and Crawl-delay,
  rate-limits per host, and stops when the site refuses automated access.
  Use of fetched content is governed by the source site's terms (DATA_NOTICE.md).
- Full Alphabet Coverage: Crawls all 27 alphabetical subpages (#, A-Z) to
  collect all terms, not just top-level highlights.
- In-Depth Content Extraction:
  * Clean Term Title & Canonical Slug
  * Lead Definition (clean introductory explanation)
  * Key Takeaways (all bullet points from callouts)
  * Table of Contents Sections (Headings, Paragraphs, Lists, FAQs)
  * The Bottom Line summary
- Concurrent & Resilient:
  * Worker threads share one per-host rate limiter, so concurrency never
    raises the request rate above the configured delay.
  * Automatic retry with exponential backoff for transient errors.
  * Incremental checkpointing to save progress and resume interrupted runs.
- Multi-format Export: JSON and CSV with UTF-8 encoding.
=============================================================================
"""

import os
import sys
import re
import time
import json
import csv
import signal
import logging
import argparse
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] 'beautifulsoup4' is required. Run: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

from polite_fetcher import AccessDeniedError, FetcherConfig, PoliteFetcher


# Canonical mapping of all 27 letter subpages on Investopedia
LETTER_SUBPAGES = {
    "#": "https://www.investopedia.com/terms-beginning-with-num-4769350",
    "A": "https://www.investopedia.com/terms-beginning-with-a-4769351",
    "B": "https://www.investopedia.com/terms-beginning-with-b-4769352",
    "C": "https://www.investopedia.com/terms-beginning-with-c-4769353",
    "D": "https://www.investopedia.com/terms-beginning-with-d-4769354",
    "E": "https://www.investopedia.com/terms-beginning-with-e-4769355",
    "F": "https://www.investopedia.com/terms-beginning-with-f-4769356",
    "G": "https://www.investopedia.com/terms-beginning-with-g-4769357",
    "H": "https://www.investopedia.com/terms-beginning-with-h-4769358",
    "I": "https://www.investopedia.com/terms-beginning-with-i-4769359",
    "J": "https://www.investopedia.com/terms-beginning-with-j-4769360",
    "K": "https://www.investopedia.com/terms-beginning-with-k-4769361",
    "L": "https://www.investopedia.com/terms-beginning-with-l-4769362",
    "M": "https://www.investopedia.com/terms-beginning-with-m-4769363",
    "N": "https://www.investopedia.com/terms-beginning-with-n-4769364",
    "O": "https://www.investopedia.com/terms-beginning-with-o-4769365",
    "P": "https://www.investopedia.com/terms-beginning-with-p-4769366",
    "Q": "https://www.investopedia.com/terms-beginning-with-q-4769367",
    "R": "https://www.investopedia.com/terms-beginning-with-r-4769368",
    "S": "https://www.investopedia.com/terms-beginning-with-s-4769369",
    "T": "https://www.investopedia.com/terms-beginning-with-t-4769370",
    "U": "https://www.investopedia.com/terms-beginning-with-u-4769371",
    "V": "https://www.investopedia.com/terms-beginning-with-v-4769372",
    "W": "https://www.investopedia.com/terms-beginning-with-w-4769373",
    "X": "https://www.investopedia.com/terms-beginning-with-x-4769374",
    "Y": "https://www.investopedia.com/terms-beginning-with-y-4769375",
    "Z": "https://www.investopedia.com/terms-beginning-with-z-4769376",
}


@dataclass
class ScraperConfig:
    hub_url: str = "https://www.investopedia.com/financial-term-dictionary-4769738"
    mode: str = "all"  # 'all' (all 27 letters) or 'hub' (top 24 curated only)
    letters: Optional[List[str]] = None  # Specific letters to scrape e.g. ['A', 'B'] or None for all
    output_prefix: str = "investopedia_terms"
    export_json: bool = True
    export_csv: bool = True
    fetch_details: bool = True  # Extract complete definitions, takeaways, and sections
    workers: int = 2
    min_delay: float = 3.0  # seconds between requests to the host; robots.txt Crawl-delay wins if larger
    timeout: int = 25
    max_retries: int = 2
    backoff_factor: float = 2.0
    max_terms: Optional[int] = None
    checkpoint_interval: int = 25
    quiet: bool = False
    log_level: int = logging.INFO


class InvestopediaScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.terms: List[Dict] = []
        self.seen_urls: Set[str] = set()
        self.interrupted: bool = False
        self.checkpoint_file = f"{self.config.output_prefix}_checkpoint.json"
        self.fetcher = PoliteFetcher(FetcherConfig(
            min_delay_seconds=self.config.min_delay,
            timeout_seconds=self.config.timeout,
            max_retries=self.config.max_retries,
            backoff_factor=self.config.backoff_factor,
        ))

        self._setup_logging()
        self._setup_signals()

    def _setup_logging(self):
        self.logger = logging.getLogger("InvestopediaScraper")
        self.logger.setLevel(logging.ERROR if self.config.quiet else self.config.log_level)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def _setup_signals(self):
        def handle_signal(sig, frame):
            self.logger.warning("\n[!] Interrupt signal received (Ctrl+C). Gracefully saving progress...")
            self.interrupted = True

        signal.signal(signal.SIGINT, handle_signal)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, handle_signal)

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page through the shared polite fetcher.

        Args:
            url: Absolute page URL.

        Returns:
            The page HTML, or ``None`` if it could not be fetched. When the site
            refuses automated access the run is stopped gracefully (progress is
            checkpointed) instead of retrying with a disguised client.
        """
        if self.interrupted:
            return None
        try:
            return self.fetcher.get(url)
        except AccessDeniedError as exc:
            self.logger.error(f"Access refused, stopping run: {exc}")
            self.interrupted = True
            return None

    def parse_letter_page(self, html: str, letter: str) -> List[Dict]:
        """
        Parses an alphabetical letter page (e.g. terms-beginning-with-a-4769351)
        and extracts ALL term links under that letter.
        """
        soup = BeautifulSoup(html, "html.parser")
        letter_terms = []

        # Find all anchors that link to individual /terms/ pages
        for a in soup.find_all("a", href=True):
            href = a.get("href", "").strip()
            if "/terms/" not in href or href.endswith("/terms/") or "terms-beginning-with-" in href:
                continue

            if href.startswith("/"):
                href = "https://www.investopedia.com" + href

            term_title = a.get_text(strip=True)
            if not term_title or len(term_title) < 2:
                continue

            # Canonical URL without hash or query
            clean_url = href.split("#")[0].split("?")[0]

            if clean_url not in self.seen_urls:
                self.seen_urls.add(clean_url)
                slug = clean_url.rstrip("/").split("/")[-1].replace(".asp", "")
                letter_terms.append({
                    "letter": letter,
                    "term": term_title,
                    "url": clean_url,
                    "slug": slug,
                    "source": f"letter_{letter}"
                })

        return letter_terms

    def parse_full_term_content(self, html: str) -> Dict:
        """
        Extracts ALL useful information from a term page:
        1. Lead definition (paragraphs before first heading)
        2. Key takeaways (all bullet points)
        3. All in-depth sections mapped to Table of Contents
        4. Bottom line summary
        """
        soup = BeautifulSoup(html, "html.parser")

        # 1. Meta description fallback
        meta_desc = ""
        m = soup.find("meta", attrs={"name": "description"})
        if m and m.get("content"):
            meta_desc = m["content"].strip()

        # 2. Key Takeaways
        takeaways = []
        callout = soup.find(class_=lambda c: c and any(k in str(c).lower() for k in ["callout", "takeaway", "whatyouneedtoknow"]))
        if callout:
            for li in callout.find_all("li"):
                txt = li.get_text(strip=True)
                if txt and len(txt) > 5:
                    takeaways.append(txt)

        # 3. Main article body
        body = soup.find("div", class_="article-body-content") or soup.find("div", id="article-body_1-0") or soup

        lead_paras = []
        first_h_seen = False
        sections = []
        current_sec = None
        bottom_line = ""

        for el in body.children:
            if not hasattr(el, "name") or not el.name:
                continue

            # Check for heading (h2 / h3)
            h = el if el.name in ["h2", "h3"] else el.find(["h2", "h3"])
            if h:
                first_h_seen = True
                htitle = h.get_text(strip=True)
                if not any(skip in htitle.lower() for skip in ["key takeaways", "related articles", "article sources", "trending", "newsletter"]):
                    if current_sec and (current_sec["paragraphs"] or current_sec["items"]):
                        sections.append(current_sec)
                    current_sec = {"title": htitle, "paragraphs": [], "items": []}

            # Collect paragraphs
            ps = el.find_all("p") if el.name != "p" else [el]
            for p in ps:
                ptxt = p.get_text(strip=True)
                if len(ptxt) > 20 and not any(skip in ptxt for skip in [
                    "Investopedia /", "Fact checked by", "Get personalized", "Our team of vetted", "Subscribe to"
                ]):
                    if not first_h_seen:
                        lead_paras.append(ptxt)
                    elif current_sec:
                        current_sec["paragraphs"].append(ptxt)
                        if "bottom line" in current_sec["title"].lower():
                            bottom_line += ptxt + " "

            # Collect list items
            if current_sec:
                for li in el.find_all("li"):
                    litxt = li.get_text(strip=True)
                    if litxt and len(litxt) > 5:
                        current_sec["items"].append(litxt)

        if current_sec and (current_sec["paragraphs"] or current_sec["items"]):
            sections.append(current_sec)

        return {
            "definition": "\n\n".join(lead_paras[:2]) if lead_paras else meta_desc,
            "key_takeaways": takeaways,
            "sections": sections,
            "bottom_line": bottom_line.strip()
        }

    def collect_all_alphabet_terms(self) -> List[Dict]:
        """
        Traverses every letter page (#, A through Z) and builds the master list
        of terms across the entire alphabet.
        """
        target_letters = self.config.letters if self.config.letters else sorted(LETTER_SUBPAGES.keys())
        self.logger.info(f"Targeting {len(target_letters)} letter categories: {target_letters}")

        master_terms = []

        for idx, letter_key in enumerate(target_letters, 1):
            if self.interrupted:
                break

            url = LETTER_SUBPAGES.get(letter_key)
            if not url:
                self.logger.warning(f"No subpage found for letter '{letter_key}'. Skipping.")
                continue

            self.logger.info(f"[{idx}/{len(target_letters)}] Crawling letter '{letter_key}' subpage: {url}")
            html = self.fetch_page(url)
            if not html:
                self.logger.error(f"Failed to fetch letter '{letter_key}' page.")
                continue

            letter_terms = self.parse_letter_page(html, letter_key)
            self.logger.info(f" -> Found {len(letter_terms)} terms under letter '{letter_key}'.")
            master_terms.extend(letter_terms)

        self.logger.info(f"Catalog collection complete. Total unique terms found across letters: {len(master_terms)}")
        return master_terms

    def fetch_term_detail_worker(self, term_dict: Dict) -> Dict:
        """Worker function for concurrent term scraping."""
        html = self.fetch_page(term_dict["url"])
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
        self.logger.info("=" * 70)
        self.logger.info(f"Investopedia Scraper: Starting Alphabet Traversal (mode='{self.config.mode}')")
        self.logger.info("=" * 70)

        # 1. Collect all terms from all letters
        if self.config.mode == "hub":
            self.logger.info(f"Scraping top curated terms from hub: {self.config.hub_url}")
            hub_html = self.fetch_page(self.config.hub_url)
            if not hub_html:
                return []
            hub_terms = self.parse_letter_page(hub_html, "HUB")
            self.terms = hub_terms
        else:
            self.terms = self.collect_all_alphabet_terms()

        if self.config.max_terms:
            self.terms = self.terms[:self.config.max_terms]
            self.logger.info(f"Truncated term list to max_terms: {self.config.max_terms}")

        total_terms = len(self.terms)
        self.logger.info(f"Ready to process {total_terms} terms.")

        # 2. Check if details should be fetched
        if self.config.fetch_details and not self.interrupted:
            self.logger.info(f"Extracting full in-depth content using {self.config.workers} concurrent workers...")
            completed_count = 0
            t_start = time.time()

            with ThreadPoolExecutor(max_workers=self.config.workers) as executor:
                futures = {executor.submit(self.fetch_term_detail_worker, t): t for t in self.terms}

                for future in as_completed(futures):
                    if self.interrupted:
                        self.logger.warning("Interrupt received. Stopping worker pool...")
                        executor.shutdown(wait=False, cancel_futures=True)
                        break

                    try:
                        res = future.result()
                        completed_count += 1
                        if completed_count % 10 == 0 or completed_count == total_terms:
                            elapsed = time.time() - t_start
                            rate = completed_count / max(elapsed, 0.1)
                            self.logger.info(f"[{completed_count}/{total_terms}] terms scraped ({rate:.1f} terms/sec)")

                        # Save checkpoint
                        if completed_count % self.config.checkpoint_interval == 0:
                            self.save_checkpoint()

                    except Exception as e:
                        self.logger.error(f"Worker exception: {e}")

        self.logger.info(f"Scraping finished. Total terms collected: {len(self.terms)}")
        self.save_results()
        return self.terms

    def save_checkpoint(self):
        try:
            with open(self.checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(self.terms, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save checkpoint: {e}")

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
        description="Rate-limited, robots.txt-compliant scraper for the Investopedia Financial Terms Dictionary."
    )
    parser.add_argument("--mode", choices=["all", "hub"], default="all",
                        help="Extraction mode: 'all' crawls every letter page (#, A-Z); 'hub' extracts curated landing terms.")
    parser.add_argument("--letters", type=str, default=None,
                        help="Comma-separated list of letters to scrape (e.g. 'A,B,C' or '#' or 'Z'). Default: all 27 letters.")
    parser.add_argument("-o", "--output", default="investopedia_terms",
                        help="Output filename prefix (default: investopedia_terms).")
    parser.add_argument("--format", choices=["json", "csv", "both"], default="both")
    parser.add_argument("--no-details", action="store_true",
                        help="Quick catalog mode: only extract term titles, URLs, and letters without fetching in-depth article bodies.")
    parser.add_argument("--workers", type=int, default=2,
                        help="Number of worker threads for detail scraping (default: 2). Workers share one per-host rate limit.")
    parser.add_argument("--min-delay", type=float, default=3.0,
                        help="Minimum seconds between requests to the host (default: 3.0). A larger robots.txt Crawl-delay wins.")
    parser.add_argument("--max-terms", type=int, default=None,
                        help="Optional limit on total terms to scrape.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Quiet mode: suppress progress output.")

    args = parser.parse_args()

    letters = None
    if args.letters:
        letters = [l.strip().upper() for l in args.letters.split(",") if l.strip()]

    return ScraperConfig(
        mode=args.mode,
        letters=letters,
        output_prefix=args.output,
        export_json=args.format in ("json", "both"),
        export_csv=args.format in ("csv", "both"),
        fetch_details=not args.no_details,
        workers=args.workers,
        min_delay=args.min_delay,
        max_terms=args.max_terms,
        quiet=args.quiet
    )


def main():
    config = parse_arguments()
    scraper = InvestopediaScraper(config)
    scraper.run()


if __name__ == "__main__":
    main()
