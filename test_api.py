# -*- coding: utf-8 -*-
"""
Automated Test Suite for MarketDict REST API v1
"""

import unittest
import json
from app import app

class MarketDictAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()

    def test_cors_headers(self):
        """Verify CORS headers are present on API responses."""
        res = self.client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("Access-Control-Allow-Origin"), "*")
        self.assertIn("GET", res.headers.get("Access-Control-Allow-Methods", ""))
        self.assertEqual(res.headers.get("X-API-Version"), "1.0.0")

    def test_health_check(self):
        """Verify health check endpoint."""
        res = self.client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["service"], "MarketDict API")
        self.assertEqual(data["data"]["status"], "healthy")
        self.assertEqual(data["data"]["total_terms"], 6108)

    def test_stats(self):
        """Verify statistics endpoint."""
        res = self.client.get("/api/v1/stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["total_terms"], 6108)
        self.assertEqual(data["data"]["total_categories"], 32)
        self.assertEqual(data["data"]["formulas_count"], 44)

    def test_openapi_spec(self):
        """Verify OpenAPI 3.0.3 specification."""
        res = self.client.get("/api/v1/openapi.json")
        self.assertEqual(res.status_code, 200)
        spec = res.get_json()
        self.assertEqual(spec["openapi"], "3.0.3")
        self.assertIn("/terms", spec["paths"])
        self.assertIn("/health", spec["paths"])
        self.assertIn("/formulas", spec["paths"])
        self.assertIn("/suggest", spec["paths"])

    def test_swagger_ui_docs(self):
        """Verify Swagger UI docs page."""
        res = self.client.get("/api/v1/docs")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"SwaggerUIBundle", res.data)
        self.assertIn(b"MarketDict REST API", res.data)

    def test_docs_redirect(self):
        """Verify /docs redirects to /api/v1/docs."""
        res = self.client.get("/docs")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/api/v1/docs", res.headers.get("Location", ""))

    def test_docs_guide_page(self):
        """Verify interactive bilingual guide page."""
        res = self.client.get("/docs/guide")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"MarketDict REST API", res.data)
        self.assertIn(b"lang-fa", res.data)
        self.assertIn(b"lang-en", res.data)

    def test_terms_list_pagination(self):
        """Verify terms listing with pagination."""
        res = self.client.get("/api/v1/terms?page=1&limit=15")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 15)
        self.assertEqual(data["pagination"]["page"], 1)
        self.assertEqual(data["pagination"]["limit"], 15)
        self.assertEqual(data["pagination"]["total"], 6108)
        self.assertTrue(data["pagination"]["has_next"])

    def test_terms_search_english(self):
        """Verify search in English."""
        res = self.client.get("/api/v1/terms?q=Sharpe+Ratio")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)
        top_term = data["data"][0]
        self.assertIn("Sharpe", top_term["term_en"])

    def test_terms_search_persian(self):
        """Verify search in Persian with text normalization."""
        res = self.client.get("/api/v1/terms?q=%D8%B4%D8%A7%D8%B1%D9%BE")  # شارپ
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)

    def test_terms_filter_category_slug(self):
        """Verify category filtering by slug (e.g. crypto)."""
        res = self.client.get("/api/v1/terms?category=crypto&limit=10")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)
        for term in data["data"]:
            self.assertEqual(term["category_id"], "crypto")

    def test_terms_filter_has_formula(self):
        """Verify filtering by terms with formulas."""
        res = self.client.get("/api/v1/terms?has_formula=true&limit=10")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)
        for term in data["data"]:
            self.assertTrue(term["has_formula"])

    def test_terms_field_projection(self):
        """Verify field projection (sparse fieldsets)."""
        res = self.client.get("/api/v1/terms?limit=5&fields=id,slug,term_en,term_fa")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        item = data["data"][0]
        self.assertIn("id", item)
        self.assertIn("slug", item)
        self.assertIn("term_en", item)
        self.assertIn("term_fa", item)
        self.assertNotIn("definition_fa", item)

    def test_term_detail_lookup_by_slug(self):
        """Verify retrieving term detail by slug with formula enrichment."""
        res = self.client.get("/api/v1/terms/sharperatio")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        term = data["data"]
        self.assertEqual(term["slug"], "sharperatio")
        self.assertIsNotNone(term["formula"])
        self.assertIn("Sharpe Ratio", term["formula"]["formula_en"])
        self.assertIn("نسبت شارپ", term["formula"]["formula_fa"])

    def test_term_detail_lookup_by_id(self):
        """Verify retrieving term detail by numeric ID."""
        res = self.client.get("/api/v1/terms/461")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["id"], 461)

    def test_term_not_found(self):
        """Verify 404 error when term does not exist."""
        res = self.client.get("/api/v1/terms/non-existent-random-term-12345")
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["error"]["code"], 404)

    def test_random_term(self):
        """Verify random term retrieval."""
        res = self.client.get("/api/v1/terms/random")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("term_en", data["data"])

    def test_random_terms_count(self):
        """Verify random multiple terms retrieval."""
        res = self.client.get("/api/v1/terms/random?count=3")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 3)

    def test_suggest_autocomplete(self):
        """Verify autocomplete prefix search."""
        res = self.client.get("/api/v1/suggest?q=bit&limit=5")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(len(data["data"]), 0)
        item = data["data"][0]
        self.assertIn("id", item)
        self.assertIn("slug", item)
        self.assertIn("term_en", item)

    def test_categories_endpoints(self):
        """Verify categories list, detail, and category terms."""
        res = self.client.get("/api/v1/categories")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 32)

        # Test single category
        res2 = self.client.get("/api/v1/categories/crypto")
        self.assertEqual(res2.status_code, 200)
        cat_data = res2.get_json()
        self.assertEqual(cat_data["data"]["id"], "crypto")

    def test_letters_endpoints(self):
        """Verify letters list and letter terms."""
        res = self.client.get("/api/v1/letters")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 27)

    def test_formulas_endpoint(self):
        """Verify financial formulas endpoint."""
        res = self.client.get("/api/v1/formulas")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 44)
        first_f = data["data"][0]
        self.assertIn("formula_en", first_f)
        self.assertIn("formula_fa", first_f)

    def test_batch_terms_post(self):
        """Verify batch retrieval with POST body."""
        payload = {"identifiers": ["sharperatio", "461", "non-existent-xyz"]}
        res = self.client.post("/api/v1/terms/batch", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["meta"]["requested"], 3)
        self.assertEqual(data["meta"]["found"], 2)
        self.assertIn("non-existent-xyz", data["meta"]["missing"])

    def test_backward_compatibility_existing_routes(self):
        """Verify existing web frontend API endpoints are 100% functional."""
        res = self.client.get("/api/stats")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["total_terms"], 6108)

        res2 = self.client.get("/api/terms?q=stock")
        self.assertEqual(res2.status_code, 200)
        self.assertIn("terms", res2.get_json())

if __name__ == "__main__":
    unittest.main()
