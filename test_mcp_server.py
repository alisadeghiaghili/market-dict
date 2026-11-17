#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification suite for MarketDict MCP Server
"""

import sys
import asyncio
import json

import mcp_server
from mcp_server import server

async def run_tests():
    print("=" * 60)
    print("MarketDict MCP Server Verification Suite")
    print("=" * 60)

    # 1. Tools list
    tools = await server.list_tools()
    tool_names = [t.name for t in tools]
    print(f"\n[1] Registered Tools ({len(tools)}):")
    for name in tool_names:
        print(f"  - {name}")
    assert "search_terms" in tool_names
    assert "suggest_terms" in tool_names
    assert "get_term_details" in tool_names
    assert "get_financial_formula" in tool_names
    assert "list_all_formulas" in tool_names
    assert "list_categories" in tool_names
    assert "list_letters" in tool_names
    assert "get_random_term" in tool_names
    assert "get_dictionary_stats" in tool_names

    # 2. Resources list
    resources = await server.list_resources()
    print(f"\n[2] Registered Resources ({len(resources)}):")
    for r in resources:
        print(f"  - {r.uri}")

    # 3. Prompts list
    prompts = await server.list_prompts()
    prompt_names = [p.name for p in prompts]
    print(f"\n[3] Registered Prompts ({len(prompts)}):")
    for name in prompt_names:
        print(f"  - {name}")
    assert "explain_financial_term" in prompt_names
    assert "compare_financial_terms" in prompt_names

    # 4. Test tool search_terms (English)
    print("\n[4] Testing search_terms('inflation'):")
    res_en = mcp_server.search_terms(query="inflation", limit=3)
    print(f"  Matches: {res_en['total']}, Returned: {len(res_en['terms'])}")
    for t in res_en["terms"]:
        print(f"    * {t['term_en']} ({t['term_fa']}) - Cat: {t['category']}")
    assert res_en["total"] > 0

    # 5. Test tool search_terms (Persian)
    print("\n[5] Testing search_terms('تورم'):")
    res_fa = mcp_server.search_terms(query="تورم", limit=3)
    print(f"  Matches: {res_fa['total']}, Returned: {len(res_fa['terms'])}")
    for t in res_fa["terms"]:
        print(f"    * {t['term_en']} ({t['term_fa']}) - Cat: {t['category']}")
    assert res_fa["total"] > 0

    # 5b. Test tool suggest_terms
    print("\n[5b] Testing suggest_terms('shar'):")
    suggs = mcp_server.suggest_terms(prefix="shar", limit=4)
    print(f"  Suggestions count: {len(suggs)}")
    for s in suggs:
        print(f"    * {s['term_en']} ({s['term_fa']})")
    assert len(suggs) > 0

    # 6. Test tool get_term_details with formula
    print("\n[6] Testing get_term_details('sharpe-ratio'):")
    details = mcp_server.get_term_details("sharpe-ratio")
    assert details["found"] is True
    print(f"  Found: {details['term_en']} | Category: {details['category']}")
    print(f"  Has formula: {details['has_formula']}")
    print(f"  Has deep sections: {details['has_deep_content']} ({len(details['sections'])} sections)")
    assert details["has_formula"] is True

    # 7. Test tool get_financial_formula
    print("\n[7] Testing get_financial_formula('ebit') and 'roe':")
    formula = mcp_server.get_financial_formula("ebit")
    assert formula["found"] is True
    print(f"  Key: {formula['key']}")
    print(f"  Formula snippet: {formula['formula_latex_en'][:60]}...")
    formula_roe = mcp_server.get_financial_formula("roe")
    assert formula_roe["found"] is True
    print(f"  ROE Key: {formula_roe['key']}")

    # 8. Test tool list_categories
    print("\n[8] Testing list_categories():")
    cats = mcp_server.list_categories()
    print(f"  Total categories: {len(cats)}")
    for c in cats[:4]:
        print(f"    {c['icon']} {c['name_fa']} ({c['name_en']}): {c['count']} terms")
    assert len(cats) >= 20

    # 9. Test tool get_dictionary_stats
    print("\n[9] Testing get_dictionary_stats():")
    stats = mcp_server.get_dictionary_stats()
    print(f"  Total terms: {stats.get('total_terms')}")
    print(f"  Total formulas: {stats.get('total_formulas')}")
    assert stats.get("total_terms", 0) > 6000

    # 10. Test tool get_random_term
    print("\n[10] Testing get_random_term():")
    rand_term = mcp_server.get_random_term(only_deep_enriched=True)
    print(f"  Random term: {rand_term.get('term_en')} ({rand_term.get('term_fa')})")

    # 11. Test prompt generation
    print("\n[11] Testing explain_financial_term prompt:")
    prompt_txt = mcp_server.explain_financial_term(term="CAPM", language="fa")
    assert "CAPM" in prompt_txt
    print(f"  Prompt length: {len(prompt_txt)} characters")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! 🚀")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_tests())
