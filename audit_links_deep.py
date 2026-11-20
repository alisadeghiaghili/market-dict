#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Link Auditor for MarketDict
Scans every single term, field, paragraph, list item, and takeaway for internal links.
Validates:
1. Target existence in database (broken link detection).
2. Proper href and data-slug syntax.
3. Self-referential links (a term linking to itself).
4. Malformed / unclosed <a> tags.
5. Nested <a> tags.
6. Links accidentally injected inside $$ KaTeX math blocks.
7. Empty anchor text.
8. External links vs internal links.
9. Link resolution against alias/lookup tables.
"""

import json
import re
from collections import Counter, defaultdict

DICT_FILE = "bilingual_dictionary.json"

print(f"Loading {DICT_FILE}...", flush=True)
with open(DICT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

valid_slugs = {item.get("slug", "").strip().lower(): item for item in data if item.get("slug")}
valid_slug_clean = {re.sub(r"[^a-z0-9]", "", s): s for s in valid_slugs}

print(f"Loaded {len(data)} terms. Total unique valid slugs: {len(valid_slugs)}")

total_links = 0
internal_links_count = 0
external_links_count = 0
broken_links = []
self_links = []
malformed_links = []
nested_links = []
math_broken_links = []
empty_text_links = []
class_mismatch_links = []
target_slug_counts = Counter()
terms_with_links = set()

link_regex = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.DOTALL | re.IGNORECASE)
href_regex = re.compile(r'href=["\']([^"\']*)["\']', re.IGNORECASE)
slug_attr_regex = re.compile(r'data-slug=["\']([^"\']*)["\']', re.IGNORECASE)

def audit_text(text, source_slug, field_name, is_fa=False):
    global total_links, internal_links_count, external_links_count
    if not text or not isinstance(text, str):
        return
    
    # 1. Check for math contamination: $$ ... <a ... </a> ... $$
    math_blocks = re.findall(r"\$\$.*?\$\$", text, flags=re.DOTALL)
    for mb in math_blocks:
        if "<a " in mb.lower():
            math_broken_links.append((source_slug, field_name, mb[:80]))
            
    # 2. Check tag balance
    open_tags = len(re.findall(r"<a\b[^>]*>", text, re.IGNORECASE))
    close_tags = len(re.findall(r"</a>", text, re.IGNORECASE))
    if open_tags != close_tags:
        malformed_links.append((source_slug, field_name, f"Tag count mismatch: {open_tags} <a vs {close_tags} </a"))

    # 3. Check each <a> tag
    for m in link_regex.finditer(text):
        total_links += 1
        attrs, inner_text = m.group(1), m.group(2)
        full_tag = m.group(0)
        
        if "<a " in inner_text.lower():
            nested_links.append((source_slug, field_name, full_tag[:100]))
            
        if not inner_text.strip():
            empty_text_links.append((source_slug, field_name, full_tag))
            
        m_slug = slug_attr_regex.search(attrs)
        m_href = href_regex.search(attrs)
        
        target_slug = ""
        is_internal = False
        
        if m_slug:
            target_slug = m_slug.group(1).strip().lower()
            is_internal = True
        elif m_href:
            href_val = m_href.group(1).strip()
            if href_val.startswith("#term/"):
                target_slug = href_val.replace("#term/", "").strip().lower()
                is_internal = True
            elif "/terms/" in href_val:
                m_inv = re.search(r"/terms/[a-z0-9]/([a-z0-9_-]+)\.asp", href_val, re.IGNORECASE)
                if m_inv:
                    target_slug = m_inv.group(1).strip().lower()
                    is_internal = True
                else:
                    external_links_count += 1
                    continue
            else:
                external_links_count += 1
                continue
        else:
            malformed_links.append((source_slug, field_name, f"No href or data-slug in: {full_tag}"))
            continue

        if is_internal:
            internal_links_count += 1
            terms_with_links.add(source_slug)
            clean_target = target_slug.replace(".asp", "").strip()
            target_slug_counts[clean_target] += 1
            
            # Check class
            if "internal-term-link" not in attrs:
                class_mismatch_links.append((source_slug, field_name, full_tag))
            
            # Check self-link
            if clean_target == source_slug:
                self_links.append((source_slug, field_name, clean_target))
                
            # Check target exists
            if clean_target not in valid_slugs:
                norm_c = re.sub(r"[^a-z0-9]", "", clean_target)
                if norm_c in valid_slug_clean:
                    # Target exists under slight spelling variation (e.g. hyphen)
                    pass
                else:
                    broken_links.append((source_slug, field_name, clean_target, inner_text[:40]))

print("Auditing all terms...", flush=True)

for item in data:
    s_slug = item.get("slug", "").strip().lower()
    for fld in ["definition_en", "bottom_line_en"]:
        audit_text(item.get(fld), s_slug, fld, is_fa=False)
    for fld in ["definition_fa", "bottom_line_fa"]:
        audit_text(item.get(fld), s_slug, fld, is_fa=True)
        
    for idx, t in enumerate(item.get("takeaways_en", [])):
        audit_text(t, s_slug, f"takeaways_en[{idx}]", is_fa=False)
    for idx, t in enumerate(item.get("takeaways_fa", [])):
        audit_text(t, s_slug, f"takeaways_fa[{idx}]", is_fa=True)
        
    for s_idx, sec in enumerate(item.get("sections", [])):
        for p_idx, p in enumerate(sec.get("paragraphs_en", [])):
            audit_text(p, s_slug, f"sec[{s_idx}].p_en[{p_idx}]", is_fa=False)
        for p_idx, p in enumerate(sec.get("paragraphs_fa", [])):
            audit_text(p, s_slug, f"sec[{s_idx}].p_fa[{p_idx}]", is_fa=True)
        for i_idx, it in enumerate(sec.get("items_en", [])):
            audit_text(it, s_slug, f"sec[{s_idx}].it_en[{i_idx}]", is_fa=False)
        for i_idx, it in enumerate(sec.get("items_fa", [])):
            audit_text(it, s_slug, f"sec[{s_idx}].it_fa[{i_idx}]", is_fa=True)

print("\n" + "=" * 50)
print("           MARKETDICT LINK AUDIT REPORT           ")
print("=" * 50)
print(f"Total Terms in Catalog:              {len(data):,}")
print(f"Terms containing Cross-Links:        {len(terms_with_links):,} ({len(terms_with_links)/len(data)*100:.1f}%)")
print(f"Total HTML Links Scanned:            {total_links:,}")
print(f"  - Internal Cross-Links:            {internal_links_count:,}")
print(f"  - External Links:                  {external_links_count:,}")
print(f"Unique Target Slugs Referenced:      {len(target_slug_counts):,}")
print("-" * 50)
print(f"Broken Links (Target not in DB):     {len(broken_links):,}")
print(f"Self-Links (Term linking to itself): {len(self_links):,}")
print(f"Malformed / Unclosed Tag Mismatches: {len(malformed_links):,}")
print(f"Nested <a> tags:                     {len(nested_links):,}")
print(f"Links inside KaTeX math:             {len(math_broken_links):,}")
print(f"Empty Anchor Text links:             {len(empty_text_links):,}")
print(f"Missing .internal-term-link class:   {len(class_mismatch_links):,}")
print("=" * 50)

if broken_links:
    print(f"\n--- Broken Link Details ({len(broken_links)}) ---")
    broken_targets = Counter(b[2] for b in broken_links)
    print(f"Unique broken targets: {len(broken_targets)}")
    for target, count in broken_targets.most_common(20):
        samples = [b for b in broken_links if b[2] == target][:2]
        sample_texts = ", ".join(f'"{s[3]}" in {s[0]}' for s in samples)
        print(f"  Target: '{target}' (occurrences: {count}) -> Samples: {sample_texts}")

if self_links:
    print(f"\n--- Self-Links Details ({len(self_links)}) ---")
    self_counts = Counter(s[0] for s in self_links)
    print(f"Terms linking to themselves: {len(self_counts)}")
    for slug, count in self_counts.most_common(10):
        print(f"  Term '{slug}': {count} self-links")

if class_mismatch_links:
    print(f"\n--- Class Mismatch Details ({len(class_mismatch_links)}) ---")
    for s in class_mismatch_links[:5]:
        print(f"  In {s[0]} ({s[1]}): {s[2]}")

if malformed_links:
    print(f"\n--- Malformed Tag Details ({len(malformed_links)}) ---")
    for m in malformed_links[:5]:
        print(f"  In {m[0]} ({m[1]}): {m[2]}")
