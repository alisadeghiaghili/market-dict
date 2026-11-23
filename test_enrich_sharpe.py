"""Deterministic unit tests for article sectioning, formula figure detection, and LaTeX parsing."""

import unittest

from bs4 import BeautifulSoup

from scrape_and_enrich_pipeline import clean_element_html

FORMULA_IMAGE_DB = {
    "sharperatio": {
        "formula_en": "$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$",
        "formula_fa": "$$\\text{نسبت شارپ} = \\frac{R_p - R_f}{\\sigma_p}$$",
    }
}


def parse_article_sections(html: str, slug: str) -> list[dict]:
    """Parse article HTML into structured sections, converting formula images to LaTeX."""
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("div", class_="article-body-content") or soup

    sections = []
    current_sec = None

    for el in body.children:
        if not hasattr(el, "name") or not el.name:
            continue
        h = el if el.name in ["h2", "h3"] else el.find(["h2", "h3"])
        if h:
            htitle = h.get_text(strip=True)
            if not any(skip in htitle.lower() for skip in ["key takeaways", "related articles", "article sources"]):
                if current_sec and (current_sec["paragraphs_en"] or current_sec["items_en"]):
                    sections.append(current_sec)
                current_sec = {
                    "title_en": htitle,
                    "paragraphs_en": [],
                    "items_en": [],
                }

        # Check for formula figures/images
        if current_sec and (el.name == "figure" or el.find("figure")):
            fig = el if el.name == "figure" else el.find("figure")
            img = fig.find("img")
            if img:
                alt = (img.get("alt") or "").lower()
                src = (img.get("src") or img.get("data-src") or "").lower()
                has_formula_kw = any(w in alt for w in ["formula", "calculation", "ratio"]) or any(w in src for w in ["formula", "ratio"])
                if has_formula_kw and slug in FORMULA_IMAGE_DB:
                    f_en = FORMULA_IMAGE_DB[slug]["formula_en"]
                    if f_en not in current_sec["paragraphs_en"]:
                        current_sec["paragraphs_en"].append(f_en)

        ps = el.find_all("p") if el.name != "p" else [el]
        for p in ps:
            ptxt = clean_element_html(p)
            is_valid_len = len(ptxt) > 20 and not any(skip in ptxt for skip in ["Investopedia /", "Fact checked by"])
            if is_valid_len and current_sec:
                current_sec["paragraphs_en"].append(ptxt)

    if current_sec and (current_sec["paragraphs_en"] or current_sec["items_en"]):
        sections.append(current_sec)

    return sections


class ArticleEnrichmentParserTestCase(unittest.TestCase):
    """Test article HTML parser and formula figure detection."""

    def test_parse_sections_and_formula_images(self):
        sample_html = """
        <div class="article-body-content">
            <h2>Understanding the Sharpe Ratio</h2>
            <p>The Sharpe ratio is one of the most widely used methods for calculating risk-adjusted return.</p>
            <figure>
                <img src="/images/sharpe-ratio-formula.png" alt="Sharpe Ratio Formula displayed mathematically" />
            </figure>
            <p>Standard deviation measures the degree to which investments fluctuate around their mean return.</p>
            <h2>Related Articles</h2>
            <p>Skip this section from being parsed.</p>
        </div>
        """
        sections = parse_article_sections(sample_html, slug="sharperatio")
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["title_en"], "Understanding the Sharpe Ratio")
        self.assertIn("$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$", sections[0]["paragraphs_en"])
        self.assertTrue(any("Standard deviation" in p for p in sections[0]["paragraphs_en"]))


if __name__ == "__main__":
    unittest.main()
