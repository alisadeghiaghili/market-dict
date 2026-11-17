# -*- coding: utf-8 -*-
"""
MarketDict API - Developer Usage Example
Demonstrates how third-party applications consume MarketDict REST API.
"""

import sys
import os

# Add parent directory to path so marketdict_client can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marketdict_client import MarketDict, MarketDictError

def main():
    print("==================================================")
    print("🚀 MarketDict API Client Demo")
    print("==================================================\n")

    client = MarketDict(base_url="http://localhost:5000/api/v1")

    # 1. Health & Statistics
    print("1️⃣ Checking Service Health & Stats...")
    try:
        health = client.health()
        print(f"   Status:    {health['status']}")
        print(f"   Total:     {health['total_terms']} financial terms")
        print(f"   Database:  {health['database']}")
    except MarketDictError as e:
        print(f"   ⚠️ Could not reach server at http://localhost:5000: {e}")
        print("   Make sure 'python app.py' is running!")
        return

    stats = client.stats()
    print(f"   Categories: {stats['total_categories']}")
    print(f"   Formulas:   {stats['formulas_count']} quantitative financial formulas\n")

    # 2. Bilingual Search
    print("2️⃣ Bilingual Search Query: 'نسبت شارپ' (Sharpe Ratio)...")
    res = client.search(query="نسبت شارپ", limit=3)
    for term in res["data"]:
        print(f"   • {term['term_en']} ({term['term_fa']}) - {term['category_icon']} {term['category_fa']}")
    print()

    # 3. Autocomplete / Instant Suggestions (<5ms)
    print("3️⃣ Autocomplete Suggestions for prefix: 'bit'...")
    suggestions = client.suggest("bit", limit=4)
    for s in suggestions:
        print(f"   👉 [{s['id']}] {s['term_en']} -> {s['term_fa']}")
    print()

    # 4. Term Details with Formula
    print("4️⃣ Retrieving Term Details for 'sharperatio'...")
    term = client.get_term("sharperatio")
    print(f"   English Title: {term['term_en']}")
    print(f"   Persian Title: {term['term_fa']}")
    print(f"   Category:      {term['category_fa']} ({term['category_en']})")
    if term.get("formula"):
        print(f"   Formula (LaTeX):\n   {term['formula']['formula_en']}")
    print()

    # 5. Financial Formulas
    print("5️⃣ Listing Financial Formulas (e.g. CAPM, Sortino, D/E)...")
    formulas = client.get_formulas()
    print(f"   Found {len(formulas)} registered financial formulas.")
    for f in formulas[:4]:
        print(f"   📐 {f['term_en']} ({f['term_fa']}): {f['slug']}")
    print()

    # 6. Random Term of the Day
    print("6️⃣ Getting Random Financial Term for Today...")
    random_term = client.get_random(has_deep=True)
    print(f"   🎲 {random_term['term_en']} | {random_term['term_fa']}")
    print(f"   Definition: {random_term['definition_fa'][:120]}...\n")

    print("==================================================")
    print("✅ All API tests completed successfully!")
    print("==================================================")

if __name__ == "__main__":
    main()
