"""Unit tests for bidirectional term linking, math preservation, and Persian normalization."""

import re
import unittest


def normalize_fa(text: str) -> str:
    """Normalize Persian text: replace half-spaces, normalize Arabic characters, collapse spaces."""
    if not text:
        return ""
    text = text.replace("\u200c", " ")
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def linkify_text(
    text: str,
    term_dict: dict[str, str],
    is_persian: bool = False,
    current_slug: str | None = None,
    max_links: int = 6,
) -> str:
    """Inject internal dictionary links into text while protecting KaTeX math and existing HTML tags."""
    if not text:
        return text

    placeholders: list[str] = []

    def add_ph(s: str) -> str:
        placeholders.append(s)
        return f"___PH_{len(placeholders)-1}___"

    # 1. Protect $$...$$ math
    clean = re.sub(r"\$\$.*?\$\$", lambda m: add_ph(m.group(0)), text, flags=re.DOTALL)
    # 2. Protect existing <a> tags
    clean = re.sub(r"<a\b[^>]*>.*?</a>", lambda m: add_ph(m.group(0)), clean, flags=re.DOTALL | re.IGNORECASE)
    # 3. Protect other HTML tags
    clean = re.sub(r"<[^>]+>", lambda m: add_ph(m.group(0)), clean)

    sorted_keys = sorted(term_dict.keys(), key=len, reverse=True)
    linked_slugs: set[str] = set()
    if current_slug:
        linked_slugs.add(current_slug)

    for k in sorted_keys:
        slug = term_dict[k]
        if slug in linked_slugs:
            continue

        if is_persian:
            pattern_str = (
                r"(?<![^\s،؛«»()\[\]{}.])("
                + re.escape(k).replace(r"\ ", r"[\s\u200c]+")
                + r")(?![^\s،؛«»()\[\]{}.])"
            )
            pattern = re.compile(pattern_str, re.IGNORECASE)
        else:
            pattern = re.compile(r"\b(" + re.escape(k) + r")\b", re.IGNORECASE)

        m = pattern.search(clean)
        if m:
            matched_str = m.group(1)
            tag = f'<a href="#term/{slug}" class="internal-term-link" data-slug="{slug}">{matched_str}</a>'
            clean = pattern.sub(add_ph(tag), clean, count=1)
            linked_slugs.add(slug)
            if len(linked_slugs) >= max_links:
                break

    # Restore placeholders
    for idx in range(len(placeholders) - 1, -1, -1):
        clean = clean.replace(f"___PH_{idx}___", placeholders[idx])

    return clean


class TermLinkerTestCase(unittest.TestCase):
    """Test suite for term linker algorithms and KaTeX protections."""

    def setUp(self):
        self.en_terms = {
            "capital asset pricing model": "capm",
            "risk-adjusted return": "riskadjustedreturn",
            "standard deviation": "standarddeviation",
            "sharpe ratio": "sharperatio",
        }
        self.fa_terms = {
            "مدل قیمت گذاری دارایی های سرمایه ای": "capm",
            "انحراف معیار": "standarddeviation",
            "نسبت شارپ": "sharperatio",
        }

    def test_normalize_fa(self):
        self.assertEqual(normalize_fa(""), "")
        self.assertEqual(normalize_fa("صورت‌های   مالي"), "صورت های مالی")
        self.assertEqual(normalize_fa("بانك  مركزي"), "بانک مرکزی")

    def test_linkify_english_terms(self):
        text = "The Sharpe ratio uses standard deviation and capital asset pricing model."
        result = linkify_text(text, self.en_terms, is_persian=False, current_slug="sharperatio")
        self.assertIn('<a href="#term/capm" class="internal-term-link" data-slug="capm">capital asset pricing model</a>', result)
        self.assertIn('<a href="#term/standarddeviation" class="internal-term-link" data-slug="standarddeviation">standard deviation</a>', result)
        self.assertNotIn('data-slug="sharperatio"', result)  # Current slug should not self-link

    def test_linkify_persian_terms(self):
        text = "برای محاسبه ریسک از انحراف معیار استفاده می‌شود."
        result = linkify_text(text, self.fa_terms, is_persian=True)
        self.assertIn('data-slug="standarddeviation"', result)
        self.assertIn("انحراف معیار</a>", result)

    def test_protect_katex_math(self):
        text = "Here is formula: $$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$ with standard deviation."
        result = linkify_text(text, self.en_terms, is_persian=False)
        self.assertIn("$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$", result)
        self.assertIn('data-slug="standarddeviation"', result)

    def test_protect_existing_links(self):
        text = 'Already linked: <a href="#term/capm">capital asset pricing model</a> and standard deviation.'
        result = linkify_text(text, self.en_terms, is_persian=False)
        self.assertEqual(result.count('data-slug="capm"'), 0)
        self.assertIn('data-slug="standarddeviation"', result)

    def test_max_links_cap(self):
        terms = {f"term_{i}": f"slug_{i}" for i in range(10)}
        text = " ".join([f"term_{i}" for i in range(10)])
        result = linkify_text(text, terms, max_links=3)
        self.assertEqual(result.count("internal-term-link"), 3)


if __name__ == "__main__":
    unittest.main()
