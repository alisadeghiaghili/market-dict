"""
Deep Content Enricher for MarketDict
Enriches dictionary items with:
- Full lead definitions
- Complete bullet-point Key Takeaways
- Complete structured in-depth sections (Formulas, Examples, Pros/Cons, Comparisons, Bottom Line)
- Persian translations for sections
"""

import json
import time
import random
from curl_cffi import requests
from bs4 import BeautifulSoup
import re

DATA_FILE = "bilingual_dictionary.json"

def parse_full_page(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("div", class_="article-body-content") or soup.find("div", id="article-body_1-0") or soup

    # 1. Key Takeaways
    takeaways = []
    callout = soup.find(class_=re.compile(r"universal-callout|whatyouneedtoknow|key-takeaways"))
    if callout:
        for li in callout.find_all("li"):
            txt = li.get_text(strip=True)
            if txt and len(txt) > 5:
                takeaways.append(txt)

    # 2. Lead Definition
    lead_paragraphs = []
    for p in body.find_all("p", recursive=True):
        if p.find_parent(class_=re.compile(r"callout|recirc|newsletter|author|ad-")):
            continue
        txt = p.get_text(strip=True)
        if len(txt) > 25 and not any(skip in txt for skip in ["Get personalized", "Investopedia /", "Fact checked by"]):
            lead_paragraphs.append(txt)
            if len(lead_paragraphs) >= 2:
                break
    lead_def = "\n\n".join(lead_paragraphs)

    # 3. Detailed Sections
    sections = []
    current_sec = None
    bottom_line = ""

    for el in body.children:
        if not hasattr(el, "name") or not el.name:
            continue

        h = el if el.name in ["h2", "h3"] else el.find(["h2", "h3"])
        if h:
            htxt = h.get_text(strip=True)
            if any(skip in htxt.lower() for skip in ["related articles", "article sources", "trending", "newsletter", "key takeaways"]):
                continue
            if current_sec and (current_sec["paragraphs"] or current_sec["items"]):
                sections.append(current_sec)
            current_sec = {"title": htxt, "paragraphs": [], "items": []}

        if current_sec:
            ps = el.find_all("p") if el.name != "p" else [el]
            for p in ps:
                ptxt = p.get_text(strip=True)
                if ptxt and len(ptxt) > 20 and not any(skip in ptxt for skip in ["Get personalized", "Investopedia /", "Fact checked by"]):
                    if "bottom line" in current_sec["title"].lower():
                        bottom_line += ptxt + " "
                    current_sec["paragraphs"].append(ptxt)

            lis = el.find_all("li")
            for li in lis:
                litxt = li.get_text(strip=True)
                if litxt and len(litxt) > 5 and len(litxt) < 300:
                    current_sec["items"].append(litxt)

    if current_sec and (current_sec["paragraphs"] or current_sec["items"]):
        sections.append(current_sec)

    return {
        "definition_en": lead_def,
        "takeaways_en": takeaways,
        "sections_en": sections,
        "bottom_line_en": bottom_line.strip()
    }

SECTION_TITLE_FA = {
    "what is": "تعریف و مفهوم",
    "understanding": "درک عمیق مفهوم",
    "formula": "فرمول و نحوه محاسبه",
    "how to calculate": "چگونگی محاسبه",
    "example": "مثال کاربردی و عملی",
    "pros and cons": "مزایا و معایب",
    "advantages": "مزایا و نقاط قوت",
    "disadvantages": "معایب و محدودیت‌ها",
    "criticism": "انتقادات و نقاط ضعف",
    "vs": "مقایسه با مفاهیم مشابه",
    "history": "تاریخچه و پیدایش",
    "bottom line": "جمع‌بندی و نتیجه‌گیری نهایی",
    "types of": "انواع و طبقه‌بندی",
    "components": "اجزا و ارکان اصلی",
    "assumptions": "مفروضات بنیادی",
    "how it works": "مکانیزم و نحوه کارکرد"
}

def translate_section_title(title_en: str) -> str:
    lower = title_en.lower()
    for kw, fa in SECTION_TITLE_FA.items():
        if kw in lower:
            return f"{fa} ({title_en})"
    return f"بخش تخصصی: {title_en}"

def enrich_database(limit=30):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    session = requests.Session(impersonate="chrome124")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

    count = 0
    # Prioritize items with urls
    for idx, item in enumerate(data):
        url = item.get("url")
        # Only enrich if not already deeply enriched
        if url and "sections" not in item:
            print(f"[{count+1}/{limit}] Fetching deep content: {item['term_en']} ({url})")
            try:
                resp = session.get(url, headers=headers, timeout=20)
                if resp.status_code == 200:
                    parsed = parse_full_page(resp.text)
                    if parsed["takeaways_en"]:
                        item["takeaways_en"] = parsed["takeaways_en"]
                    if parsed["definition_en"]:
                        item["definition_en"] = parsed["definition_en"]
                    
                    item["bottom_line_en"] = parsed["bottom_line_en"]
                    
                    # Construct bilingual sections
                    bilingual_sections = []
                    for s in parsed["sections_en"]:
                        bilingual_sections.append({
                            "title_en": s["title"],
                            "title_fa": translate_section_title(s["title"]),
                            "paragraphs_en": s["paragraphs"],
                            "items_en": s["items"]
                        })
                    item["sections"] = bilingual_sections
                    item["deep_enriched"] = True
                    count += 1
                else:
                    print(f"Status {resp.status_code} on {url}")
            except Exception as e:
                print(f"Error on {url}: {e}")

            time.sleep(random.uniform(0.6, 1.2))

            if count >= limit:
                break

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] Enriched {count} terms with full in-depth content. Saved {DATA_FILE}")

if __name__ == "__main__":
    enrich_database(limit=35)
