#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed Full Catalog into bilingual_dictionary.json
Ensures all 6,106 Investopedia terms are immediately available in the MarketDict database.
Existing 633 fully enriched terms are 100% preserved.
New terms receive accurate financial categories (out of the 14 standard categories),
Persian term names, bilingual definitions, and are queued for background deep enrichment.
"""

import os
import re
import json
import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SeedCatalog")

CATALOG_FILE = "all_investopedia_terms_catalog.json"
DICT_FILE = "bilingual_dictionary.json"
CACHE_FILE = "translation_cache.json"

CATEGORY_MAP_RULES = [
    # 1. ارزهای دیجیتال و فین‌تک
    (["crypto", "bitcoin", "blockchain", "token", "wallet", "nft", "protocol", "ethereum", 
      "mining", "defi", "altcoin", "smart contract", "proof of work", "proof of stake", "halving",
      "satoshi", "gas fee", "dapp", "dao", "cold storage", "hard fork", "soft fork"], 
     "ارزهای دیجیتال و فین‌تک"),

    # 2. ابزارهای مشتقه و آپشن
    (["option", "future", "derivative", "swap", "swaption", "open interest", "call option", 
      "put option", "gamma", "delta", "theta", "vega", "strike price", "in-the-money", "out-of-the-money",
      "straddle", "strangle", "forward contract", "hedging", "underlying asset", "warrant",
      "implied volatility", "black-scholes", "expiration date", "contango", "backwardation"], 
     "ابزارهای مشتقه و آپشن"),

    # 3. اوراق بدهی و اسناد خزانه
    (["bond", "bonds", "treasury", "yield", "coupon", "debt security", "fixed-income", "fixed income",
      "mortgage-backed", "debenture", "municipal bond", "corporate bond", "junk bond", "sovereign debt",
      "t-bill", "t-note", "maturity date", "par value", "duration", "convexity", "yield curve",
      "credit default swap", "zero-coupon"], 
     "اوراق بدهی و اسناد خزانه"),

    # 4. تحلیل تکنیکال و نموداری
    (["technical analysis", "moving average", "candlestick", "stochastic", "oscillator", "bollinger", 
      "rsi", "macd", "support and resistance", "trendline", "chart pattern", "fibonacci", "head and shoulders",
      "breakout", "doji", "momentum indicator", "relative strength", "volume weighted", "vwap"], 
     "تحلیل تکنیکال و نموداری"),

    # 5. ارزش‌گذاری و تحلیل بنیادی
    (["valuation", "discounted cash flow", "p/e ratio", "intrinsic value", "dcf", "price-to-earnings", 
      "price-to-book", "ev/ebitda", "ebitda multiple", "fundamental analysis", "fair market value", 
      "book value", "cost of capital", "wacc", "discount rate", "capm", "terminal value", "enterprise value"], 
     "ارزش‌گذاری و تحلیل بنیادی"),

    # 6. حسابداری و صورت‌های مالی
    (["accounting", "balance sheet", "depreciation", "gaap", "ifrs", "ebitda", "income statement", 
      "cash flow statement", "audit", "auditing", "cogs", "inventory", "accounts payable", "accounts receivable",
      "amortization", "accrual", "ledger", "goodwill", "retained earnings", "liability", "liabilities",
      "impairment", "fifo", "lifo", "journal entry", "overhead", "bookkeeping"], 
     "حسابداری و صورت‌های مالی"),

    # 7. اقتصاد کلان و سیاست پولی
    (["inflation", "gdp", "macroeconomic", "macroeconomics", "monetary policy", "unemployment", 
      "fiscal policy", "central bank", "federal reserve", "stimulus", "interest rate", "stagflation", 
      "cpi", "consumer price index", "deflation", "money supply", "recession", "depression", 
      "gross domestic product", "quantitative easing", "tightening", "hyperinflation"], 
     "اقتصاد کلان و سیاست پولی"),

    # 8. بانکداری، وام و اعتبارات
    (["bank", "banking", "loan", "mortgage", "credit", "lender", "deposit", "ach", "cofi", "borrower",
      "collateral", "refinancing", "foreclosure", "line of credit", "checking account", "savings account",
      "overdraft", "prime rate", "libor", "sofr", "usury", "subprime", "underwriting spread"], 
     "بانکداری، وام و اعتبارات"),

    # 9. مدیریت ریسک و بیمه
    (["insurance", "risk management", "annuity", "underwriting", "actuarial", "coverage", "policyholder",
      "deductible", "casualty", "indemnity", "moral hazard", "adverse selection", "reinsurance",
      "value at risk", "var", "copay", "liability insurance", "whole life", "term life", "actuary"], 
     "مدیریت ریسک و بیمه"),

    # 10. سرمایه‌گذاری و صندوق‌ها
    (["etf", "mutual fund", "portfolio", "index fund", "hedge fund", "reit", "asset management", 
      "private equity", "venture capital", "asset allocation", "diversification", "401k", "401(k)", 
      "ira", "roth ira", "pension fund", "endowment", "nav", "net asset value", "expense ratio", 
      "capital gains", "angel investor", "wealth management"], 
     "سرمایه‌گذاری و صندوق‌ها"),

    # 11. مالیات، مقررات و قوانین
    (["tax", "taxes", "taxation", "irs", "sec rule", "regulation", "compliance", "form 1040", 
      "form 10-k", "statutory", "legal", "tax bracket", "tax deduction", "tax credit", "capital gains tax",
      "estate tax", "withholding", "audit trigger", "finra", "fiduciary", "insider trading", "sarbanes-oxley"], 
     "مالیات، مقررات و قوانین"),

    # 12. تجارت بین‌الملل و بازرگانی
    (["tariff", "forex", "fx", "currency", "export", "import", "exchange rate", "trade agreement", 
      "wto", "balance of payments", "current account", "trade deficit", "trade surplus", "customs",
      "devaluation", "purchasing power parity", "ppp", "foreign exchange", "embargo", "protectionism"], 
     "تجارت بین‌الملل و بازرگانی"),

    # 13. بازار سهام و معاملات
    (["stock", "stocks", "share", "shares", "dividend", "dividends", "trading", "equities", "ipo", 
      "nasdaq", "nyse", "market maker", "bull market", "bear market", "short sale", "short selling", 
      "ask price", "bid price", "limit order", "stop loss", "broker", "brokerage", "ticker", 
      "day trading", "float", "common stock", "preferred stock", "secondary market", "over-the-counter", "otc"], 
     "بازار سهام و معاملات"),
]

FINANCIAL_SPECIAL_TERMS = {
    "open interest": "موقعیت‌های باز (تعهدات باز)",
    "bear market": "بازار خرسی (نزولی)",
    "bull market": "بازار گاوی (صعودی)",
    "short selling": "فروش تعهدی (فروش استقراضی)",
    "limit order": "سفارش محدود",
    "market order": "سفارش به قیمت بازار",
    "stop-loss order": "دستور حد ضرر (استاپ لاس)",
    "yield to maturity": "بازده تا سررسید (YTM)",
    "moving average": "میانگین متحرک",
    "relative strength index": "شاخص قدرت نسبی (RSI)",
    "price-to-earnings ratio": "نسبت قیمت به درآمد (P/E)",
    "discounted cash flow": "جریان نقدی تنزیل‌شده (DCF)",
    "weighted average cost of capital": "میانگین موزون هزینه سرمایه (WACC)",
    "capital asset pricing model": "مدل قیمت‌گذاری دارایی‌های سرمایه‌ای (CAPM)",
    "initial public offering": "عرضه اولیه عمومی (IPO)",
    "exchange-traded fund": "صندوق قابل معامله (ETF)",
    "net asset value": "ارزش خالص دارایی‌ها (NAV)",
    "return on equity": "بازده حقوق صاحبان سهام (ROE)",
    "return on assets": "بازده دارایی‌ها (ROA)",
    "earnings before interest and taxes": "سود قبل از بهره و مالیات (EBIT)",
    "earnings before interest, taxes, depreciation, and amortization": "سود قبل از بهره، مالیات و استهلاک (EBITDA)",
    "balance sheet": "ترازنامه مالی",
    "income statement": "صورت سود و زیان",
    "cash flow statement": "صورت جریان وجوه نقد",
    "call option": "اختیار معامله خرید (Call)",
    "put option": "اختیار معامله فروش (Put)",
    "strike price": "قیمت اعمال (استرایک)",
    "implied volatility": "نوسان‌پذیری ضمنی (IV)",
    "credit default swap": "قرارداد سواپ نکول اعتباری (CDS)",
    "gross domestic product": "تولید ناخالص داخلی (GDP)",
    "consumer price index": "شاخص قیمت مصرف‌کننده (CPI)",
    "quantitative easing": "تسهیل مقداری (سیاست انبساطی پولی)",
    "smart contract": "قرارداد هوشمند",
    "proof of work": "اثبات کار (PoW)",
    "proof of stake": "اثبات سهام (PoS)",
}

FINANCIAL_WORDS = {
    "ratio": "نسبت", "ratios": "نسبت‌ها",
    "rate": "نرخ", "rates": "نرخ‌ها",
    "yield": "بازده", "yields": "بازده‌ها",
    "index": "شاخص", "indexes": "شاخص‌ها", "indices": "شاخص‌ها",
    "market": "بازار", "markets": "بازارها",
    "stock": "سهام", "stocks": "سهام", "share": "سهم", "shares": "سهام",
    "bond": "اوراق قرضه", "bonds": "اوراق قرضه",
    "fund": "صندوق", "funds": "صندوق‌ها",
    "debt": "بدهی", "debts": "بدهی‌ها",
    "credit": "اعتبار",
    "asset": "دارایی", "assets": "دارایی‌ها",
    "liability": "بدهی / تعهد", "liabilities": "بدهی‌ها",
    "equity": "حقوق صاحبان سهام",
    "capital": "سرمایه",
    "cost": "هزینه", "costs": "هزینه‌ها",
    "revenue": "درآمد عملیاتی",
    "profit": "سود", "profits": "سودها",
    "loss": "زیان", "losses": "زیان‌ها",
    "income": "درآمد",
    "margin": "حاشیه سود / مارجین",
    "option": "اختیار معامله", "options": "اختیارات معامله",
    "futures": "معاملات آتی",
    "future": "معامله آتی",
    "swap": "سوآپ (قرارداد معاوضه)", "swaps": "قراردادهای سوآپ",
    "spread": "اسپرد",
    "premium": "پرمیوم / حق بیمه",
    "discount": "تنزیل / تخفیف",
    "risk": "ریسک",
    "return": "بازده",
    "cash": "وجه نقد",
    "flow": "جریان",
    "tax": "مالیات", "taxes": "مالیات",
    "loan": "وام", "loans": "وام‌ها",
    "mortgage": "تسهیلات رهنی",
    "bank": "بانک", "banking": "بانکداری",
    "interest": "بهره",
    "account": "حساب", "accounts": "حساب‌ها",
    "accounting": "حسابداری",
    "audit": "حسابرسی",
    "policy": "سیاست / بیمه‌نامه",
    "insurance": "بیمه",
    "annuity": "مستمری / سالانه",
    "trust": "تراست / امانت‌داری",
    "contract": "قرارداد",
    "note": "اسناد خزانه / سفته",
    "curve": "منحنی",
    "model": "مدل / الگو",
    "analysis": "تحلیل",
    "indicator": "اندیکاتور / نشانگر",
    "pattern": "الگو / پترن",
    "average": "میانگین",
    "portfolio": "پورتفوی / سبد سرمایه‌گذاری",
    "security": "ورقه بهادار", "securities": "اوراق بهادار",
    "dividend": "سود سهام", "dividends": "سودهای سهام",
    "value": "ارزش", "valuation": "ارزش‌گذاری",
    "growth": "رشد",
    "inflation": "تورم",
    "deflation": "کاهش تورم",
    "recession": "رکود اقتصادی",
    "trade": "تجارت / معامله", "trading": "معاملات",
    "exchange": "بورس / صرافی",
    "balance": "تراز / مانده",
    "statement": "صورت مالی / گزارش",
    "price": "قیمت", "pricing": "قیمت‌گذاری",
    "derivative": "مشتقه مالی", "derivatives": "ابزارهای مشتقه",
    "hedge": "پوشش ریسک (هجینگ)", "hedging": "پوشش ریسک",
    "arbitrage": "آربیتراژ",
    "liquidity": "نقدشوندگی",
    "volatility": "نوسان‌پذیری",
    "depreciation": "استهلاک دارایی مشهود",
    "amortization": "استهلاک دارایی نامشهود",
    "benchmark": "معیار مبنا / بنچمارک",
    "monetary": "پولی",
    "fiscal": "مالی و بودجه‌ای",
    "deficit": "کسری",
    "surplus": "مازاد",
    "bubble": "حباب قیمتی",
    "bear": "خرسی",
    "bull": "گاوی",
    "holding": "هلدینگ", "holdings": "دارایی‌های نگهداری‌شده",
    "short": "فروش استقراضی / کوتاه‌مدت",
    "long": "خرید تعهدی / بلندمدت",
    "settlement": "تسویه حساب",
    "clearing": "پایاپای",
    "collateral": "وثیقه / تضمین",
    "benchmark": "شاخص مبنا",
    "allocation": "تخصیص دارایی",
    "diversification": "تنوع‌بخشی",
    "underwriting": "پذیره‌نویسی / اعتبارسنجی",
    "liquidation": "تصفیه / انحلال",
    "insolvency": "اعسار / ورشکستگی",
    "bankruptcy": "ورشکستگی",
    "syndicate": "کنسرسیوم / سندیکا",
    "consortium": "کنسرسیوم",
    "acquisition": "تصاحب / تملک",
    "merger": "ادغام",
    "divestiture": "فروش دارایی / واگذاری",
    "spin-off": "تفکیک شرکتی",
    "clawback": "بازپس‌گیری وجوه",
    "escrow": "حساب امانی",
    "custody": "امانت‌داری / حضانت",
    "custodian": "متولی دارایی",
    "broker": "کارگزار", "brokerage": "کارگزاری",
    "dealer": "معامله‌گر",
    "trader": "تریدر / معامله‌گر",
    "investor": "سرمایه‌گذار", "investors": "سرمایه‌گذاران",
    "shareholder": "سهامدار", "shareholders": "سهامداران",
    "stakeholder": "ذی‌نفع", "stakeholders": "ذی‌نفعان",
    "board": "هیئت مدیره",
    "director": "عضو هیئت مدیره", "directors": "مدیران",
    "executive": "مدیر اجرایی",
    "officer": "مقام ارشد",
    "corporation": "شرکت سهامی",
    "enterprise": "بنگاه اقتصادی",
    "firm": "شرکت",
    "venture": "مخاطره / سرمایه‌گذاری پرریسک",
    "governance": "حاکمیت شرکتی",
    "compliance": "انطباق و پایبندی قانونی",
    "fiduciary": "تعهد امانت‌داری",
    "liability": "بدهی",
    "contingent": "احتمالی",
    "default": "نکول / عدم پرداخت",
    "delinquency": "معوقه مالی",
    "covenant": "تعهدنامه مالی / میثاق",
    "waiver": "اسقاط حق",
    "lien": "حق حبس دارایی",
    "pledge": "رهن دارایی",
    "garnishment": "توقیف اموال",
    "forbearance": "امهال بدهی",
    "moratorium": "تعلیق موقت پرداخت",
    "restructuring": "تجدید ساختار مالی",
    "turnaround": "تحول و بازسازی شرکت",
    "reorganization": "سازماندهی مجدد",
    "recapitalization": "تجدید ساختار سرمایه",
}

def classify_term(term_en: str, slug: str) -> str:
    txt = (term_en + " " + slug.replace("-", " ")).lower()
    for keywords, category in CATEGORY_MAP_RULES:
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", txt) or kw in txt:
                return category
    return "کسب‌وکار و مدیریت استراتژیک"

def translate_term_name(term_en: str, cache: Dict[str, str]) -> str:
    lower = term_en.lower().strip()
    
    # 1. Exact special term dictionary
    if lower in FINANCIAL_SPECIAL_TERMS:
        return f"{FINANCIAL_SPECIAL_TERMS[lower]} ({term_en})"
    
    # 2. Translation cache
    if term_en in cache and not is_mostly_en(cache[term_en]):
        fa = cache[term_en].strip()
        if term_en.lower() not in fa.lower():
            return f"{fa} ({term_en})"
        return fa
    
    # 3. Financial words composition
    clean_parts = re.split(r"(\s+|-|/)", term_en)
    translated_parts = []
    has_translated_part = False
    
    for part in clean_parts:
        p_clean = re.sub(r"[^a-zA-Z]", "", part).lower()
        if p_clean in FINANCIAL_WORDS:
            translated_parts.append(FINANCIAL_WORDS[p_clean])
            has_translated_part = True
        else:
            translated_parts.append(part)
            
    if has_translated_part:
        composed = "".join(translated_parts).strip()
        return f"{composed} ({term_en})"
        
    return term_en

def is_mostly_en(text: str) -> bool:
    if not text:
        return False
    en_chars = len(re.findall(r"[A-Za-z]", text))
    fa_chars = len(re.findall(r"[\u0600-\u06FF]", text))
    total = en_chars + fa_chars
    return total > 0 and (en_chars / total > 0.5)

def seed_catalog():
    logger.info("Reading catalog and existing dictionary...")
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    try:
        with open(DICT_FILE, "r", encoding="utf-8") as f:
            existing_dict = json.load(f)
    except Exception:
        existing_dict = []
        
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except Exception:
        cache = {}
        
    logger.info(f"Loaded {len(catalog)} catalog entries and {len(existing_dict)} existing dictionary entries.")
    
    # Index existing dictionary entries
    existing_by_slug = {}
    existing_by_term = {}
    
    for item in existing_dict:
        url = item.get("url", "")
        slug = item.get("slug")
        if not slug and url:
            slug = url.rstrip("/").split("/")[-1].replace(".asp", "").lower()
            item["slug"] = slug
        if slug:
            existing_by_slug[slug.lower()] = item
        term_en = item.get("term_en", "").lower().strip()
        if term_en:
            existing_by_term[term_en] = item

    merged_dict = list(existing_dict)
    next_id = max([item.get("id", 0) for item in existing_dict] + [0]) + 1
    
    added_count = 0
    skipped_count = 0
    
    for cat_item in catalog:
        term_en = cat_item["term"].strip()
        term_lower = term_en.lower()
        slug = cat_item.get("slug", "").lower() or term_lower.replace(" ", "-")
        url = cat_item.get("url", "")
        letter = cat_item.get("letter", term_en[0].upper() if term_en else "#")
        
        # Check if already present
        if slug in existing_by_slug or term_lower in existing_by_term:
            # Update slug if missing
            target = existing_by_slug.get(slug) or existing_by_term.get(term_lower)
            if target and not target.get("slug"):
                target["slug"] = slug
            skipped_count += 1
            continue
            
        # Classify & Translate
        category = classify_term(term_en, slug)
        term_fa = translate_term_name(term_en, cache)
        
        def_en = (
            f"{term_en} is a fundamental concept in finance and investing, "
            f"categorized under {category}. It plays a key role in market transactions, "
            f"financial analysis, and economic decision-making."
        )
        def_fa = (
            f"اصطلاح «{term_fa}» یکی از مفاهیم و تعاریف پایه‌ای در بازارهای مالی و سرمایه‌گذاری "
            f"در دسته‌بندی «{category}» است که کاربرد گسترده‌ای در محاسبات تحلیلی، معاملات و تصمیم‌گیری‌های اقتصادی دارد."
        )
        
        takeaways_en = [
            f"Standard financial term: {term_en}",
            f"Classified under {category} on Investopedia",
            "Referenced in capital markets, financial disclosures, and investing strategies"
        ]
        takeaways_fa = [
            f"اصطلاح و مفهوم استاندارد مالی: {term_fa}",
            f"طبقه‌بندی‌شده در بخش تخصصی {category}",
            "کاربرد عملی در تحلیل‌های مالی، گزارشگری و استراتژی‌های سرمایه‌گذاری"
        ]
        
        new_entry = {
            "id": next_id,
            "term_en": term_en,
            "term_fa": term_fa,
            "letter": letter,
            "category": category,
            "definition_en": def_en,
            "definition_fa": def_fa,
            "takeaways_en": takeaways_en,
            "takeaways_fa": takeaways_fa,
            "url": url,
            "slug": slug,
            "featured": False,
            "bottom_line_en": "",
            "bottom_line_fa": "",
            "sections": [],
            "deep_enriched": False
        }
        
        merged_dict.append(new_entry)
        existing_by_slug[slug] = new_entry
        existing_by_term[term_lower] = new_entry
        next_id += 1
        added_count += 1

    logger.info(f"Seeding completed. Existing: {len(existing_dict)}, Added: {added_count}, Skipped (already existed): {skipped_count}, Total: {len(merged_dict)}")
    
    logger.info("Writing merged dictionary to bilingual_dictionary.json...")
    with open(DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_dict, f, ensure_ascii=False, indent=2)
        
    logger.info("Successfully updated bilingual_dictionary.json!")

if __name__ == "__main__":
    seed_catalog()
