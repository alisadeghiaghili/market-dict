#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
MarketDict: Full Alphabet Continuous Ingestion & Translation Engine
=============================================================================
Iterates through all 6,106 Investopedia terms across all 27 letters (#, A-Z),
scrapes complete in-depth content (Definition, Takeaways, Table of Contents
Sections, Bottom Line) while preserving internal term cross-links converted
to internal application links (<a class="internal-term-link" ...>),
translates to fluent Persian, and updates bilingual_dictionary.json continuously.
=============================================================================
"""

import os
os.environ["translators_default_region"] = "EN"

import sys
import re
import time
import json
import random
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] beautifulsoup4 is required.", file=sys.stderr)
    sys.exit(1)

try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

try:
    import translators as ts
except ImportError:
    print("[ERROR] translators is required.", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Pipeline")

CATALOG_FILE = "all_investopedia_terms_catalog.json"
DICT_FILE = "bilingual_dictionary.json"
CACHE_FILE = "translation_cache.json"

# Load translation cache
logger.info(f"Loading translation cache from {CACHE_FILE}...")
try:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
except Exception:
    cache = {}
logger.info(f"Loaded {len(cache)} cached translations.")

def is_mostly_english(text: str) -> bool:
    if not text:
        return False
    # Strip HTML tags before checking character distribution
    clean = re.sub(r"<[^>]+>", "", text)
    en_chars = len(re.findall(r"[A-Za-z]", clean))
    fa_chars = len(re.findall(r"[\u0600-\u06FF]", clean))
    total = en_chars + fa_chars
    return total > 0 and (en_chars / total > 0.5)

def tr(text: str) -> str:
    """Translates text with cache and multi-provider fallback, preserving HTML tags."""
    if not text or not text.strip():
        return ""
    cleaned = text.strip()
    if cleaned in cache and not is_mostly_english(cache[cleaned]):
        return cache[cleaned]

    # Provider 1: Google (best at keeping HTML tags unchanged)
    try:
        time.sleep(0.05)
        res = ts.translate_text(cleaned, translator="google", from_language="en", to_language="fa")
        if res and not is_mostly_english(res):
            cache[cleaned] = res
            return res
    except Exception:
        pass

    # Provider 2: Bing
    try:
        time.sleep(0.05)
        res = ts.translate_text(cleaned, translator="bing", from_language="en", to_language="fa")
        if res and not is_mostly_english(res):
            cache[cleaned] = res
            return res
    except Exception:
        pass

    # Provider 3: Alibaba
    try:
        time.sleep(0.05)
        res = ts.translate_text(cleaned, translator="alibaba", from_language="en", to_language="fa")
        if res and not is_mostly_english(res):
            cache[cleaned] = res
            return res
    except Exception:
        pass

    return cleaned

def tr_chunks(texts: List[str]) -> List[str]:
    """Translates a list of texts by batching them with double newlines to minimize network requests."""
    if not texts:
        return []

    results = []
    uncached = []
    for idx, t in enumerate(texts):
        c = t.strip()
        if c in cache and not is_mostly_english(cache[c]):
            results.append(cache[c])
        else:
            results.append(None)
            uncached.append((idx, c))

    if not uncached:
        return results

    combined = "\n\n".join([u[1] for u in uncached])
    trans = tr(combined)
    parts = [p.strip() for p in trans.split("\n\n")]

    if len(parts) == len(uncached):
        for (idx, orig), p in zip(uncached, parts):
            results[idx] = p
            cache[orig] = p
    else:
        # Fallback to per-item translation if part count diverges
        for idx, orig in uncached:
            r = tr(orig)
            results[idx] = r
            cache[orig] = r

    return [r if r is not None else "" for r in results]

def clean_element_html(el) -> str:
    """
    Cleans an HTML element (p, li) by:
    1. Removing unwanted tags (scripts, styles, figures, buttons, ads)
    2. Converting internal Investopedia /terms/ links into internal app links:
       <a href="#term/{slug}" class="internal-term-link" data-slug="{slug}">{text}</a>
    3. Unwrapping external links to avoid taking users out of the dictionary.
    4. Normalizing whitespace.
    """
    for bad in el.find_all(["script", "style", "figure", "img", "button", "svg", "iframe", "form"]):
        bad.decompose()

    for a in el.find_all("a"):
        href = a.get("href", "")
        if "/terms/" in href:
            m = re.search(r"/terms/(?:[a-z0-9#]/)?([^/?#]+?)(?:\.asp)?$", href.lower())
            if m:
                slug = m.group(1).replace(".asp", "")
                a.attrs = {
                    "href": f"#term/{slug}",
                    "class": "internal-term-link",
                    "data-slug": slug
                }
                continue
        a.unwrap()

    raw = "".join(str(c) for c in el.contents).strip()
    return re.sub(r"\s+", " ", raw)

def classify_category(title: str, text: str) -> str:
    content = (title + " " + text).lower()
    if any(k in content for k in ["crypto", "bitcoin", "blockchain", "token", "wallet", "nft", "protocol", "ethereum", "mining"]):
        return "ارزهای دیجیتال و فین‌تک"
    if any(k in content for k in ["option", "future", "derivative", "swap", "spread", "open interest", "call option", "put option", "gamma", "delta"]):
        return "ابزارهای مشتقه و آپشن"
    if any(k in content for k in ["bond", "treasury", "yield", "coupon", "debt security", "fixed-income", "mortgage-backed"]):
        return "اوراق بدهی و اسناد خزانه"
    if any(k in content for k in ["technical analysis", "moving average", "candlestick", "stochastic", "oscillator", "bollinger", "rsi", "macd"]):
        return "تحلیل تکنیکال و نموداری"
    if any(k in content for k in ["valuation", "discounted cash flow", "p/e ratio", "intrinsic value", "dcf", "multiple"]):
        return "ارزش‌گذاری و تحلیل بنیادی"
    if any(k in content for k in ["accounting", "balance sheet", "depreciation", "gaap", "ebitda", "income statement", "audit", "cogs", "inventory"]):
        return "حسابداری و صورت‌های مالی"
    if any(k in content for k in ["inflation", "gdp", "macroeconomic", "monetary policy", "unemployment", "fiscal policy", "central bank", "stimulus"]):
        return "اقتصاد کلان و سیاست پولی"
    if any(k in content for k in ["bank", "loan", "mortgage", "credit", "interest rate", "lender", "deposit", "ach", "cofi"]):
        return "بانکداری، وام و اعتبارات"
    if any(k in content for k in ["insurance", "risk management", "annuity", "underwriting", "actuarial", "coverage", "policyholder"]):
        return "مدیریت ریسک و بیمه"
    if any(k in content for k in ["etf", "mutual fund", "portfolio", "index fund", "hedge fund", "reit", "asset management"]):
        return "سرمایه‌گذاری و صندوق‌ها"
    if any(k in content for k in ["tax", "irs", "sec rule", "regulation", "compliance", "form 1040", "statutory", "legal"]):
        return "مالیات، مقررات و قوانین"
    if any(k in content for k in ["tariff", "forex", "currency", "export", "import", "exchange rate", "trade agreement", "wto"]):
        return "تجارت بین‌الملل و بازرگانی"
    if any(k in content for k in ["stock", "share", "dividend", "trading", "equities", "ipo", "nasdaq", "nyse", "market maker"]):
        return "بازار سهام و معاملات"
    return "کسب‌وکار و مدیریت استراتژیک"

def fetch_page_with_retry(url: str, session=None, max_retries=2) -> Optional[str]:
    """Dual-layer ultra-fast fetcher using system curl.exe with curl_cffi fallback."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    # 1. Primary: System curl.exe with HTTP/2 and Brotli/Gzip decompression
    for attempt in range(max_retries):
        try:
            cmd = [
                "curl.exe", "--compressed", "-s", "--max-time", "15",
                "-H", f"User-Agent: {headers['User-Agent']}",
                "-H", f"Accept: {headers['Accept']}",
                "-H", f"Accept-Language: {headers['Accept-Language']}",
                "-H", f"Referer: {headers['Referer']}",
                url
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", timeout=18)
            if res.returncode == 0 and len(res.stdout) > 5000:
                return res.stdout
        except Exception:
            pass
        time.sleep(0.5)

    # 2. Secondary fallback: curl_cffi with edge101 impersonation
    if HAS_CURL_CFFI:
        try:
            resp = cffi_requests.get(url, impersonate="edge101", headers=headers, timeout=12)
            if resp.status_code == 200 and len(resp.text) > 5000:
                return resp.text
        except Exception:
            pass

    return None

def parse_and_enrich_term(item: Dict, session=None) -> Optional[Dict]:
    url = item["url"]
    html = fetch_page_with_retry(url, session)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("div", class_="article-body-content") or soup.find("div", id="article-body_1-0") or soup

    # 1. Lead definition (with link preservation)
    lead = []
    for p in body.find_all("p", recursive=True):
        cleaned = clean_element_html(p)
        if len(cleaned) > 25 and not any(skip in cleaned for skip in [
            "Investopedia /", "Fact checked by", "Get personalized", "Our team of vetted", "Subscribe to"
        ]):
            lead.append(cleaned)
            if len(lead) >= 2:
                break
    def_en = "\n\n".join(lead)

    # 2. Key Takeaways
    takeaways_en = []
    callout = soup.find(class_=lambda c: c and any(k in str(c).lower() for k in ["callout", "takeaway", "whatyouneedtoknow"]))
    if callout:
        for li in callout.find_all("li"):
            litxt = clean_element_html(li)
            if litxt and len(litxt) > 5:
                takeaways_en.append(litxt)

    # 3. Sections
    sections = []
    current_sec = None
    bottom_line_en = ""

    for el in body.children:
        if not hasattr(el, "name") or not el.name:
            continue
        h = el if el.name in ["h2", "h3"] else el.find(["h2", "h3"])
        if h:
            htitle = h.get_text(strip=True)
            if not any(skip in htitle.lower() for skip in ["key takeaways", "related articles", "article sources", "trending", "newsletter"]):
                if current_sec and (current_sec["paragraphs_en"] or current_sec["items_en"]):
                    sections.append(current_sec)
                current_sec = {
                    "title_en": htitle,
                    "title_fa": tr(htitle),
                    "paragraphs_en": [],
                    "paragraphs_fa": [],
                    "items_en": [],
                    "items_fa": []
                }
        ps = el.find_all("p") if el.name != "p" else [el]
        for p in ps:
            ptxt = clean_element_html(p)
            if len(ptxt) > 20 and not any(skip in ptxt for skip in [
                "Investopedia /", "Fact checked by", "Get personalized", "Our team of vetted", "Subscribe to"
            ]):
                if current_sec:
                    current_sec["paragraphs_en"].append(ptxt)
                    if "bottom line" in current_sec["title_en"].lower():
                        bottom_line_en += ptxt + " "
        if current_sec:
            for li in el.find_all("li"):
                litxt = clean_element_html(li)
                if litxt and len(litxt) > 5:
                    current_sec["items_en"].append(litxt)

    if current_sec and (current_sec["paragraphs_en"] or current_sec["items_en"]):
        sections.append(current_sec)

    # Batch translate section contents with tr_chunks for high performance
    for sec in sections:
        sec["paragraphs_fa"] = tr_chunks(sec["paragraphs_en"])
        sec["items_fa"] = tr_chunks(sec["items_en"])

    term_en = item.get("term_en") or item.get("term", "")
    slug = item.get("slug") or url.rstrip("/").split("/")[-1].replace(".asp", "").lower()
    term_fa_raw = tr(term_en)
    term_fa = f"{term_fa_raw} ({term_en})" if term_en not in term_fa_raw and len(term_en) <= 30 else term_fa_raw
    category = classify_category(term_en, def_en)

    return {
        "letter": item.get("letter", "OTHER"),
        "category": category,
        "term_en": term_en,
        "term_fa": term_fa,
        "slug": slug,
        "url": url,
        "definition_en": def_en,
        "definition_fa": tr(def_en),
        "takeaways_en": takeaways_en,
        "takeaways_fa": tr_chunks(takeaways_en),
        "bottom_line_en": bottom_line_en.strip(),
        "bottom_line_fa": tr(bottom_line_en.strip()) if bottom_line_en.strip() else "",
        "sections": sections,
        "deep_enriched": True
    }

def run_pipeline(batch_limit=None, letters_filter=None):
    logger.info("Starting Full Alphabet Continuous Ingestion Engine...")

    with open(DICT_FILE, "r", encoding="utf-8") as f:
        dict_data = json.load(f)

    logger.info(f"Existing terms in dictionary: {len(dict_data)}")

    # Identify terms requiring deep TOC section enrichment
    unenriched_terms = [t for t in dict_data if not t.get("deep_enriched") or not t.get("sections")]

    if letters_filter:
        letters_filter = [l.strip().upper() for l in letters_filter]
        unenriched_terms = [t for t in unenriched_terms if t.get("letter", "").upper() in letters_filter]

    if batch_limit:
        unenriched_terms = unenriched_terms[:batch_limit]

    total_to_process = len(unenriched_terms)
    logger.info(f"Total terms queued for deep enrichment: {total_to_process}")

    if total_to_process == 0:
        logger.info("All terms in the dictionary are 100% deep enriched with TOC sections!")
        return

    # Map by id / url for fast in-place update
    dict_map = {t.get("url"): t for t in dict_data if t.get("url")}

    enriched_count = 0
    t0 = time.time()

    for idx, item in enumerate(unenriched_terms, 1):
        try:
            target_url = item.get("url")
            term_obj = parse_and_enrich_term(item)
            if term_obj and target_url in dict_map:
                target_entry = dict_map[target_url]
                target_entry["definition_en"] = term_obj["definition_en"]
                target_entry["definition_fa"] = term_obj["definition_fa"]
                target_entry["takeaways_en"] = term_obj["takeaways_en"]
                target_entry["takeaways_fa"] = term_obj["takeaways_fa"]
                target_entry["bottom_line_en"] = term_obj.get("bottom_line_en", "")
                target_entry["bottom_line_fa"] = term_obj.get("bottom_line_fa", "")
                target_entry["sections"] = term_obj["sections"]
                target_entry["deep_enriched"] = True
                if term_obj.get("category"):
                    target_entry["category"] = term_obj["category"]

                enriched_count += 1
                logger.info(f"[{idx}/{total_to_process}] Enriched: {term_obj['term_en']} -> {term_obj['term_fa']} ({len(term_obj['sections'])} sections, slug: {term_obj['slug']})")

            # Save incrementally every 5 terms
            if enriched_count > 0 and (enriched_count % 5 == 0 or idx == total_to_process):
                with open(DICT_FILE, "w", encoding="utf-8") as f:
                    json.dump(dict_data, f, ensure_ascii=False, indent=2)

                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump(cache, f, ensure_ascii=False, indent=2)

                elapsed = time.time() - t0
                rate = enriched_count / max(elapsed, 0.1)
                logger.info(f"--- Checkpoint saved: {enriched_count} terms enriched ({rate:.2f} terms/sec) ---")

        except Exception as e:
            logger.error(f"Error processing {item.get('term_en', item.get('term'))}: {e}")

    logger.info(f"Pipeline run finished! Successfully enriched {enriched_count} terms.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Limit number of terms to process in this run")
    parser.add_argument("--letters", type=str, default=None, help="Comma-separated letters to process e.g. 'O,Z,#'")
    args = parser.parse_args()

    letters = args.letters.split(",") if args.letters else None
    run_pipeline(batch_limit=args.limit, letters_filter=letters)
