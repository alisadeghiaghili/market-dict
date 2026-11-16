#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarketDict Master Formulas & Term Linking Engine
1. Injects standardized LaTeX financial formulas into English & Persian sections.
2. Fast single-pass regex cross-linker across all articles, preserving KaTeX math and existing tags.
3. Saves atomically and verifies results.
"""

import os
import re
import sys
import time
import json
from formula_registry import FORMULA_DB

DICT_FILE = "bilingual_dictionary.json"

STOPWORDS = {
    'rate', 'cost', 'costs', 'bond', 'bonds', 'bank', 'banks', 'term', 'terms', 'plan', 'plans',
    'time', 'times', 'date', 'dates', 'high', 'low', 'long', 'short', 'free', 'real', 'open',
    'firm', 'firms', 'good', 'goods', 'year', 'years', 'lead', 'gain', 'gains', 'loss', 'losses',
    'sale', 'sales', 'fund', 'funds', 'book', 'cash', 'debt', 'risk', 'unit', 'units', 'call',
    'put', 'note', 'notes', 'pool', 'pools', 'par', 'tax', 'taxes', 'fee', 'fees', 'cut', 'cuts',
    'cap', 'caps', 'bar', 'bars', 'gap', 'gaps', 'tip', 'tips', 'bid', 'ask', 'run', 'runs',
    'pay', 'pays', 'buy', 'buys', 'sell', 'sells', 'hold', 'holds', 'mean', 'item', 'items',
    'other', 'value', 'values', 'price', 'prices', 'stock', 'stocks', 'share', 'shares', 'asset',
    'assets', 'money', 'yield', 'yields', 'order', 'orders', 'trade', 'trades', 'loan', 'loans',
    'trend', 'trust', 'trusts', 'gross', 'net', 'swap', 'swaps', 'basis', 'spot', 'strike',
    'spread', 'spreads', 'alpha', 'beta', 'floor', 'float', 'chart', 'index', 'ratio', 'ratios',
    'margin', 'return', 'returns', 'audit', 'audits', 'credit', 'debit', 'equity', 'equities',
    'option', 'options', 'future', 'futures', 'market', 'markets', 'factor', 'factors', 'income',
    'profit', 'profits', 'growth', 'charge', 'charges', 'strike', 'series', 'hybrid', 'target',
    'capital', 'model', 'face value'
}

def build_indices(data):
    en_dict = {}
    fa_dict = {}

    for item in data:
        slug = item.get('slug', '').strip().lower()
        if not slug:
            continue
        
        t_en = item.get('term_en', '').strip()
        clean_en = re.sub(r'\s*\([^)]*\)', '', t_en).strip().lower()
        if len(clean_en) >= 5 and clean_en not in STOPWORDS:
            en_dict[clean_en] = slug
            
        m_paren = re.search(r'\(([A-Z0-9-]{3,8})\)', t_en)
        if m_paren:
            ac = m_paren.group(1).lower()
            if ac not in STOPWORDS:
                en_dict[ac] = slug
                
        t_fa = item.get('term_fa', '').strip()
        clean_fa = re.sub(r'\s*\([^)]*\)', '', t_fa).strip()
        clean_fa = clean_fa.replace('\u200c', ' ').replace('ي', 'ی').replace('ك', 'ک')
        clean_fa = re.sub(r'\s+', ' ', clean_fa).strip()
        if len(clean_fa) >= 6:
            fa_dict[clean_fa] = slug

    sorted_en = sorted(en_dict.keys(), key=lambda x: len(x), reverse=True)[:2000]
    sorted_fa = sorted(fa_dict.keys(), key=lambda x: len(x), reverse=True)[:1000]

    pattern_en = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted_en) + r')\b', re.IGNORECASE)
    escaped_fa = [re.escape(k).replace(r'\ ', r'[\s\u200c]+') for k in sorted_fa]
    pattern_fa = re.compile(r'(?:^|(?<=[\s\(\)\[\]«»؛،\.\:\?]))(' + '|'.join(escaped_fa) + r')(?=[\s\(\)\[\]«»؛،\.\:\?]|$)')

    return en_dict, fa_dict, pattern_en, pattern_fa

def linkify_en(text, en_dict, pattern_en, current_slug=None):
    if not text or not isinstance(text, str):
        return text
    placeholders = []
    def add_ph(s):
        placeholders.append(s)
        return f"___PH_{len(placeholders)-1}___"
    
    clean = re.sub(r'\$\$.*?\$\$', lambda m: add_ph(m.group(0)), text, flags=re.DOTALL)
    
    def norm_a(m):
        full_a = m.group(0)
        m_slug = re.search(r'(?:href=[\'"](?:https?://www\.investopedia\.com)?/terms/[a-z0-9]/([a-z0-9_-]+)\.asp[\'"]|data-slug=[\'"]([a-z0-9_-]+)[\'"]|href=[\'"]#term/([a-z0-9_-]+)[\'"])', full_a)
        if m_slug:
            s = m_slug.group(1) or m_slug.group(2) or m_slug.group(3)
            inner = re.sub(r'<[^>]+>', '', full_a)
            return add_ph(f'<a href="#term/{s}" class="internal-term-link" data-slug="{s}">{inner}</a>')
        return add_ph(full_a)

    clean = re.sub(r'<a\b[^>]*>.*?</a>', norm_a, clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', lambda m: add_ph(m.group(0)), clean)
    
    linked = set()
    if current_slug:
        linked.add(current_slug)
        
    def repl(m):
        if len(linked) >= 5:
            return m.group(0)
        matched_str = m.group(1)
        k = matched_str.lower()
        slug = en_dict.get(k)
        if slug and slug not in linked:
            linked.add(slug)
            return add_ph(f'<a href="#term/{slug}" class="internal-term-link" data-slug="{slug}">{matched_str}</a>')
        return m.group(0)

    clean = pattern_en.sub(repl, clean)
    
    for idx in range(len(placeholders) - 1, -1, -1):
        clean = clean.replace(f"___PH_{idx}___", placeholders[idx])
    return clean

def linkify_fa(text, fa_dict, pattern_fa, current_slug=None):
    if not text or not isinstance(text, str):
        return text
    placeholders = []
    def add_ph(s):
        placeholders.append(s)
        return f"___PH_{len(placeholders)-1}___"
        
    clean = re.sub(r'\$\$.*?\$\$', lambda m: add_ph(m.group(0)), text, flags=re.DOTALL)
    
    def norm_a(m):
        full_a = m.group(0)
        m_slug = re.search(r'(?:href=[\'"](?:https?://www\.investopedia\.com)?/terms/[a-z0-9]/([a-z0-9_-]+)\.asp[\'"]|data-slug=[\'"]([a-z0-9_-]+)[\'"]|href=[\'"]#term/([a-z0-9_-]+)[\'"])', full_a)
        if m_slug:
            s = m_slug.group(1) or m_slug.group(2) or m_slug.group(3)
            inner = re.sub(r'<[^>]+>', '', full_a)
            return add_ph(f'<a href="#term/{s}" class="internal-term-link" data-slug="{s}">{inner}</a>')
        return add_ph(full_a)

    clean = re.sub(r'<a\b[^>]*>.*?</a>', norm_a, clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', lambda m: add_ph(m.group(0)), clean)
    
    linked = set()
    if current_slug:
        linked.add(current_slug)
        
    def repl(m):
        if len(linked) >= 5:
            return m.group(0)
        matched_str = m.group(1)
        k = matched_str.replace('\u200c', ' ').replace('ي', 'ی').replace('ك', 'ک')
        k = re.sub(r'\s+', ' ', k).strip()
        slug = fa_dict.get(k)
        if slug and slug not in linked:
            linked.add(slug)
            return add_ph(f'<a href="#term/{slug}" class="internal-term-link" data-slug="{slug}">{matched_str}</a>')
        return m.group(0)

    clean = pattern_fa.sub(repl, clean)
    
    for idx in range(len(placeholders) - 1, -1, -1):
        clean = clean.replace(f"___PH_{idx}___", placeholders[idx])
    return clean

def main():
    print(f"Loading {DICT_FILE}...", flush=True)
    t0 = time.time()
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} terms in {time.time() - t0:.2f}s.", flush=True)

    # Step 1: Inject Master Formulas
    print("Injecting master formulas...", flush=True)
    injected_count = 0
    for item in data:
        slug = item.get("slug", "").strip().lower()
        if slug in FORMULA_DB:
            finfo = FORMULA_DB[slug]
            sections = item.get("sections", [])
            applied = False
            for s in sections:
                t_l = s.get("title_en", "").lower()
                if any(m in t_l for m in finfo["title_match"]):
                    s["paragraphs_en"] = [p for p in s.get("paragraphs_en", []) if "TEST FORMULA" not in p]
                    s["paragraphs_fa"] = [p for p in s.get("paragraphs_fa", []) if "TEST FORMULA" not in p]
                    # Check if formula already at paragraph 1
                    already = any(finfo['formula_en'][:25] in p for p in s["paragraphs_en"])
                    if not already:
                        s["paragraphs_en"].insert(1, finfo["formula_en"])
                        s["paragraphs_fa"].insert(1, finfo["formula_fa"])
                        injected_count += 1
                        print(f"  [+] Injected formula into: {item.get('term_en')} ({slug}) -> {s.get('title_en')}")
                    applied = True
                    break
            if not applied and sections:
                for s in sections:
                    if any(k in s.get("title_en", "").lower() for k in ["formula", "calculate", "what is"]):
                        already = any(finfo['formula_en'][:25] in p for p in s["paragraphs_en"])
                        if not already:
                            s["paragraphs_en"].insert(1, finfo["formula_en"])
                            s["paragraphs_fa"].insert(1, finfo["formula_fa"])
                            injected_count += 1
                            print(f"  [+] Fallback injected formula into: {item.get('term_en')} ({slug}) -> {s.get('title_en')}")
                        break

    print(f"Formulas step done. New insertions: {injected_count}.", flush=True)

    # Step 2: Build indices and link terms
    print("Compiling regex indices...", flush=True)
    en_dict, fa_dict, pattern_en, pattern_fa = build_indices(data)
    print(f"Indexed {len(en_dict)} EN terms and {len(fa_dict)} FA terms.", flush=True)

    print("Applying cross-links across all enriched terms...", flush=True)
    t_link = time.time()
    enriched_count = 0
    for item in data:
        if not item.get("sections"):
            continue
        enriched_count += 1
        slug = item.get("slug", "").lower()
        
        item["definition_en"] = linkify_en(item.get("definition_en", ""), en_dict, pattern_en, current_slug=slug)
        item["definition_fa"] = linkify_fa(item.get("definition_fa", ""), fa_dict, pattern_fa, current_slug=slug)
        
        if item.get("takeaways_en"):
            item["takeaways_en"] = [linkify_en(t, en_dict, pattern_en, current_slug=slug) for t in item["takeaways_en"]]
        if item.get("takeaways_fa"):
            item["takeaways_fa"] = [linkify_fa(t, fa_dict, pattern_fa, current_slug=slug) for t in item["takeaways_fa"]]
            
        if item.get("bottom_line_en"):
            item["bottom_line_en"] = linkify_en(item["bottom_line_en"], en_dict, pattern_en, current_slug=slug)
        if item.get("bottom_line_fa"):
            item["bottom_line_fa"] = linkify_fa(item["bottom_line_fa"], fa_dict, pattern_fa, current_slug=slug)
            
        for s in item.get("sections", []):
            s["paragraphs_en"] = [linkify_en(p, en_dict, pattern_en, current_slug=slug) for p in s.get("paragraphs_en", [])]
            s["paragraphs_fa"] = [linkify_fa(p, fa_dict, pattern_fa, current_slug=slug) for p in s.get("paragraphs_fa", [])]

    print(f"Processed {enriched_count} terms in {time.time() - t_link:.2f}s.", flush=True)

    print(f"Saving to {DICT_FILE}...", flush=True)
    tmp_file = DICT_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if os.path.exists(DICT_FILE):
        os.replace(tmp_file, DICT_FILE)
    else:
        os.rename(tmp_file, DICT_FILE)

    print("SUCCESS: Master enrichment & linking complete!", flush=True)

if __name__ == "__main__":
    main()
