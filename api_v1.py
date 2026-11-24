"""
MarketDict API v1 Blueprint
High-performance RESTful API for external applications and integrations.
"""

import json
import math
import os
import random
import re
import sqlite3
import time
from typing import Any

from flask import Blueprint, Response, jsonify, render_template_string, request

from categories_engine import (
    CATEGORY_ALIASES,
    TAXONOMY,
    TAXONOMY_BY_FA,
    normalize_category,
)
from formula_registry import FORMULA_DB
from openapi_spec import get_openapi_spec

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Service Start Time for Uptime Reporting
_SERVICE_START_TIME = time.time()

# Internal References (injected via init_api_v1 or imported from app)
_CACHE_REF: dict[str, Any] | None = None
_DETAIL_CACHE_REF: dict[str, Any] | None = None
_GET_DB_CONN_FUNC = None
_ENSURE_CACHE_FUNC = None
_NORMALIZE_TEXT_FUNC = None
_CLEAN_KEY_FUNC = None

# Build Category Lookup Maps
# Allows querying by slug (e.g. 'crypto', 'stock_capital_markets'), English name, or Persian name
CATEGORY_LOOKUP: dict[str, str] = {}
TAXONOMY_BY_ID: dict[str, dict[str, Any]] = {}

for item in TAXONOMY:
    cat_id = item["id"].lower()
    cat_fa = item["fa"]
    cat_en = item["en"].lower()
    CATEGORY_LOOKUP[cat_id] = cat_fa
    CATEGORY_LOOKUP[cat_fa.lower()] = cat_fa
    CATEGORY_LOOKUP[cat_en] = cat_fa
    TAXONOMY_BY_ID[cat_id] = item

for alias, canon_fa in CATEGORY_ALIASES.items():
    canon = TAXONOMY_BY_FA.get(canon_fa, TAXONOMY[-1])
    CATEGORY_LOOKUP[alias.lower()] = canon["fa"]

def get_category_meta(name_fa: str) -> dict[str, Any]:
    canon = normalize_category(name_fa)
    return {
        "id": canon["id"],
        "fa": canon["fa"],
        "en": canon["en"],
        "icon": canon["icon"]
    }

def _clean_key_fallback(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]", "", str(text).lower().replace(".asp", ""))

