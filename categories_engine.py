"""
Categories Engine for Market-Dict
Comprehensive 28-category bilingual taxonomy with compiled regex patterns.
"""

import re
from typing import Any

TAXONOMY = [
    # 1. Crypto & Blockchain
    {
        "id": "crypto",
        "fa": "ارزهای دیجیتال و بلاک‌چین",
        "en": "Cryptocurrency & Blockchain",
        "icon": "🪙",
        "regex": r"\b(crypto|cryptocurrency|cryptocurrencies|bitcoin|blockchain|tokens?|wallets?|nfts?|ethereum|mining|miners?|defi|altcoins?|smart contracts?|proof of work|proof of stake|halving|satoshi|gas fees?|dapps?|daos?|cold storage|hard fork|soft fork|web3|hashrate|lightning network|memecoins?|dex|hodl|airdrop|ledgerx|erc[-\s]?\d+|tether|stablecoins?|hyperledger|digital currenc(y|ies)|solana|binance|cardano|xrp|ripple|cbdcs?|distributed ledger|peer-to-peer network)\b|(بلاک‌چین|بلاک چین|بیت‌کوین|بیت کوین|اتریوم|ارز دیجیتال|رمزارز|رمز ارز|توکن|ماینینگ|استخراج ارز|کیف پول دیجیتال|قرارداد هوشمند|اثبات سهام|اثبات کار|صرافی غیرمتمرکز|دیفای)"
    },
    # 2. Technical Analysis & Charting
    {
        "id": "technical_analysis",
        "fa": "تحلیل تکنیکال و پرایس اکشن",
        "en": "Technical Analysis & Charting",
        "icon": "📊",
        "regex": r"\b(technical analysis|technical indicators?|candlesticks?|candles?|stochastics?|oscillators?|bollinger|rsi|macd|support and resistance|trendlines?|fibonacci|head and shoulders|breakouts?|doji|momentum indicators?|relative strength|vwap|ichimoku|cup and handle|price actions?|average true range|atrs?|overbought|oversold|divergences?|swing trad(ing|er)?|scalp(ing|er)?|chart patterns?|moving averages?|pullbacks?|pivot points?|flag patterns?|pennant patterns?|trailing stops?|dead cat bounce|golden cross|death cross|keltner|parabolic|fractals?|elliott wave|volume profile|accumulation distribution|chaikin|heikin ashi|dow theory|darvas box|dmi|fisher transform|donchian channels?|tweezer|negative volume index|money flow index|mfi|nvi|bar charts?|line charts?|price bars?|dark cloud cover|shooting star|hanging man|morning star|evening star|three white soldiers|three black crows|harami|marubozu|spinning top|gravestone doji|dragonfly doji|double (bottom|top)|triple (bottom|top)|triangles?|gaps?|wedges?|rectangle pattern|charts?\b)\b|(تحلیل تکنیکال|پرایس اکشن|کندل‌استیک|اندیکاتور|اسیلاتور|میانگین متحرک|خط روند|حمایت و مقاومت|باند بولینگر|الگوی سر و شانه|فیبوناچی|واگرایی|ایچیموکو|امواج الیوت)"
    },
    # 3. Derivatives, Options & Futures
    {
        "id": "derivatives",
        "fa": "ابزارهای مشتقه، آپشن و آتی",
        "en": "Derivatives, Options & Futures",
        "icon": "⚡",
        "regex": r"\b(options?|futures?|derivatives?|swaps?|swaptions?|open interest|call options?|put options?|calls?\b|puts?\b|gamma|delta|theta|vega|rho|strike prices?|in[\s-]the[\s-]money|out[\s-]of[\s-]the[\s-]money|at[\s-]the[\s-]money|straddles?|strangles?|collars?|iron condors?|butterfly spreads?|forward contracts?|forwards?\b|hedging|hedged|underlying assets?|warrants?|implied volatilit(y|ies)|black[\s-]scholes|expiration dates?|contango|backwardation|naked options?|covered calls?|synthetic assets?|interest rate swaps?|basis risks?|cfds?|contracts? for differences?|cvrs?|contingent value rights?|exercise prices?|cheapest to deliver|ctd|cme|cboe|buy to open|buy to close|sell to open|sell to close|cash[\s-]and[\s-]carry[\s-]arbitrage|non[\s-]deliverable forward|ndf|horizontal spread|vertical spread|calendar spread|e[\s-]mini|volatility arbitrage|arbitrages?\b)\b|(مشتقه|مشتقات|قرارداد آتی|اختیار معامله|قرارداد اختیار|سوآپ|سواپ|قیمت اعمال|اختیار خرید|اختیار فروش|بلک شولز|نوسان ضمنی|پوشش ریسک|کال آپشن|پوت آپشن|قرارداد سلف|وارانت)"
    },
    # 4. Fixed Income & Bond Markets
    {
        "id": "fixed_income",
        "fa": "اوراق درآمد ثابت و بدهی",
        "en": "Fixed Income & Bond Markets",
        "icon": "📜",
        "regex": r"\b(bonds?|treasur(y|ies)|yields?|yield curves?|coupons?|debt securit(y|ies)|fixed[\s-]incomes?|debentures?|municipal bonds?|corporate bonds?|junk bonds?|sovereign debts?|t[\s-]bills?|t[\s-]notes?|maturity dates?|par values?|bond durations?|convexity|zero[\s-]coupons?|mortgage[\s-]backed|mbs|credit default swaps?|cds|accrued interests?|gilts?|bunds?|us treasur(y|ies)|yield to maturity|ytm|face values?|callable bonds?|convertible bonds?|commercial papers?|certificates? of deposit|debt instruments?|contingent convertibles?|coco bonds?|emtn|euro medium term|debt issues?|sovereign bonds?|promissory notes?|collateralized debt obligations?|cdos?|durations?|dollar duration|macaulay duration|indentures?|notes?\b|rates?\b)\b|(اوراق قرضه|اوراق مشارکت|درآمد ثابت|اوراق بدهی|کوپن اوراق|بازده تا سررسید|اسناد خزانه|صکوک|منحنی بازده|ارزش اسمی اوراق)"
    },
    # 5. Quantitative Methods & Financial Math
    {
        "id": "quant_math",
        "fa": "روش‌های کمی و ریاضیات مالی",
        "en": "Quantitative Methods & Financial Math",
        "icon": "📐",
        "regex": r"\b(quantitat(ive|ion)|probabilit(y|ies)|variances?|standard deviations?|regressions?|correlations?|anova|bayes(ian)?|central limit theorem|time value of money|compound interests?|cagr|present values?|future values?|normal distributions?|monte carlo|random walks?|arithmetic means?|geometric means?|medians?|modes?|skewness|kurtosis|confidence intervals?|statistics?|statistical|samplings?|z[\s-]scores?|t[\s-]tests?|z[\s-]tests?|f[\s-]tests?|chi[\s-]squares?|p[\s-]values?|coefficients?|hypothesis test(ing)?|null hypothes(is|es)|alternative hypothes(is|es)|standard errors?|covariances?|econometrics?|logarithms?|bell curves?|poisson|binomial|matrices|matrix|linear programming|markov|continuous compounding|rule of 72|weighted averages?|quintiles?|quartiles?|deciles?|growth rates?|sensitivity analysis|percentage change|hubbert curve|compounding|variabilit(y|ies)|uniform distributions?|degrees of freedom|data smoothing|cost[\s-]benefit analysis|numbers?\b|formulas?\b|dispersion|delphi method|random variables?)\b|(روش‌های کمی|آمار و احتمال|انحراف معیار|واریانس|رگرسیون|توزیع نرمال|آزمون فرض|فرضیه صفر|ارزش زمانی پول|سود مرکب|شبیه‌سازی مونت کارلو|همبستگی|کوواریانس|اقتصادسنجی|میانگین هندسی|انحراف از معیار)"
    },
    # 6. Real Estate & Mortgage Finance
    {
        "id": "real_estate",
        "fa": "املاک، مستغلات و تأمین مسکن",
        "en": "Real Estate & Mortgage Finance",
        "icon": "🏘️",
        "regex": r"\b(real estates?|reits?|mortgages?|propert(y|ies)|landlords?|tenants?|foreclosures?|appraisals?|deeds?|zonings?|home equity|escrows?|commercial real estates?|residential properties?|closing costs?|leases?|leasing|subleases?|rents?|rentals?|realtors?|homeowners?|housings?|easements?|liens?|condominiums?|condos?|property taxes?|tenanc(y|ies)|bungalows?|cash[\s-]out refinanc(e|ing)|cash[\s-]on[\s-]cash returns?|cap rates?|home loans?|vacation homes?|voluntary conveyance|landlocked|capital improvements?|capitalization rates?|homes?\b|houses?\b|gift letters?)\b|(املاک|مستغلات|رهن|سند ملک|اجاره|موجر|مستاجر|سرمایه‌گذاری ملکی|صندوق املاک و مستغلات|تسهیلات مسکن|زمین|عوارض نوسازی|رهن و اجاره)"
    },
    # 7. Retirement, Pensions & Benefits
    {
        "id": "retirement",
        "fa": "بازنشستگی و مزایای رفاهی",
        "en": "Retirement, Pensions & Benefits",
        "icon": "🏖️",
        "regex": r"\b(401k|401\(k\)|403b|403\(b\)|roth|iras?|pensions?|retirements?|social security|annuit(y|ies)|defined[\s-]benefits?|defined[\s-]contributions?|vest(ing|ed)|medicare|457 plans?|keogh plans?|retirees?|pensioners?|post[\s-]retirement|annuitants?|required minimum distributions?|rmds?|four percent rules?|nest eggs?|pension funds?|beneficiar(y|ies)|in[\s-]service withdrawals?|rabbi trusts?|affordable care act|aca|dpsp|deferred profit sharing|domestic relations orders?|qdros?|plans?\b|retire early|fire movement)\b|(بازنشستگی|مستمری|صندوق بازنشستگی|حق بیمه بازنشستگی|تأمین اجتماعی|مستمری‌بگیر|مزایای پایان خدمت|طرح بازنشستگی|مستمری سالانه)"
    },
    # 8. Risk Management & Insurance
    {
        "id": "risk_insurance",
        "fa": "مدیریت ریسک، بیمه و اکچوئری",
        "en": "Risk Management & Insurance",
        "icon": "🛡️",
        "regex": r"\b(insurances?|insured|insurers?|risk managements?|underwrit(ing|er|ers)|actuar(ial|y|ies)|coverages?|policyholders?|deductibles?|casualt(y|ies)|indemnit(y|ies)|moral hazards?|reinsurances?|value at risks?|vars?|copays?|liability insurances?|life insurances?|health insurances?|insurance premiums?|claims?|idiosyncratic risks?|systemic risks?|systematic risks?|adverse selections?|risk tolerances?|underinsured|loss adjustments?|umbrella polic(y|ies)|contingenc(y|ies)|counterparty risks?|universal life|group universal life|gulp|gross exposures?|black swans?|operational risks?|country risks?|ibnr|incurred but not reported|coinsurance|combined ratios?|cash surrender values?|business risks?|certainty equivalent|death benefits?|counterparty|risks?\b|hazard|hazards|open cover)\b|(بیمه|مدیریت ریسک|بیمه‌نامه|بیمه‌گذار|بیمه‌گر|اکچوئری|خسارت بیمه|حق بیمه|ریسک سیستماتیک|ارزش در معرض ریسک|بیمه عمر|بیمه مسئولیت|بیمه اتکایی|پوشش بیمه)"
    },
    # 9. Funds & Portfolio Management
    {
        "id": "funds_portfolio",
        "fa": "صندوق‌ها و مدیریت سبد دارایی",
        "en": "Funds & Portfolio Management",
        "icon": "💼",
        "regex": r"\b(etfs?|mutual funds?|portfolios?|index funds?|hedge funds?|asset managements?|asset allocations?|diversificat(ion|ed)|endowments?|navs?|net asset values?|expense ratios?|sharpe ratios?|sortino ratios?|treynors?|active management|passive invest(ing)?|benchmarks?|alphas?|betas?|assets under management|aum|fund managers?|closed[\s-]end funds?|open[\s-]end funds?|tracking errors?|growth funds?|income funds?|growth investing|value investing|equal weights?|funds?\b|buy[\s-]sides?|capital market lines?|cmls?|abnormal returns?|commingled funds?|floating rate funds?|morningstar|unaffiliated investments?|bdcs?|business development compan(y|ies)|bottom[\s-]up investing|top[\s-]down investing|total returns?|total return index|george soros|julian robertson|custodians?|asset-liability committee|alco|investments?|investing|investors?|institutional investors?|distributions?\b|front[\s-]end load|back[\s-]end load|fama|high minus low|hml|smb\b)\b|(صندوق سرمایه‌گذاری|مدیریت سبد|پورتفوی|پرتفوی|صندوق قابل معامله|صندوق شاخصی|صندوق سرمایه‌گذاری مشترک|تنوع‌بخشی|تخصیص دارایی|ضریب بتا|ضریب آلفا|ارزش خالص دارایی|نسبت شارپ|مدیر صندوق)"
    },
    # 10. Valuation & Fundamental Analysis
    {
        "id": "valuation",
        "fa": "ارزش‌گذاری و تحلیل بنیادی",
        "en": "Valuation & Fundamental Analysis",
        "icon": "🔍",
        "regex": r"\b(valuat(ion|ing)|discounted cash flows?|dcfs?|p/e ratios?|intrinsic values?|price[\s-]to[\s-]earnings|price[\s-]to[\s-]books?|ev/ebitda|ebitda multiples?|fundamental analysis|fair market values?|fair values?|book values?|cost of capital|wacc|capm|terminal values?|enterprise values?|free cash flows?|ddms?|dividend discount|economic value added|eva|price[\s-]to[\s-]sales|financial ratios?|residual incomes?|dupont analysis|margin of safety|cape ratios?|earning power values?|graham numbers?|multiples? valuation|modified dietz|comparable company analysis|cca|comparative market analysis|comps\b|ratios?\b|values?\b|returns?\b|rate of return|discount(s|ing|ed)?\b|payback(s)?\b|hurdle rates?)\b|(ارزش‌گذاری|تحلیل بنیادی|جریان وجوه نقد تنزیل شده|ارزش ذاتی|نسبت قیمت به سود|ارزش دفتری|ارزش منصفانه|هزینه سرمایه|ارزش شرکت|جریان نقد آزاد|حاشیه امنیت)"
    },
    # 11. Financial Accounting & Reporting
    {
        "id": "accounting",
        "fa": "حسابداری و صورت‌های مالی",
        "en": "Financial Accounting & Reporting",
        "icon": "📑",
        "regex": r"\b(account(ing|ant|ants)?|balance sheets?|depreciat(ion|ed)|gaap|ifrs|ebitda|ebit|ebitdar|income statements?|cash flows?|cash flow statements?|audits?|auditing|auditors?|cogs|inventor(y|ies)|accounts? payables?|accounts? receivables?|amortizat(ion|ed)|accruals?|ledgers?|goodwills?|retained earnings|impairments?|fifo|lifo|journal entry|bookkeep(ing|er)?|cost of goods sold|revenue recognitions?|overhead costs?|operating expenses?|gross margins?|net incomes?|operating incomes?|financial statements?|footnotes? to financial|salvage values?|cost basis|bad debts?|contra accounts?|deferred tax(es)?|direct costs?|indirect costs?|cost accounting|trial balances?|controllers?|cash conversion cycles?|cash equivalents?|capital employed|capitalized costs?|capitalized interests?|working capitals?|operating cash flows?|fiscal years?|general ledgers?|quarter on quarter|qoq|year[\s-]over[\s-]year|yoy|book[\s-]to[\s-]bill|gross revenues?|gross profits?|normalized earnings|earnings reports?|entity theory|cash managements?|cash ratios?|chart of accounts|coa|quick ratios?|asset turnover ratios?|triple bottom line|tbl|turnovers?|total[\s-]debt[\s-]to[\s-]total[\s-]assets|current assets?|debits?\b|contingent (assets?|liabilities|liability)|contributed capital|cook the books|cost control|cost of revenue|cost[\s-]plus|cost[\s-]volume[\s-]profit|cvp|declining balance method|defensive interval ratio|deferred interest|deferred revenue|revenues?\b|expenses?\b|costs?\b|earnings?\b|assets?\b|incomes?\b|profits?\b|losses?\b|gross\b|net\b|deplet(ion|ed)\b|disclos(ure|ures)\b|direct method|indirect method|double[\s-]entry|single[\s-]entry|disposition\b)\b|(حسابداری|صورت مالی|ترازنامه|صورت سود و زیان|صورت جریان وجوه نقد|استهلاک|حسابرسی|حسابرس|بهای تمام شده|بدهی جاری|مطالبات|دفتر روزنامه|دفتر کل|سود انباشته|درآمد ناخالص|سود خالص|هزینه عملیاتی|حاشیه سود ناخالص|گردش دارایی)"
    },
    # 12. Banking, Lending & Credit
    {
        "id": "banking_credit",
        "fa": "بانکداری، وام و اعتبارات",
        "en": "Banking, Lending & Credit",
        "icon": "🏦",
        "regex": r"\b(banks?|banking|bankers?|loans?|lending|lenders?|borrowers?|borrowings?|collaterals?|lines? of credit|checking accounts?|savings accounts?|overdrafts?|prime rates?|libor|sofr|usury|commercial banks?|investment banks?|credit unions?|fractional reserves?|fdic|syndicated loans?|letters? of credit|debt services?|creditworthiness|default risks?|subprime loans?|interbanks?|central banks?|bank runs?|liquidity ratios?|repos?|repurchase agreements?|canceled checks?|capital adequacy|basel|interest[\s-]only loans?|npls?|non[\s-]performing loans?|cash advances?|money transfers?|deposits?|hawala|excess reserves?|automated clearing house|achs?|bear stearns|capital adequacy ratios?|car ratios?|checks?\b|collection agenc(y|ies)|community reinvestment act|cra|debit cards?|debts?\b|debtors?|creditors?|default rates?|delinquency rates?|covenants?\b|payments?\b|moneys?\b|credits?\b|deposit(ory|ary)?\b|financ(e|ing)\b|guarante(e|es|ed)\b|fees?\b|demand draft|disintermediat(ion|ed)\b|documentary collection|underbanked|obligor|payee|reserve requirements?|micr\b)\b|(بانکداری|بانک|وام|تسهیلات بانکی|اعتبار|سپرده|بانک مرکزی|ضمانت‌نامه بانکی|اعتبار اسنادی|سفته|چک|کفایت سرمایه|ذخیره قانونی|حواله|بدهی|تعهدنامه مالی)"
    },
    # 13. Commodities, Energy & Metals
    {
        "id": "commodities",
        "fa": "کالاها، انرژی و فلزات گرانبها",
        "en": "Commodities, Energy & Metals",
        "icon": "🛢️",
        "regex": r"\b(commodit(y|ies)|crude oils?|oils?\b|petroleum|brent|wti|golds?|silver|natural gas|agricultures?|precious metals?|spot prices?|energy markets?|opec|wheats?|corns?|coppers?|raw materials?|barrels?|grains?|livestocks?|soft commodit(y|ies)|diamonds?|gsci|energy returns?|eroi|petrodollars?)\b|(کالاها|فلزات گرانبها|نفت خام|نفت برنت|طلا|نقره|گاز طبیعی|اوپک|محصولات کشاورزی|مواد خام|بازار کالا|بورس کالا)"
    },
    # 14. Forex & International Trade
    {
        "id": "forex_trade",
        "fa": "تجارت بین‌الملل و فارکس (FX)",
        "en": "Forex & International Trade",
        "icon": "🌐",
        "regex": r"\b(forex|fx|currenc(y|ies)|foreign exchanges?|exchange rates?|exports?|imports?|trade agreements?|wto|balance of payments?|current accounts?|trade deficits?|trade surplus(es)?|customs?|devaluat(ion|ed)|purchasing power parity|ppps?|protectionisms?|cross rates?|currency pegs?|international trade|brexit|currency wars?|imf|world banks?|free trades?|comparative advantages?|dumpings?|euros?|eurocurrency|terms of trade|tot|certificates? of origin|huf|hungarian forint|internationalization|countertrade|arab league|foreign\b|international\b|embargo(es)?|transaction exposure)\b|(فارکس|ارزهای خارجی|نرخ ارز|تجارت بین‌الملل|صادرات|واردات|تراز تجاری|صندوق بین‌المللی پول|بانک جهانی|سازمان تجارت جهانی|برابری قدرت خرید)"
    },
    # 15. Macroeconomics & Monetary Policy
    {
        "id": "macroeconomics",
        "fa": "اقتصاد کلان و سیاست پولی",
        "en": "Macroeconomics & Monetary Policy",
        "icon": "🏛️",
        "regex": r"\b(inflat(ion|ionary)|gdps?|macroeconomic(s)?|monetary polic(y|ies)|fiscal polic(y|ies)|unemployment|stimulus|interest rates?|stagflation|cpis?|consumer price index|deflat(ion|ionary)|money supply|recessions?|recessionary|depressions?|quantitative easing|hyperinflat(ion|ionary)|federal reserve|keynesian|monetarism|economic growths?|phillips curves?|aggregate demands?|aggregate supply|national incomes?|contractionary|expansionary|cost[\s-]push|demand[\s-]pull|cost[\s-]of[\s-]living|cola|gross domestic|gross national|gnps?|group of 20|g[\s-]?20|g[\s-]?8|g[\s-]?7|business cycles?|economic cycles?|gini (index|coefficient)|cap and trade|bric|human development index|hdi|net national product|nnp|goldilocks econom(y|ies)|boom and bust cycle|austerity|circular flow of income|classical economics|closed econom(y|ies)|centrally planned econom(y|ies)|communism|neoliberalism|karl marx|invisible hand|kyoto protocol|united nations|crowding out effect|david ricardo|deficits?\b|econom(y|ies|ic|ics)\b|growth\b|policy|policies|disinflat(ion|ionary)|dollarizat(ion|ed)|bubbles?\b|mania\b|dotcom\b|demographic(s)?|socialism|paradox of thrift|tobin|expansion)\b|(اقتصاد کلان|تورم|تولید ناخالص داخلی|سیاست پولی|سیاست مالی|رکود اقتصادی|شاخص قیمت مصرف‌کننده|عرضه پول|تسهیل مقداری|بیکاری|کسری بودجه|رشد اقتصادی|چرخه اقتصادی|کمونیسم|دست نامرئی)"
    },
    # 16. Microeconomics & Market Structures
    {
        "id": "microeconomics",
        "fa": "اقتصاد خرد و ساختار بازار",
        "en": "Microeconomics & Market Structures",
        "icon": "⚖️",
        "regex": r"\b(microeconomic(s)?|supply and demand|elasticit(y|ies)|monopol(y|ies)|monopolistic|oligopol(y|ies)|competitions?|opportunity costs?|consumer surplus|producer surplus|deadweight loss|game theor(y|ies)|nash equilibrium|marginal utilit(y|ies)|marginal costs?|marginal revenues?|economies of scale|scarcit(y|ies)|externalit(y|ies)|market failures?|say's law|price ceilings?|price floors?|indifference curves?|pareto|coase theorem|diminishing returns|price elasticity|buyer's markets?|seller's markets?|market equilibriums?|equilibriums?|collusion|ceteris paribus|arrow's impossibility theorem|theor(y|ies)\b|demand(s|ed)?\b|diseconom(y|ies)\b|disequilibrium\b|veblen goods?|giffen goods?)\b|(اقتصاد خرد|عرضه و تقاضا|کشش قیمتی|انحصار|انحصار چندجانبه|هزینه فرصت|نظریه بازی‌ها|تعادل نش|مطلوبیت نهایی|هزینه نهایی|صرفه‌های ناشی از مقیاس)"
    },
    # 17. Behavioral Finance & Psychology
    {
        "id": "behavioral_finance",
        "fa": "اقتصاد رفتاری و روان‌شناسی بازار",
        "en": "Behavioral Finance & Psychology",
        "icon": "🧠",
        "regex": r"\b(behavioral economics?|behavioral finances?|cognitive biass?(es)?|loss aversions?|anchor(ing)?|herdings?|herd mentalit(y|ies)|mental accounting|prospect theor(y|ies)|overconfidences?|fomo|confirmation biass?(es)?|sentiments?|heuristics?|framings?|panic sell(ing)?|euphoria|market sentiments?|sunk costs?|endowment effects?|status quo biass?(es)?|hyperbolic discounting|irrational exuberance|investor psychology|gambler's fallac(y|ies)|hindsight biass?(es)?|contrarians?|fear and greed|groupthinks?|capitulations?|home bias|greater fool theory|psycholog(y|ical))\b|(اقتصاد رفتاری|روان‌شناسی بازار|سوگیری شناختی|زیان‌گریزی|رفتار گله‌ای|حسابداری ذهنی|اعتماد به نفس کاذب|احساسات بازار|شاخص ترس و طمع|هزینه غرق‌شده)"
    },
    # 18. Taxation, Financial Law & Regulation
    {
        "id": "tax_law",
        "fa": "مالیات، حقوق مالی و مقررات",
        "en": "Taxation, Financial Law & Regulation",
        "icon": "⚖️",
        "regex": r"\b(tax(es)?|taxat(ion|ed)|taxables?|irs|sec\b|regulat(ion|ions|ory)|compliances?|form 10[-\s]?[kq]?|w[-\s]?\d+ forms?|forms?\b|statutes?|statutory|legals?|deduct(ion|ions)|tax credits?|capital gains?|estate taxes?|finra|insider trad(ing)?|sarbanes[-\s]?oxley|dodd[-\s]?frank|antitrust|lawsuits?|tax brackets?|withholdings?|fiduciar(y|ies)|securities laws?|litigat(ion|ed)|subpoenas?|tax shelters?|tariffs?|tax avoidances?|tax evasions?|jurisdictions?|loss carryforwards?|carrybacks?|uniform commercial code|ucc|partnership acts?|attorneys?|contract laws?|eins?|employer identification numbers?|enrolled agents?|capital loss carryovers?|novations?|best endeavors?|buy and sell agreements?|limited partnerships?|lps?|llcs?|c corporations?|s corporations?|money laundering|ponzi schemes?|wire fraud|racketeering|jones act|statute of limitations|notar(y|ization)|exempt transactions?|exempt incomes?|joint return tests?|section 1250|acts? of \d{4}|environmental protection agency|epa|zzzz best|unlimited liability|non[\s-]disclosure agreements?|ndas?|common law|compensatory damages|letters? of intent|lois?\b|memorandums? of understanding|mous?\b|agreements?\b|contracts?\b|copyrights?|delaware corporations?|acts?\b|laws?\b|rules?\b|clause|clauses|deregulat(ion|ed)|deposit(ion|ions)|interstate commerce|filings?|double irish|domicile|uncle sam|laffer curve|general partnership)\b|(مالیات|قانون مالیات|معافیت مالیاتی|سازمان امور مالیاتی|مقررات مالی|حقوقی|جرایم مالیاتی|مالیات بر ارزش افزوده|مالیات بر عایدی سرمایه|اظهارنامه مالیاتی|ممیزی مالیاتی|پولشویی|طرح پانزی|کلاهبرداری مالی)"
    },
    # 19. Corporate Governance & Organization
    {
        "id": "governance_ethics",
        "fa": "حاکمیت شرکتی و ساختار سازمانی",
        "en": "Corporate Governance & Organization",
        "icon": "👔",
        "regex": r"\b(governances?|boards? of directors?|fiduciary dut(y|ies)|shareholder rights?|proxy vot(ing)?|codes? of ethics?|business ethics?|executive compensations?|whistleblowers?|csrs?|esg|stakeholders?|chief executives?|corporate cultures?|conflicts? of interest|corporate charters?|corporate citizenship|corporate governances?|staggered boards?|annual meetings?|bylaws?|clawbacks?|ethical invest(ing)?|c[\s-]suites?|cfos?|chief financial officers?|coos?|chief operating officers?|ctos?|chief technology officers?|ceos?|organizational structures?|bureaucrac(y|ies)|agency theor(y|ies)|checks and balances|incumbents?|holding compan(y|ies)|holding\b|corporate hierarch(y|ies)|yale school of management|corporations?\b|compan(y|ies)\b|dissenters? rights|voting rights|preemptive rights|demutualization|quorums?|gmbh|waiver of notice)\b|(حاکمیت شرکتی|هیئت مدیره|اخلاق کسب‌وکار|مسئولیت اجتماعی شرکت|افشاگر|پاداش مدیران|حقوق ذی‌نفعان|اساسنامه شرکت|مدیرعامل|مدیر ارشد مالی|شرکت هلدینگ)"
    },
    # 20. Corporate Finance & M&A
    {
        "id": "corporate_finance",
        "fa": "مالی شرکتی، ادغام و تملک (M&A)",
        "en": "Corporate Finance & M&A",
        "icon": "🏢",
        "regex": r"\b(mergers?|acquisitions?|m&a|restructur(ing|ed)|takeovers?|capital structures?|leveraged buyouts?|lbos?|divestitures?|spinoffs?|poison pills?|corporate finances?|capital budgets?|joint ventures?|bankruptc(y|ies)|chapter 11|liquidat(ion|ed)|buybacks?|synerg(y|ies)|conglomerates?|hostile takeovers?|hostile bids?|tender offers?|recapitalizat(ion|ed)|flotations?|follow[\s-]on offerings?|fpos?|carve[\s-]outs?|reverse mergers?|golden parachutes?|white knights?|crown jewels?|buyouts?|management buyouts?|mbos?|capital projects?|capital investments?|leveraged leases?|build[\s-]operate[\s-]transfer|bot contracts?|capitalization|bimbo|debt financing|debt overhang|debt[\s-]to[\s-]capital|debtor in possession|dip|degree of (financial|combined|operating) leverage|deleverag(ing|ed)?|consolidat(ion|e)|capitaliz(e|ation)|corporate\b|capitals?\b|divest(ment|ing)?|disinvestment|stalking[\s-]horse)\b|(مالی شرکتی|ادغام و تملک|خرید اهرمی|تجدید ساختار|تصاحب خصمانه|ورشکستگی|فروش دارایی|هم‌افزایی|پیشنهاد مناقصه|ساختار سرمایه)"
    },
    # 21. Venture Capital & Private Equity
    {
        "id": "venture_capital",
        "fa": "سرمایه‌گذاری خطرپذیر و استارتاپ",
        "en": "Venture Capital & Private Equity",
        "icon": "🚀",
        "regex": r"\b(venture capitals?|private equit(y|ies)|vcs?|angel investors?|seed rounds?|seed capitals?|seed fundings?|series [abcde]\b|startups?|incubators?|accelerators?|unicorns?|term sheets?|pre[\s-]money|post[\s-]money|bootstrapp(ing)?|pitch decks?|founders?|venture debts?|cap tables?|capitalization tables?|burn rates?|runways?|exit strateg(y|ies)|crowdfund(ing)?|sweat equit(y|ies)|accredited investors?|convertible notes?|safe agreements?|carried interests?)\b|(سرمایه‌گذاری خطرپذیر|استارتاپ|سرمایه‌گذار فرشته|مرحله بذری|سرمایه خصوصی|شتاب‌دهنده|یونیکورن|جذب سرمایه|خروج استارتاپی)"
    },
    # 22. Operations & Supply Chain
    {
        "id": "operations_supply_chain",
        "fa": "مدیریت عملیات و زنجیره تأمین",
        "en": "Operations & Supply Chain",
        "icon": "🚚",
        "regex": r"\b(supply chains?|logistics?|lean manufactur(ing)?|six sigma|procurements?|vendors?|warehouses?|manufacturing|productions?|capacit(y|ies)|lead times?|bottlenecks?|quality controls?|distribution centers?|freights?|cfr|cif|just in time|jit|scalabilit(y|ies)|idle times?|bill of lading|incoterms?|total quality management|tqm|inventory managements?|eoq|kanban|business continuity|bcps?|capital goods|outsourc(ing)?|kpos?|bpos?|business process outsourcing|mass customization|requests? for proposals?|rfps?|cash on delivery|cod|industrial revolution|consignments?|deliverables?|delivered at frontier|daf|delivered ex ship|des|operations?|operating|supply)\b|(زنجیره تأمین|لجستیک|مدیریت عملیات|تولید ناب|شش سیگما|انبارداری|کنترل کیفیت|زمان تحویل|تولید به هنگام|مدیریت موجودی|بارنامه|اینکوترمز)"
    },
    # 23. Marketing, Branding & Sales
    {
        "id": "marketing_sales",
        "fa": "بازاریابی، برندینگ و فروش",
        "en": "Marketing, Branding & Sales",
        "icon": "📢",
        "regex": r"\b(marketings?|brandings?|brands?|advertis(ing|ement|ements)|sales leads?|sales?\b|customers?|consumers?|pricings?|market penetrations?|market orientations?|market shares?|promotions?|crms?|distribution channels?|telemarketings?|direct marketings?|public relations?|prs?|b2b|b2c|b2g|business to government|target markets?|value propositions?|conversion rates?|churn rates?|loss leaders?|ecommerce|brand equit(y|ies)|cost per click|cpcs?|cost per thousand|cpms?|click[\s-]through|ctrs?|gross merchandise values?|gmvs?|cash cows?|franchises?|fast fashion|channel stuffing|consumerism|commercialization|cross[\s-]sell|dagmar|mobile commerce)\b|(بازاریابی|برندینگ|تبلیغات|فروش|سهم بازار|مشتری‌مداری|روابط عمومی|تجارت الکترونیک|نرخ تبدیل|ارزش پیشنهادی|کانال توزیع)"
    },
    # 24. Human Resources & Labor Relations
    {
        "id": "human_resources",
        "fa": "منابع انسانی و روابط کارگری",
        "en": "Human Resources & Labor Relations",
        "icon": "👥",
        "regex": r"\b(human resources?|hrs?|labor|labour|employees?|employments?|wages?|salar(y|ies)|bonuses?|hirings?|workforces?|labor unions?|unions?\b|severances?|onboardings?|collective bargainings?|minimum wages?|workers?|payrolls?|headcounts?|turnover rates?|workplace safet(y|ies)|brown bag meetings?|golden handcuffs?|organizational behavior|interpersonal skills|brain drain|cover letters?|benefits?\b|hawthorne effect)\b|(منابع انسانی|حقوق و دستمزد|کارکنان|استخدام|اتحادیه کارگری|پاداش|روابط کارگری|حداقل دستمزد|ایمنی محیط کار|فرار مغزها)"
    },
    # 25. Fintech, Technology & Financial Data
    {
        "id": "fintech_data",
        "fa": "فین‌تک، فناوری و داده‌های مالی",
        "en": "Fintech, Technology & Financial Data",
        "icon": "💻",
        "regex": r"\b(fintechs?|financial technolog(y|ies)|artificial intelligence|ais?\b|machine learnings?|big data|cloud comput(ing)?|saas|softwares?|apis?\b|cybersecurit(y|ies)|data analytics?|business intelligence|bis?\b|visual basics?|vbas?|moore's law|capital iq|automations?|data sciences?|neural networks?|deep learning|predictive analytics?|databases?|it infrastructures?|internet of things|iot|value[\s-]added networks?|van|edgar|wearable technology|dark web|data warehousing|decision support systems?|dss|technolog(y|ies)|datas?|disruptive innovation|innovat(ion|ions)|gpus?|hardware|insurtech|regtech)\b|(فین‌تک|فناوری مالی|هوش مصنوعی|یادگیری ماشین|کلان داده|رایانش ابری|تحلیل داده|پایگاه داده)"
    },
    # 26. Personal Finance & Wealth Planning
    {
        "id": "personal_finance",
        "fa": "مالی شخصی و مدیریت بودجه",
        "en": "Personal Finance & Wealth Planning",
        "icon": "💰",
        "regex": r"\b(personal finances?|credit scores?|credit cards?|credit reports?|budgets?|budget(ing|ed)?|student loans?|emergency funds?|wealth managements?|estate plann(ing)?|trust funds?|inheritances?|inherit(ed)?|living wills?|net worths?|fico|spendings?|savings?\b|consumer debts?|paychecks?|identity thefts?|personal loans?|households?|living expenses?|frugal|allowances?|debt consolidations?|payday loans?|family trusts?|probates?|estates?\b|annualized incomes?|personal propert(y|ies)|certified financial planners?|cfps?|carding|american dream|generation x|gen x|declarations? of trust|trusts?\b|trustees?|personal\b|executors?|per stirpes)\b|(مالی شخصی|بودجه‌بندی شخصی|مدیریت ثروت|کارت اعتباری|وام دانشجویی|صندوق اضطراری|برنامه‌ریزی ارث|انتقال ترکه|دارایی خالص شخصی|هزینه خانوار|پس‌انداز)"
    },
    # 27. Stock Market & Equities Trading
    {
        "id": "stock_market",
        "fa": "بازار سهام و معاملات",
        "en": "Stock Market & Equities Trading",
        "icon": "📈",
        "regex": r"\b(stocks?|shares?|shareholders?|dividends?|trad(ing|er|ers)|equities|equity markets?|ipos?|nasdaq|nyse|market makers?|bull(ish)?|bear(ish)?|bull markets?|bear markets?|short sal(e|es)|short sell(ing)?|short sellers?|ask prices?|bid prices?|limit orders?|market orders?|stop loss(es)?|stop orders?|iceberg orders?|fill or kill|brokers?|brokerages?|tickers?|day trading|public floats?|common stocks?|preferred stocks?|secondary markets?|otc|over[\s-]the[\s-]counter|order books?|listings?|delistings?|trading volumes?|rall(y|ies)|sell[\s-]offs?|odd lots?|round lots?|blue chips?|penny stocks?|market caps?|floor traders?|quotes?|clearinghouses?|direct market access|dma|high frequency trading|hft|short interests?|squeezes?|bag holders?|wash trad(e|ing)|pump and dump|circuit breakers?|depth of market|buy and hold|buy the dips?|buy to cover|buying on margin|buying power|margin calls?|stock splits?|reverse splits?|ex[\s-]dividends?|capital markets?|initial public offerings?|s&p 500|dow jones|dow 30|dax (index)?|market index(es)?|equities trading|gics|buy[\s-]ins?|commissions?|clearing|churning|dark pools?|day orders?|dealers?\b|dealer markets?|cusip numbers?|market corrections?|corrections?\b|markets?\b|indices\b|index(es)?|orders?\b|trades?\b|prices?\b|offer(s|ing|ings)?|dpo|depositary receipts?|adrs?\b|gdrs?\b|dematerialization|demat|sectors?|industr(y|ies)|securit(y|ies)|dogs of the dow|dow\b|spreads?\b|short interest|nikkei|speculat(or|ion)|painting the tape|series \d+)\b|(بازار سهام|بورس|سهام|سهامدار|عرضه اولیه|معاملات روزانه|کارگزار|کارگزاری|سفارش محدود|سفارش بازار|حد ضرر|فروش استقراضی|بازار خرسی|بازار گاوی|نماد معاملاتی|سود نقدی|شاخص کل|شاخص بورس|مارجین|صف خرید|صف فروش)"
    },
    # 28. Business Strategy & Management (Fallback)
    {
        "id": "business_strategy",
        "fa": "مدیریت کسب‌وکار و استراتژی",
        "en": "Business Strategy & Management",
        "icon": "💡",
        "regex": r".*"
    }
]

