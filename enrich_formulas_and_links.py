import json
import re

# Load dictionary
with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} terms.")

# 1. Master Formula Database for Financial Ratios & Concepts
# Maps slug / keywords to standard LaTeX formulas and Persian translations
FORMULA_DB = {
    'sharperatio': {
        'title_en_match': ['formula and calculation', 'formula', 'calculation'],
        'formula_en': '$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Return of portfolio} \\\\ &R_f = \\text{Risk-free rate} \\\\ &\\sigma_p = \\text{Standard deviation of the portfolio\'s excess return} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت شارپ} = \\frac{R_p - R_f}{\\sigma_p}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده سبد سرمایه‌گذاری (پرتفوی)} \\\\ &R_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\sigma_p = \\text{انحراف معیار بازده مازاد پرتفوی} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'sortinoratio': {
        'title_en_match': ['how to calculate the sortino ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Sortino Ratio} = \\frac{R_p - r_f}{\\sigma_d}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Actual or expected portfolio return} \\\\ &r_f = \\text{Risk-free rate} \\\\ &\\sigma_d = \\text{Standard deviation of the downside} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت سورتینو} = \\frac{R_p - r_f}{\\sigma_d}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده واقعی یا مورد انتظار پرتفوی} \\\\ &r_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\sigma_d = \\text{انحراف معیار بازده‌های نزولی (ریسک منفی)} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'treynorratio': {
        'title_en_match': ['the formula for the treynor ratio is', 'formula', 'calculation'],
        'formula_en': '$$\\text{Treynor Ratio} = \\frac{r_p - r_f}{\\beta_p}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &r_p = \\text{Portfolio return} \\\\ &r_f = \\text{Risk-free rate} \\\\ &\\beta_p = \\text{Beta of the portfolio} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت ترینور} = \\frac{r_p - r_f}{\\beta_p}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &r_p = \\text{بازده پرتفوی} \\\\ &r_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\beta_p = \\text{بتای پرتفوی (ریسک سیستماتیک)} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'informationratio': {
        'title_en_match': ['how to calculate', 'formula', 'calculation'],
        'formula_en': '$$\\text{Information Ratio (IR)} = \\frac{R_p - R_b}{\\text{Tracking Error}}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Portfolio return} \\\\ &R_b = \\text{Benchmark return} \\\\ &\\text{Tracking Error} = \\text{Standard deviation of excess return} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت اطلاعات (IR)} = \\frac{R_p - R_b}{\\text{خطای ردیابی}}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده پرتفوی} \\\\ &R_b = \\text{بازده شاخص مبنا (بنچ‌مارک)} \\\\ &\\text{خطای ردیابی} = \\text{انحراف معیار بازده مازاد نسبت به بنچ‌مارک} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'accounting-equation': {
        'title_en_match': ['accounting equation formula and calculation', 'formula'],
        'formula_en': '$$\\text{Assets} = \\text{Liabilities} + \\text{Shareholders\' Equity}$$',
        'formula_fa': '$$\\text{دارایی‌ها} = \\text{بدهی‌ها} + \\text{حقوق صاحبان سهام}$$',
        'insert_after_idx': 0
    },
    'arr': {
        'title_en_match': ['calculating arr', 'formula', 'calculation'],
        'formula_en': '$$\\text{ARR} = \\frac{\\text{Average Annual Profit}}{\\text{Initial Investment}}$$',
        'formula_fa': '$$\\text{نرخ بازده حسابداری (ARR)} = \\frac{\\text{میانگین سود خالص سالانه}}{\\text{سرمایه‌گذاری اولیه}}$$',
        'insert_after_idx': 0
    },
    'breakevenanalysis': {
        'title_en_match': ['break-even point (bep) formula', 'formula'],
        'formula_en': '$$\\text{Break-Even Point (BEP)} = \\frac{\\text{Total Fixed Costs}}{\\text{Price per Unit} - \\text{Variable Cost per Unit}}$$',
        'formula_fa': '$$\\text{نقطه سربه‌سر (BEP)} = \\frac{\\text{کل هزینه‌های ثابت}}{\\text{قیمت فروش هر واحد} - \\text{هزینه متغیر هر واحد}}$$',
        'insert_after_idx': 0
    },
    'debtequityratio': {
        'title_en_match': ['calculating the d/e ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Debt / Equity Ratio} = \\frac{\\text{Total Liabilities}}{\\text{Total Shareholders\' Equity}}$$',
        'formula_fa': '$$\\text{نسبت بدهی به حقوق صاحبان سهام (D/E)} = \\frac{\\text{مجموع بدهی‌ها}}{\\text{مجموع حقوق صاحبان سهام}}$$',
        'insert_after_idx': 0
    },
    'dscr': {
        'title_en_match': ['calculating the dscr', 'formula', 'calculation'],
        'formula_en': '$$\\text{DSCR} = \\frac{\\text{Net Operating Income (NOI)}}{\\text{Total Debt Service}}$$',
        'formula_fa': '$$\\text{نسبت پوشش اصل و بهره بدهی (DSCR)} = \\frac{\\text{درآمد خالص عملیاتی (NOI)}}{\\text{کل خدمات بدهی (اقساط اصل و سود)}}$$',
        'insert_after_idx': 0
    },
    'ebit': {
        'title_en_match': ['formula and calculation', 'formula'],
        'formula_en': '$$\\text{EBIT} = \\text{Revenue} - \\text{COGS} - \\text{Operating Expenses}$$',
        'formula_fa': '$$\\text{سود قبل از بهره و مالیات (EBIT)} = \\text{درآمد فروش} - \\text{بهای تمام‌شده کالای فروش‌رفته} - \\text{هزینه‌های عملیاتی}$$',
        'insert_after_idx': 0
    },
    'ebita': {
        'title_en_match': ['how to calculate ebita', 'formula'],
        'formula_en': '$$\\text{EBITA} = \\text{EBIT} + \\text{Amortization}$$',
        'formula_fa': '$$\\text{EBITA} = \\text{سود قبل از بهره و مالیات} + \\text{استهلاک دارایی‌های نامشهود}$$',
        'insert_after_idx': 0
    },
    'jensensmeasure': {
        'title_en_match': ['how to calculate jensen\'s measure', 'formula'],
        'formula_en': '$$\\alpha = R_p - [R_f + \\beta_p (R_m - R_f)]$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Portfolio return} \\\\ &R_f = \\text{Risk-free rate} \\\\ &\\beta_p = \\text{Portfolio beta} \\\\ &R_m = \\text{Market return} \\end{aligned}$$',
        'formula_fa': '$$\\alpha = R_p - [R_f + \\beta_p (R_m - R_f)]$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده سبد سرمایه‌گذاری} \\\\ &R_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\beta_p = \\text{ضریب بتای سبد سرمایه‌گذاری} \\\\ &R_m = \\text{بازده کل بازار} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'loantovalue': {
        'title_en_match': ['calculating the ltv ratio', 'formula'],
        'formula_en': '$$\\text{LTV} = \\frac{\\text{Mortgage Amount}}{\\text{Appraised Property Value}} \\times 100\\%$$',
        'formula_fa': '$$\\text{نسبت وام به ارزش وثیقه (LTV)} = \\frac{\\text{مبلغ وام دریافتی}}{\\text{ارزش کارشناسی ملک/وثیقه}} \\times ۱۰۰\\%$$',
        'insert_after_idx': 0
    },
    'macd': {
        'title_en_match': ['macd formula', 'formula'],
        'formula_en': '$$\\begin{aligned} &\\text{MACD Line} = \\text{12-Period EMA} - \\text{26-Period EMA} \\\\ &\\text{Signal Line} = \\text{9-Period EMA of MACD Line} \\\\ &\\text{MACD Histogram} = \\text{MACD Line} - \\text{Signal Line} \\end{aligned}$$',
        'formula_fa': '$$\\begin{aligned} &\\text{خط MACD} = \\text{میانگین متحرک نمایی ۱۲ دوره‌ای} - \\text{میانگین متحرک نمایی ۲۶ دوره‌ای} \\\\ &\\text{خط سیگنال} = \\text{میانگین متحرک نمایی ۹ دوره‌ای خط MACD} \\\\ &\\text{هیستوگرام MACD} = \\text{خط MACD} - \\text{خط سیگنال} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'nav': {
        'title_en_match': ['nav formula', 'formula'],
        'formula_en': '$$\\text{NAV} = \\frac{\\text{Total Assets} - \\text{Total Liabilities}}{\\text{Total Shares Outstanding}}$$',
        'formula_fa': '$$\\text{ارزش خالص هر سهم / واحد (NAV)} = \\frac{\\text{مجموع دارایی‌ها} - \\text{مجموع بدهی‌ها}}{\\text{تعداد کل سهام / واحدهای منتشره}}$$',
        'insert_after_idx': 0
    },
    'networth': {
        'title_en_match': ['how to calculate net worth', 'formula'],
        'formula_en': '$$\\text{Net Worth} = \\text{Total Assets} - \\text{Total Liabilities}$$',
        'formula_fa': '$$\\text{ارزش خالص دارایی} = \\text{مجموع دارایی‌ها} - \\text{مجموع بدهی‌ها}$$',
        'insert_after_idx': 0
    },
    'normaldistribution': {
        'title_en_match': ['the formula for normal distribution', 'formula'],
        'formula_en': '$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x - \\mu}{\\sigma}\\right)^2}$$',
        'formula_fa': '$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x - \\mu}{\\sigma}\\right)^2}$$',
        'insert_after_idx': 0
    },
    'grossprofit': {
        'title_en_match': ['calculating gross profit', 'formula'],
        'formula_en': '$$\\text{Gross Profit} = \\text{Revenue} - \\text{Cost of Goods Sold (COGS)}$$',
        'formula_fa': '$$\\text{سود ناخالص} = \\text{درآمد فروش} - \\text{بهای تمام‌شده کالای فروش‌رفته (COGS)}$$',
        'insert_after_idx': 0
    },
    'compoundinterest': {
        'title_en_match': ['approach two: fixed formula', 'fixed formula', 'formula'],
        'formula_en': '$$A = P \\left(1 + \\frac{r}{n}\\right)^{nt}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &A = \\text{Final amount} \\\\ &P = \\text{Initial principal} \\\\ &r = \\text{Annual interest rate} \\\\ &n = \\text{Compounding frequency per year} \\\\ &t = \\text{Time in years} \\end{aligned}$$',
        'formula_fa': '$$A = P \\left(1 + \\frac{r}{n}\\right)^{nt}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &A = \\text{مبلغ نهایی سرمایه} \\\\ &P = \\text{اصل سرمایه اولیه} \\\\ &r = \\text{نرخ سود سالانه} \\\\ &n = \\text{تعداد دوره‌های ترکیب در سال} \\\\ &t = \\text{مدت زمان به سال} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'cagr': {
        'title_en_match': ['cagr formula', 'formula', 'calculation'],
        'formula_en': '$$\\text{CAGR} = \\left(\\frac{\\text{Ending Value}}{\\text{Beginning Value}}\\right)^{\\frac{1}{n}} - 1$$',
        'formula_fa': '$$\\text{نرخ رشد مرکب سالانه (CAGR)} = \\left(\\frac{\\text{ارزش پایانی}}{\\text{ارزش اولیه}}\\right)^{\\frac{1}{n}} - 1$$',
        'insert_after_idx': 0
    },
    'dividendpayoutratio': {
        'title_en_match': ['calculating the dividend payout ratio', 'formula'],
        'formula_en': '$$\\text{Dividend Payout Ratio} = \\frac{\\text{Total Dividends Paid}}{\\text{Net Income}}$$',
        'formula_fa': '$$\\text{نسبت پرداخت سود نقدی} = \\frac{\\text{مجموع سود نقدی سهام پرداختی}}{\\text{سود خالص شرکت}}$$',
        'insert_after_idx': 0
    },
    'eps': {
        'title_en_match': ['formula for eps', 'formula', 'calculation'],
        'formula_en': '$$\\text{EPS} = \\frac{\\text{Net Income} - \\text{Preferred Dividends}}{\\text{Weighted Average Common Shares Outstanding}}$$',
        'formula_fa': '$$\\text{سود هر سهم (EPS)} = \\frac{\\text{سود خالص} - \\text{سود سهام ممتاز}}{\\text{میانگین موزون تعداد سهام عادی در گردش}}$$',
        'insert_after_idx': 0
    },
    'equity': {
        'title_en_match': ['formula and how to calculate', 'formula'],
        'formula_en': '$$\\text{Shareholders\' Equity} = \\text{Total Assets} - \\text{Total Liabilities}$$',
        'formula_fa': '$$\\text{حقوق صاحبان سهام} = \\text{مجموع دارایی‌ها} - \\text{مجموع بدهی‌ها}$$',
        'insert_after_idx': 0
    },
    'absorptioncosting': {
        'title_en_match': ['formula for absorption costing', 'formula'],
        'formula_en': '$$\\text{Absorption Cost per Unit} = \\frac{\\text{Direct Materials} + \\text{Direct Labor} + \\text{Variable Overhead} + \\text{Fixed Overhead}}{\\text{Total Units Produced}}$$',
        'formula_fa': '$$\\text{بهای تمام‌شده هر واحد (هزینه‌یابی جذبی)} = \\frac{\\text{مواد مستقیم} + \\text{دستمزد مستقیم} + \\text{سربار متغیر} + \\text{سربار ثابت}}{\\text{تعداد کل واحدهای تولیدشده}}$$',
        'insert_after_idx': 0
    },
    'affo': {
        'title_en_match': ['how to calculate adjusted funds from operations (affo)', 'formula'],
        'formula_en': '$$\\begin{aligned} &\\text{FFO} = \\text{Net Income} + \\text{Amortization} + \\text{Depreciation} - \\text{Capital Gains from Property Sales} \\\\ &\\text{AFFO} = \\text{FFO} + \\text{Rent Increases} - \\text{CapEx} - \\text{Routine Maintenance} \\end{aligned}$$',
        'formula_fa': '$$\\begin{aligned} &\\text{FFO} = \\text{سود خالص} + \\text{استهلاک} - \\text{سود حاصل از فروش املاک} \\\\ &\\text{AFFO} = \\text{FFO} + \\text{تعدیلات اجاره} - \\text{مخارج سرمایه‌ای نگهداری} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'adjusted-ebitda': {
        'title_en_match': ['how to understand the adjusted ebitda formula', 'formula'],
        'formula_en': '$$\\begin{aligned} &\\text{EBITDA} = \\text{Net Income} + \\text{Interest} + \\text{Taxes} + \\text{D\\&A} \\\\ &\\text{Adjusted EBITDA} = \\text{EBITDA} \\pm \\text{Non-Recurring Adjustments} \\end{aligned}$$',
        'formula_fa': '$$\\begin{aligned} &\\text{EBITDA} = \\text{سود خالص} + \\text{بهره} + \\text{مالیات} + \\text{استهلاک} \\\\ &\\text{EBITDA تعدیل‌شده} = \\text{EBITDA} \\pm \\text{اقلام غیرتکراری و استثنایی} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'zero-couponbond': {
        'title_en_match': ['calculating zero-coupon bond prices', 'formula'],
        'formula_en': '$$\\text{Price} = \\frac{M}{(1 + r)^n}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &M = \\text{Maturity value / Par value} \\\\ &r = \\text{Required interest rate} \\\\ &n = \\text{Number of years until maturity} \\end{aligned}$$',
        'formula_fa': '$$\\text{قیمت اوراق بدون کوپن} = \\frac{M}{(1 + r)^n}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &M = \\text{ارزش اسمی در سررسید} \\\\ &r = \\text{نرخ بازده مورد انتظار} \\\\ &n = \\text{تعداد سال‌های مانده تا سررسید} \\end{aligned}$$',
        'insert_after_idx': 0
    },
    'liquidity-coverage-ratio': {
        'title_en_match': ['calculating the liquidity coverage ratio', 'formula'],
        'formula_en': '$$\\text{LCR} = \\frac{\\text{High-Quality Liquid Assets (HQLA)}}{\\text{Total Net Cash Outflow over 30 Days}} \\ge 100\\%$$',
        'formula_fa': '$$\\text{نسبت پوشش نقدینگی (LCR)} = \\frac{\\text{دارایی‌های نقدی باکیفیت بالا (HQLA)}}{\\text{کل خروجی خالص وجه نقد طی ۳۰ روز}} \\ge ۱۰۰\\%$$',
        'insert_after_idx': 0
    },
    'oid': {
        'title_en_match': ['formula and calculation of oid', 'formula'],
        'formula_en': '$$\\text{OID} = \\text{Stated Redemption Price at Maturity} - \\text{Issue Price}$$',
        'formula_fa': '$$\\text{کسر اوراق اولیه (OID)} = \\text{قیمت بازخرید در سررسید (ارزش اسمی)} - \\text{قیمت انتشار اولیه}$$',
        'insert_after_idx': 0
    },
    'bayes-theorem': {
        'title_en_match': ['deriving the bayes\' theorem formula', 'formula'],
        'formula_en': '$$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$',
        'formula_fa': '$$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$',
        'insert_after_idx': 0
    },
    'irr': {
        'title_en_match': ['the formula for irr', 'how to calculate the irr', 'formula'],
        'formula_en': '$$0 = \\text{NPV} = \\sum_{t=1}^{T} \\frac{C_t}{(1 + \\text{IRR})^t} - C_0$$',
        'formula_fa': '$$0 = \\text{NPV} = \\sum_{t=1}^{T} \\frac{C_t}{(1 + \\text{IRR})^t} - C_0$$',
        'insert_after_idx': 0
    },
    'consumerpriceindex': {
        'title_en_match': ['cpi-u formula', 'formula'],
        'formula_en': '$$\\text{CPI} = \\frac{\\text{Cost of Market Basket in Given Year}}{\\text{Cost of Market Basket in Base Year}} \\times 100$$',
        'formula_fa': '$$\\text{شاخص بهای مصرف‌کننده (CPI)} = \\frac{\\text{قیمت سبد کالا در سال جاری}}{\\text{قیمت سبد کالا در سال پایه}} \\times ۱۰۰$$',
        'insert_after_idx': 0
    },
    'capitalexpenditure': {
        'title_en_match': ['calculating capital expenditures: formula and method', 'formula'],
        'formula_en': '$$\\text{CapEx} = \\text{PP\\&E}_{\\text{current}} - \\text{PP\\&E}_{\\text{prior}} + \\text{Depreciation}$$',
        'formula_fa': '$$\\text{مخارج سرمایه‌ای (CapEx)} = \\text{اموال، ماشین‌آلات و تجهیزات دوره جاری} - \\text{دوره قبل} + \\text{استهلاک}$$',
        'insert_after_idx': 0
    },
    'gdp': {
        'title_en_match': ['gdp formula', 'formula'],
        'formula_en': '$$\\text{GDP} = C + I + G + (X - M)$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &C = \\text{Consumption} \\\\ &I = \\text{Investment} \\\\ &G = \\text{Government spending} \\\\ &X = \\text{Exports} \\\\ &M = \\text{Imports} \\end{aligned}$$',
        'formula_fa': '$$\\text{تولید ناخالص داخلی (GDP)} = C + I + G + (X - M)$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &C = \\text{مصرف بخش خصوصی} \\\\ &I = \\text{سرمایه‌گذاری ناخالص} \\\\ &G = \\text{مخارج دولت} \\\\ &X = \\text{صادرات} \\\\ &M = \\text{واردات} \\end{aligned}$$',
        'insert_after_idx': 0
    }
}

updated_formula_count = 0

for item in data:
    slug = item.get('slug', '').lower()
    if slug in FORMULA_DB:
        finfo = FORMULA_DB[slug]
        sections = item.get('sections', [])
        applied = False
        for s in sections:
            t_l = s.get('title_en', '').lower()
            if any(m in t_l for m in finfo['title_en_match']):
                # Check if section already has formula
                if not any('$$' in p for p in s.get('paragraphs_en', [])):
                    ins_idx = finfo.get('insert_after_idx', 0)
                    if ins_idx < len(s['paragraphs_en']):
                        s['paragraphs_en'].insert(ins_idx + 1, finfo['formula_en'])
                        s['paragraphs_fa'].insert(ins_idx + 1, finfo['formula_fa'])
                    else:
                        s['paragraphs_en'].append(finfo['formula_en'])
                        s['paragraphs_fa'].append(finfo['formula_fa'])
                    applied = True
                    updated_formula_count += 1
                    print(f"Added formula to: {item['term_en']} ({slug}) in section '{s['title_en']}'")
                    break
        if not applied and sections:
            # Fallback to first section mentioning formula/how or first section
            for s in sections:
                if any(k in s.get('title_en', '').lower() for k in ['formula', 'calculate', 'what is']):
                    s['paragraphs_en'].insert(1, finfo['formula_en'])
                    s['paragraphs_fa'].insert(1, finfo['formula_fa'])
                    applied = True
                    updated_formula_count += 1
                    print(f"Fallback added formula to: {item['term_en']} ({slug}) in section '{s['title_en']}'")
                    break

print(f"Total specific formulas updated: {updated_formula_count}")
