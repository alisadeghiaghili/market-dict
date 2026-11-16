# -*- coding: utf-8 -*-
"""
Categories Engine for Market-Dict
Comprehensive financial taxonomy with Persian and English names, icons,
and multi-tier matching rules for titles, slugs, and definitions.
"""

import re
from typing import Dict, List, Any

TAXONOMY = [
    {
        "id": "crypto",
        "fa": "ارزهای دیجیتال و بلاک‌چین",
        "en": "Cryptocurrency & Blockchain",
        "icon": "🪙",
        "roots": [
            "crypto", "bitcoin", "blockchain", "token", "tokens", "wallet", "wallets", "nft", "nfts",
            "ethereum", "mining", "miner", "defi", "altcoin", "smart contract", "smart contracts",
            "proof of work", "proof of stake", "halving", "satoshi", "gas fee", "dapp", "dao",
            "cold storage", "hard fork", "soft fork", "web3", "hashrate", "lightning network",
            "memecoin", "dex", "hodl", "cryptocurrency", "airdrop", "ledgerx", "cryptographic",
            "erc-20", "tether", "stablecoin"
        ]
    },
    {
        "id": "technical_analysis",
        "fa": "تحلیل تکنیکال و پرایس اکشن",
        "en": "Technical Analysis & Charting",
        "icon": "📊",
        "roots": [
            "technical", "chart", "charts", "candlestick", "candlesticks", "candle", "stochastic",
            "oscillator", "oscillators", "bollinger", "rsi", "macd", "support", "resistance",
            "trendline", "trendlines", "trend", "fibonacci", "head and shoulders", "breakout",
            "breakouts", "doji", "momentum", "relative strength", "vwap", "ichimoku", "cup and handle",
            "price action", "average true range", "atr", "overbought", "oversold", "divergence",
            "swing", "scalp", "scalping", "pattern", "patterns", "moving average", "pullback",
            "pivot point", "channel", "flag pattern", "pennant", "trailing stop", "reversal",
            "dead cat bounce", "golden cross", "death cross", "keltner", "parabolic"
        ]
    },
    {
        "id": "derivatives",
        "fa": "ابزارهای مشتقه، آپشن و آتی",
        "en": "Derivatives, Options & Futures",
        "icon": "⚡",
        "roots": [
            "option", "options", "future", "futures", "derivative", "derivatives", "swap", "swaps",
            "swaption", "swaptions", "open interest", "call option", "put option", "gamma", "delta",
            "theta", "vega", "rho", "strike price", "strike", "in-the-money", "out-of-the-money",
            "at-the-money", "straddle", "strangle", "spread", "collar", "iron condor", "forward contract",
            "forward contracts", "forwards", "hedging", "hedged", "hedge", "underlying asset",
            "warrant", "warrants", "implied volatility", "black-scholes", "expiration", "contango",
            "backwardation", "naked option", "covered call", "synthetic"
        ]
    },
    {
        "id": "stock_market",
        "fa": "بازار سهام و معاملات",
        "en": "Stock Market & Equities Trading",
        "icon": "📈",
        "roots": [
            "stock", "stocks", "share", "shares", "shareholder", "shareholders", "dividend",
            "dividends", "trading", "trader", "traders", "equities", "equity", "ipo", "ipos",
            "nasdaq", "nyse", "market maker", "bull market", "bear market", "short sale",
            "short selling", "short seller", "ask price", "bid price", "limit order", "market order",
            "stop loss", "stop-loss", "stop order", "iceberg order", "fill or kill", "broker",
            "brokerage", "ticker", "day trading", "float", "common stock", "preferred stock",
            "secondary market", "otc", "order book", "listing", "delisting", "volume", "rally",
            "sell-off", "odd lot", "round lot", "blue chip", "penny stock", "market cap",
            "securities", "security", "exchange-traded", "floor trader", "quote", "clearinghouse",
            "spread", "market-on-close", "overbought", "oversold", "fill"
        ]
    },
    {
        "id": "quant_math",
        "fa": "روش‌های کمی و ریاضیات مالی",
        "en": "Quantitative Methods & Financial Math",
        "icon": "📐",
        "roots": [
            "quantitative", "probability", "probabilities", "variance", "variances", "standard deviation",
            "regression", "regressions", "correlation", "anova", "bayes", "bayesian", "central limit theorem",
            "time value of money", "compound interest", "cagr", "present value", "future value",
            "distribution", "normal distribution", "monte carlo", "random walk", "mean", "median",
            "mode", "skewness", "kurtosis", "confidence interval", "statistic", "statistics",
            "statistical", "sampling", "sample", "samples", "z-score", "t-test", "p-value",
            "coefficient", "formula", "algorithm", "hypothesis testing", "hypothesis", "geometric mean",
            "null hypothesis", "standard error", "covariance", "econometrics", "logarithm",
            "bell curve", "correlation coefficient", "stochastic"
        ]
    },
    {
        "id": "fixed_income",
        "fa": "اوراق درآمد ثابت و بدهی",
        "en": "Fixed Income & Bond Markets",
        "icon": "📜",
        "roots": [
            "bond", "bonds", "treasury", "treasuries", "yield", "yields", "coupon", "coupons",
            "debt security", "debt securities", "fixed income", "fixed-income", "debenture",
            "debentures", "municipal bond", "corporate bond", "junk bond", "sovereign debt",
            "t-bill", "t-note", "maturity", "par value", "duration", "convexity", "zero-coupon",
            "mortgage-backed", "mbs", "credit default swap", "cds", "accrued interest", "gilt",
            "bund", "us treasury", "yield curve", "face value", "callable bond", "convertible bond"
        ]
    },
    {
        "id": "valuation",
        "fa": "ارزش‌گذاری و تحلیل بنیادی",
        "en": "Valuation & Fundamental Analysis",
        "icon": "🔍",
        "roots": [
            "valuation", "valuing", "discounted cash flow", "dcf", "p/e ratio", "intrinsic value",
            "price-to-earnings", "price-to-book", "ev/ebitda", "ebitda multiple", "fundamental analysis",
            "fair market value", "fair value", "book value", "cost of capital", "wacc", "capm",
            "terminal value", "enterprise value", "free cash flow", "ddm", "dividend discount",
            "economic value added", "eva", "multiples", "net asset value", "graham", "buffett",
            "price-to-sales", "financial ratio", "financial ratios", "residual income"
        ]
    },
    {
        "id": "accounting",
        "fa": "حسابداری و صورت‌های مالی",
        "en": "Financial Accounting & Reporting",
        "icon": "📑",
        "roots": [
            "account", "accounting", "accountant", "balance sheet", "depreciation", "gaap",
            "ifrs", "ebitda", "ebit", "income statement", "cash flow", "audit", "auditing",
            "auditor", "cogs", "inventory", "inventories", "payable", "receivable", "amortization",
            "accrual", "accruals", "ledger", "goodwill", "retained earnings", "impairment",
            "fifo", "lifo", "journal entry", "journal", "bookkeeping", "cost of goods",
            "revenue recognition", "overhead", "operating expense", "operating expenses",
            "gross margin", "net income", "financial statement", "financial statements", "footnote",
            "footnotes", "salvage value", "cost basis", "bad debt", "contra account", "deferred tax"
        ]
    },
    {
        "id": "banking_credit",
        "fa": "بانکداری، وام و اعتبارات",
        "en": "Banking, Lending & Credit",
        "icon": "🏦",
        "roots": [
            "bank", "banking", "banks", "banker", "loan", "loans", "lending", "lender", "lenders",
            "credit", "deposit", "deposits", "ach", "borrower", "borrowing", "collateral",
            "line of credit", "checking account", "savings account", "overdraft", "prime rate",
            "libor", "sofr", "usury", "commercial bank", "investment bank", "credit union",
            "fractional reserve", "fdic", "clearing", "syndicate", "promissory note",
            "letter of credit", "debt service", "creditworthiness", "default", "subprime",
            "interbank", "central bank", "bank run", "liquidity ratio"
        ]
    },
    {
        "id": "real_estate",
        "fa": "املاک، مستغلات و تأمین مسکن",
        "en": "Real Estate & Mortgage Finance",
        "icon": "🏘️",
        "roots": [
            "real estate", "reit", "reits", "mortgage", "mortgages", "property", "properties",
            "landlord", "tenant", "foreclosure", "appraisal", "deed", "zoning", "home equity",
            "escrow", "title", "commercial real estate", "residential", "closing cost", "lease",
            "leasing", "sublease", "rent", "rental", "realtor", "homeowner", "housing",
            "easement", "lien", "condominium", "subprime mortgage"
        ]
    },
    {
        "id": "tax_law",
        "fa": "مالیات، حقوق مالی و مقررات",
        "en": "Taxation, Financial Law & Regulation",
        "icon": "⚖️",
        "roots": [
            "tax", "taxes", "taxation", "taxable", "irs", "sec", "regulation", "regulations",
            "regulatory", "compliance", "form 10", "statute", "statutory", "legal", "deduction",
            "deductions", "tax credit", "capital gain", "estate tax", "finra", "insider",
            "sarbanes", "dodd-frank", "antitrust", "lawsuit", "tax bracket", "withholding",
            "audit", "statute of limitations", "fiduciary", "securities law", "litigation",
            "subpoena", "tax shelter", "tariff", "tax avoidance", "tax evasion", "jurisdiction"
        ]
    },
    {
        "id": "retirement",
        "fa": "بازنشستگی و مزایای رفاهی",
        "en": "Retirement, Pensions & Benefits",
        "icon": "🏖️",
        "roots": [
            "401k", "401(k)", "401a", "403b", "403(b)", "roth", "ira", "pension", "pensions",
            "retirement", "social security", "annuity", "annuities", "defined benefit",
            "defined contribution", "vesting", "vested", "medicare", "457 plan", "keogh",
            "retiree", "pensioner", "post-retirement", "annuitant", "required minimum distribution", "rmd"
        ]
    },
    {
        "id": "personal_finance",
        "fa": "مالی شخصی و مدیریت بودجه",
        "en": "Personal Finance & Wealth Planning",
        "icon": "💰",
        "roots": [
            "personal finance", "credit score", "credit card", "credit cards", "credit report",
            "budget", "budgeting", "student loan", "student loans", "emergency fund", "debt",
            "wealth", "estate plan", "trust fund", "inheritance", "inherit", "living will",
            "net worth", "fico", "spending", "savings", "consumer debt", "paycheck",
            "identity theft", "personal loan", "household", "living expense", "frugal", "allowance"
        ]
    },
    {
        "id": "corporate_finance",
        "fa": "مالی شرکتی، ادغام و تملک (M&A)",
        "en": "Corporate Finance & M&A",
        "icon": "🏢",
        "roots": [
            "merger", "mergers", "acquisition", "acquisitions", "m&a", "working capital",
            "restructuring", "takeover", "capital structure", "leveraged buyout", "lbo",
            "divestiture", "spinoff", "poison pill", "corporate finance", "capital budget",
            "joint venture", "bankruptcy", "chapter 11", "liquidation", "buyback", "synergy",
            "conglomerate", "hostile", "tender offer", "recapitalization", "flotation",
            "follow-on offering", "fpo", "carve-out", "reverse merger", "spin-off"
        ]
    },
    {
        "id": "funds_portfolio",
        "fa": "صندوق‌ها و مدیریت سبد دارایی",
        "en": "Funds & Portfolio Management",
        "icon": "💼",
        "roots": [
            "etf", "etfs", "mutual fund", "mutual funds", "portfolio", "portfolios",
            "index fund", "index funds", "hedge fund", "hedge funds", "asset management",
            "asset allocation", "diversification", "endowment", "nav", "net asset value",
            "expense ratio", "sharpe", "sortino", "treynor", "active management", "passive investing",
            "benchmark", "alpha", "beta", "assets under management", "aum", "fund manager",
            "closed-end fund", "open-end fund"
        ]
    },
    {
        "id": "venture_capital",
        "fa": "سرمایه‌گذاری خطرپذیر و استارتاپ",
        "en": "Venture Capital & Private Equity",
        "icon": "🚀",
        "roots": [
            "venture capital", "private equity", "vc", "angel investor", "angel investors",
            "seed round", "seed capital", "seed funding", "series a", "series b", "series c",
            "startup", "startups", "incubator", "accelerator", "unicorn", "term sheet",
            "pre-money", "post-money", "bootstrapping", "pitch deck", "founder", "founders",
            "venture debt", "cap table", "burn rate", "runway", "exit strategy", "crowdfunding",
            "sweat equity", "accredited investor"
        ]
    },
    {
        "id": "risk_insurance",
        "fa": "مدیریت ریسک، بیمه و اکچوئری",
        "en": "Risk Management & Insurance",
        "icon": "🛡️",
        "roots": [
            "insurance", "insured", "insurer", "risk management", "underwriting", "underwriter",
            "actuarial", "actuary", "coverage", "policyholder", "policyholders", "deductible",
            "casualty", "indemnity", "moral hazard", "reinsurance", "value at risk", "var",
            "copay", "liability insurance", "life insurance", "health insurance", "premium",
            "claim", "claims", "idiosyncratic risk", "systemic risk", "adverse selection",
            "risk tolerance", "underinsured"
        ]
    },
    {
        "id": "macroeconomics",
        "fa": "اقتصاد کلان و سیاست پولی",
        "en": "Macroeconomics & Monetary Policy",
        "icon": "🏛️",
        "roots": [
            "inflation", "inflationary", "gdp", "macroeconomic", "macroeconomics", "monetary policy",
            "fiscal policy", "unemployment", "stimulus", "interest rate", "interest rates",
            "stagflation", "cpi", "deflation", "money supply", "recession", "recessionary",
            "depression", "quantitative easing", "hyperinflation", "central bank", "central banks",
            "federal reserve", "keynesian", "monetarism", "economic growth", "phillips curve",
            "aggregate demand", "aggregate supply", "sovereign debt"
        ]
    },
    {
        "id": "microeconomics",
        "fa": "اقتصاد خرد و ساختار بازار",
        "en": "Microeconomics & Market Structures",
        "icon": "⚖️",
        "roots": [
            "microeconomic", "microeconomics", "supply and demand", "elasticity", "monopoly",
            "monopolies", "oligopoly", "competition", "opportunity cost", "consumer surplus",
            "producer surplus", "deadweight loss", "game theory", "nash equilibrium",
            "marginal utility", "marginal cost", "marginal revenue", "economies of scale",
            "scarcity", "externality", "externalities", "market failure", "say's law",
            "price ceiling", "price floor", "indifference curve", "pareto", "coase theorem",
            "diminishing returns", "price elasticity"
        ]
    },
    {
        "id": "behavioral_finance",
        "fa": "اقتصاد رفتاری و روان‌شناسی بازار",
        "en": "Behavioral Finance & Psychology",
        "icon": "🧠",
        "roots": [
            "behavioral economics", "behavioral finance", "cognitive bias", "loss aversion",
            "anchoring", "herding", "herd", "mental accounting", "prospect theory",
            "overconfidence", "fomo", "confirmation bias", "sentiment", "heuristics",
            "heuristic", "framing", "panic selling", "euphoria", "market sentiment",
            "sunk cost", "endowment effect", "status quo bias", "hyperbolic discounting",
            "irrational exuberance", "investor psychology", "gambler's fallacy"
        ]
    },
    {
        "id": "commodities",
        "fa": "کالاها، انرژی و فلزات گرانبها",
        "en": "Commodities, Energy & Metals",
        "icon": "🛢️",
        "roots": [
            "commodity", "commodities", "crude oil", "oil", "petroleum", "brent", "wti",
            "gold", "silver", "natural gas", "agriculture", "precious metal", "precious metals",
            "spot price", "energy market", "opec", "wheat", "corn", "copper", "raw material",
            "raw materials", "barrel", "grain", "livestock", "soft commodity"
        ]
    },
    {
        "id": "forex_trade",
        "fa": "تجارت بین‌الملل و فارکس (FX)",
        "en": "Forex & International Trade",
        "icon": "🌐",
        "roots": [
            "forex", "fx", "currency", "currencies", "foreign exchange", "exchange rate",
            "exchange rates", "export", "exports", "import", "imports", "trade agreement",
            "wto", "balance of payment", "balance of payments", "current account", "trade deficit",
            "trade surplus", "customs", "devaluation", "purchasing power parity", "ppp",
            "protectionism", "cross rate", "peg", "international trade", "brexit", "currency war",
            "imf", "world bank"
        ]
    },
    {
        "id": "governance_ethics",
        "fa": "حاکمیت شرکتی و اخلاق حرفه‌ای",
        "en": "Corporate Governance & Ethics",
        "icon": "👔",
        "roots": [
            "governance", "board of director", "board of directors", "fiduciary duty",
            "shareholder right", "shareholder rights", "proxy voting", "code of ethic",
            "code of ethics", "business ethic", "business ethics", "executive compensation",
            "whistleblower", "csr", "esg", "stakeholder", "stakeholders", "chief executive",
            "corporate culture", "conflict of interest", "corporate charter", "corporate citizenship",
            "corporate governance", "golden parachute", "staggered board", "annual meeting", "bylaws"
        ]
    },
    {
        "id": "operations_supply_chain",
        "fa": "مدیریت عملیات و زنجیره تأمین",
        "en": "Operations & Supply Chain",
        "icon": "🚚",
        "roots": [
            "supply chain", "logistic", "logistics", "lean", "six sigma", "procurement",
            "vendor", "warehouse", "manufacturing", "production", "capacity", "lead time",
            "bottleneck", "quality control", "distribution center", "freight", "cfr", "cif",
            "just in time", "jit", "scalability", "idle time", "bill of lading", "incoterms"
        ]
    },
    {
        "id": "marketing_sales",
        "fa": "بازاریابی، برندینگ و فروش",
        "en": "Marketing, Branding & Sales",
        "icon": "📢",
        "roots": [
            "marketing", "branding", "brand", "advertising", "sales lead", "sales",
            "customer", "consumer", "pricing", "market penetration", "market orientation",
            "market share", "promotion", "crm", "distribution channel", "telemarketing",
            "direct marketing", "public relations", "pr", "b2b", "b2c", "target market",
            "value proposition", "conversion rate", "churn"
        ]
    },
    {
        "id": "human_resources",
        "fa": "منابع انسانی و روابط کارگری",
        "en": "Human Resources & Labor Relations",
        "icon": "👥",
        "roots": [
            "human resources", "hr", "labor", "employee", "employees", "employment",
            "wage", "wages", "salary", "salaries", "bonus", "hiring", "workforce",
            "labor union", "union", "severance", "onboarding", "collective bargaining",
            "minimum wage", "worker", "workers", "job", "payroll", "headcount", "turnover rate"
        ]
    },
    {
        "id": "business_strategy",
        "fa": "مدیریت کسب‌وکار و استراتژی",
        "en": "Business Strategy & Management",
        "icon": "💡",
        "roots": [] # Fallback for strategic management, business models, etc.
    }
]

