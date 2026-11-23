#!/usr/bin/env python3
"""
MarketDict - Financial Terms Dictionary
Backend Server using Flask with Ultra-Fast Binary Cache & SQLite Hybrid Indexing.
"""

import json
import os
import pickle
import random
import re
import sqlite3
import threading
import time
from typing import Any

from flask import Flask, jsonify, render_template, request, Response

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

def apply_reverse_proxy(flask_app: Flask, allowed_ips: Any = "*") -> Flask:
    """
    Wrap Flask WSGI app with Werkzeug ProxyFix to respect X-Forwarded-For,
    X-Forwarded-Proto, X-Forwarded-Host, X-Forwarded-Port, X-Forwarded-Prefix
    from trusted reverse proxy IP addresses.
    """
    from werkzeug.middleware.proxy_fix import ProxyFix

    allowed: set | None = None
    if isinstance(allowed_ips, str):
        if allowed_ips.strip() != "*":
            allowed = {ip.strip() for ip in allowed_ips.split(",") if ip.strip()}
    elif isinstance(allowed_ips, (list, set, tuple)):
        allowed = set(allowed_ips)

    base_wsgi = getattr(flask_app, "_base_wsgi_app", flask_app.wsgi_app)
    flask_app._base_wsgi_app = base_wsgi

    proxy_fix = ProxyFix(
        base_wsgi,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1,
        x_prefix=1
    )

    def reverse_proxy_wsgi(environ, start_response):
        remote_addr = environ.get("REMOTE_ADDR", "")
        if allowed is None or remote_addr in allowed:
            return proxy_fix(environ, start_response)
        return base_wsgi(environ, start_response)

    flask_app.wsgi_app = reverse_proxy_wsgi
    flask_app.config["REVERSE_PROXY_ENABLED"] = True
    flask_app.config["FORWARDED_ALLOW_IPS"] = allowed_ips
    return flask_app

