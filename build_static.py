#!/usr/bin/env python3
"""
Static Site Builder for MarketDict
Generates a 100% static, serverless build for GitHub Pages in `dist/`.
"""

import os
import re
import json
import shutil
import sys
import time

def clean_key(text):
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]", "", str(text).lower().replace(".asp", ""))

from categories_engine import TAXONOMY, TAXONOMY_BY_FA

CATEGORY_ICONS = {item["fa"]: item["icon"] for item in TAXONOMY}

def build():
    start_time = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "bilingual_dictionary.json")
    static_src = os.path.join(base_dir, "static")
    template_src = os.path.join(base_dir, "templates", "index.html")
    dist_dir = os.path.join(base_dir, "dist")
    dist_data_dir = os.path.join(dist_dir, "data")
    dist_terms_dir = os.path.join(dist_data_dir, "terms")
    dist_static_dir = os.path.join(dist_dir, "static")

    print(f"🚀 Starting MarketDict static site build...")
    print(f"📁 Source dictionary: {data_file}")
    print(f"📁 Output directory:  {dist_dir}")

    if not os.path.exists(data_file):
        print(f"❌ Error: {data_file} not found!")
        sys.exit(1)

    clean_build = "--clean" in sys.argv or not os.path.exists(dist_terms_dir)

    # Clean and recreate dist directories if requested
    if clean_build and os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_terms_dir, exist_ok=True)
    os.makedirs(dist_data_dir, exist_ok=True)

    # 1. Copy static assets
    if os.path.exists(static_src):
        shutil.copytree(static_src, dist_static_dir, dirs_exist_ok=True)
        print(f"✅ Copied static assets -> {dist_static_dir}")

    # 2. Add .nojekyll for GitHub Pages
    with open(os.path.join(dist_dir, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")

    # 3. Read dictionary data
    print("⏳ Loading dictionary data...")
    with open(data_file, "r", encoding="utf-8") as f:
        terms_data = json.load(f)

    total_terms = len(terms_data)
    print(f"📊 Loaded {total_terms} terms from bilingual_dictionary.json")

    # 4. Generate individual terms JSON and aggregate bundle
    lookup = {}
    summary_terms = []
    category_counts = {}
    letter_counts = {}
    deep_count = 0

    print("⏳ Writing term files & building bundle index...")
    for item in terms_data:
        slug = item.get("slug", "").strip()
        if not slug:
            term_en = item.get("term_en", "")
            slug = clean_key(term_en)
            item["slug"] = slug

        # Save individual term file if clean build or missing
        term_file = os.path.join(dist_terms_dir, f"{slug}.json")
        if clean_build or not os.path.exists(term_file):
            with open(term_file, "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False)

        cat = item.get("category", "سایر")
        category_counts[cat] = category_counts.get(cat, 0) + 1

        ltr = (item.get("letter") or "#").strip().upper()
        letter_counts[ltr] = letter_counts.get(ltr, 0) + 1

        has_deep = bool(item.get("sections") or item.get("deep_enriched"))
        if has_deep:
            deep_count += 1

        summary_terms.append({
            "id": item.get("id"),
            "term_en": item.get("term_en", ""),
            "term_fa": item.get("term_fa", ""),
            "letter": ltr,
            "category": cat,
            "category_fa": item.get("category_fa", cat),
            "category_en": item.get("category_en", ""),
            "definition_fa": item.get("definition_fa", "")[:240],
            "definition_en": item.get("definition_en", "")[:240],
            "slug": slug,
            "has_deep": has_deep,
            "url": item.get("url", "")
        })

        # Register lookup aliases
        lookup[slug] = slug
        slug_clean = clean_key(slug)
        if slug_clean:
            lookup[slug_clean] = slug
        if "-" in slug:
            lookup[slug.replace("-", "")] = slug
        if "_" in slug:
            lookup[slug.replace("_", "")] = slug

        item_id = str(item.get("id", ""))
        if item_id:
            lookup[item_id] = slug

        term_en = item.get("term_en", "")
        if term_en:
            clean_en = clean_key(term_en)
            if clean_en:
                lookup[clean_en] = slug
            lookup[term_en.lower()] = slug
            clean_term_no_space = clean_key(term_en.replace(" ", "-"))
            if clean_term_no_space:
                lookup[clean_term_no_space] = slug

        url = item.get("url", "")
        if url:
            url_slug = url.rstrip("/").split("/")[-1].replace(".asp", "").lower()
            lookup[url_slug] = slug
            clean_u = clean_key(url_slug)
            if clean_u:
                lookup[clean_u] = slug

    # Sort categories and letters
    sorted_cats = [
        {
            "name": k,
            "name_fa": TAXONOMY_BY_FA.get(k, {}).get("fa", k),
            "name_en": TAXONOMY_BY_FA.get(k, {}).get("en", ""),
            "count": v,
            "icon": TAXONOMY_BY_FA.get(k, {}).get("icon", CATEGORY_ICONS.get(k, "🏷️"))
        }
        for k, v in sorted(category_counts.items(), key=lambda x: -x[1])
    ]
    sorted_letters = [
        {"letter": k, "count": v}
        for k, v in sorted(letter_counts.items(), key=lambda x: (x[0] != "#", x[0]))
    ]

    bundle = {
        "stats": {
            "total_terms": total_terms,
            "total_categories": len(category_counts),
            "total_letters": len(letter_counts),
            "deep_enriched_count": deep_count
        },
        "categories": sorted_cats,
        "letters": sorted_letters,
        "terms": summary_terms,
        "lookup": lookup
    }

    bundle_path = os.path.join(dist_data_dir, "bundle.json")
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False)

    bundle_size_mb = os.path.getsize(bundle_path) / (1024 * 1024)
    print(f"✅ Generated {bundle_path} ({bundle_size_mb:.2f} MB)")
    print(f"✅ Generated {total_terms} term detail files in {dist_terms_dir}")

    # 5. Process index.html template for static serving
    with open(template_src, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Normalize asset references to relative paths
    html_content = html_content.replace('href="/static/', 'href="static/')
    html_content = html_content.replace('src="/static/', 'src="static/')
    html_content = html_content.replace('href="/favicon.ico"', 'href="static/favicon.svg"')

    dist_index = os.path.join(dist_dir, "index.html")
    with open(dist_index, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 6. Copy 404.html for GitHub Pages single-page routing
    dist_404 = os.path.join(dist_dir, "404.html")
    with open(dist_404, "w", encoding="utf-8") as f:
        f.write(html_content)

    elapsed = time.time() - start_time
    print(f"🎉 Build completed successfully in {elapsed:.2f} seconds!")
    print(f"🌟 Output ready in: {dist_dir}")

if __name__ == "__main__":
    build()