TAXONOMY_BY_ID: dict[str, dict[str, Any]] = {c["id"]: c for c in TAXONOMY}
TAXONOMY_BY_FA: dict[str, dict[str, Any]] = {c["fa"]: c for c in TAXONOMY}

# Comprehensive mapping of legacy or variant category names to canonical Persian names
CATEGORY_ALIASES: dict[str, str] = {
    # Stock market variants
    "بورس، سهام و بازار سرمایه": "بازار سهام و معاملات",
    "stock_capital_markets": "بازار سهام و معاملات",
    "stock & capital markets": "بازار سهام و معاملات",

    # Macroeconomics variants
    "اقتصاد کلان و سیاست‌های پولی": "اقتصاد کلان و سیاست پولی",
    "macroeconomics_alt": "اقتصاد کلان و سیاست پولی",

    # Banking variants
    "بانکداری و خدمات مالی": "بانکداری، وام و اعتبارات",

    # Forex variants
    "ارزها و بازارهای فارکس": "تجارت بین‌الملل و فارکس (FX)",

    # Technical analysis variants
    "تحلیل تکنیکال و نموداری": "تحلیل تکنیکال و پرایس اکشن",

    # Accounting & Tax variants
    "قوانین و صورت‌های مالی": "مالیات، حقوق مالی و مقررات",
    "accounting_regulations": "مالیات، حقوق مالی و مقررات",
    "حسابداری و استانداردهای مالی": "حسابداری و صورت‌های مالی",
    "accounting_standards": "حسابداری و صورت‌های مالی",

    # Real estate variants
    "املاک، مستغلات و مسکن": "املاک، مستغلات و تأمین مسکن",

    # Crypto variants
    "بلاکچین، ارز دیجیتال و رمزدارایی‌ها": "ارزهای دیجیتال و بلاک‌چین",
}