# Auto-enable reverse proxy middleware if PROXY_HEADERS environment variable is active
if os.environ.get("PROXY_HEADERS", "").strip().lower() in ("true", "1", "yes"):
    apply_reverse_proxy(app, allowed_ips=os.environ.get("FORWARDED_ALLOW_IPS", "*"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "bilingual_dictionary.json")
CACHE_FILE = os.path.join(BASE_DIR, "cache_index.pkl")
DB_FILE = os.path.join(BASE_DIR, "market_dict.db")

from categories_engine import TAXONOMY, TAXONOMY_BY_FA, normalize_category

CATEGORY_ICONS = {item["fa"]: item["icon"] for item in TAXONOMY}

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = text.replace("ي", "ی").replace("ك", "ک").replace("ة", "ه").replace("ۀ", "ه")
    text = text.replace("\u200c", " ")
    text = text.replace("  ", " ")
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    return text.strip()

def clean_key(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]", "", str(text).lower().replace(".asp", ""))

_LOCK = threading.Lock()
_CACHE: dict[str, Any] = {
    "mtime": 0,
    "summaries": [],
    "search_index": [],
    "stats": {},
    "letters": [],
    "categories": [],
    "by_letter": {},
    "by_category": {},
    "lookup_keys": {},
    "deep_pool_slugs": []
}

_DETAIL_CACHE: dict[str, Any] = {}
_DB_CONN: sqlite3.Connection | None = None
_IS_RELOADING = False
_LAST_CHECK_TIME = 0.0

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn

def _rebuild_all_cache(current_mtime: float):
    global _DB_CONN, _IS_RELOADING
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # Temporary sqlite file with unique name to prevent locking conflict
        temp_db = os.path.join(BASE_DIR, f"market_dict_tmp_{int(time.time()*1000)}.db")

        conn = sqlite3.connect(temp_db)
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode = WAL")
        cur.execute("PRAGMA synchronous = NORMAL")
        cur.execute("DROP TABLE IF EXISTS terms")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY,
            slug TEXT,
            letter TEXT,
            category TEXT,
            term_en TEXT,
            term_fa TEXT,
            full_json TEXT
        )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_slug ON terms(slug)")

        summaries = []
        search_index = []
        lookup_keys = {}
        letter_counts: dict[str, int] = {}
        category_counts: dict[str, int] = {}
        by_letter: dict[str, list[int]] = {}
        by_category: dict[str, list[int]] = {}
        deep_pool_slugs = []
        deep_count = 0

        terms_insert_rows = []

        for idx, item in enumerate(raw_data):
            slug = item.get("slug", "").strip()
            if not slug:
                slug = clean_key(item.get("term_en", ""))
                item["slug"] = slug

            item_id = str(item.get("id", ""))
            raw_cat = item.get("category", "")
            canon_cat = normalize_category(raw_cat)
            cat = canon_cat["fa"]
            cat_fa = canon_cat["fa"]
            cat_en = canon_cat["en"]
            ltr = (item.get("letter") or "#").strip().upper()
            has_deep = bool(item.get("sections") or item.get("deep_enriched"))
            if has_deep:
                deep_count += 1
                deep_pool_slugs.append(slug)

            letter_counts[ltr] = letter_counts.get(ltr, 0) + 1
            category_counts[cat] = category_counts.get(cat, 0) + 1

            if ltr not in by_letter:
                by_letter[ltr] = []
            by_letter[ltr].append(idx)

            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(idx)

            summary = {
                "id": item.get("id"),
                "term_en": item.get("term_en", ""),
                "term_fa": item.get("term_fa", ""),
                "letter": ltr,
                "category": cat,
                "category_fa": cat_fa,
                "category_en": cat_en,
                "definition_fa": item.get("definition_fa", "")[:350],
                "definition_en": item.get("definition_en", "")[:350],
                "slug": slug,
                "has_deep": has_deep,
                "url": item.get("url", ""),
                "takeaways_en": item.get("takeaways_en", []),
                "takeaways_fa": item.get("takeaways_fa", []),
                "bottom_line_en": item.get("bottom_line_en", ""),
                "bottom_line_fa": item.get("bottom_line_fa", "")
            }
            summaries.append(summary)

            search_entry = {
                "idx": idx,
                "norm_en": normalize_text(item.get("term_en", "")),
                "norm_fa": normalize_text(item.get("term_fa", "")),
                "norm_def_fa": normalize_text(item.get("definition_fa", "")[:300]),
                "norm_def_en": normalize_text(item.get("definition_en", "")[:300]),
                "norm_cat": normalize_text(cat),
                "letter": ltr,
                "category": cat,
                "id_str": item_id,
                "slug": slug
            }
            search_index.append(search_entry)

            if slug:
                lookup_keys[slug.lower()] = slug
                slug_c = clean_key(slug)
                if slug_c:
                    lookup_keys[slug_c] = slug
            if item_id:
                lookup_keys[item_id] = slug
            term_en = item.get("term_en", "")
            if term_en:
                lookup_keys[term_en.lower()] = slug
                en_c = clean_key(term_en)
                if en_c:
                    lookup_keys[en_c] = slug
            url = item.get("url", "")
            if url:
                url_slug = url.rstrip("/").split("/")[-1].replace(".asp", "").lower()
                if url_slug:
                    lookup_keys[url_slug] = slug
                    u_c = clean_key(url_slug)
                    if u_c:
                        lookup_keys[u_c] = slug

            terms_insert_rows.append((
                item.get("id"),
                slug,
                ltr,
                cat,
                term_en,
                item.get("term_fa", ""),
                json.dumps(item, ensure_ascii=False)
            ))

        cur.executemany("INSERT INTO terms VALUES (?, ?, ?, ?, ?, ?, ?)", terms_insert_rows)
        conn.commit()
        conn.close()

        # Safely replace DB_FILE
        if _DB_CONN:
            try:
                _DB_CONN.close()
            except sqlite3.Error:
                pass
            _DB_CONN = None

        import shutil
        try:
            shutil.copy2(temp_db, DB_FILE)
            try:
                os.remove(temp_db)
            except OSError:
                pass
        except OSError:
            try:
                os.replace(temp_db, DB_FILE)
            except OSError:
                pass

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

        cache_data = {
            "mtime": current_mtime,
            "summaries": summaries,
            "search_index": search_index,
            "stats": {
                "total_terms": len(raw_data),
                "total_categories": len(category_counts),
                "total_letters": len(letter_counts),
                "deep_enriched_count": deep_count
            },
            "letters": sorted_letters,
            "categories": sorted_cats,
            "by_letter": by_letter,
            "by_category": by_category,
            "lookup_keys": lookup_keys,
            "deep_pool_slugs": deep_pool_slugs
        }

        try:
            temp_cache = CACHE_FILE + ".tmp"
            with open(temp_cache, "wb") as f:
                pickle.dump(cache_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            if os.path.exists(CACHE_FILE):
                try:
                    os.remove(CACHE_FILE)
                except OSError:
                    pass
            os.rename(temp_cache, CACHE_FILE)
        except OSError:
            pass

        _CACHE.update(cache_data)
        _DB_CONN = get_db_connection()
        _DETAIL_CACHE.clear()

    except (json.JSONDecodeError, OSError, sqlite3.Error, pickle.PickleError):
        import traceback
        traceback.print_exc()
    finally:
        _IS_RELOADING = False

def _async_reload(current_mtime: float):
    global _IS_RELOADING
    with _LOCK:
        if _IS_RELOADING:
            return
        _IS_RELOADING = True
    _rebuild_all_cache(current_mtime)

def ensure_cache():
    global _DB_CONN, _LAST_CHECK_TIME
    if not os.path.exists(DATA_FILE):
        return

    now = time.time()

    # If cache is already hot in memory:
    if _CACHE.get("summaries"):
        # Check for disk updates at most once every 30 seconds
        if now - _LAST_CHECK_TIME > 30.0:
            _LAST_CHECK_TIME = now
            try:
                current_mtime = os.path.getmtime(DATA_FILE)
                if current_mtime != _CACHE.get("mtime") and not _IS_RELOADING:
                    # Asynchronously reload in background so current user is never blocked!
                    threading.Thread(target=_async_reload, args=(current_mtime,), daemon=True).start()
            except OSError:
                pass
        return

    # Cold start: must populate _CACHE for the first time
    with _LOCK:
        if _CACHE.get("summaries"):
            return

        try:
            current_mtime = os.path.getmtime(DATA_FILE)
        except OSError:
            current_mtime = 0

        # Fast path: load pre-indexed binary cache in 0.2s!
        if os.path.exists(CACHE_FILE) and os.path.exists(DB_FILE):
            try:
                with open(CACHE_FILE, "rb") as f:
                    cached = pickle.load(f)
                if cached.get("summaries"):
                    _CACHE.update(cached)
                    _DB_CONN = get_db_connection()
                    _LAST_CHECK_TIME = now
                    # If file on disk is newer, update in background
                    if cached.get("mtime") != current_mtime:
                        threading.Thread(target=_async_reload, args=(current_mtime,), daemon=True).start()
                    return
            except (pickle.PickleError, EOFError, OSError):
                pass

        # If cache file missing, rebuild synchronously once
        _rebuild_all_cache(current_mtime)
        _LAST_CHECK_TIME = now

def get_dictionary() -> list[dict[str, Any]]:
    ensure_cache()
    if _DB_CONN:
        cur = _DB_CONN.cursor()
        cur.execute("SELECT full_json FROM terms ORDER BY id")
        return [json.loads(r[0]) for r in cur.fetchall()]
    return []

# Preload cache immediately at module load
ensure_cache()

from api_v1 import init_api_v1

init_api_v1(
    app=app,
    cache_dict=_CACHE,
    detail_cache_dict=_DETAIL_CACHE,
    get_db_func=get_db_connection,
    ensure_cache_func=ensure_cache,
    norm_func=normalize_text,
    clean_func=clean_key
)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept"
    return response

@app.route("/docs")
def docs_redirect():
    from flask import redirect
    return redirect("/api/v1/docs")

@app.route("/docs/guide")
@app.route("/api/v1/guide")
def api_guide():
    return render_template("api_guide.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.svg")

@app.route("/api/stats")
def get_stats():
    ensure_cache()
    return jsonify(_CACHE["stats"])

@app.route("/api/letters")
def get_letters():
    ensure_cache()
    return jsonify(_CACHE["letters"])

@app.route("/api/categories")
def get_categories():
    ensure_cache()
    return jsonify(_CACHE["categories"])

@app.route("/api/terms")
def search_terms():
    ensure_cache()
    query = request.args.get("q", "").strip()
    letter = request.args.get("letter", "").strip().upper()
    category = request.args.get("category", "").strip()
    ids_param = request.args.get("ids", "").strip()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 24))

    search_index = _CACHE["search_index"]
    summaries = _CACHE["summaries"]
    by_letter = _CACHE["by_letter"]
    by_category = _CACHE["by_category"]

    # Filter candidate indices
    resolved_cat = normalize_category(category)["fa"] if category and category != "ALL" else None

    if letter and letter != "ALL" and letter in by_letter:
        candidate_indices = by_letter[letter]
        if resolved_cat:
            candidate_indices = [i for i in candidate_indices if search_index[i]["category"] == resolved_cat]
    elif resolved_cat and resolved_cat in by_category:
        candidate_indices = by_category[resolved_cat]
    else:
        candidate_indices = range(len(search_index))

    if ids_param:
        id_set = set(re.split(r"[,;|\s]+", ids_param))
        candidate_indices = [
            i for i in candidate_indices 
            if search_index[i]["id_str"] in id_set or search_index[i]["slug"] in id_set
        ]

    if query:
        norm_query = normalize_text(query)
        scored_results = []
        for i in candidate_indices:
            entry = search_index[i]
            term_en = entry["norm_en"]
            term_fa = entry["norm_fa"]
            score = 0
            if norm_query == term_en or norm_query == term_fa:
                score += 100
            elif term_en.startswith(norm_query) or term_fa.startswith(norm_query):
                score += 50
            elif norm_query in term_en or norm_query in term_fa:
                score += 30
            elif norm_query in entry["norm_cat"]:
                score += 15
            elif norm_query in entry["norm_def_fa"] or norm_query in entry["norm_def_en"]:
                score += 10

            if score > 0:
                scored_results.append((score, i))

        scored_results.sort(key=lambda x: -x[0])
        matched_indices = [i for _, i in scored_results]
    else:
        matched_indices = list(candidate_indices)

    total_matches = len(matched_indices)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_items = [summaries[i] for i in matched_indices[start_idx:end_idx]]

    return jsonify({
        "terms": paginated_items,
        "total": total_matches,
        "page": page,
        "limit": limit,
        "has_more": end_idx < total_matches
    })

