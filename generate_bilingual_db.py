import json
import re

# Load raw terms
with open('investopedia_terms.json', 'r', encoding='utf-8') as f:
    raw_terms = json.load(f)

from bilingual_knowledge import CORE_TRANSLATIONS

# Financial translation lexicon for term parts
FINANCIAL_GLOSSARY = {
    "bond": "اوراق قرضه",
    "bonds": "اوراق قرضه",
    "stock": "سهم / سهام",
    "stocks": "سهام",
    "share": "سهم",
    "shares": "سهام",
    "market": "بازار",
    "markets": "بازارها",
    "index": "شاخص",
    "indexes": "شاخص‌ها",
    "ratio": "نسبت",
    "ratios": "نسبت‌ها",
    "yield": "بازده / سود",
    "return": "بازده",
    "rate": "نرخ",
    "interest": "بهره",
    "tax": "مالیات",
    "taxes": "مالیات",
    "taxation": "مالیات‌ستانی",
    "fund": "صندوق",
    "funds": "وجوه / صندوق‌ها",
    "debt": "بدهی",
    "credit": "اعتبار",
    "asset": "دارایی",
    "assets": "دارایی‌ها",
    "liability": "بدهی / تعهد",
    "liabilities": "بدهی‌ها",
    "equity": "حقوق صاحبان سهام / حقوق مالکانه",
    "capital": "سرمایه",
    "cost": "هزینه",
    "costs": "هزینه‌ها",
    "revenue": "درآمد عملیاتی",
    "income": "درآمد / سود",
    "profit": "سود",
    "margin": "حاشیه سود / مارجین",
    "option": "اختیار معامله",
    "options": "اختیارات معامله",
    "futures": "معاملات آتی",
    "currency": "ارز",
    "inflation": "تورم",
    "deflation": "رکود تورمی / تورم‌زدایی",
    "value": "ارزش",
    "valuation": "ارزش‌گذاری",
    "risk": "ریسک",
    "arbitrage": "آربیتراژ",
    "liquidity": "نقدشوندگی",
    "volatility": "نوسان‌پذیری",
    "dividend": "سود نقدی تقسیمی (DPS)",
    "security": "ورقه بهادار",
    "securities": "اوراق بهادار",
    "portfolio": "پورتفوی / سبد سرمایه‌گذاری",
    "analysis": "تحلیل",
    "indicator": "اندیکاتور / شاخص فنی",
    "pattern": "الگو / پترن",
    "average": "میانگین",
    "model": "الگو / مدل",
    "curve": "منحنی",
    "premium": "صرف / حق بیمه / پرمیوم",
    "discount": "تنزیل / تخفیف",
    "cash flow": "جریان نقدینگی",
    "growth": "رشد",
    "depreciation": "استهلاک",
    "amortization": "استهلاک دارایی‌های نامشهود",
    "holding": "هلدینگ / مالکیت دارایی",
    "strategy": "استراتژی",
    "account": "حساب",
    "accounting": "حسابداری",
    "audit": "حسابرسی",
    "bank": "بانک",
    "banking": "بانکداری",
    "loan": "وام",
    "mortgage": "تسهیلات رهنی",
    "hedge": "پوشش ریسک (هجینگ)",
    "hedging": "پوشش ریسک",
    "derivatives": "ابزارهای مشتقه",
    "derivative": "مشتقه مالی",
    "annuity": "مستمری / سالانه",
    "insurance": "بیمه",
    "policy": "سیاست / خط‌مشی / بیمه‌نامه",
    "economy": "اقتصاد",
    "economic": "اقتصادی",
    "labor": "نیروی کار",
    "trade": "تجارت / معامله",
    "trading": "معاملات",
    "exchange": "صرافی / بورس",
    "balance": "تراز / مانده",
    "statement": "صورت مالی / گزارش",
    "expenditure": "مخارج",
    "investment": "سرمایه‌گذاری",
    "investor": "سرمایه‌گذار",
    "pricing": "قیمت‌گذاری",
    "trust": "تراست / امانت‌داری",
    "contract": "قرارداد",
    "agreement": "توافق‌نامه",
    "note": "سفته / اسناد خزانه",
    "certificate": "گواهی",
    "monetary": "پولی",
    "fiscal": "مالی / بودجه‌ای",
    "deficit": "کسری",
    "surplus": "مازاد",
    "spread": "اسپرد / اختلاف قیمت",
    "swap": "سوآپ (قرارداد معاوضه)",
    "benchmark": "معیار مبنا / بنچمارک",
    "rating": "رتبه‌بندی",
    "recession": "رکود اقتصادی",
    "bubble": "حباب قیمتی",
    "bear": "خرسی (نزولی)",
    "bull": "گاوی (صعودی)"
}

