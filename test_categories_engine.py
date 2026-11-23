"""Unit tests for Market-Dict Categories Engine and taxonomy classifiers."""

import unittest

from categories_engine import (
    CATEGORY_ALIASES,
    TAXONOMY,
    TAXONOMY_BY_FA,
    TAXONOMY_BY_ID,
    classify_term,
    normalize_category,
)


class CategoriesEngineTestCase(unittest.TestCase):
    """Test suite for taxonomy normalization and multi-priority term classification."""

    def test_taxonomy_data_integrity(self):
        self.assertEqual(len(TAXONOMY), 28)
        for cat in TAXONOMY:
            self.assertIn("id", cat)
            self.assertIn("fa", cat)
            self.assertIn("en", cat)
            self.assertIn("icon", cat)
            self.assertIn("regex", cat)
            self.assertIn(cat["fa"], TAXONOMY_BY_FA)
            self.assertIn(cat["id"], TAXONOMY_BY_ID)

    def test_normalize_category_exact_fa(self):
        cat = normalize_category("ارزهای دیجیتال و بلاک‌چین")
        self.assertEqual(cat["id"], "crypto")

    def test_normalize_category_by_id(self):
        cat = normalize_category("crypto")
        self.assertEqual(cat["id"], "crypto")
        cat_upper = normalize_category("TECHNICAL_ANALYSIS")
        self.assertEqual(cat_upper["id"], "technical_analysis")

    def test_normalize_category_by_english_name(self):
        cat = normalize_category("Cryptocurrency & Blockchain")
        self.assertEqual(cat["id"], "crypto")

    def test_normalize_category_legacy_alias(self):
        first_alias = next(iter(CATEGORY_ALIASES.keys()))
        cat = normalize_category(first_alias)
        self.assertIsNotNone(cat)
        self.assertIn(cat["fa"], TAXONOMY_BY_FA)

    def test_normalize_category_fallback(self):
        cat = normalize_category("NonExistentCategoryXYZ")
        self.assertEqual(cat["id"], TAXONOMY[-1]["id"])

    def test_classify_term_by_title_en(self):
        term = {
            "term_en": "Bitcoin Mining",
            "slug": "bitcoin-mining",
            "term_fa": "",
            "definition_en": "",
            "definition_fa": "",
        }
        res = classify_term(term)
        self.assertEqual(res["id"], "crypto")

    def test_classify_term_by_title_fa(self):
        term = {
            "term_en": "Unknown Term",
            "slug": "unknown-term",
            "term_fa": "استخراج ارز دیجیتال",
            "definition_en": "",
            "definition_fa": "",
        }
        res = classify_term(term)
        self.assertEqual(res["id"], "crypto")

    def test_classify_term_by_definition_en(self):
        term = {
            "term_en": "Generic Widget",
            "slug": "generic-widget",
            "term_fa": "ویجت عمومی",
            "definition_en": "An option is a derivative contract giving the buyer the right to buy or sell.",
            "definition_fa": "",
        }
        res = classify_term(term)
        self.assertEqual(res["id"], "derivatives")

    def test_classify_term_by_definition_fa(self):
        term = {
            "term_en": "Generic Thing",
            "slug": "generic-thing",
            "term_fa": "مورد آزمایشی",
            "definition_en": "Short text.",
            "definition_fa": "اوراق قرضه دولتی یک ابزار درآمد ثابت معتبر در بازار بدهی است.",
        }
        res = classify_term(term)
        self.assertEqual(res["id"], "fixed_income")

    def test_classify_term_fallback(self):
        term = {
            "term_en": "Unclassifiable Foobar",
            "slug": "unclassifiable-foobar",
            "term_fa": "مورد تعریف نشده",
            "definition_en": "Short.",
            "definition_fa": "کوتاه.",
        }
        res = classify_term(term)
        self.assertEqual(res["id"], TAXONOMY[-1]["id"])


if __name__ == "__main__":
    unittest.main()