@app.route("/api/terms/<term_identifier>")
def get_term_by_id(term_identifier: str):
    ensure_cache()
    norm = term_identifier.lower().strip().replace(".asp", "")
    norm_clean = clean_key(norm)
    lookup_keys = _CACHE["lookup_keys"]

    target_slug = lookup_keys.get(norm) or lookup_keys.get(norm_clean) or norm
    if target_slug in _DETAIL_CACHE:
        return jsonify(_DETAIL_CACHE[target_slug])

    if _DB_CONN:
        cur = _DB_CONN.cursor()
        cur.execute("SELECT full_json FROM terms WHERE slug = ?", (target_slug,))
        row = cur.fetchone()
        if row:
            data = json.loads(row[0])
            if len(_DETAIL_CACHE) < 500:
                _DETAIL_CACHE[target_slug] = data
            return jsonify(data)

    return jsonify({"error": "Term not found"}), 404

@app.route("/api/random")
def get_random_term():
    ensure_cache()
    pool = _CACHE["deep_pool_slugs"] or list(_CACHE["lookup_keys"].values())
    if not pool:
        return jsonify({"error": "No terms available"}), 404
    rand_slug = random.choice(pool)
    return get_term_by_id(rand_slug)

# In-memory LRU cache for generated neural TTS audio chunks
_TTS_CACHE: Dict[str, bytes] = {}
_TTS_LOCK = threading.Lock()