def _normalize_text_fallback(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = text.replace("ي", "ی").replace("ك", "ک").replace("ة", "ه").replace("ۀ", "ه")
    text = text.replace("\u200c", " ")
    text = text.replace("  ", " ")
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    return text.strip()

def get_cache() -> dict[str, Any]:
    if _ENSURE_CACHE_FUNC:
        _ENSURE_CACHE_FUNC()
    elif _CACHE_REF is None:
        try:
            import app as main_app
            main_app.ensure_cache()
            return main_app._CACHE
        except (ImportError, AttributeError):
            pass
    return _CACHE_REF or {}

def get_detail_cache() -> dict[str, Any]:
    global _DETAIL_CACHE_REF
    if _DETAIL_CACHE_REF is None:
        try:
            import app as main_app
            _DETAIL_CACHE_REF = main_app._DETAIL_CACHE
        except (ImportError, AttributeError):
            _DETAIL_CACHE_REF = {}
    return _DETAIL_CACHE_REF

def get_db():
    if _GET_DB_CONN_FUNC:
        return _GET_DB_CONN_FUNC()
    try:
        import app as main_app
        return main_app.get_db_connection()
    except (ImportError, AttributeError):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_dict.db")
        return sqlite3.connect(db_path, check_same_thread=False)

def normalize_text(text: str) -> str:
    if _NORMALIZE_TEXT_FUNC:
        return _NORMALIZE_TEXT_FUNC(text)
    return _normalize_text_fallback(text)

def clean_key(text: str) -> str:
    if _CLEAN_KEY_FUNC:
        return _CLEAN_KEY_FUNC(text)
    return _clean_key_fallback(text)


def init_api_v1(app, cache_dict, detail_cache_dict, get_db_func, ensure_cache_func, norm_func, clean_func):
    """Initialize API v1 with shared memory caches and database handlers."""
    global _CACHE_REF, _DETAIL_CACHE_REF, _GET_DB_CONN_FUNC, _ENSURE_CACHE_FUNC, _NORMALIZE_TEXT_FUNC, _CLEAN_KEY_FUNC
    _CACHE_REF = cache_dict
    _DETAIL_CACHE_REF = detail_cache_dict
    _GET_DB_CONN_FUNC = get_db_func
    _ENSURE_CACHE_FUNC = ensure_cache_func
    _NORMALIZE_TEXT_FUNC = norm_func
    _CLEAN_KEY_FUNC = clean_func

    app.register_blueprint(api_v1)


# ----------------------------------------------------------------------
# CORS & Response Helpers
# ----------------------------------------------------------------------

@api_v1.after_request
def add_cors_headers(response: Response) -> Response:
    """Ensure CORS is completely open for external third-party applications."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept"
    response.headers["X-API-Version"] = "1.0.0"
    return response

@api_v1.route("/<path:dummy>", methods=["OPTIONS"])
def handle_options(dummy):
    """Handle CORS preflight requests cleanly."""
    return "", 204

def success_response(data: Any, pagination: dict[str, Any] | None = None, meta: dict[str, Any] | None = None, code: int = 200):
    payload = {"status": "success", "data": data}
    if pagination is not None:
        payload["pagination"] = pagination
    if meta is not None:
        payload["meta"] = meta
    return jsonify(payload), code

def error_response(message: str, code: int = 400, details: str | None = None):
    payload = {
        "status": "error",
        "error": {
            "code": code,
            "message": message,
            "details": details or message
        }
    }
    return jsonify(payload), code

def filter_fields(item: dict[str, Any], fields_set: set | None) -> dict[str, Any]:
    if not fields_set:
        return item
    return {k: v for k, v in item.items() if k in fields_set}

def enrich_term_summary(term: dict[str, Any]) -> dict[str, Any]:
    """Attach category_id and has_formula flag to a term summary."""
    res = dict(term)
    cat_fa = res.get("category", "")
    tax = get_category_meta(cat_fa)
    res["category_id"] = tax["id"]
    res["category_fa"] = cat_fa
    res["category_en"] = tax["en"]
    res["category_icon"] = tax["icon"]

    # Check formula
    slug = res.get("slug", "")
    c_key = clean_key(slug)
    res["has_formula"] = c_key in FORMULA_DB
    return res

def fetch_term_detail(target_slug_or_id: str) -> dict[str, Any] | None:
    """Retrieve full term details from memory cache or SQLite database."""
    cache = get_cache()
    lookup_keys = cache.get("lookup_keys", {})
    detail_cache = get_detail_cache()

    ident = str(target_slug_or_id).strip()
    norm = ident.lower().replace(".asp", "")
    norm_clean = clean_key(norm)

    target_slug = lookup_keys.get(norm) or lookup_keys.get(norm_clean) or norm

    if target_slug in detail_cache:
        data = dict(detail_cache[target_slug])
    else:
        conn = get_db()
        try:
            cur = conn.cursor()
            # Search by slug or numeric ID
            if ident.isdigit():
                cur.execute("SELECT full_json FROM terms WHERE id = ? OR slug = ? LIMIT 1", (int(ident), target_slug))
            else:
                cur.execute("SELECT full_json FROM terms WHERE slug = ? LIMIT 1", (target_slug,))
            row = cur.fetchone()
        finally:
            conn.close()
        if not row:
            return None
        data = json.loads(row[0])
        if len(detail_cache) < 1000:
            detail_cache[target_slug] = data

    # Enrich with category ID and icon
    cat_fa = data.get("category", "")
    tax = get_category_meta(cat_fa)
    data["category_id"] = tax["id"]
    data["category_fa"] = cat_fa
    data["category_en"] = tax["en"]
    data["category_icon"] = tax["icon"]

    # Enrich with formula if registered in FORMULA_DB
    c_key = clean_key(data.get("slug", ""))
    if c_key in FORMULA_DB:
        f_entry = FORMULA_DB[c_key]
        data["formula"] = {
            "formula_en": f_entry.get("formula_en", ""),
            "formula_fa": f_entry.get("formula_fa", "")
        }
    else:
        data["formula"] = None

    return data


# ----------------------------------------------------------------------
# 1. System Endpoints: Health, Stats, OpenAPI JSON & Interactive Docs
# ----------------------------------------------------------------------

@api_v1.route("/health", methods=["GET"])
@api_v1.route("/ping", methods=["GET"])
def health_check():
    """Service health and operational status."""
    cache = get_cache()
    stats = cache.get("stats", {})
    uptime = round(time.time() - _SERVICE_START_TIME, 2)
    return success_response({
        "service": "MarketDict API",
        "version": "1.0.0",
        "status": "healthy",
        "uptime_seconds": uptime,
        "total_terms": stats.get("total_terms", len(cache.get("summaries", []))),
        "total_categories": stats.get("total_categories", len(cache.get("categories", []))),
        "total_letters": stats.get("total_letters", len(cache.get("letters", []))),
        "database": "sqlite_wal_active",
        "cache_status": "hot" if bool(cache.get("summaries")) else "warming"
    })

@api_v1.route("/stats", methods=["GET"])
def get_stats():
    """Overall dictionary statistics."""
    cache = get_cache()
    stats = dict(cache.get("stats", {}))
    stats["formulas_count"] = len(FORMULA_DB)
    stats["languages"] = ["fa", "en"]
    return success_response(stats)

@api_v1.route("/openapi.json", methods=["GET"])
def openapi_json():
    """Machine-readable OpenAPI 3.0.3 specification."""
    root = request.script_root.rstrip("/")
    relative_url = f"{root}/api/v1" if root else "/api/v1"
    host_url = request.host_url.rstrip("/") + relative_url
    spec = get_openapi_spec(host_url, relative_url=relative_url)
    return jsonify(spec)

@api_v1.route("/docs", methods=["GET"])
def swagger_ui():
    """Interactive Swagger UI Documentation."""
    root = request.script_root.rstrip("/")
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MarketDict API - Interactive Documentation & Explorer</title>
  <link rel="icon" type="image/svg+xml" href="{root}/favicon.ico">
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #0f172a;
      color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .topbar {{ display: none !important; }}
    .custom-header {{
      background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%);
      border-bottom: 1px solid #1e293b;
      padding: 20px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .custom-header h1 {{
      margin: 0;
      font-size: 1.4rem;
      font-weight: 700;
      color: #34d399;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .custom-header p {{
      margin: 4px 0 0;
      color: #94a3b8;
      font-size: 0.88rem;
    }}
    .custom-header .badge {{
      background: rgba(16, 185, 129, 0.2);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 600;
    }}
    .nav-links a {{
      color: #38bdf8;
      text-decoration: none;
      font-size: 0.875rem;
      margin-left: 16px;
      transition: color 0.2s;
    }}
    .nav-links a:hover {{
      color: #7dd3fc;
      text-decoration: underline;
    }}
    .swagger-ui .info .title {{
      color: #f8fafc !important;
    }}
    .swagger-ui {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px 16px;
    }}
  </style>
</head>
<body>
  <div class="custom-header">
    <div>
      <h1>📈 MarketDict REST API <span class="badge">v1.0.0</span></h1>
      <p>High-performance bilingual financial dictionary API (6,108 terms, 32 categories, formulas, fuzzy search)</p>
    </div>
    <div class="nav-links">
      <a href="{root}/" target="_blank">🌐 Web App</a>
      <a href="{root}/docs/guide" target="_blank">📚 Developer Guide (FA / EN)</a>
      <a href="{root}/api/v1/openapi.json" target="_blank">📄 OpenAPI JSON</a>
      <a href="{root}/api/v1/health" target="_blank">🩺 Health Check</a>
    </div>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = function() {{
      SwaggerUIBundle({{
        url: "{root}/api/v1/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      }});
    }};
  </script>
</body>
</html>"""
    return render_template_string(html_template)


# ----------------------------------------------------------------------
# 2. Terms Endpoints: Search, Lookup, Random, Batch
# ----------------------------------------------------------------------

@api_v1.route("/terms", methods=["GET"])
def get_terms():
    """
    Search and filter financial terms with pagination.
    Query Params:
      q: search string (bilingual fuzzy search)
      letter: initial letter filter (# or A-Z)
      category: category ID or Persian name
      has_deep: true/false
      has_formula: true/false
      sort: relevance, term_en, term_fa, id
      order: asc, desc
      page: page number (default 1)
      limit: page size (default 20, max 100)
      fields: comma-separated field list
      raw: true/false (return un-enveloped array)
    """
    cache = get_cache()
    summaries = cache.get("summaries", [])
    search_index = cache.get("search_index", [])
    by_letter = cache.get("by_letter", {})
    by_category = cache.get("by_category", {})

    query = request.args.get("q", "").strip()
    letter = request.args.get("letter", "").strip().upper()
    cat_param = request.args.get("category", "").strip()
    has_deep_param = request.args.get("has_deep")
    has_formula_param = request.args.get("has_formula")
    sort_by = request.args.get("sort", "").strip().lower()
    order = request.args.get("order", "asc").strip().lower()
    raw = request.args.get("raw", "").lower() in ("true", "1", "yes")

    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1

    try:
        limit = min(100, max(1, int(request.args.get("limit", 20))))
    except ValueError:
        limit = 20

    fields_arg = request.args.get("fields", "").strip()
    fields_set = {f.strip() for f in fields_arg.split(",")} if fields_arg else None

    # Resolve category param (supports 'crypto', 'ارزهای دیجیتال و بلاک‌چین', etc.)
    target_category_fa = None
    if cat_param and cat_param.upper() != "ALL":
        target_category_fa = CATEGORY_LOOKUP.get(cat_param.lower(), cat_param)

    # 1. Determine candidate indices from index buckets
    if letter and letter != "ALL" and letter in by_letter:
        candidate_indices = by_letter[letter]
        if target_category_fa and target_category_fa in by_category:
            target_set = set(by_category[target_category_fa])
            candidate_indices = [i for i in candidate_indices if i in target_set]
    elif target_category_fa and target_category_fa in by_category:
        candidate_indices = by_category[target_category_fa]
    else:
        candidate_indices = range(len(search_index))

    # 2. Filter by deep enrichment if requested
    if has_deep_param is not None:
        want_deep = has_deep_param.lower() in ("true", "1", "yes")
        candidate_indices = [i for i in candidate_indices if summaries[i]["has_deep"] == want_deep]

    # 3. Filter by formula presence if requested
    if has_formula_param is not None:
        want_formula = has_formula_param.lower() in ("true", "1", "yes")
        candidate_indices = [
            i for i in candidate_indices
            if (clean_key(summaries[i]["slug"]) in FORMULA_DB) == want_formula
        ]

    # 4. Search Query Scoring
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

        # Default sort for query is relevance
        if not sort_by or sort_by == "relevance":
            scored_results.sort(key=lambda x: -x[0])
            matched_indices = [i for _, i in scored_results]
        else:
            matched_indices = [i for _, i in scored_results]
    else:
        matched_indices = list(candidate_indices)

    # 5. Sorting (when specified or not sorting by relevance)
    if sort_by in ("term_en", "term_fa", "id"):
        reverse = (order == "desc")
        if sort_by == "term_en":
            matched_indices.sort(key=lambda i: summaries[i]["term_en"].lower(), reverse=reverse)
        elif sort_by == "term_fa":
            matched_indices.sort(key=lambda i: summaries[i]["term_fa"], reverse=reverse)
        elif sort_by == "id":
            matched_indices.sort(key=lambda i: summaries[i].get("id") or 0, reverse=reverse)

    # 6. Pagination
    total = len(matched_indices)
    total_pages = math.ceil(total / limit) if total > 0 else 1
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit

    paged_items = []
    for i in matched_indices[start_idx:end_idx]:
        summary_obj = enrich_term_summary(summaries[i])
        paged_items.append(filter_fields(summary_obj, fields_set))

    if raw:
        return jsonify(paged_items)

    pagination_meta = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": end_idx < total,
        "has_prev": page > 1,
        "next_page": page + 1 if end_idx < total else None,
        "prev_page": page - 1 if page > 1 else None
    }

    return success_response(paged_items, pagination=pagination_meta)