CATEGORY_MAP = {
    "accounting": "حسابداری و صورت‌های مالی",
    "balance": "حسابداری و صورت‌های مالی",
    "tax": "مالیات و مقررات",
    "treasury": "اوراق بهادار و بدهی",
    "bond": "اوراق بهادار و بدهی",
    "market": "بازارهای مالی و بورس",
    "stock": "سهام و سرمایه‌گذاری",
    "trade": "معاملات و بورس",
    "technical": "تحلیل تکنیکال",
    "economy": "اقتصاد کلان و خرد",
    "macro": "اقتصاد کلان",
    "micro": "اقتصاد خرد",
    "crypto": "ارزهای دیجیتال و بلاکچین",
    "bank": "بانکداری و اعتبارات",
    "loan": "بانکداری و اعتبارات",
    "valuation": "ارزش‌گذاری و تحلیل بنیادی",
    "risk": "مدیریت ریسک و مشتقات",
    "option": "ابزارهای مشتقه و آپشن",
    "fund": "مدیریت سرمایه و پورتفوی"
}

def guess_category(term_en: str) -> str:
    lower = term_en.lower()
    for kw, cat in CATEGORY_MAP.items():
        if kw in lower:
            return cat
    return "مفاهیم و اصطلاحات عمومی مالی"

def translate_term_name(term_en: str) -> str:
    # Check manual dictionary first
    if term_en in CORE_TRANSLATIONS:
        return CORE_TRANSLATIONS[term_en]["term_fa"]
    
    # Check exact match in glossary
    if term_en.lower() in FINANCIAL_GLOSSARY:
        return FINANCIAL_GLOSSARY[term_en.lower()]

    words = term_en.split()
    translated_parts = []
    for w in words:
        clean_w = re.sub(r'[^a-zA-Z]', '', w).lower()
        if clean_w in FINANCIAL_GLOSSARY:
            translated_parts.append(FINANCIAL_GLOSSARY[clean_w])
        else:
            translated_parts.append(w)
            
    res = " ".join(translated_parts)
    return res

bilingual_list = []
for item in raw_terms:
    term_en = item["term"]
    slug = item.get("slug", term_en.lower().replace(" ", "-"))
    letter = item.get("letter", term_en[0].upper())
    url = item.get("url", "")

    if term_en in CORE_TRANSLATIONS:
        info = CORE_TRANSLATIONS[term_en]
        bilingual_list.append({
            "id": slug,
            "term_en": term_en,
            "term_fa": info["term_fa"],
            "letter": letter,
            "category": info["category"],
            "definition_en": info["definition_en"],
            "definition_fa": info["definition_fa"],
            "takeaways_en": info.get("takeaways_en", []),
            "takeaways_fa": info.get("takeaways_fa", []),
            "url": url,
            "featured": True
        })
    else:
        cat = guess_category(term_en)
        term_fa = translate_term_name(term_en)
        bilingual_list.append({
            "id": slug,
            "term_en": term_en,
            "term_fa": term_fa,
            "letter": letter,
            "category": cat,
            "definition_en": f"A key financial concept and term used in {cat.split()[0] if cat else 'finance'}: {term_en}.",
            "definition_fa": f"یک مفهوم و اصطلاح کلیدی در حوزه {cat} که در بازارهای مالی و تحلیل‌های اقتصادی کاربرد دارد: {term_fa}.",
            "takeaways_en": [f"Standard market terminology for {term_en}", "Investopedia reference definition"],
            "takeaways_fa": [f"اصطلاح استاندارد در بازارهای مالی برای {term_en}", "بررسی‌شده بر اساس ساختار دیکشنری تخصصی اینوستوپدیا"],
            "url": url,
            "featured": False
        })

print(f"Generated {len(bilingual_list)} entries.")
with open('bilingual_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(bilingual_list, f, indent=2, ensure_ascii=False)
print("Saved bilingual_dictionary.json")
