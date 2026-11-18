#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarketDict MCP Server
Model Context Protocol (MCP) server for MarketDict - Bilingual Financial Terms Dictionary & Knowledge Base.
Provides AI assistants (Claude, Cursor, Antigravity, etc.) with real-time access to:
- 6,108 financial terms in English and Persian
- Intelligent bilingual search with Persian text normalization
- Standardized LaTeX mathematical formulas and variable definitions
- 28 taxonomy categories (Crypto, Derivatives, Quant, Corporate Finance, etc.)
- Deep comprehensive multi-section financial articles and key takeaways
"""

import os
import sys
import json
import random
import logging
import argparse
from typing import List, Dict, Any, Optional

# Configure stderr-only logging so stdout remains pure JSON-RPC for stdio transport
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("marketdict-mcp")

# MCP Server Import (Supports both mcp 2.x and 1.x)
try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer
    except ImportError:
        logger.error("The 'mcp' package is required. Install with: pip install mcp")
        sys.exit(1)

# Import MarketDict engines and data helpers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import app
from formula_registry import FORMULA_DB
from categories_engine import TAXONOMY, TAXONOMY_BY_FA, normalize_category

FORMULA_ALIASES = {
    "roe": "returnonequity",
    "roa": "returnonassets",
    "sharpe": "sharperatio",
    "sortino": "sortinoratio",
    "treynor": "treynorratio",
    "fcf": "freecashflow",
    "capex": "capitalexpenditure",
    "ev": "enterprisevalue",
    "bep": "breakevenanalysis",
    "cpi": "consumerpriceindex",
    "de": "debtequityratio",
    "d/e": "debtequityratio",
    "ir": "informationratio",
    "ltv": "loantovalue",
    "lcr": "liquidity-coverage-ratio",
}

# Initialize Server
server = MCPServer(
    name="MarketDict",
    instructions=(
        "MarketDict is a bilingual (English & Persian) financial dictionary and encyclopedia "
        "containing 6,108 financial terms, 28 taxonomy categories, LaTeX formulas, and deep articles. "
        "Use search_terms to find terms, get_term_details to fetch comprehensive definitions, "
        "get_financial_formula for LaTeX math, and list_categories for taxonomy exploration."
    )
)

# Ensure cache and database are warm
logger.info("Initializing MarketDict cache and indexes...")
app.ensure_cache()
logger.info("MarketDict ready. Total terms: %s", app._CACHE.get("stats", {}).get("total_terms", 0))


def _clean_key(text: str) -> str:
    """Normalize slug or query string for exact key lookup."""
    return app.clean_key(text)


def _resolve_term_slug(identifier: str) -> Optional[str]:
    """Resolve an identifier (slug, title, ID, or clean key) to a canon slug."""
    app.ensure_cache()
    if not identifier:
        return None

    raw = identifier.strip().lower().replace(".asp", "")
    lookup = app._CACHE.get("lookup_keys", {})

    # 1. Direct lookup
    if raw in lookup:
        return lookup[raw]

    # 2. Clean key lookup
    cleaned = _clean_key(raw)
    if cleaned in lookup:
        return lookup[cleaned]

    # 3. Search index match by title (English or Persian)
    norm_ident = app.normalize_text(identifier)
    for entry in app._CACHE.get("search_index", []):
        if entry["norm_en"] == raw or entry["norm_en"] == norm_ident:
            return entry["slug"]
        if entry["norm_fa"] == norm_ident or entry["norm_fa"] == raw:
            return entry["slug"]

    # 4. Partial slug fallback
    for slug in lookup.values():
        if raw == slug.lower() or cleaned == _clean_key(slug):
            return slug

    return None


def _fetch_term_data(slug: str) -> Optional[Dict[str, Any]]:
    """Retrieve full term JSON object from SQLite database."""
    app.ensure_cache()
    if not app._DB_CONN:
        return None

    cur = app._DB_CONN.cursor()
    cur.execute("SELECT full_json FROM terms WHERE slug = ?", (slug,))
    row = cur.fetchone()
    if not row:
        return None

    try:
        data = json.loads(row[0])
    except Exception as e:
        logger.warning(f"Error parsing JSON for term {slug}: {e}")
        return None

    # Attach mathematical formula if registered
    clean_s = _clean_key(slug)
    if slug in FORMULA_DB:
        data["formula"] = FORMULA_DB[slug]
    elif clean_s in FORMULA_DB:
        data["formula"] = FORMULA_DB[clean_s]

    return data


# ==============================================================================
# MCP Tools
# ==============================================================================

@server.tool()
def search_terms(
    query: str,
    category: Optional[str] = None,
    letter: Optional[str] = None,
    limit: int = 10,
    page: int = 1
) -> Dict[str, Any]:
    """
    Search 6,108 bilingual (English & Persian) financial terms with fuzzy matching and Persian text normalization.

    Args:
        query: Search query in English or Persian (e.g. 'inflation', 'تورم', 'sharpe', 'صندوق سرمایه‌گذاری').
        category: Optional category filter (e.g. 'ارزهای دیجیتال و بلاک‌چین', 'crypto', 'ابزارهای مشتقه').
        letter: Optional alphabetical section filter ('#' or 'A' through 'Z').
        limit: Max number of results to return (1-50, default 10).
        page: Page number for pagination (default 1).

    Returns:
        A dictionary containing total matching terms, pagination info, and a list of term summaries.
    """
    app.ensure_cache()
    limit = max(1, min(limit, 50))
    page = max(1, page)

    search_index = app._CACHE["search_index"]
    summaries = app._CACHE["summaries"]
    by_letter = app._CACHE["by_letter"]
    by_category = app._CACHE["by_category"]

    # Normalize letter filter
    ltr = letter.strip().upper() if letter else ""

    # Normalize category filter
    cat_filter = normalize_category(category)["fa"] if category else ""

    # Narrow candidate indices
    if ltr and ltr != "ALL" and ltr in by_letter:
        candidate_indices = by_letter[ltr]
        if cat_filter and cat_filter in by_category:
            candidate_indices = [i for i in candidate_indices if search_index[i]["category"] == cat_filter]
    elif cat_filter and cat_filter in by_category:
        candidate_indices = by_category[cat_filter]
    else:
        candidate_indices = range(len(search_index))

    # Scoring search
    if query and query.strip():
        norm_query = app.normalize_text(query)
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
    page_indices = matched_indices[start_idx:end_idx]

    results = []
    for i in page_indices:
        s = summaries[i]
        slug = s.get("slug", "")
        clean_s = _clean_key(slug)
        has_formula = (slug in FORMULA_DB) or (clean_s in FORMULA_DB)
        results.append({
            "id": s.get("id"),
            "slug": slug,
            "term_en": s.get("term_en", ""),
            "term_fa": s.get("term_fa", ""),
            "letter": s.get("letter", ""),
            "category": s.get("category", ""),
            "category_en": s.get("category_en", ""),
            "definition_en": s.get("definition_en", ""),
            "definition_fa": s.get("definition_fa", ""),
            "takeaways_en": s.get("takeaways_en", []),
            "takeaways_fa": s.get("takeaways_fa", []),
            "has_deep_content": s.get("has_deep", False),
            "has_formula": has_formula,
            "url": s.get("url", "")
        })

    return {
        "query": query,
        "total": total_matches,
        "page": page,
        "limit": limit,
        "has_more": end_idx < total_matches,
        "terms": results
    }


@server.tool()
def suggest_terms(prefix: str, limit: int = 8) -> List[Dict[str, Any]]:
    """
    Ultra-fast autocomplete prefix search for financial terms (<5ms).

    Args:
        prefix: Starting letters or phrase in English or Persian (e.g. 'infl', 'تور', 'shar', 'der').
        limit: Max number of suggestions (1-20, default 8).

    Returns:
        List of matching term suggestions with slug, English title, Persian title, and category.
    """
    app.ensure_cache()
    if not prefix or not prefix.strip():
        return []

    norm_prefix = app.normalize_text(prefix)
    limit = max(1, min(limit, 20))
    search_index = app._CACHE["search_index"]
    summaries = app._CACHE["summaries"]

    matches = []
    # 1. Exact startswith title
    for i, entry in enumerate(search_index):
        if entry["norm_en"].startswith(norm_prefix) or entry["norm_fa"].startswith(norm_prefix):
            matches.append((100, i))
            if len(matches) >= limit * 2:
                break

    # 2. Substring in title if needed
    if len(matches) < limit:
        for i, entry in enumerate(search_index):
            if i in [m[1] for m in matches]:
                continue
            if norm_prefix in entry["norm_en"] or norm_prefix in entry["norm_fa"]:
                matches.append((50, i))
                if len(matches) >= limit:
                    break

    matches.sort(key=lambda x: -x[0])
    suggestions = []
    for _, idx in matches[:limit]:
        s = summaries[idx]
        suggestions.append({
            "slug": s.get("slug"),
            "term_en": s.get("term_en"),
            "term_fa": s.get("term_fa"),
            "category": s.get("category"),
            "category_en": s.get("category_en", "")
        })

    return suggestions


@server.tool()
def get_term_details(term_identifier: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive bilingual details for a specific financial term.
    Includes English/Persian definitions, key takeaways, bottom line, deep article sections,
    and standardized LaTeX mathematical formulas where available.

    Args:
        term_identifier: Term slug (e.g. 'sharpe-ratio'), English name ('Sharpe Ratio'), Persian name ('نسبت شارپ'), or numerical ID.

    Returns:
        Full bilingual term data object or error details if not found.
    """
    app.ensure_cache()
    slug = _resolve_term_slug(term_identifier)

    if not slug:
        # Provide suggestions for similar terms
        search_res = search_terms(term_identifier, limit=3)
        suggestions = [t["term_en"] for t in search_res.get("terms", [])]
        return {
            "found": False,
            "error": f"Term '{term_identifier}' not found.",
            "suggestions": suggestions
        }

    data = _fetch_term_data(slug)
    if not data:
        return {
            "found": False,
            "error": f"Detailed data for slug '{slug}' could not be loaded."
        }

    # Format response cleanly
    has_deep = bool(data.get("sections") or data.get("deep_enriched"))
    formula_obj = data.get("formula")

    return {
        "found": True,
        "id": data.get("id"),
        "slug": data.get("slug", slug),
        "term_en": data.get("term_en", ""),
        "term_fa": data.get("term_fa", ""),
        "letter": data.get("letter", ""),
        "category": data.get("category", ""),
        "category_fa": data.get("category_fa", data.get("category", "")),
        "category_en": data.get("category_en", ""),
        "definition_en": data.get("definition_en", ""),
        "definition_fa": data.get("definition_fa", ""),
        "takeaways_en": data.get("takeaways_en", []),
        "takeaways_fa": data.get("takeaways_fa", []),
        "bottom_line_en": data.get("bottom_line_en", ""),
        "bottom_line_fa": data.get("bottom_line_fa", ""),
        "has_formula": bool(formula_obj),
        "formula": formula_obj,
        "has_deep_content": has_deep,
        "sections": data.get("sections", []),
        "investopedia_url": data.get("url", "")
    }