@api_v1.route("/terms/<identifier>", methods=["GET"])
def get_term(identifier: str):
    """
    Retrieve full term details by numeric ID, slug, or clean title.
    Enriched with LaTeX formula and Persian explanation if available.
    """
    term_data = fetch_term_detail(identifier)
    if not term_data:
        return error_response(
            message=f"Term '{identifier}' not found",
            code=404,
            details=f"No financial term matched the identifier '{identifier}'."
        )

    fields_arg = request.args.get("fields", "").strip()
    if fields_arg:
        fields_set = {f.strip() for f in fields_arg.split(",")}
        term_data = filter_fields(term_data, fields_set)

    raw = request.args.get("raw", "").lower() in ("true", "1", "yes")
    if raw:
        return jsonify(term_data)

    return success_response(term_data)

@api_v1.route("/terms/random", methods=["GET"])
def get_random():
    """
    Get one or more random terms (count: 1-10).
    Ideal for 'Financial Term of the Day' widgets, trading bots, and study cards.
    """
    cache = get_cache()
    summaries = cache.get("summaries", [])
    by_category = cache.get("by_category", {})

    if not summaries:
        return error_response("Dictionary cache empty", 503)

    cat_param = request.args.get("category", "").strip()
    has_deep_param = request.args.get("has_deep")

    try:
        count = min(10, max(1, int(request.args.get("count", 1))))
    except ValueError:
        count = 1

    candidate_slugs = []
    if cat_param:
        target_cat = CATEGORY_LOOKUP.get(cat_param.lower(), cat_param)
        if target_cat in by_category:
            candidate_slugs = [summaries[i]["slug"] for i in by_category[target_cat]]
    elif has_deep_param and has_deep_param.lower() in ("true", "1", "yes"):
        candidate_slugs = cache.get("deep_pool_slugs", [])

    if not candidate_slugs:
        candidate_slugs = [s["slug"] for s in summaries]

    chosen_slugs = random.sample(candidate_slugs, min(count, len(candidate_slugs)))
    results = []
    for slug in chosen_slugs:
        detail = fetch_term_detail(slug)
        if detail:
            results.append(detail)

    if count == 1 and results:
        data = results[0]
    else:
        data = results

    raw = request.args.get("raw", "").lower() in ("true", "1", "yes")
    if raw:
        return jsonify(data)

    return success_response(data)

