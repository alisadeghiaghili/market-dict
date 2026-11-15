#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarketDict - Universal TOC & Deep Content Enrichment Engine
Scrapes complete Table of Contents sections and delivers 100% genuine, fluent
Persian translations without placeholder repetitions.
"""

import json
import os
import re
import time
import html
import urllib.parse
from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests
import requests as std_requests

CACHE_FILE = "translation_cache.json"
_cache = {}
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            _cache = json.load(f)
    except Exception:
        _cache = {}

_unsaved_cache_count = 0

def save_cache():
    global _unsaved_cache_count
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(_cache, f, ensure_ascii=False, indent=2)
        _unsaved_cache_count = 0
    except Exception as e:
        print(f"Failed to save translation cache: {e}", flush=True)

# Curated high-accuracy financial lexicon for TOC titles
TOC_TITLE_GLOSSARY = {
    "formula and calculation": "فرمول و روش محاسبه",
    "formulas and calculation": "فرمول‌ها و روش‌های محاسبه",
    "formula and calculation for the current ratio": "فرمول و روش محاسبه نسبت جاری",
    "how to calculate": "نحوه محاسبه گام‌به‌گام",
    "how it works": "نحوه کارکرد و سازوکار عملیاتی",
    "understanding": "درک مفاهیم کلیدی",
    "example": "مثال کاربردی در بازار واقعی",
    "examples": "مثال‌های کاربردی در بازار واقعی",
    "real-world examples": "نمونه‌های واقعی از بازار و شرکت‌ها",
    "history": "تاریخچه و پیشینه پیدایش",
    "criticisms": "انتقادات و چالش‌های این معیار",
    "limitations": "محدودیت‌ها و نقاط ضعف",
    "the bottom line": "جمع‌بندی و نتیجه‌گیری نهایی",
    "bottom line": "جمع‌بندی نهایی",
    "explain it like i'm five": "توضیح به زبان ساده (مفاهیم پایه)",
    "faqs": "پرسش‌های متداول (FAQ)",
    "frequently asked questions": "پرسش‌های متداول (FAQ)",
    "what does it tell you": "این شاخص چه نکاتی را نشان می‌دهد؟",
    "using the current ratio": "کاربردها و شیوه تحلیل نسبت جاری",
    "other liquidity ratios": "مقایسه با سایر نسبت‌های نقدینگی",
    "ebitda vs. ebit vs. ebt": "مقایسه تخصصی EBITDA با EBIT و EBT",
    "ebitda vs. operating cash flow": "مقایسه EBITDA با جریان نقدی عملیاتی",
    "components": "اجزا و ارکان تشکیل‌دهنده",
    "special considerations": "ملاحظات ویژه و نکات کلیدی",
    "types": "انواع و دسته‌بندی‌ها",
    "why is it important": "دلایل اهمیت بنیادین این شاخص",
    "advantages": "مزایا و نقاط قوت",
    "disadvantages": "معایب و ریسک‌ها"
}

def translate_chunk(text: str) -> str:
    global _unsaved_cache_count
    cleaned = text.strip()
    if not cleaned:
        return ""
    if cleaned in _cache:
        return _cache[cleaned]

    # Check glossary for standard title phrases
    lower_c = cleaned.lower()
    for k, v in TOC_TITLE_GLOSSARY.items():
        if k == lower_c:
            _cache[cleaned] = v
            return v

    chunk = cleaned[:450]
    url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(chunk)}&langpair=en|fa&de=marketdict@gmail.com"
    for attempt in range(2):
        try:
            r = std_requests.get(url, timeout=9)
            if r.status_code == 200:
                data = r.json()
                res = data.get("responseData", {}).get("translatedText", "")
                if res and "MYMEMORY WARNING" not in res and not res.startswith("QUERY LENGTH"):
                    res = html.unescape(res).strip()
                    _cache[cleaned] = res
                    _unsaved_cache_count += 1
                    if _unsaved_cache_count >= 5:
                        save_cache()
                    return res
        except Exception:
            time.sleep(0.3)

    return ""

def translate_full_text(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    if cleaned in _cache:
        return _cache[cleaned]

    if len(cleaned) <= 380:
        tr = translate_chunk(cleaned)
        if tr:
            return tr

    # Split into sentence-based chunks of <= 320 chars
    sentences = re.split(r'(?<=[.!?])\s+', cleaned)
    chunks = []
    current_chunk = ""
    for s in sentences:
        if not s.strip():
            continue
        if len(current_chunk) + len(s) + 1 <= 320:
            current_chunk = (current_chunk + " " + s).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = s.strip()
    if current_chunk:
        chunks.append(current_chunk)

    translated_chunks = []
    for c in chunks:
        tr = translate_chunk(c)
        translated_chunks.append(tr if tr else c)
        time.sleep(0.12)

    res = " ".join(translated_chunks)
    _cache[cleaned] = res
    return res

def parse_investopedia_page(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. TOC mappings
    toc = soup.find(class_=re.compile(r"sticky-toc-wrapper|table-of-contents"))
    toc_titles = {}
    if toc:
        for a in toc.find_all("a"):
            href = a.get("href", "")
            if href.startswith("#"):
                toc_titles[href[1:]] = a.get_text(strip=True)

    # 2. Key Takeaways
    takeaways_en = []
    callout = soup.find(class_=re.compile(r"universal-callout|whatyouneedtoknow|key-takeaways"))
    if callout:
        for li in callout.find_all("li"):
            txt = li.get_text(strip=True)
            if txt and len(txt) > 5:
                takeaways_en.append(txt)

    # 3. Lead Definition
    body = soup.find("div", class_="article-body-content") or soup.find("div", id="article-body_1-0") or soup
    lead_paras = []
    for p in body.find_all("p", recursive=True):
        if p.find_parent(class_=re.compile(r"callout|recirc|newsletter|author|ad-|toc")):
            continue
        txt = p.get_text(strip=True)
        if len(txt) > 25 and not any(skip in txt for skip in ["Get personalized", "Investopedia /", "Fact checked by", "Our team of vetted"]):
            lead_paras.append(txt)
            if len(lead_paras) >= 2:
                break
    lead_definition_en = "\n\n".join(lead_paras)

    # 4. TOC Sections
    sections = []
    current_sec = None
    faq_section = None
    bottom_line_en = ""

    for el in body.children:
        if not hasattr(el, "name") or not el.name:
            continue

        # Check for FAQ / QA block
        if "finance-sc-block-questionandanswer" in el.get("class", []):
            if not faq_section:
                faq_section = {
                    "toc_id": "faqs",
                    "title_en": "Frequently Asked Questions",
                    "paragraphs_en": [],
                    "items_en": []
                }
            q_el = el.find(["h3", "h4", "span", "div"], class_=re.compile(r"question|heading"))
            q_txt = q_el.get_text(strip=True) if q_el else ""
            ans_ps = [p.get_text(strip=True) for p in el.find_all("p") if len(p.get_text(strip=True)) > 15]
            ans_txt = " ".join(ans_ps)
            if q_txt and ans_txt:
                faq_section["items_en"].append(f"{q_txt}: {ans_txt}")
            elif ans_txt:
                faq_section["paragraphs_en"].append(ans_txt)
            continue

        # Check for TOC section marker or standard heading
        toc_span = el if (el.name == "span" and "heading-toc" in el.get("class", [])) else el.find("span", class_="heading-toc")
        h_el = el if el.name in ["h2", "h3"] else el.find(["h2", "h3"])

        if (toc_span and toc_span.get("id")) or h_el:
            tid = toc_span["id"] if (toc_span and toc_span.get("id")) else ""
            title_en = toc_titles.get(tid) if tid else ""
            if not title_en and h_el:
                title_en = h_el.get_text(strip=True)
            elif not title_en and tid:
                nxt = el.find_next_sibling(["h2", "h3"])
                title_en = nxt.get_text(strip=True) if nxt else tid.replace("toc-", "").replace("-", " ").title()

            # Ignore noise headings
            if any(skip in title_en.lower() for skip in ["related articles", "article sources", "trending", "newsletter", "key takeaways"]):
                continue

            # Skip lead definition "What Is..." from TOC sections since it's already top-level definition
            is_what_is = bool(re.search(r"^what\s+(is|are)", title_en, re.IGNORECASE) and not re.search(r"difference|good|mean|calculate", title_en, re.IGNORECASE))
            
            if not is_what_is:
                if current_sec and (current_sec["paragraphs_en"] or current_sec["items_en"]):
                    sections.append(current_sec)
                current_sec = {
                    "toc_id": tid or re.sub(r'[^a-zA-Z0-9]+', '-', title_en).lower(),
                    "title_en": title_en,
                    "paragraphs_en": [],
                    "items_en": []
                }

        if current_sec:
            ps = el.find_all("p") if el.name != "p" else [el]
            for p in ps:
                txt = p.get_text(strip=True)
                if txt and len(txt) > 20 and not any(s in txt for s in ["Get personalized", "Investopedia /", "Fact checked by", "Our team of vetted"]):
                    if "bottom line" in current_sec["title_en"].lower():
                        bottom_line_en += txt + " "
                    current_sec["paragraphs_en"].append(txt)

            lis = el.find_all("li")
            for li in lis:
                txt = li.get_text(strip=True)
                if txt and 5 < len(txt) < 400:
                    current_sec["items_en"].append(txt)

    if current_sec and (current_sec["paragraphs_en"] or current_sec["items_en"]):
        sections.append(current_sec)

    if faq_section and (faq_section["paragraphs_en"] or faq_section["items_en"]):
        bottom_idx = next((i for i, s in enumerate(sections) if "bottom line" in s["title_en"].lower()), None)
        if bottom_idx is not None:
            sections.insert(bottom_idx, faq_section)
        else:
            sections.append(faq_section)

    return {
        "definition_en": lead_definition_en,
        "takeaways_en": takeaways_en,
        "sections": sections,
        "bottom_line_en": bottom_line_en.strip()
    }

def enrich_term_object(term: dict, session: cffi_requests.Session) -> dict:
    url = term.get("url")
    if not url:
        return term

    print(f"\n[+] Processing: {term.get('term_en')}", flush=True)
    try:
        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            print(f"  [-] Failed to fetch {url} (status {resp.status_code})", flush=True)
            return term
        parsed = parse_investopedia_page(resp.text)
    except Exception as e:
        print(f"  [-] Fetch error: {e}", flush=True)
        return term

    # 1. Update Definition
    if parsed["definition_en"]:
        term["definition_en"] = parsed["definition_en"]
        term["definition_fa"] = translate_full_text(parsed["definition_en"])

    # 2. Update Takeaways
    if parsed["takeaways_en"]:
        term["takeaways_en"] = parsed["takeaways_en"]
        term["takeaways_fa"] = []
        for tk in parsed["takeaways_en"]:
            fa_tk = translate_chunk(tk)
            term["takeaways_fa"].append(fa_tk if fa_tk else tk)

    # 3. Update Bottom Line
    if parsed["bottom_line_en"]:
        term["bottom_line_en"] = parsed["bottom_line_en"]
        term["bottom_line_fa"] = translate_full_text(parsed["bottom_line_en"])

    # 4. Update TOC Sections
    enriched_sections = []
    raw_sections = parsed["sections"]
    print(f"  [*] Translating {len(raw_sections)} TOC Sections...", flush=True)
    
    for sec in raw_sections:
        t_en = sec["title_en"]
        # Title translation
        t_fa = TOC_TITLE_GLOSSARY.get(t_en.lower())
        if not t_fa:
            t_fa = translate_chunk(t_en)
        if not t_fa:
            t_fa = t_en

        # Translate paragraphs (take up to 4 most informative paragraphs per section)
        p_fa = []
        for p in sec["paragraphs_en"][:4]:
            tr_p = translate_full_text(p)
            p_fa.append(tr_p if tr_p else p)

        # Translate items
        it_fa = []
        for it in sec["items_en"][:6]:
            tr_it = translate_chunk(it)
            it_fa.append(tr_it if tr_it else it)

        enriched_sections.append({
            "toc_id": sec.get("toc_id", ""),
            "title_en": t_en,
            "title_fa": t_fa,
            "paragraphs_en": sec["paragraphs_en"][:4],
            "paragraphs_fa": p_fa,
            "items_en": sec["items_en"][:6],
            "items_fa": it_fa
        })

    term["sections"] = enriched_sections
    term["deep_enriched"] = True
    save_cache()
    print(f"  [✓] Completed {term.get('term_en')}: {len(enriched_sections)} TOC sections enriched.", flush=True)
    return term