@server.tool()
def get_financial_formula(term: str) -> Dict[str, Any]:
    """
    Retrieve the standardized LaTeX mathematical formula and variable definitions for financial concepts
    (e.g. Sharpe Ratio, Sortino, CAPM, ROE, ROA, DuPont Analysis, Debt-to-Equity, EBIT, Free Cash Flow, etc.).

    Args:
        term: Term name, slug, or acronym (e.g. 'sharpe-ratio', 'roe', 'roa', 'ebit', 'debtequityratio', 'cagr').

    Returns:
        A dictionary containing English and Persian LaTeX expressions and variable definitions.
    """
    clean_t = _clean_key(term)
    raw_lower = term.strip().lower()
    matched_key = None

    # 1. Alias lookup
    if raw_lower in FORMULA_ALIASES:
        matched_key = FORMULA_ALIASES[raw_lower]
    elif clean_t in FORMULA_ALIASES:
        matched_key = FORMULA_ALIASES[clean_t]
    # 2. Direct key lookup
    elif term in FORMULA_DB:
        matched_key = term
    elif clean_t in FORMULA_DB:
        matched_key = clean_t
    else:
        # 3. Check resolved slug
        slug = _resolve_term_slug(term)
        if slug:
            if slug in FORMULA_DB:
                matched_key = slug
            elif _clean_key(slug) in FORMULA_DB:
                matched_key = _clean_key(slug)

    # 4. Substring fallback among keys
    if not matched_key:
        for k in FORMULA_DB.keys():
            if clean_t and (clean_t in k or k in clean_t):
                matched_key = k
                break

    if not matched_key:
        available = list(FORMULA_DB.keys())[:12]
        return {
            "found": False,
            "error": f"No mathematical formula registered for '{term}'.",
            "available_examples": available,
            "total_registered_formulas": len(FORMULA_DB)
        }

    formula_entry = FORMULA_DB[matched_key]
    term_details = None
    slug = _resolve_term_slug(matched_key) or matched_key
    if slug:
        term_data = _fetch_term_data(slug)
        if term_data:
            term_details = {
                "term_en": term_data.get("term_en"),
                "term_fa": term_data.get("term_fa"),
                "category": term_data.get("category"),
                "url": term_data.get("url")
            }

    return {
        "found": True,
        "key": matched_key,
        "term_info": term_details,
        "formula_latex_en": formula_entry.get("formula_en"),
        "formula_latex_fa": formula_entry.get("formula_fa")
    }