@api_v1.route("/terms/batch", methods=["GET", "POST"])
def batch_terms():
    """
    Batch retrieve multiple terms by IDs or slugs.
    POST body: {"identifiers": ["sharpe-ratio", 42, "ebitda"]}
    GET query: ?ids=sharpe-ratio,42,ebitda
    """
    identifiers = []
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        identifiers = payload.get("identifiers", [])
    else:
        ids_param = request.args.get("ids", "").strip()
        if ids_param:
            identifiers = [x.strip() for x in re.split(r"[,;|\s]+", ids_param) if x.strip()]

    if not identifiers:
        return error_response("No identifiers provided", 400, "Provide a list of IDs or slugs in 'identifiers' array or 'ids' query parameter.")

    found_terms = []
    missing = []
    for ident in identifiers[:100]:  # Cap at 100 per request
        detail = fetch_term_detail(str(ident))
        if detail:
            found_terms.append(detail)
        else:
            missing.append(str(ident))

    meta = {
        "requested": len(identifiers),
        "found": len(found_terms),
        "missing": missing
    }
    return success_response(found_terms, meta=meta)


# ----------------------------------------------------------------------
# 3. Autocomplete / Suggest Endpoint (<5ms response time)
# ----------------------------------------------------------------------

@api_v1.route("/suggest", methods=["GET"])
@api_v1.route("/autocomplete", methods=["GET"])
def autocomplete():
    """
    Ultra-fast autocomplete endpoint designed for search inputs and typeaheads.
    Query Params:
      q: prefix/query (min 1 character)
      limit: max results (default 10, max 30)
    """
    query = request.args.get("q", "").strip()
    if not query:
        return success_response([])

    try:
        limit = min(30, max(1, int(request.args.get("limit", 10))))
    except ValueError:
        limit = 10

    cache = get_cache()
    search_index = cache.get("search_index", [])
    summaries = cache.get("summaries", [])
    norm_query = normalize_text(query)

    suggestions = []
    # 1. Prefix matches on English or Persian term
    for entry in search_index:
        term_en = entry["norm_en"]
        term_fa = entry["norm_fa"]
        if term_en.startswith(norm_query) or term_fa.startswith(norm_query):
            sum_item = summaries[entry["idx"]]
            suggestions.append({
                "id": sum_item.get("id"),
                "slug": sum_item.get("slug"),
                "term_en": sum_item.get("term_en"),
                "term_fa": sum_item.get("term_fa"),
                "category": sum_item.get("category")
            })
            if len(suggestions) >= limit:
                break

    # 2. Substring matches if prefix matches didn't fill limit
    if len(suggestions) < limit:
        seen_ids = {s["id"] for s in suggestions}
        for entry in search_index:
            if entry["id_str"] in seen_ids:
                continue
            term_en = entry["norm_en"]
            term_fa = entry["norm_fa"]
            if (norm_query in term_en) or (norm_query in term_fa):
                sum_item = summaries[entry["idx"]]
                suggestions.append({
                    "id": sum_item.get("id"),
                    "slug": sum_item.get("slug"),
                    "term_en": sum_item.get("term_en"),
                    "term_fa": sum_item.get("term_fa"),
                    "category": sum_item.get("category")
                })
                if len(suggestions) >= limit:
                    break

    return success_response(suggestions)