def normalize_category(cat_name: Any) -> dict[str, Any]:
    """
    Given any category identifier, Persian name, English name, or legacy variant,
    returns the canonical category dictionary from TAXONOMY (with id, fa, en, icon).
    Defaults to the fallback category if unrecognized.
    """
    if not cat_name or not isinstance(cat_name, str):
        return TAXONOMY[-1]

    name = cat_name.strip()
    # 1. Exact match in canonical Persian names
    if name in TAXONOMY_BY_FA:
        return TAXONOMY_BY_FA[name]

    # 2. Match in legacy aliases
    if name in CATEGORY_ALIASES:
        canonical_fa = CATEGORY_ALIASES[name]
        if canonical_fa in TAXONOMY_BY_FA:
            return TAXONOMY_BY_FA[canonical_fa]

    # 3. Match by ID (case-insensitive)
    name_lower = name.lower()
    if name_lower in TAXONOMY_BY_ID:
        return TAXONOMY_BY_ID[name_lower]

    # 4. Match in alias by lowercase
    for alias, canon in CATEGORY_ALIASES.items():
        if alias.lower() == name_lower and canon in TAXONOMY_BY_FA:
            return TAXONOMY_BY_FA[canon]

    # 5. Match by English name (case-insensitive)
    for cat in TAXONOMY:
        if cat["en"].lower() == name_lower:
            return cat

    # Default fallback
    return TAXONOMY[-1]