@server.tool()
def list_all_formulas(query: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all registered financial mathematical formulas in MarketDict.

    Args:
        query: Optional string to filter formula names or keys.

    Returns:
        List of registered formulas with their key, English formula snippet, and related term.
    """
    results = []
    q = query.lower().strip() if query else None

    for key, val in FORMULA_DB.items():
        if q and q not in key and q not in val.get("formula_en", "").lower():
            continue

        slug = _resolve_term_slug(key) or key
        t_data = _fetch_term_data(slug) if slug else None

        results.append({
            "key": key,
            "slug": slug,
            "term_en": t_data.get("term_en", key.title()) if t_data else key.title(),
            "term_fa": t_data.get("term_fa", "") if t_data else "",
            "formula_snippet": val.get("formula_en", "")[:120]
        })

    results.sort(key=lambda x: x["key"])
    return results


@server.tool()
def list_categories() -> List[Dict[str, Any]]:
    """
    List all financial domains and categories in the MarketDict taxonomy (including primary and variant categories).

    Returns:
        List of categories with ID, Persian name, English name, icon, and term counts.
    """
    app.ensure_cache()
    cached_cats = {c["name"]: c["count"] for c in app._CACHE.get("categories", [])}

    output = []
    for item in TAXONOMY:
        cat_fa = item["fa"]
        count = cached_cats.get(cat_fa, 0)
        output.append({
            "id": item["id"],
            "name_fa": cat_fa,
            "name_en": item["en"],
            "icon": item["icon"],
            "count": count
        })

    output.sort(key=lambda x: -x["count"])
    return output


@server.tool()
def list_letters() -> List[Dict[str, Any]]:
    """
    List all alphabetical sections ('#' and 'A' to 'Z') with their term count.

    Returns:
        List of letter sections and counts.
    """
    app.ensure_cache()
    return app._CACHE.get("letters", [])


@server.tool()
def get_random_term(
    category: Optional[str] = None,
    only_deep_enriched: bool = True
) -> Dict[str, Any]:
    """
    Get a random financial term for educational purposes, daily learning, or quizzes.

    Args:
        category: Optional category filter.
        only_deep_enriched: If True, select only from terms with comprehensive multi-section articles.

    Returns:
        Full details of a randomly selected term.
    """
    app.ensure_cache()
    summaries = app._CACHE.get("summaries", [])
    if not summaries:
        return {"error": "Dictionary is empty."}

    candidates = summaries
    if only_deep_enriched:
        candidates = [s for s in candidates if s.get("has_deep")]

    if category:
        canon_fa = normalize_category(category)["fa"]
        candidates = [s for s in candidates if s.get("category") == canon_fa]

    if not candidates:
        candidates = summaries

    selected = random.choice(candidates)
    return get_term_details(selected["slug"])


@server.tool()
def get_dictionary_stats() -> Dict[str, Any]:
    """
    Get high-level summary statistics of the MarketDict database.

    Returns:
        Dictionary statistics including total terms, deep articles, categories, and letters.
    """
    app.ensure_cache()
    stats = dict(app._CACHE.get("stats", {}))
    stats["total_formulas"] = len(FORMULA_DB)
    stats["languages"] = ["English", "Persian"]
    return stats


# ==============================================================================
# MCP Resources
# ==============================================================================

@server.resource("marketdict://categories")
def get_resource_categories() -> str:
    """Resource returning the complete 28-category financial taxonomy."""
    return json.dumps(list_categories(), ensure_ascii=False, indent=2)


@server.resource("marketdict://stats")
def get_resource_stats() -> str:
    """Resource returning MarketDict database statistics."""
    return json.dumps(get_dictionary_stats(), ensure_ascii=False, indent=2)


@server.resource("marketdict://formulas")
def get_resource_formulas() -> str:
    """Resource returning all registered financial mathematical formulas."""
    return json.dumps(list_all_formulas(), ensure_ascii=False, indent=2)


@server.resource("marketdict://terms/{slug}")
def get_resource_term(slug: str) -> str:
    """Resource returning full JSON representation of a specific financial term."""
    data = get_term_details(slug)
    return json.dumps(data, ensure_ascii=False, indent=2)


# ==============================================================================
# MCP Prompts
# ==============================================================================

@server.prompt()
def explain_financial_term(
    term: str,
    language: str = "bilingual",
    target_audience: str = "general"
) -> str:
    """
    Generates a prompt to explain a financial concept using authentic definitions and formulas from MarketDict.

    Args:
        term: The financial concept to explain (e.g. 'Sharpe Ratio', 'تورم', 'WACC').
        language: Output language ('fa' for Persian, 'en' for English, or 'bilingual').
        target_audience: Audience level ('beginner', 'general', 'advanced', 'student').
    """
    details = get_term_details(term)
    data_context = json.dumps(details, ensure_ascii=False, indent=2)

    return (
        f"You are a CFA-certified bilingual financial educator. "
        f"Explain the financial concept '{term}' for a '{target_audience}' audience in {language} language.\n\n"
        f"Here is the verified data and definition from MarketDict:\n"
        f"```json\n{data_context}\n```\n\n"
        f"Instructions:\n"
        f"1. Begin with a clear, concise definition in both English and Persian if requested.\n"
        f"2. Detail the key takeaways and why this concept matters in real-world markets.\n"
        f"3. If a mathematical formula exists in the data, present the LaTeX formula and clearly define each variable.\n"
        f"4. Provide a practical real-world numerical example illustrating its application.\n"
        f"5. End with common pitfalls or limitations."
    )


@server.prompt()
def compare_financial_terms(
    term1: str,
    term2: str,
    language: str = "bilingual"
) -> str:
    """
    Generates a comparative analysis prompt between two financial concepts.

    Args:
        term1: First term (e.g. 'Sharpe Ratio', 'APR').
        term2: Second term (e.g. 'Sortino Ratio', 'APY').
        language: Target response language ('fa', 'en', 'bilingual').
    """
    d1 = get_term_details(term1)
    d2 = get_term_details(term2)

    return (
        f"Compare and contrast the two financial concepts: '{term1}' and '{term2}'.\n\n"
        f"Reference Data for '{term1}':\n"
        f"```json\n{json.dumps(d1, ensure_ascii=False, indent=2)}\n```\n\n"
        f"Reference Data for '{term2}':\n"
        f"```json\n{json.dumps(d2, ensure_ascii=False, indent=2)}\n```\n\n"
        f"Instructions:\n"
        f"1. Provide a side-by-side comparison table (Definition, Primary Use, Key Formula, Risk Metric).\n"
        f"2. Explain when an investor or analyst should use {term1} versus {term2}.\n"
        f"3. Highlight critical mathematical differences or assumptions.\n"
        f"4. Respond in {language}."
    )


# ==============================================================================
# CLI Runner
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="MarketDict Model Context Protocol (MCP) Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (default: stdio)"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for SSE / HTTP transport (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE / HTTP transport (default: 8000)")
    args = parser.parse_args()

    logger.info("Starting MarketDict MCP server using '%s' transport...", args.transport)

    if args.transport == "stdio":
        server.run(transport="stdio")
    elif args.transport == "sse":
        server.run(transport="sse", host=args.host, port=args.port)
    elif args.transport == "streamable-http":
        server.run(transport="streamable-http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