# ----------------------------------------------------------------------
# 4. Categories Endpoints
# ----------------------------------------------------------------------

@api_v1.route("/categories", methods=["GET"])
def list_categories():
    """List all financial categories with English and Persian names, icon, and term counts."""
    cache = get_cache()
    categories = cache.get("categories", [])
    result = []
    root = request.script_root.rstrip("/")
    for cat in categories:
        name_fa = cat["name_fa"]
        tax = get_category_meta(name_fa)
        cat_id = tax["id"]
        result.append({
            "id": cat_id,
            "name_fa": name_fa,
            "name_en": tax["en"],
            "icon": tax["icon"] or cat.get("icon", "🏷️"),
            "count": cat.get("count", 0),
            "terms_url": f"{root}/api/v1/categories/{cat_id}/terms"
        })
    return success_response(result)

@api_v1.route("/categories/<category_id>", methods=["GET"])
def get_category_detail(category_id: str):
    """Retrieve details and statistics for a specific category."""
    cache = get_cache()
    categories = cache.get("categories", [])
    target_fa = CATEGORY_LOOKUP.get(category_id.lower(), category_id)

    matched = None
    for cat in categories:
        if cat["name_fa"].lower() == target_fa.lower() or cat["name"].lower() == target_fa.lower():
            matched = cat
            break

    if not matched:
        return error_response(f"Category '{category_id}' not found", 404)

    name_fa = matched["name_fa"]
    tax = get_category_meta(name_fa)
    cat_id = tax["id"]
    root = request.script_root.rstrip("/")

    return success_response({
        "id": cat_id,
        "name_fa": name_fa,
        "name_en": tax["en"],
        "icon": tax["icon"] or matched.get("icon", "🏷️"),
        "count": matched.get("count", 0),
        "terms_url": f"{root}/api/v1/categories/{cat_id}/terms"
    })