@app.route("/api/tts")
def handle_tts():
    """
    Stream high-quality neural TTS audio for Persian and English.
    Query parameters:
      - text: string to speak (required)
      - lang: 'fa' or 'en' (default: 'fa')
      - voice: optional explicit voice name
    """
    text = (request.args.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    lang = (request.args.get("lang") or "fa").strip().lower()
    voice = (request.args.get("voice") or "").strip()
    if not voice:
        voice = "fa-IR-DilaraNeural" if lang == "fa" else "en-US-AriaNeural"

    cache_key = f"{voice}:{text}"
    with _TTS_LOCK:
        if cache_key in _TTS_CACHE:
            return Response(_TTS_CACHE[cache_key], mimetype="audio/mpeg")

    try:
        import asyncio
        import edge_tts

        async def _generate_audio():
            comm = edge_tts.Communicate(text, voice)
            buf = bytearray()
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    buf.extend(chunk["data"])
            return bytes(buf)

        audio_bytes = asyncio.run(_generate_audio())

        if not audio_bytes:
            return jsonify({"error": "Failed to synthesize speech"}), 500

        with _TTS_LOCK:
            if len(_TTS_CACHE) > 500:
                oldest_key = next(iter(_TTS_CACHE))
                _TTS_CACHE.pop(oldest_key, None)
            _TTS_CACHE[cache_key] = audio_bytes

        return Response(audio_bytes, mimetype="audio/mpeg")
    except Exception as exc:
        app.logger.warning(f"TTS synthesis error: {exc}")
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="MarketDict - Bilingual Financial Terms Web App & REST API Server"
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", "0.0.0.0"),
        help="Host IP to bind to (default: 0.0.0.0 or $HOST)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "5000")),
        help="Port to listen on (default: 5000 or $PORT)"
    )
    parser.add_argument(
        "--proxy-headers",
        action=argparse.BooleanOptionalAction,
        default=os.environ.get("PROXY_HEADERS", "false").strip().lower() in ("true", "1", "yes"),
        help="Enable/disable reverse proxy headers (X-Forwarded-For, X-Forwarded-Proto, etc.)"
    )
    parser.add_argument(
        "--forwarded-allow-ips",
        default=os.environ.get("FORWARDED_ALLOW_IPS", "*"),
        help="Comma-separated list of trusted proxy IPs or '*' for all (default: '*' or $FORWARDED_ALLOW_IPS)"
    )
    args = parser.parse_args()

    if args.proxy_headers:
        apply_reverse_proxy(app, allowed_ips=args.forwarded_allow_ips)
        proxy_status = f"ENABLED (Trusted IPs: {args.forwarded_allow_ips})"
    else:
        proxy_status = "DISABLED"

    print("\n=======================================================")
    print("🚀 MarketDict Web App & API are running!")
    print(f"👉 Host:          {args.host}")
    print(f"👉 Port:          {args.port}")
    print(f"👉 Reverse Proxy: {proxy_status}")
    print(f"👉 Web App:       http://{args.host}:{args.port}")
    print(f"👉 REST API:      http://{args.host}:{args.port}/api/v1")
    print(f"👉 API Docs:      http://{args.host}:{args.port}/docs")
    print("=======================================================\n")
    app.run(host=args.host, port=args.port, debug=False, threaded=True)