TAXONOMY_BY_FA = {item["fa"]: item for item in TAXONOMY}
TAXONOMY_BY_ID = {item["id"]: item for item in TAXONOMY}

def compile_engine():
    rules = []
    for cat in TAXONOMY:
        roots = cat.get("roots", [])
        if roots:
            pats = [r"\b" + re.escape(r) for r in roots]
            combined = re.compile("|".join(pats), re.IGNORECASE)
            rules.append((cat, combined))
        else:
            rules.append((cat, None))
    return rules

COMPILED_RULES = compile_engine()

def classify_term(term: Dict[str, Any]) -> Dict[str, Any]:
    """Classify a term entry into its best-fitting category."""
    title = (term.get("term_en") or "").lower()
    slug = (term.get("slug") or "").replace("-", " ").lower()
    title_slug = f"{title} {slug}"
    
    # Priority 1: Match Title and Slug
    for cat, pattern in COMPILED_RULES:
        if pattern and pattern.search(title_slug):
            return cat
            
    # Priority 2: Match Definition & Takeaways if available and not placeholder
    defn = (term.get("definition_en") or "")
    if "fundamental concept in finance and investing" not in defn:
        defn_text = f"{defn[:350]} {' '.join(term.get('takeaways_en') or [])[:200]}".lower()
        for cat, pattern in COMPILED_RULES:
            if pattern and pattern.search(defn_text):
                return cat

    return TAXONOMY[-1]