@api_v1.route("/categories/<category_id>/terms", methods=["GET"])
def get_category_terms(category_id: str):
    """Paginated terms within a specific category."""
    target_fa = CATEGORY_LOOKUP.get(category_id.lower(), category_id)
    cache = get_cache()
    by_category = cache.get("by_category", {})

    if target_fa not in by_category:
        return error_response(f"Category '{category_id}' not found", 404)

    # Delegate to get_terms with category pre-filtered
    # We can inject category into request args
    kwargs = dict(request.args)
    kwargs["category"] = target_fa
    # Re-use terms search logic seamlessly
    with request.environ:
        request.args = type(request.args)(kwargs)
        return get_terms()


# ----------------------------------------------------------------------
# 5. Letters Endpoints
# ----------------------------------------------------------------------

@api_v1.route("/letters", methods=["GET"])
def list_letters():
    """List all letters with term counts."""
    cache = get_cache()
    letters = cache.get("letters", [])
    root = request.script_root.rstrip("/")
    result = []
    for ltr in letters:
        char = ltr["letter"]
        result.append({
            "letter": char,
            "count": ltr["count"],
            "terms_url": f"{root}/api/v1/letters/{char}/terms"
        })
    return success_response(result)

@api_v1.route("/letters/<letter>/terms", methods=["GET"])
def get_letter_terms(letter: str):
    """Paginated terms starting with a specific letter."""
    ltr = letter.strip().upper()
    cache = get_cache()
    by_letter = cache.get("by_letter", {})

    if ltr not in by_letter:
        return error_response(f"Letter '{letter}' not found", 404)

    kwargs = dict(request.args)
    kwargs["letter"] = ltr
    with request.environ:
        request.args = type(request.args)(kwargs)
        return get_terms()