COMPILED_RULES = [(cat, re.compile(cat["regex"], re.IGNORECASE)) for cat in TAXONOMY]

def classify_term(term: dict[str, Any]) -> dict[str, Any]:
    """Classify a term into its primary financial category."""
    title = (term.get("term_en") or "").lower()
    slug = (term.get("slug") or "").replace("-", " ").lower()
    title_slug = f"{title} {slug}"
    title_fa = (term.get("term_fa") or "").lower()

    # Priority 1: Title and Slug (EN)
    for cat, pattern in COMPILED_RULES[:-1]:
        if pattern.search(title_slug):
            return cat

    # Priority 2: Title (FA)
    if title_fa:
        for cat, pattern in COMPILED_RULES[:-1]:
            if pattern.search(title_fa):
                return cat

    # Priority 3: Definition & Takeaways (EN)
    defn_en = term.get("definition_en") or ""
    if "fundamental concept in finance" not in defn_en and len(defn_en) > 20:
        sample = defn_en[:400]
        for cat, pattern in COMPILED_RULES[:-1]:
            if pattern.search(sample):
                return cat

    # Priority 4: Definition (FA)
    defn_fa = term.get("definition_fa") or ""
    if len(defn_fa) > 20:
        sample = defn_fa[:400]
        for cat, pattern in COMPILED_RULES[:-1]:
            if pattern.search(sample):
                return cat

    # Fallback: Business Strategy & Management
    return TAXONOMY[-1]
