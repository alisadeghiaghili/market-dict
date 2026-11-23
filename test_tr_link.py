"""Deterministic unit tests for translation cache and markup preservation in translation pipeline."""

import unittest
from unittest.mock import patch

import scrape_and_enrich_pipeline as pipeline


class TranslationLinkPreservationTestCase(unittest.TestCase):
    """Test translation pipeline with mocked network and cached translations."""

    def test_empty_translation(self):
        self.assertEqual(pipeline.tr(""), "")
        self.assertEqual(pipeline.tr("   "), "")

    def test_katex_math_bypass(self):
        math = "$$\\text{Assets} = \\text{Liabilities} + \\text{Equity}$$"
        self.assertEqual(pipeline.tr(math), math)

    def test_cache_hit_returns_cached_translation(self):
        sample_en = "Internal Test String For Translation"
        sample_fa = "رشته آزمایشی داخلی برای ترجمه"
        pipeline.cache[sample_en] = sample_fa

        try:
            result = pipeline.tr(sample_en)
            self.assertEqual(result, sample_fa)
        finally:
            pipeline.cache.pop(sample_en, None)

    @patch("scrape_and_enrich_pipeline.ts.translate_text")
    def test_translation_preserves_internal_link_tags(self, mock_translate):
        text = 'The <a href="#term/capm" class="internal-term-link" data-slug="capm">capital asset pricing model</a> is used.'
        mock_translate.return_value = 'از <a href="#term/capm" class="internal-term-link" data-slug="capm">مدل قیمت گذاری دارایی سرمایه</a> استفاده می شود.'

        result = pipeline.tr(text)
        self.assertIn('data-slug="capm"', result)
        self.assertIn('class="internal-term-link"', result)


if __name__ == "__main__":
    unittest.main()
