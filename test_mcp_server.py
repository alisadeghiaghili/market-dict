"""Verification suite for MarketDict MCP Server."""

import unittest

import mcp_server
from mcp_server import server


class MarketDictMCPServerTestCase(unittest.IsolatedAsyncioTestCase):
    """Test suite covering tools, resources, and prompts in MarketDict MCP server."""

    async def test_tools_list(self):
        tools = await server.list_tools()
        tool_names = [t.name for t in tools]
        expected = [
            "search_terms",
            "suggest_terms",
            "get_term_details",
            "get_financial_formula",
            "list_all_formulas",
            "list_categories",
            "list_letters",
            "get_random_term",
            "get_dictionary_stats",
        ]
        for name in expected:
            self.assertIn(name, tool_names)

    async def test_resources_list(self):
        resources = await server.list_resources()
        resource_uris = [r.uri for r in resources]
        self.assertIn("marketdict://categories", resource_uris)
        self.assertIn("marketdict://stats", resource_uris)
        self.assertIn("marketdict://formulas", resource_uris)

    async def test_prompts_list(self):
        prompts = await server.list_prompts()
        prompt_names = [p.name for p in prompts]
        self.assertIn("explain_financial_term", prompt_names)
        self.assertIn("compare_financial_terms", prompt_names)

    def test_search_terms_english(self):
        res_en = mcp_server.search_terms(query="inflation", limit=3)
        self.assertGreater(res_en["total"], 0)
        self.assertLessEqual(len(res_en["terms"]), 3)

    def test_search_terms_persian(self):
        res_fa = mcp_server.search_terms(query="تورم", limit=3)
        self.assertGreater(res_fa["total"], 0)
        self.assertLessEqual(len(res_fa["terms"]), 3)

    def test_suggest_terms(self):
        suggs = mcp_server.suggest_terms(prefix="shar", limit=4)
        self.assertGreater(len(suggs), 0)
        self.assertLessEqual(len(suggs), 4)

    def test_get_term_details_with_formula(self):
        details = mcp_server.get_term_details("sharpe-ratio")
        self.assertTrue(details["found"])
        self.assertTrue(details["has_formula"])
        self.assertTrue(details["has_deep_content"])
        self.assertGreater(len(details["sections"]), 0)

    def test_get_financial_formula(self):
        formula = mcp_server.get_financial_formula("ebit")
        self.assertTrue(formula["found"])
        self.assertEqual(formula["key"], "ebit")
        self.assertIn("EBIT", formula["formula_latex_en"])

        formula_roe = mcp_server.get_financial_formula("roe")
        self.assertTrue(formula_roe["found"])
        self.assertEqual(formula_roe["key"], "returnonequity")

    def test_list_categories(self):
        cats = mcp_server.list_categories()
        self.assertGreaterEqual(len(cats), 20)

    def test_get_dictionary_stats(self):
        stats = mcp_server.get_dictionary_stats()
        self.assertGreater(stats.get("total_terms", 0), 6000)
        self.assertGreater(stats.get("total_formulas", 0), 30)

    def test_get_random_term(self):
        rand_term = mcp_server.get_random_term(only_deep_enriched=True)
        self.assertTrue(bool(rand_term.get("term_en")))
        self.assertTrue(bool(rand_term.get("term_fa")))

    def test_explain_financial_term_prompt(self):
        prompt_txt = mcp_server.explain_financial_term(term="CAPM", language="fa")
        self.assertIn("CAPM", prompt_txt)
        self.assertGreater(len(prompt_txt), 100)


if __name__ == "__main__":
    unittest.main()
