#!/usr/bin/env python3
"""
MarketDict - Financial Terms Dictionary
Backend Server using Flask.
"""

import os
import re
import json
import random
from typing import List, Dict, Any, Optional
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")

DATA_FILE = os.path.join(os.path.dirname(__file__), "bilingual_dictionary.json")
_CACHE = {"mtime": 0, "data": []}

CATEGORY_ICONS = {
    "بازار سهام و معاملات": "📈",
    "حسابداری و صورت‌های مالی": "📊",
    "اقتصاد کلان و سیاست پولی": "🏛️",
    "ارزش‌گذاری و تحلیل بنیادی": "⚖️",
    "تحلیل تکنیکال و نموداری": "📉",
    "ابزارهای مشتقه و آپشن": "⚡",
    "اوراق بدهی و اسناد خزانه": "📜",
    "بانکداری، وام و اعتبارات": "🏦",
    "مدیریت ریسک و بیمه": "🛡️",
    "سرمایه‌گذاری و صندوق‌ها": "💼",
    "مالیات، مقررات و قوانین": "⚖️",
    "تجارت بین‌الملل و بازرگانی": "🌐",
    "ارزهای دیجیتال و فین‌تک": "🪙",
    "کسب‌وکار و مدیریت استراتژیک": "💡"
}

def get_dictionary() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        current_mtime = os.path.getmtime(DATA_FILE)
    except OSError:
        return _CACHE["data"]

    if current_mtime != _CACHE["mtime"]:
        for attempt in range(4):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    _CACHE["data"] = loaded
                    _CACHE["mtime"] = current_mtime
                    break
            except (json.JSONDecodeError, PermissionError, OSError):
                import time
                time.sleep(0.15)

    return _CACHE["data"]

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = text.replace("ي", "ی").replace("ك", "ک").replace("ة", "ه").replace("ۀ", "ه")
    text = text.replace("\u200c", " ")
    text = text.replace("  ", " ")
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    return text.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.svg")

@app.route("/api/stats")
def get_stats():
    dictionary = get_dictionary()
    categories = set(t.get("category", "") for t in dictionary if t.get("category"))
    letters = set(t.get("letter", "") for t in dictionary if t.get("letter"))
    deep_count = sum(1 for t in dictionary if t.get("deep_enriched") or t.get("sections"))
    return jsonify({
        "total_terms": len(dictionary),
        "total_categories": len(categories),
        "total_letters": len(letters),
        "deep_enriched_count": deep_count
    })

@app.route("/api/letters")
def get_letters():
    dictionary = get_dictionary()
    counts: Dict[str, int] = {}
    for item in dictionary:
        ltr = item.get("letter", "#").upper()
        counts[ltr] = counts.get(ltr, 0) + 1
    
    sorted_letters = sorted(counts.keys(), key=lambda x: (x != "#", x))
    return jsonify([{"letter": l, "count": counts[l]} for l in sorted_letters])

@app.route("/api/categories")
def get_categories():
    dictionary = get_dictionary()
    counts: Dict[str, int] = {}
    for item in dictionary:
        cat = item.get("category", "سایر")
        counts[cat] = counts.get(cat, 0) + 1
    
    sorted_cats = sorted(counts.items(), key=lambda x: -x[1])
    return jsonify([
        {
            "name": k,
            "count": v,
            "icon": CATEGORY_ICONS.get(k, "🏷️")
        } for k, v in sorted_cats
    ])

@app.route("/api/terms")
def search_terms():
    query = request.args.get("q", "").strip()
    letter = request.args.get("letter", "").strip().upper()
    category = request.args.get("category", "").strip()
    ids_param = request.args.get("ids", "").strip()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 24))

    filtered = get_dictionary()

    # Filter by IDs (used by Bookmarks / Favorites)
    if ids_param:
        id_set = set(re.split(r"[,;|\s]+", ids_param))
        filtered = [t for t in filtered if str(t.get("id")) in id_set or str(t.get("slug")) in id_set]

    # Filter by Letter
    if letter and letter != "ALL":
        filtered = [t for t in filtered if t.get("letter", "").upper() == letter]

    # Filter by Category
    if category and category != "ALL":
        filtered = [t for t in filtered if t.get("category", "") == category]

    # Filter by Search Query
    if query:
        norm_query = normalize_text(query)
        scored_results = []
        for item in filtered:
            term_en = normalize_text(item.get("term_en", ""))
            term_fa = normalize_text(item.get("term_fa", ""))
            def_en = normalize_text(item.get("definition_en", ""))
            def_fa = normalize_text(item.get("definition_fa", ""))
            cat = normalize_text(item.get("category", ""))

            score = 0
            if norm_query == term_en or norm_query == term_fa:
                score += 100
            elif term_en.startswith(norm_query) or term_fa.startswith(norm_query):
                score += 50
            elif norm_query in term_en or norm_query in term_fa:
                score += 30
            elif norm_query in cat:
                score += 15
            elif norm_query in def_en or norm_query in def_fa:
                score += 10

            if score > 0:
                scored_results.append((score, item))

        scored_results.sort(key=lambda x: -x[0])
        filtered = [item for _, item in scored_results]

    total_matches = len(filtered)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_items = filtered[start_idx:end_idx]

    return jsonify({
        "terms": paginated_items,
        "total": total_matches,
        "page": page,
        "limit": limit,
        "has_more": end_idx < total_matches
    })

@app.route("/api/terms/<term_identifier>")
def get_term_by_id(term_identifier: str):
    norm = term_identifier.lower().strip().replace(".asp", "")
    norm_clean = re.sub(r"[^a-z0-9]", "", norm)
    dictionary = get_dictionary()
    
    # 1. Exact match pass
    for item in dictionary:
        item_id = str(item.get("id", "")).lower()
        item_slug = item.get("slug", "").lower().replace(".asp", "")
        item_en = normalize_text(item.get("term_en", ""))
        url = item.get("url", "")
        url_slug = url.rstrip("/").split("/")[-1].replace(".asp", "").lower() if url else ""

        if norm in (item_id, item_slug, item_en, url_slug):
            return jsonify(item)
            
    # 2. Alphanumeric normalized pass (ignores hyphens, underscores, spaces)
    if norm_clean:
        for item in dictionary:
            item_slug_clean = re.sub(r"[^a-z0-9]", "", item.get("slug", "").lower().replace(".asp", ""))
            url = item.get("url", "")
            url_slug = url.rstrip("/").split("/")[-1].replace(".asp", "").lower() if url else ""
            url_slug_clean = re.sub(r"[^a-z0-9]", "", url_slug)
            item_en_clean = re.sub(r"[^a-z0-9]", "", item.get("term_en", "").lower())
            
            if norm_clean in (item_slug_clean, url_slug_clean, item_en_clean):
                return jsonify(item)

    return jsonify({"error": "Term not found"}), 404

@app.route("/api/random")
def get_random_term():
    dictionary = get_dictionary()
    if not dictionary:
        return jsonify({"error": "No terms available"}), 404
    deep_pool = [t for t in dictionary if t.get("sections")]
    pool = deep_pool if deep_pool and random.random() < 0.8 else dictionary
    return jsonify(random.choice(pool))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"🚀 MarketDict Web App is running!")
    print(f"👉 Local URL: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=True)