# ----------------------------------------------------------------------
# 6. Quantitative Formulas Endpoint
# ----------------------------------------------------------------------

@api_v1.route("/formulas", methods=["GET"])
def list_formulas():
    """
    List all financial terms with registered LaTeX formulas.
    Covers Sharpe Ratio, Sortino Ratio, Treynor Ratio, CAPM, Black-Scholes, BEP, CAGR, D/E, etc.
    """
    cache = get_cache()
    summaries = cache.get("summaries", [])
    slug_to_summary = {clean_key(s["slug"]): s for s in summaries}

    formula_items = []
    for clean_slug, f_data in FORMULA_DB.items():
        summary_term = slug_to_summary.get(clean_slug)
        formula_items.append({
            "slug": summary_term["slug"] if summary_term else clean_slug,
            "term_en": summary_term["term_en"] if summary_term else clean_slug,
            "term_fa": summary_term["term_fa"] if summary_term else "",
            "category": summary_term["category"] if summary_term else "روش‌های کمی و ریاضیات مالی",
            "category_id": "quant_math",
            "formula_en": f_data.get("formula_en", ""),
            "formula_fa": f_data.get("formula_fa", "")
        })

    formula_items.sort(key=lambda x: x["term_en"].lower())
    return success_response(formula_items, meta={"total_formulas": len(formula_items)})
