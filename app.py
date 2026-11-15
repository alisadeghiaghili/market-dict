#!/usr/bin/env python3
"""
MarketDict - Bilingual Financial Terms Web Application
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

def load_dictionary() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

DICTIONARY: List[Dict[str, Any]] = load_dictionary()

# Persian text normalization for accurate search
def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    # Persian/Arabic character unification
    text = text.replace("ي", "ی").replace("ك", "ک").replace("ة", "ه").replace("ۀ", "ه")
    text = text.replace("\u200c", " ")  # zero-width non-joiner to space
    text = text.replace("  ", " ")
    # remove common Persian diacritics
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    return text.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def get_stats():
    categories = set(t.get("category", "") for t in DICTIONARY if t.get("category"))
    letters = set(t.get("letter", "") for t in DICTIONARY if t.get("letter"))
    featured_count = sum(1 for t in DICTIONARY if t.get("featured"))
    return jsonify({
        "total_terms": len(DICTIONARY),
        "total_categories": len(categories),
        "total_letters": len(letters),
        "featured_count": featured_count
    })

@app.route("/api/letters")
def get_letters():
    counts: Dict[str, int] = {}
    for item in DICTIONARY:
        ltr = item.get("letter", "#").upper()
        counts[ltr] = counts.get(ltr, 0) + 1
    
    sorted_letters = sorted(counts.keys(), key=lambda x: (x != "#", x))
    return jsonify([{"letter": l, "count": counts[l]} for l in sorted_letters])

@app.route("/api/categories")
def get_categories():
    counts: Dict[str, int] = {}
    for item in DICTIONARY:
        cat = item.get("category", "سایر")
        counts[cat] = counts.get(cat, 0) + 1
    
    sorted_cats = sorted(counts.items(), key=lambda x: -x[1])
    return jsonify([{"name": k, "count": v} for k, v in sorted_cats])

@app.route("/api/terms")
def search_terms():
    query = request.args.get("q", "").strip()
    letter = request.args.get("letter", "").strip().upper()
    category = request.args.get("category", "").strip()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 24))

    filtered = DICTIONARY

    # Filter by Letter
    if letter and letter != "ALL":
        filtered = [t for t in filtered if t.get("letter", "").upper() == letter]

    # Filter by Category
    if category and category != "ALL":
        filtered = [t for t in filtered if t.get("category", "") == category]

    # Filter by Search Query (Bilingual)
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
            # Exact matches get highest score
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

@app.route("/api/terms/<term_id>")
def get_term_by_id(term_id: str):
    term_id_norm = term_id.lower().strip()
    for item in DICTIONARY:
        if item.get("id", "").lower() == term_id_norm or normalize_text(item.get("term_en", "")) == term_id_norm:
            return jsonify(item)
    return jsonify({"error": "Term not found"}), 404

@app.route("/api/random")
def get_random_term():
    if not DICTIONARY:
        return jsonify({"error": "No terms available"}), 404
    # Prefer featured terms if available
    featured = [t for t in DICTIONARY if t.get("featured")]
    pool = featured if featured and random.random() < 0.7 else DICTIONARY
    return jsonify(random.choice(pool))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"🚀 MarketDict Bilingual Web App is running!")
    print(f"👉 Local URL: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=True)
