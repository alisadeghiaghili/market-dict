"""
Comprehensive Bilingual Financial Knowledge Base (English & Persian)
Rich, high-precision translations, categories, and explanations.
"""

CORE_TRANSLATIONS = {
    # Numbers
    "1%/10 Net 30": {
        "term_fa": "تخفیف ۱٪ نقدی در ۱۰ روز، مهلت ۳۰ روز",
        "category": "حسابداری و اعتبارات",
        "definition_en": "A trade credit cash discount term where the debtor receives a 1% discount if payment is completed within 10 days; otherwise, the full balance is due within 30 days.",
        "definition_fa": "یک شرط اعتباری تجاری که در صورت پرداخت صورت‌حساب ظرف ۱۰ روز، ۱٪ تخفیف نقدی به خریدار اعطا می‌کند؛ در غیر این‌صورت کل مبلغ باید ظرف ۳۰ روز پرداخت شود.",
        "takeaways_en": ["Incentivizes early payment", "Improves cash flow velocity for vendors"],
        "takeaways_fa": ["ایجاد انگیزه برای پرداخت سریع‌تر بدهی", "بهبود سرعت گردش نقدینگی فروشنده"]
    },
    "10-K": {
        "term_fa": "گزارش سالانه ۱۰-کا (فرم 10-K)",
        "category": "قوانین و صورت‌های مالی",
        "definition_en": "A comprehensive annual report filed by publicly traded companies about their financial performance, audited and mandated by the SEC.",
        "definition_fa": "گزارش جامع و حسابرسی‌شده سالانه‌ای است که تمام شرکت‌های سهامی عام موظفند طبق قوانین کمیسیون بورس و اوراق بهادار (SEC) از عملکرد مالی خود منتشر کنند.",
        "takeaways_en": ["Mandatory audited disclosure", "Contains balance sheet, income statement, and executive discussion"],
        "takeaways_fa": ["افشای الزامی حسابرسی‌شده", "شامل ترازنامه، صورت سود و زیان و تحلیل مدیریت"]
    },
    "10-Q SEC Form": {
        "term_fa": "گزارش سه‌ماهه ۱۰-کیو (فرم 10-Q)",
        "category": "قوانین و صورت‌های مالی",
        "definition_en": "A quarterly report filed by public companies that provides an unaudited continuous view of financial condition during the fiscal year.",
        "definition_fa": "گزارش سه‌ماهه حسابرسی‌نشده‌ای که شرکت‌های سهامی عام برای تشریح وضعیت مالی مداوم خود در طول سال مالی به SEC ارائه می‌دهند.",
        "takeaways_en": ["Filed 3 times a year", "Unaudited quarterly updates"],
        "takeaways_fa": ["سه بار در سال ارائه می‌شود", "به‌روزرسانی فصلی بدون حسابرسی کامل"]
    },
    "10-Year Treasury Note": {
        "term_fa": "اوراق خزانه ۱۰ ساله آمریکا",
        "category": "اوراق بهادار و بدهی",
        "definition_en": "A debt obligation issued by the United States government with a fixed maturity of 10 years, serving as a global interest rate benchmark.",
        "definition_fa": "اوراق قرضه دولتی منتشره توسط وزارت خزانه‌داری آمریکا با سررسید ۱۰ ساله که بازده آن به عنوان مهم‌ترین نرخ بهره بدون ریسک و معیار اقتصادی جهان شناخته می‌شود.",
        "takeaways_en": ["Global benchmark for long-term yields", "Backed by the US government"],
        "takeaways_fa": ["معیار جهانی بازده اوراق بلندمدت", "پشتوانه کامل دولت فدرال"]
    },
    "401(k) Plan": {
        "term_fa": "طرح بازنشستگی ۴۰۱(ک)",
        "category": "سرمایه‌گذاری و بازنشستگی",
        "definition_en": "A company-sponsored retirement account that employees can contribute to with tax advantages, often featuring employer matching.",
        "definition_fa": "طرح پس‌انداز بازنشستگی تحت حمایت کارفرما که کارمندان می‌توانند مبالغی از حقوق خود را قبل یا بعد از مالیات در آن سرمایه‌گذاری کنند.",
        "takeaways_en": ["Tax-deferred investment", "Potential employer matching"],
        "takeaways_fa": ["معافیت یا تعویق مالیاتی", "امکان پرداخت همپوشان توسط کارفرما"]
    },
    "51% Attack": {
        "term_fa": "حمله ۵۱ درصدی (بلاکچین)",
        "category": "ارزهای دیجیتال و بلاکچین",
        "definition_en": "An attack on a blockchain by a single entity or pool that controls more than 50% of the network's mining power or hash rate.",
        "definition_fa": "حمله‌ای در شبکه‌های بلاکچین که در آن یک گروه یا ماینر با تصاحب بیش از ۵۰ درصد قدرت محاسباتی شبکه (هش‌ریت)، می‌تواند تراکنش‌ها را دستکاری کرده یا دوباره خرج کند.",
        "takeaways_en": ["Threatens blockchain immutability", "Enables double spending"],
        "takeaways_fa": ["تهدید تغییرناپذیری بلاکچین", "امکان دوبار خرج کردن سکه‌ها (Double Spending)"]
    },
    "52-Week High/Low": {
        "term_fa": "بالاترین و پایین‌ترین قیمت ۵۲ هفته",
        "category": "تحلیل تکنیکال و بازار",
        "definition_en": "The highest and lowest price at which an asset, such as a stock, has traded during the previous 52 weeks (one year).",
        "definition_fa": "بیشترین و کمترین قیمتی که یک دارایی یا سهم طی یک سال گذشته (۵۲ هفته) در بازار معامله شده است و به عنوان سطوح حمایت و مقاومت روانی ارزیابی می‌شود.",
        "takeaways_en": ["Key psychological support and resistance levels", "Indicates long-term momentum"],
        "takeaways_fa": ["سطوح کلیدی حمایت و مقاومت روانی", "نشان‌دهنده شتاب حرکتی در مقیاس یک‌ساله"]
    },

    # Letter A
    "Absolute Advantage": {
        "term_fa": "مزیت مطلق",
        "category": "اقتصاد و تجارت بین‌الملل",
        "definition_en": "The ability of an entity to produce a greater quantity of a good or service with the same or fewer resources than competitors.",
        "definition_fa": "توانایی یک تولیدکننده یا کشور در تولید کالا یا خدمتی با بازدهی بیشتر و مصرف منابع کمتر در مقایسه با رقبا.",
        "takeaways_en": ["First formulated by Adam Smith", "Focuses on direct input efficiency"],
        "takeaways_fa": ["نخستین بار توسط آدام اسمیت مطرح شد", "تمرکز بر کارایی مستقیم نهاده‌ها"]
    },
    "Accounting Equation": {
        "term_fa": "معادله اساسی حسابداری",
        "category": "حسابداری و صورت‌های مالی",
        "definition_en": "The foundational principle of double-entry accounting stating that Assets equal Liabilities plus Shareholder's Equity (Assets = Liabilities + Equity).",
        "definition_fa": "اصل بنیادین حسابداری دوبل که بیان می‌کند دارایی‌های یک شرکت همواره برابر است با مجموع بدهی‌ها و حقوق صاحبان سهام (دارایی = بدهی + سرمایه).",
        "takeaways_en": ["Assets = Liabilities + Equity", "Foundation of the balance sheet"],
        "takeaways_fa": ["دارایی = بدهی + حقوق مالکانه", "اساس تشکیل ترازنامه"]
    },
    "Accounting Rate of Return (ARR)": {
        "term_fa": "نرخ بازده حسابداری (ARR)",
        "category": "بودجه‌بندی سرمایه‌ای",
        "definition_en": "A capital budgeting metric that calculates the expected percentage return of an investment based on net income divided by initial or average cost.",
        "definition_fa": "معیاری در بودجه‌بندی سرمایه‌ای که بازده درصدی مورد انتظار از یک سرمایه‌گذاری را بر اساس سود خالص سالانه نسبت به هزینه اولیه یا متوسط سرمایه‌گذاری می‌سنجد.",
        "takeaways_en": ["Simple to calculate from financial statements", "Ignores the time value of money"],
        "takeaways_fa": ["محاسبه آسان از روی صورت‌های مالی", "ارزش زمانی پول را نادیده می‌گیرد"]
    },
    "Acid-Test Ratio": {
        "term_fa": "نسبت آنی (نسبت اسیدی / Acid-Test)",
        "category": "نسبت‌های نقدینگی و تحلیل بنیادی",
        "definition_en": "A strict liquidity metric that measures a company's ability to cover short-term obligations with its most liquid assets, excluding inventory.",
        "definition_fa": "یک نسبت نقدینگی سخت‌گیرانه که توانایی شرکت را در بازپرداخت بدهی‌های کوتاه‌مدت با نقدترین دارایی‌ها (بدون احتساب موجودی کالا) می‌سنجد.",
        "takeaways_en": ["Formula: (Cash + Marketable Securities + Receivables) / Current Liabilities", "Excludes illiquid inventory"],
        "takeaways_fa": ["فرمول: (وجه نقد + اوراق سریع‌المعامله + مطالبات) تقسیم بر بدهی‌های جاری", "موجودی کالای با نقدشوندگی کند را حذف می‌کند"]
    },
    "Asset": {
        "term_fa": "دارایی",
        "category": "حسابداری و مفاهیم مالی",
        "definition_en": "A resource with economic value that an individual, corporation, or country owns or controls with the expectation that it will provide a future benefit.",
        "definition_fa": "منبعی با ارزش اقتصادی که یک فرد، شرکت یا کشور مالک آن است یا بر آن کنترل دارد و انتظار می‌رود منافع اقتصادی آتی برای آن به همراه داشته باشد.",
        "takeaways_en": ["Recorded on balance sheet", "Classified into current and non-current (fixed) assets"],
        "takeaways_fa": ["در سمت راست ترازنامه ثبت می‌شود", "به دارایی‌های جاری و غیرجاری (ثابت) تقسیم می‌شود"]
    },
    "Asset Management": {
        "term_fa": "مدیریت دارایی‌ها (سبدگردانی)",
        "category": "مدیریت سرمایه‌گذاری",
        "definition_en": "The direction of all or part of a client's portfolio by a financial services firm or professional manager to maximize returns within risk tolerance.",
        "definition_fa": "فرآیند تخصصی هدایت و سرمایه‌گذاری دارایی‌های افراد یا نهادها توسط شرکت‌های مالی و سبدگردان‌ها با هدف دستیابی به بیشترین بازدهی متناسب با سطح ریسک‌پذیری.",
        "takeaways_en": ["Professional fiduciary responsibility", "Diversifies investments across asset classes"],
        "takeaways_fa": ["مسئولیت امانت‌داری حرفه‌ای", "تنوع‌بخشی به سرمایه‌گذاری‌ها میان طبقات مختلف دارایی"]
    },
    "Assets Under Management (AUM)": {
        "term_fa": "دارایی‌های تحت مدیریت (AUM)",
        "category": "صندوق‌های سرمایه‌گذاری",
        "definition_en": "The total market value of the investments that a person or entity manages on behalf of clients.",
        "definition_fa": "مجموع ارزش روز بازاری کلیه دارایی‌ها و سرمایه‌گذاری‌هایی که یک صندوق یا موسسه مالی از طرف مشتریان و سهام‌داران خود مدیریت می‌کند.",
        "takeaways_en": ["Key metric for fund scale and performance", "Drives management fee revenue"],
        "takeaways_fa": ["شاخص کلیدی مقیاس و بزرگی صندوق مالی", "مبنای محاسبه کارمزد مدیریت سبدگردان"]
    },

    # Letter B
    "Balance Sheet": {
        "term_fa": "ترازنامه (صورت وضعیت مالی)",
        "category": "حسابداری و صورت‌های مالی",
        "definition_en": "A primary financial statement that reports a company's total assets, liabilities, and shareholders' equity at a specific point in time.",
        "definition_fa": "از اساسی‌ترین صورت‌های مالی که تصویری لحظه‌ای از کلیه دارایی‌ها، بدهی‌ها و حقوق صاحبان سهام شرکت را در یک تاریخ معین ارائه می‌دهد.",
        "takeaways_en": ["Snapshot in time of financial health", "Reflects the accounting equation"],
        "takeaways_fa": ["تصویر لحظه‌ای از سلامت مالی شرکت", "منعکس‌کننده معادله بنیادین حسابداری"]
    },
    "Balanced Scorecard": {
        "term_fa": "کارت امتیازی متوازن (BSC)",
        "category": "مدیریت استراتژیک",
        "definition_en": "A strategic management performance metric used to identify and improve various internal business functions and external outcomes.",
        "definition_fa": "یک ابزار و رویکرد مدیریت استراتژیک برای ارزیابی عملکرد سازمان از چهار منظر: مالی، مشتریان، فرآیندهای داخلی و رشد و یادگیری.",
        "takeaways_en": ["Looks beyond purely financial measures", "Balances short-term and long-term goals"],
        "takeaways_fa": ["فراتر رفتن از معیارهای صِرف مالی", "برقراری تعادل میان اهداف کوتاه‌مدت و بلندمدت"]
    },
    "Bond": {
        "term_fa": "اوراق قرضه",
        "category": "اوراق بهادار و بدهی",
        "definition_en": "A fixed-income instrument that represents a loan made by an investor to a borrower (typically corporate or governmental).",
        "definition_fa": "ابزار مالی با درآمد ثابت که نشان‌دهنده وامی است که سرمایه‌گذار به یک شرکت یا دولت پرداخت کرده و در ازای آن بهره مشخص (کوپن) و اصل سرمایه را در سررسید دریافت می‌کند.",
        "takeaways_en": ["Fixed interest payments (coupons)", "Lower risk compared to equity stocks"],
        "takeaways_fa": ["پرداخت‌های دوره‌ای بهره مشخص (کوپن)", "ریسک پایین‌تر در مقایسه با سهام عادی"]
    },

    # Letter C
    "Capital": {
        "term_fa": "سرمایه",
        "category": "مالی و اقتصاد",
        "definition_en": "Financial assets, goods, or resources owned by someone or an organization used for investment, operations, or production.",
        "definition_fa": "دارایی‌های مالی، تجهیزات و منابعی که یک فرد یا بنگاه برای تولید، عملیات تجاری یا سرمایه‌گذاری جهت کسب ارزش اقتصادی به کار می‌گیرد.",
        "takeaways_en": ["Essential factor of production", "Includes cash, equipment, and working capital"],
        "takeaways_fa": ["از عوامل حیاتی تولید", "شامل وجه نقد، تجهیزات و سرمایه در گردش"]
    },
    "Capital Asset Pricing Model (CAPM)": {
        "term_fa": "الگوی قیمت‌گذاری دارایی‌های سرمایه‌ای (CAPM)",
        "category": "سرمایه‌گذاری و ارزش‌گذاری",
        "definition_en": "A financial model that calculates the expected rate of return for an asset based on risk-free rate, beta (systematic risk), and market risk premium.",
        "definition_fa": "مدل ریاضی مشهوری که بازده مورد انتظار یک سهم یا دارایی را بر مبنای نرخ بهره بدون ریسک، ضریب بتا (ریسک سیستماتیک) و صرف ریسک بازار تخمین می‌زند.",
        "takeaways_en": ["Formula: E(R) = Rf + Beta*(Rm - Rf)", "Quantifies systematic market risk"],
        "takeaways_fa": ["فرمول: بازده = نرخ بدون ریسک + بتا × صرف ریسک بازار", "محاسبه دقیق ریسک سیستماتیک دارایی"]
    },
    "Capital Expenditure": {
        "term_fa": "مخارج سرمایه‌ای (کپکس / CapEx)",
        "category": "مالی شرکتی",
        "definition_en": "Funds used by a company to acquire, upgrade, and maintain physical assets such as property, plants, buildings, or equipment.",
        "definition_fa": "وجوهی که یک شرکت برای خرید، ارتقا یا حفظ دارایی‌های فیزیکی بلندمدت مانند کارخانه‌ها، تجهیزات و فناوری هزینه می‌کند.",
        "takeaways_en": ["Capitalized on balance sheet rather than expensed", "Crucial for assessing company reinvestment and growth"],
        "takeaways_fa": ["در ترازنامه ثبت می‌شود نه به عنوان هزینه دوره‌ای در سود و زیان", "شاخص کلیدی بررسی رشد و توسعه شرکت"]
    },
    "Capitalism": {
        "term_fa": "سرمایه‌داری (کاپیتالیسم)",
        "category": "مکاتب اقتصادی",
        "definition_en": "An economic system in which private individuals or businesses own capital goods and production is driven by market supply and demand.",
        "definition_fa": "نظام اقتصادی مبتنی بر مالکیت خصوصی ابزارهای تولید، تجارت آزاد و هدایت تولید و قیمت‌ها از طریق نیروهای عرضه و تقاضای بازار آزاد.",
        "takeaways_en": ["Driven by private property and profit incentive", "Free market competition allocates resources"],
        "takeaways_fa": ["مبتنی بر مالکیت خصوصی و انگیزه کسب سود", "تخصیص بهینه منابع از طریق رقابت در بازار آزاد"]
    },
    "Consumer Price Index (CPI)": {
        "term_fa": "شاخص قیمت مصرف‌کننده (تورم CPI)",
        "category": "اقتصاد کلان و شاخص‌ها",
        "definition_en": "A key macroeconomic measure that examines the weighted average of prices of a basket of consumer goods and services, used to measure inflation.",
        "definition_fa": "شاخص اصلی اقتصاد کلان که میانگین وزنی تغییرات قیمت سبدی مشخص از کالاها و خدمات مصرفی خانوارها را سنجیده و به عنوان سنجه اصلی نرخ تورم شناخته می‌شود.",
        "takeaways_en": ["Primary measure of consumer inflation", "Monitored closely by central banks for interest rate decisions"],
        "takeaways_fa": ["سنجه اصلی نرخ تورم عمومی", "مبنای تصمیم‌گیری بانک‌های مرکزی برای تعیین نرخ بهره"]
    },
    "Current Ratio": {
        "term_fa": "نسبت جاری (نسبت نقدینگی)",
        "category": "نسبت‌های نقدینگی و تحلیل بنیادی",
        "definition_en": "A liquidity ratio that measures a company's ability to cover its short-term obligations with its short-term assets (Current Assets / Current Liabilities).",
        "definition_fa": "از رایج‌ترین نسبت‌های نقدینگی که توان شرکت در بازپرداخت بدهی‌های جاری از محل دارایی‌های جاری را ارزیابی می‌کند (دارایی جاری تقسیم بر بدهی جاری).",
        "takeaways_en": ["Healthy benchmark is typically 1.5 to 2.0", "Below 1.0 may indicate working capital strain"],
        "takeaways_fa": ["عدد ۱.۵ تا ۲ نشانه نقدینگی مناسب است", "کمتر از ۱ نشانه هشدار کمبود نقدینگی کوتاه‌مدت است"]
    },

    # Letter D
    "Debt-to-Equity Ratio (D/E)": {
        "term_fa": "نسبت بدهی به حقوق صاحبان سهام (نسبت D/E)",
        "category": "نسبت‌های اهرمی و ساختار سرمایه",
        "definition_en": "A leverage ratio that calculates the weight of total debt and financial liabilities against total shareholders' equity.",
        "definition_fa": "نسبت اهرمی مهمی که میزان استفاده شرکت از بدهی و استقراض را در مقایسه با حقوق مالکانه سهام‌داران نشان می‌دهد (کل بدهی / حقوق صاحبان سهام).",
        "takeaways_en": ["Measures financial leverage and solvency risk", "Higher ratios indicate greater reliance on debt financing"],
        "takeaways_fa": ["سنجش ریسک اهرم مالی و ورشکستگی", "نسبت‌های بالا نشان‌دهنده اتکای شدید به استقراض است"]
    },
    "Days Sales Outstanding (DSO)": {
        "term_fa": "دوره وصول مطالبات (DSO)",
        "category": "نسبت‌های مالی و نقدینگی",
        "definition_en": "A measure of the average number of days that it takes a company to collect payment after a sale has been made on credit.",
        "definition_fa": "معیاری که نشان می‌دهد یک شرکت به‌طور میانگین ظرف چند روز وجوه حاصل از فروش‌های نسیه و اعتباری خود را از مشتریان وصول می‌کند.",
        "takeaways_en": ["Lower DSO indicates better cash collection efficiency", "High DSO may signal credit risk or customer dissatisfaction"],
        "takeaways_fa": ["عدد کمتر نشان‌دهنده کارایی بالاتر در وصول نقدینگی است", "عدد بالا می‌تواند نشانگر ریسک عدم وصول باشد"]
    },
    "Dividend Payout Ratio": {
        "term_fa": "نسبت پرداخت سود نقدی (DPS/EPS)",
        "category": "سهام و سودآوری",
        "definition_en": "The percentage of net earnings paid out as dividends to shareholders rather than retained for business reinvestment.",
        "definition_fa": "درصدی از کل سود خالص شرکت که به صورت سود نقدی بین سهام‌داران تقسیم می‌شود به جای اینکه برای توسعه ذخیره گردد.",
        "takeaways_en": ["Formula: Total Dividends / Net Income", "High ratios typical in mature stable cash flow companies"],
        "takeaways_fa": ["فرمول: سود نقدی تقسیمی تقسیم بر سود خالص", "نسبت‌های بالا در شرکت‌های پایدار و بالغ رایج‌تر است"]
    },

    # Letter E
    "Earnings Before Interest and Taxes (EBIT)": {
        "term_fa": "سود قبل از بهره و مالیات (EBIT)",
        "category": "حسابداری و سودآوری",
        "definition_en": "An indicator of a company's profitability, calculated as revenue minus expenses excluding tax and interest expenses, also called operating profit.",
        "definition_fa": "سنجه‌ای از سودآوری که عملکرد عملیاتی خالص شرکت را قبل از کسر هزینه‌های بهره وام و مالیات نشان می‌دهد و سود عملیاتی نیز نامیده می‌شود.",
        "takeaways_en": ["Reflects pure operating earnings", "Allows cross-company comparisons regardless of debt structure"],
        "takeaways_fa": ["بیانگر سود خالص عملیاتی", "امکان مقایسه شرکت‌ها بدون تاثیر ساختار بدهی و مالیات"]
    },
    "Earnings Before Interest, Taxes, Depreciation and Amortization (EBITDA)": {
        "term_fa": "سود قبل از بهره، مالیات و استهلاک (EBITDA)",
        "category": "ارزش‌گذاری و مالی شرکتی",
        "definition_en": "A widely used metric that evaluates a company's operating performance by adding depreciation and amortization expenses back to EBIT.",
        "definition_fa": "شاخص پرکاربرد تحلیلگران برای سنجش جریان نقد عملیاتی که با بازگرداندن هزینه‌های غیرنقدی استهلاک به EBIT محاسبه می‌شود.",
        "takeaways_en": ["Proxy for operating cash flow", "Standard metric used in M&A valuation multiples"],
        "takeaways_fa": ["تقریبی از جریان نقد عملیاتی شرکت", "معیار استاندارد مضارب ارزش‌گذاری و خرید شرکت‌ها"]
    },
    "Enterprise Value (EV)": {
        "term_fa": "ارزش کل بنگاه (Enterprise Value / EV)",
        "category": "ارزش‌گذاری و تحلیل بنیادی",
        "definition_en": "A comprehensive measure of a company's total value, calculated as market capitalization plus total debt minus cash and cash equivalents.",
        "definition_fa": "معیار جامع ارزش اقتصادی کل شرکت که نشان‌دهنده هزینه واقعی خرید کل شرکت است (ارزش بازار سهام + کل بدهی‌ها منهای وجه نقد).",
        "takeaways_en": ["Formula: Market Cap + Debt - Cash", "More complete picture than simple market cap"],
        "takeaways_fa": ["فرمول: ارزش بازار سهام + بدهی‌ها - نقدینگی", "تصویری کامل‌تر و واقع‌بینانه‌تر از مارکت کپ ساده"]
    },
    "Exchange-Traded Fund (ETF)": {
        "term_fa": "صندوق قابل معامله در بورس (ETF)",
        "category": "صندوق‌های سرمایه‌گذاری و بورس",
        "definition_en": "A pooled investment security that operates like a mutual fund but trades on a public stock exchange just like a regular stock.",
        "definition_fa": "صندوق سرمایه‌گذاری مشترکی که سبدی از دارایی‌ها (مانند سهام، طلا یا اوراق) را در خود جای داده اما واحدهای آن درست شبیه سهام عادی در طول ساعات بازار معامله می‌شود.",
        "takeaways_en": ["Trades intraday with live market pricing", "Provides low-cost instant diversification"],
        "takeaways_fa": ["معامله لحظه‌ای در طول روز معاملاتی", "تنوع‌بخشی فوری به سبد دارایی با کمترین هزینه"]
    },

    # Letter F
    "FAANG Stocks": {
        "term_fa": "سهام فنگ (FAANG)",
        "category": "بازار سهام و فناوری",
        "definition_en": "An acronym referring to the stocks of five prominent American tech companies: Meta (formerly Facebook), Amazon, Apple, Netflix, and Alphabet (Google).",
        "definition_fa": "اصطلاحی پرکاربرد که به پنج غول فناوری بازار بورس آمریکا یعنی متا (فیس‌بوک سابق)، آمازون، اپل، نتفلیکس و گوگل (آلفابت) اشاره دارد.",
        "takeaways_en": ["Represented massive weight in S&P 500", "Often seen as market leaders in tech"],
        "takeaways_fa": ["سهم بسیار بزرگ در شاخص S&P 500", "لیدرهای بلامنازع بازار فناوری"]
    },
    "Federal Funds Rate": {
        "term_fa": "نرخ بهره فدرال رزرو (Federal Funds Rate)",
        "category": "بانکداری مرکزی و سیاست پولی",
        "definition_en": "The target interest rate set by the Federal Reserve at which commercial banks lend overnight funds to each other.",
        "definition_fa": "نرخ بهره کلیدی هدف‌گذاری شده توسط بانک مرکزی آمریکا (فدرال رزرو) که بانک‌های تجاری بر اساس آن وجوه شبانه را به یکدیگر قرض می‌دهند و مبنای نرخ‌های وام در دنیاست.",
        "takeaways_en": ["Primary monetary policy instrument", "Dictates cost of borrowing across global economies"],
        "takeaways_fa": ["ابزار اصلی سیاست‌های پولی فدرال رزرو", "تعیین‌کننده هزینه استقراض و وام در اقتصاد جهان"]
    },

    # Letter G
    "Game Theory": {
        "term_fa": "نظریه بازی‌ها",
        "category": "اقتصاد و تصمیم‌گیری",
        "definition_en": "A theoretical framework for conceiving social situations among competing players to produce optimal decision-making.",
        "definition_fa": "چارچوبی ریاضی و اقتصادی برای مدل‌سازی تعاملات استراتژیک میان بازیگران منطقی و پیش‌بینی نتایج و استراتژی‌های بهینه در شرایط رقابتی.",
        "takeaways_en": ["Analyzes strategic interdependence", "Nash equilibrium is a core concept"],
        "takeaways_fa": ["تحلیل وابستگی متقابل استراتژیک", "تعادل نش یکی از مفاهیم کلیدی آن است"]
    },

    # Letter H
    "Head And Shoulders Pattern": {
        "term_fa": "الگوی سر و شانه (تحلیل تکنیکال)",
        "category": "تحلیل تکنیکال و نمودارها",
        "definition_en": "A technical analysis chart formation that resembles a baseline with three peaks, predicting a bullish-to-bearish trend reversal.",
        "definition_fa": "یک الگوی معتبر بازگشتی در نمودارهای تحلیل تکنیکال شامل سه قله (شانه چپ، سر، و شانه راست) که سیگنال پایان روند صعودی و آغاز روند نزولی است.",
        "takeaways_en": ["Reliable reversal chart pattern", "Neckline break confirms sell signal"],
        "takeaways_fa": ["الگوی معتبر تغییر جهت روند", "شکست خط گردن (Neckline) تایید سیگنال فروش است"]
    },

    # Letter I
    "Income Statement": {
        "term_fa": "صورت سود و زیان",
        "category": "حسابداری و صورت‌های مالی",
        "definition_en": "A financial statement showing a company’s revenues, costs, and expenses incurred during a specific accounting period.",
        "definition_fa": "صورت مالی اساسی که درآمدها، هزینه‌ها و در نهایت سود یا زیان خالص یک شرکت را در طول یک دوره مالی مشخص نمایش می‌دهد.",
        "takeaways_en": ["Shows operational profitability over a period", "Leads to bottom-line net profit"],
        "takeaways_fa": ["نمایش سودآوری عملیاتی طی دوره", "منتهی به سود خالص پایانی شرکت"]
    },

    # Letter L
    "Law of Demand": {
        "term_fa": "قانون تقاضا",
        "category": "اقتصاد خرد",
        "definition_en": "A fundamental economic principle stating that, ceteris paribus, as the price of a good increases, consumer demand for it will decrease.",
        "definition_fa": "اصل بنیادین در علم اقتصاد خرد که بیان می‌کند با فرض ثبات سایر شرایط، هرگاه قیمت یک کالا افزایش یابد، مقدار تقاضا برای آن کاهش خواهد یافت.",
        "takeaways_en": ["Inverse relationship between price and quantity demanded", "Creates downward-sloping demand curve"],
        "takeaways_fa": ["رابطه معکوس میان قیمت و مقدار تقاضا", "تشکیل منحنی تقاضای نزولی"]
    },
    "Law of Supply": {
        "term_fa": "قانون عرضه",
        "category": "اقتصاد خرد",
        "definition_en": "A microeconomic rule stating that, ceteris paribus, as the price of a good rises, the quantity supplied by producers will increase.",
        "definition_fa": "اصل اقتصادی که بیان می‌کند با فرض ثبات سایر متغیرها، هرچه قیمت کالا در بازار بالاتر برود، تولیدکنندگان تمایل به عرضه حجم بیشتری از آن خواهند داشت.",
        "takeaways_en": ["Direct relationship between price and quantity supplied", "Creates upward-sloping supply curve"],
        "takeaways_fa": ["رابطه مستقیم میان قیمت و مقدار عرضه", "تشکیل منحنی عرضه صعودی"]
    },

    # Letter M
    "Macroeconomics": {
        "term_fa": "اقتصاد کلان",
        "category": "اقتصاد",
        "definition_en": "The branch of economics that studies the behavior, performance, structure, and decision-making of an entire economy, including GDP, inflation, and unemployment.",
        "definition_fa": "شاخه‌ای از علم اقتصاد که به بررسی متغیرها و عملکرد کل اقتصاد در سطح ملی و جهانی مانند تولید ناخالص داخلی (GDP)، تورم، بیکاری و سیاست‌های پولی می‌پردازد.",
        "takeaways_en": ["Studies aggregate economic indicators", "Guides monetary and fiscal policy"],
        "takeaways_fa": ["بررسی شاخص‌های تجمیعی اقتصاد", "راهنمای سیاست‌گذاری‌های مالی و پولی بانک مرکزی و دولت"]
    },

    # Letter N
    "Nasdaq": {
        "term_fa": "بورس نزدک (NASDAQ)",
        "category": "بازارهای مالی و بورس",
        "definition_en": "An American electronic stock exchange, the second-largest exchange in the world by market capitalization, known for technology heavyweights.",
        "definition_fa": "دومین بازار بورس بزرگ دنیا از حیث ارزش بازار که معاملات آن کاملاً الکترونیکی است و مهد اصلی نمادهای برجسته فناوری جهان به شمار می‌رود.",
        "takeaways_en": ["World's first electronic stock exchange", "Home to major tech giants like Apple, Microsoft, NVIDIA"],
        "takeaways_fa": ["نخستین بورس تمام الکترونیکی دنیا", "میزبان شرکت‌های بزرگ فناوری مانند اپل و انویدیا"]
    },
    "Nash Equilibrium": {
        "term_fa": "تعادل نش (نظریه بازی‌ها)",
        "category": "اقتصاد و تصمیم‌گیری",
        "definition_en": "A stable decision state in game theory where no participant can gain by unilaterally changing their strategy if the others keep theirs unchanged.",
        "definition_fa": "وضعیتی پایدار در نظریه بازی‌ها که در آن هیچ بازیکنی با تغییر یک‌جانبه استراتژی خود سودی به دست نمی‌آورد با این فرض که سایر بازیکنان استراتژی خود را ثابت نگه دارند.",
        "takeaways_en": ["Formulated by John Nash (Nobel laureate)", "Applicable to economics, geopolitics, and pricing"],
        "takeaways_fa": ["فرموله‌شده توسط جان نش (برنده نوبل)", "کاربرد گسترده در اقتصاد، ژئوپلیتیک و قیمت‌گذاری رقابتی"]
    },

    # Letter S
    "S&P 500 Index (Standard & Poor's 500 Index)": {
        "term_fa": "شاخص اس‌اند‌پی ۵۰۰ (S&P 500)",
        "category": "شاخص‌ها و بازارهای مالی",
        "definition_en": "A market-capitalization-weighted index of 500 of the largest publicly traded companies in the United States, viewed as the premier gauge of US equities.",
        "definition_fa": "شاخصی موزون بر مبنای ارزش بازار ۵۰۰ شرکت برتر سهامی عام در ایالات متحده که به عنوان معتبرترین شاخص سنجش کلیت بازار سهام و اقتصاد آمریکا شناخته می‌شود.",
        "takeaways_en": ["Covers ~80% of available market capitalization", "Primary benchmark for institutional funds"],
        "takeaways_fa": ["پوشش‌دهنده حدود ۸۰٪ ارزش کل بازار سرمایه آمریکا", "معیار اصلی ارزیابی عملکرد صندوق‌های سرمایه‌گذاری"]
    },
    "Securities and Exchange Commission (SEC)": {
        "term_fa": "کمیسیون بورس و اوراق بهادار آمریکا (SEC)",
        "category": "نهادهای نظارتی و رگولاتوری",
        "definition_en": "An independent federal government regulatory agency responsible for protecting investors, maintaining fair and orderly functioning of securities markets.",
        "definition_fa": "آژانس مستقل فدرال ناظر بر بازارهای مالی آمریکا که ماموریت حفاظت از سرمایه‌گذاران، تضمین شفافیت اطلاعاتی و جلوگیری از تقلب در بازار را برعهده دارد.",
        "takeaways_en": ["Enforces federal securities laws", "Mandates corporate financial disclosures"],
        "takeaways_fa": ["اجرای قوانین حاکم بر اوراق بهادار", "الزام شرکت‌ها به افشای صورت‌های مالی شفاف"]
    },

    # Letter T
    "Technical Analysis": {
        "term_fa": "تحلیل تکنیکال (فنی)",
        "category": "معاملات و تحلیل تکنیکال",
        "definition_en": "A trading discipline employed to evaluate investments and identify trading opportunities by analyzing statistical trends gathered from trading activity, such as price movement and volume.",
        "definition_fa": "روشی برای تحلیل و پیش‌بینی حرکت آتی قیمت دارایی‌ها بر پایه مطالعه رفتارهای گذشته بازار، نمودار قیمت‌ها، الگوها و حجم معاملات.",
        "takeaways_en": ["Focuses on price and volume patterns", "Assumes past market psychology repeats"],
        "takeaways_fa": ["تمرکز بر الگوهای قیمتی و حجم معاملات", "بر این فرض استوار است که رفتار روانی بازار تکرار می‌شود"]
    },

    # Letter V
    "Valuation": {
        "term_fa": "ارزش‌گذاری (تعیین ارزش دارایی)",
        "category": "ارزش‌گذاری و مالی شرکتی",
        "definition_en": "The analytical process of determining the current (or projected) worth of an asset, company, or liability using quantitative financial modeling.",
        "definition_fa": "فرآیند تحلیلی تعیین ارزش منصفانه و واقعی یک شرکت، پروژه یا دارایی مالی با به‌کارگیری مدل‌های تنزیل جریان نقدی (DCF)، مضارب قیمت یا دارایی‌محور.",
        "takeaways_en": ["Critical for investing and acquisitions", "Methods include DCF and Comparable Multiples"],
        "takeaways_fa": ["حیاتی در تصمیمات سرمایه‌گذاری و ادغام شرکت‌ها", "شامل روش‌های DCF و مقایسه مضارب بازار"]
    },
    "Value Added": {
        "term_fa": "ارزش افزوده (Value Added)",
        "category": "اقتصاد و مدیریت عملیات",
        "definition_en": "The enhancement a company gives to a product or service before offering it to customers, creating positive economic margin.",
        "definition_fa": "ارزش اضافی که یک بنگاه تولیدی یا خدماتی در طی فرآیند تولید به مواد اولیه یا خدمات می‌افزاید و اختلاف قیمت محصول نهایی با هزینه نهاده‌ها را شکل می‌دهد.",
        "takeaways_en": ["Basis for Value-Added Tax (VAT)", "Reflects competitive differentiation and pricing power"],
        "takeaways_fa": ["پایه محاسباتی مالیات بر ارزش افزوده (VAT)", "بیانگر تمایز رقابتی و قدرت قیمت‌گذاری محصول"]
    },
    "Value Chain": {
        "term_fa": "زنجیره ارزش (مایکل پورتر)",
        "category": "مدیریت استراتژیک",
        "definition_en": "A business model describing the full range of activities needed to create a product or service from design and supply to delivery and customer service.",
        "definition_fa": "مدل استراتژیک توسعه‌یافته توسط مایکل پورتر که کلیه فعالیت‌های خلق ارزش (لجستیک، عملیات، بازاریابی، خدمات پس از فروش و زیرساخت) را توصیف می‌کند.",
        "takeaways_en": ["Identifies cost reduction opportunities", "Focuses on competitive advantage generation"],
        "takeaways_fa": ["شناسایی فرصت‌های کاهش بهای تمام‌شده", "تمرکز بر خلق مزیت رقابتی پایدار"]
    }
}
