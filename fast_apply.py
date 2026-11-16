#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-Speed Single-Pass Regex Enrichment Engine for MarketDict
1. Injects complete LaTeX formulas for image-based & unformatted formulas across all terms.
2. Ultra-fast single-pass regex for both English and Persian internal term linking.
3. Completely safe: protects KaTeX math ($$...$$) and existing <a> tags.
"""

import json
import re
import os
import time

DICT_FILE = "bilingual_dictionary.json"

t_start = time.time()
print(f"Loading {DICT_FILE}...", flush=True)
with open(DICT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} terms in {time.time() - t_start:.2f}s.", flush=True)

# 1. Master Formula Registry
FORMULA_DB = {
    'sharperatio': {
        'title_match': ['formula and calculation', 'how is', 'formula', 'calculation'],
        'formula_en': '$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Return of portfolio} \\\\ &R_f = \\text{Risk-free rate} \\\\ &\\sigma_p = \\text{Standard deviation of portfolio excess return} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت شارپ} = \\frac{R_p - R_f}{\\sigma_p}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده سبد سرمایه‌گذاری (پرتفوی)} \\\\ &R_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\sigma_p = \\text{انحراف معیار بازده مازاد پرتفوی} \\end{aligned}$$',
    },
    'sortinoratio': {
        'title_match': ['how to calculate the sortino ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Sortino Ratio} = \\frac{R_p - r_f}{\\sigma_d}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Actual or expected portfolio return} \\\\ &r_f = \\text{Risk-free rate} \\\\ &\\sigma_d = \\text{Standard deviation of the downside} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت سورتینو} = \\frac{R_p - r_f}{\\sigma_d}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده واقعی یا مورد انتظار پرتفوی} \\\\ &r_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\sigma_d = \\text{انحراف معیار بازده‌های منفی (ریسک نزولی)} \\end{aligned}$$',
    },
    'treynorratio': {
        'title_match': ['the formula for the treynor ratio is', 'formula', 'calculation'],
        'formula_en': '$$\\text{Treynor Ratio} = \\frac{r_p - r_f}{\\beta_p}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &r_p = \\text{Portfolio return} \\\\ &r_f = \\text{Risk-free rate} \\\\ &\\beta_p = \\text{Beta of the portfolio} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت ترینور} = \\frac{r_p - r_f}{\\beta_p}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &r_p = \\text{بازده سبد سرمایه‌گذاری} \\\\ &r_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\beta_p = \\text{بتای پرتفوی (ریسک سیستماتیک)} \\end{aligned}$$',
    },
    'informationratio': {
        'title_match': ['how to calculate', 'formula', 'calculation'],
        'formula_en': '$$\\text{Information Ratio (IR)} = \\frac{R_p - R_b}{\\text{Tracking Error}}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Portfolio return} \\\\ &R_b = \\text{Benchmark return} \\\\ &\\text{Tracking Error} = \\text{Standard deviation of excess return} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت اطلاعات (IR)} = \\frac{R_p - R_b}{\\text{خطای ردیابی}}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده پرتفوی} \\\\ &R_b = \\text{بازده شاخص مبنا (بنچ‌مارک)} \\\\ &\\text{خطای ردیابی} = \\text{انحراف معیار بازده مازاد نسبت به بنچ‌مارک} \\end{aligned}$$',
    },
    'accounting-equation': {
        'title_match': ['accounting equation formula and calculation', 'formula', 'calculation'],
        'formula_en': '$$\\text{Assets} = \\text{Liabilities} + \\text{Shareholders\' Equity}$$',
        'formula_fa': '$$\\text{دارایی‌ها} = \\text{بدهی‌ها} + \\text{حقوق صاحبان سهام}$$',
    },
    'arr': {
        'title_match': ['calculating arr', 'formula', 'calculation'],
        'formula_en': '$$\\text{ARR} = \\frac{\\text{Average Annual Profit}}{\\text{Initial Investment}}$$',
        'formula_fa': '$$\\text{نرخ بازده حسابداری (ARR)} = \\frac{\\text{میانگین سود خالص سالانه}}{\\text{سرمایه‌گذاری اولیه}}$$',
    },
    'breakevenanalysis': {
        'title_match': ['break-even point (bep) formula', 'formula', 'calculation'],
        'formula_en': '$$\\text{Break-Even Point (BEP)} = \\frac{\\text{Total Fixed Costs}}{\\text{Price per Unit} - \\text{Variable Cost per Unit}}$$',
        'formula_fa': '$$\\text{نقطه سربه‌سر (BEP)} = \\frac{\\text{کل هزینه‌های ثابت}}{\\text{قیمت فروش هر واحد} - \\text{هزینه متغیر هر واحد}}$$',
    },
    'debtequityratio': {
        'title_match': ['calculating the d/e ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Debt / Equity Ratio} = \\frac{\\text{Total Liabilities}}{\\text{Total Shareholders\' Equity}}$$',
        'formula_fa': '$$\\text{نسبت بدهی به حقوق صاحبان سهام (D/E)} = \\frac{\\text{مجموع بدهی‌ها}}{\\text{مجموع حقوق صاحبان سهام}}$$',
    },
    'dscr': {
        'title_match': ['calculating the dscr', 'formula', 'calculation'],
        'formula_en': '$$\\text{DSCR} = \\frac{\\text{Net Operating Income (NOI)}}{\\text{Total Debt Service}}$$',
        'formula_fa': '$$\\text{نسبت پوشش اصل و بهره بدهی (DSCR)} = \\frac{\\text{درآمد خالص عملیاتی (NOI)}}{\\text{کل خدمات بدهی (اقساط اصل و سود)}}$$',
    },
    'ebit': {
        'title_match': ['formula and calculation', 'formula', 'calculation'],
        'formula_en': '$$\\text{EBIT} = \\text{Revenue} - \\text{COGS} - \\text{Operating Expenses}$$',
        'formula_fa': '$$\\text{سود قبل از بهره و مالیات (EBIT)} = \\text{درآمد فروش} - \\text{بهای تمام‌شده کالای فروش‌رفته} - \\text{هزینه‌های عملیاتی}$$',
    },
    'ebita': {
        'title_match': ['how to calculate ebita', 'formula', 'calculation'],
        'formula_en': '$$\\text{EBITA} = \\text{EBIT} + \\text{Amortization}$$',
        'formula_fa': '$$\\text{EBITA} = \\text{سود قبل از بهره و مالیات} + \\text{استهلاک دارایی‌های نامشهود}$$',
    },
    'jensensmeasure': {
        'title_match': ['how to calculate jensen\'s measure', 'formula', 'calculation'],
        'formula_en': '$$\\alpha = R_p - [R_f + \\beta_p (R_m - R_f)]$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Portfolio return} \\\\ &R_f = \\text{Risk-free rate} \\\\ &\\beta_p = \\text{Portfolio beta} \\\\ &R_m = \\text{Market return} \\end{aligned}$$',
        'formula_fa': '$$\\alpha = R_p - [R_f + \\beta_p (R_m - R_f)]$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده سبد سرمایه‌گذاری} \\\\ &R_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\beta_p = \\text{ضریب بتای سبد سرمایه‌گذاری} \\\\ &R_m = \\text{بازده کل بازار} \\end{aligned}$$',
    },
    'loantovalue': {
        'title_match': ['calculating the ltv ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{LTV} = \\frac{\\text{Mortgage Amount}}{\\text{Appraised Property Value}} \\times 100\\%$$',
        'formula_fa': '$$\\text{نسبت وام به ارزش وثیقه (LTV)} = \\frac{\\text{مبلغ وام دریافتی}}{\\text{ارزش کارشناسی ملک/وثیقه}} \\times ۱۰۰\\%$$',
    },
    'macd': {
        'title_match': ['macd formula', 'formula', 'calculation'],
        'formula_en': '$$\\begin{aligned} &\\text{MACD Line} = \\text{12-Period EMA} - \\text{26-Period EMA} \\\\ &\\text{Signal Line} = \\text{9-Period EMA of MACD Line} \\\\ &\\text{MACD Histogram} = \\text{MACD Line} - \\text{Signal Line} \\end{aligned}$$',
        'formula_fa': '$$\\begin{aligned} &\\text{خط MACD} = \\text{میانگین متحرک نمایی ۱۲ دوره‌ای} - \\text{میانگین متحرک نمایی ۲۶ دوره‌ای} \\\\ &\\text{خط سیگنال} = \\text{میانگین متحرک نمایی ۹ دوره‌ای خط MACD} \\\\ &\\text{هیستوگرام MACD} = \\text{خط MACD} - \\text{خط سیگنال} \\end{aligned}$$',
    },
    'nav': {
        'title_match': ['nav formula', 'formula', 'calculation'],
        'formula_en': '$$\\text{NAV} = \\frac{\\text{Total Assets} - \\text{Total Liabilities}}{\\text{Total Shares Outstanding}}$$',
        'formula_fa': '$$\\text{ارزش خالص هر سهم / واحد (NAV)} = \\frac{\\text{مجموع دارایی‌ها} - \\text{مجموع بدهی‌ها}}{\\text{تعداد کل سهام / واحدهای منتشره}}$$',
    },
    'networth': {
        'title_match': ['how to calculate net worth', 'formula', 'calculation'],
        'formula_en': '$$\\text{Net Worth} = \\text{Total Assets} - \\text{Total Liabilities}$$',
        'formula_fa': '$$\\text{ارزش خالص دارایی} = \\text{مجموع دارایی‌ها} - \\text{مجموع بدهی‌ها}$$',
    },
    'normaldistribution': {
        'title_match': ['the formula for normal distribution', 'formula', 'calculation'],
        'formula_en': '$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x - \\mu}{\\sigma}\\right)^2}$$',
        'formula_fa': '$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x - \\mu}{\\sigma}\\right)^2}$$',
    },
    'grossprofit': {
        'title_match': ['calculating gross profit', 'formula', 'calculation'],
        'formula_en': '$$\\text{Gross Profit} = \\text{Revenue} - \\text{Cost of Goods Sold (COGS)}$$',
        'formula_fa': '$$\\text{سود ناخالص} = \\text{درآمد فروش} - \\text{بهای تمام‌شده کالای فروش‌رفته (COGS)}$$',
    },
    'compoundinterest': {
        'title_match': ['approach two: fixed formula', 'fixed formula', 'formula'],
        'formula_en': '$$A = P \\left(1 + \\frac{r}{n}\\right)^{nt}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &A = \\text{Final amount} \\\\ &P = \\text{Initial principal} \\\\ &r = \\text{Annual interest rate} \\\\ &n = \\text{Compounding frequency per year} \\\\ &t = \\text{Time in years} \\end{aligned}$$',
        'formula_fa': '$$A = P \\left(1 + \\frac{r}{n}\\right)^{nt}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &A = \\text{مبلغ نهایی سرمایه} \\\\ &P = \\text{اصل سرمایه اولیه} \\\\ &r = \\text{نرخ سود سالانه} \\\\ &n = \\text{تعداد دوره‌های ترکیب در سال} \\\\ &t = \\text{مدت زمان به سال} \\end{aligned}$$',
    },
    'cagr': {
        'title_match': ['cagr formula', 'formula', 'calculation'],
        'formula_en': '$$\\text{CAGR} = \\left(\\frac{\\text{Ending Value}}{\\text{Beginning Value}}\\right)^{\\frac{1}{n}} - 1$$',
        'formula_fa': '$$\\text{نرخ رشد مرکب سالانه (CAGR)} = \\left(\\frac{\\text{ارزش پایانی}}{\\text{ارزش اولیه}}\\right)^{\\frac{1}{n}} - 1$$',
    },
    'dividendpayoutratio': {
        'title_match': ['calculating the dividend payout ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Dividend Payout Ratio} = \\frac{\\text{Total Dividends Paid}}{\\text{Net Income}}$$',
        'formula_fa': '$$\\text{نسبت پرداخت سود نقدی} = \\frac{\\text{مجموع سود نقدی سهام پرداختی}}{\\text{سود خالص شرکت}}$$',
    },
    'eps': {
        'title_match': ['formula for eps', 'formula', 'calculation'],
        'formula_en': '$$\\text{EPS} = \\frac{\\text{Net Income} - \\text{Preferred Dividends}}{\\text{Weighted Average Common Shares Outstanding}}$$',
        'formula_fa': '$$\\text{سود هر سهم (EPS)} = \\frac{\\text{سود خالص} - \\text{سود سهام ممتاز}}{\\text{میانگین موزون تعداد سهام عادی در گردش}}$$',
    },
    'equity': {
        'title_match': ['formula and how to calculate', 'formula', 'calculation'],
        'formula_en': '$$\\text{Shareholders\' Equity} = \\text{Total Assets} - \\text{Total Liabilities}$$',
        'formula_fa': '$$\\text{حقوق صاحبان سهام} = \\text{مجموع دارایی‌ها} - \\text{مجموع بدهی‌ها}$$',
    },
    'absorptioncosting': {
        'title_match': ['formula for absorption costing', 'formula', 'calculation'],
        'formula_en': '$$\\text{Absorption Cost per Unit} = \\frac{\\text{Direct Materials} + \\text{Direct Labor} + \\text{Variable Overhead} + \\text{Fixed Overhead}}{\\text{Total Units Produced}}$$',
        'formula_fa': '$$\\text{بهای تمام‌شده هر واحد (هزینه‌یابی جذبی)} = \\frac{\\text{مواد مستقیم} + \\text{دستمزد مستقیم} + \\text{سربار متغیر} + \\text{سربار ثابت}}{\\text{تعداد کل واحدهای تولیدشده}}$$',
    },
    'affo': {
        'title_match': ['how to calculate adjusted funds from operations (affo)', 'formula', 'calculation'],
        'formula_en': '$$\\begin{aligned} &\\text{FFO} = \\text{Net Income} + \\text{Amortization} + \\text{Depreciation} - \\text{Capital Gains from Property Sales} \\\\ &\\text{AFFO} = \\text{FFO} + \\text{Rent Increases} - \\text{CapEx} - \\text{Routine Maintenance} \\end{aligned}$$',
        'formula_fa': '$$\\begin{aligned} &\\text{FFO} = \\text{سود خالص} + \\text{استهلاک} - \\text{سود حاصل از فروش املاک} \\\\ &\\text{AFFO} = \\text{FFO} + \\text{تعدیلات اجاره} - \\text{مخارج سرمایه‌ای نگهداری} \\end{aligned}$$',
    },
    'adjusted-ebitda': {
        'title_match': ['how to understand the adjusted ebitda formula', 'formula', 'calculation'],
        'formula_en': '$$\\begin{aligned} &\\text{EBITDA} = \\text{Net Income} + \\text{Interest} + \\text{Taxes} + \\text{D\\&A} \\\\ &\\text{Adjusted EBITDA} = \\text{EBITDA} \\pm \\text{Non-Recurring Adjustments} \\end{aligned}$$',
        'formula_fa': '$$\\begin{aligned} &\\text{EBITDA} = \\text{سود خالص} + \\text{بهره} + \\text{مالیات} + \\text{استهلاک} \\\\ &\\text{EBITDA تعدیل‌شده} = \\text{EBITDA} \\pm \\text{اقلام غیرتکراری و استثنایی} \\end{aligned}$$',
    },
    'zero-couponbond': {
        'title_match': ['calculating zero-coupon bond prices', 'formula', 'calculation'],
        'formula_en': '$$\\text{Price} = \\frac{M}{(1 + r)^n}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &M = \\text{Maturity value / Par value} \\\\ &r = \\text{Required interest rate} \\\\ &n = \\text{Number of years until maturity} \\end{aligned}$$',
        'formula_fa': '$$\\text{قیمت اوراق بدون کوپن} = \\frac{M}{(1 + r)^n}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &M = \\text{ارزش اسمی در سررسید} \\\\ &r = \\text{نرخ بازده مورد انتظار} \\\\ &n = \\text{تعداد سال‌های مانده تا سررسید} \\end{aligned}$$',
    },
    'liquidity-coverage-ratio': {
        'title_match': ['calculating the liquidity coverage ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{LCR} = \\frac{\\text{High-Quality Liquid Assets (HQLA)}}{\\text{Total Net Cash Outflow over 30 Days}} \\ge 100\\%$$',
        'formula_fa': '$$\\text{نسبت پوشش نقدینگی (LCR)} = \\frac{\\text{دارایی‌های نقدی باکیفیت بالا (HQLA)}}{\\text{کل خروجی خالص وجه نقد طی ۳۰ روز}} \\ge ۱۰۰\\%$$',
    },
    'oid': {
        'title_match': ['formula and calculation of oid', 'formula', 'calculation'],
        'formula_en': '$$\\text{OID} = \\text{Stated Redemption Price at Maturity} - \\text{Issue Price}$$',
        'formula_fa': '$$\\text{کسر اوراق اولیه (OID)} = \\text{قیمت بازخرید در سررسید (ارزش اسمی)} - \\text{قیمت انتشار اولیه}$$',
    },
    'bayes-theorem': {
        'title_match': ['deriving the bayes\' theorem formula', 'formula', 'calculation'],
        'formula_en': '$$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$',
        'formula_fa': '$$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$',
    },
    'irr': {
        'title_match': ['the formula for irr', 'how to calculate the irr', 'formula'],
        'formula_en': '$$0 = \\text{NPV} = \\sum_{t=1}^{T} \\frac{C_t}{(1 + \\text{IRR})^t} - C_0$$',
        'formula_fa': '$$0 = \\text{NPV} = \\sum_{t=1}^{T} \\frac{C_t}{(1 + \\text{IRR})^t} - C_0$$',
    },
    'consumerpriceindex': {
        'title_match': ['cpi-u formula', 'formula', 'calculation'],
        'formula_en': '$$\\text{CPI} = \\frac{\\text{Cost of Market Basket in Given Year}}{\\text{Cost of Market Basket in Base Year}} \\times 100$$',
        'formula_fa': '$$\\text{شاخص بهای مصرف‌کننده (CPI)} = \\frac{\\text{قیمت سبد کالا در سال جاری}}{\\text{قیمت سبد کالا در سال پایه}} \\times ۱۰۰$$',
    },
    'capitalexpenditure': {
        'title_match': ['calculating capital expenditures: formula and method', 'formula', 'calculation'],
        'formula_en': '$$\\text{CapEx} = \\text{PP\\&E}_{\\text{current}} - \\text{PP\\&E}_{\\text{prior}} + \\text{Depreciation}$$',
        'formula_fa': '$$\\text{مخارج سرمایه‌ای (CapEx)} = \\text{اموال، ماشین‌آلات و تجهیزات دوره جاری} - \\text{دوره قبل} + \\text{استهلاک}$$',
    },
    'gdp': {
        'title_match': ['gdp formula', 'formula', 'calculation'],
        'formula_en': '$$\\text{GDP} = C + I + G + (X - M)$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &C = \\text{Consumption} \\\\ &I = \\text{Investment} \\\\ &G = \\text{Government spending} \\\\ &X = \\text{Exports} \\\\ &M = \\text{Imports} \\end{aligned}$$',
        'formula_fa': '$$\\text{تولید ناخالص داخلی (GDP)} = C + I + G + (X - M)$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &C = \\text{مصرف بخش خصوصی} \\\\ &I = \\text{سرمایه‌گذاری ناخالص} \\\\ &G = \\text{مخارج دولت} \\\\ &X = \\text{صادرات} \\\\ &M = \\text{واردات} \\end{aligned}$$',
    },
    'keyrateduration': {
        'title_match': ['key rate duration formula explained', 'formula', 'calculation'],
        'formula_en': '$$\\text{Key Rate Duration} = \\frac{P_- - P_+}{2 \\times \\Delta y \\times P_0}$$',
        'formula_fa': '$$\\text{دیرش نرخ کلیدی} = \\frac{P_- - P_+}{2 \\times \\Delta y \\times P_0}$$',
    },
    'currentratio': {
        'title_match': ['current ratio formula', 'how to calculate the current ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Current Ratio} = \\frac{\\text{Current Assets}}{\\text{Current Liabilities}}$$',
        'formula_fa': '$$\\text{نسبت جاری} = \\frac{\\text{دارایی‌های جاری}}{\\text{بدهی‌های جاری}}$$',
    },
    'quickratio': {
        'title_match': ['quick ratio formula', 'how to calculate the quick ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Quick Ratio} = \\frac{\\text{Cash} + \\text{Marketable Securities} + \\text{Accounts Receivable}}{\\text{Current Liabilities}}$$',
        'formula_fa': '$$\\text{نسبت آنی (سریع)} = \\frac{\\text{وجه نقد} + \\text{اوراق بهادار کوتاه‌مدت} + \\text{حساب‌های دریافتنی}}{\\text{بدهی‌های جاری}}$$',
    },
    'cashratio': {
        'title_match': ['cash ratio formula', 'how to calculate the cash ratio', 'formula', 'calculation'],
        'formula_en': '$$\\text{Cash Ratio} = \\frac{\\text{Cash and Cash Equivalents}}{\\text{Current Liabilities}}$$',
        'formula_fa': '$$\\text{نسبت وجه نقد} = \\frac{\\text{موجودی نقد و معادل‌های نقد}}{\\text{بدهی‌های جاری}}$$',
    },
    'returnonequity': {
        'title_match': ['roe formula', 'how to calculate roe', 'formula', 'calculation'],
        'formula_en': '$$\\text{ROE} = \\frac{\\text{Net Income}}{\\text{Shareholders\' Equity}}$$',
        'formula_fa': '$$\\text{بازده حقوق صاحبان سهام (ROE)} = \\frac{\\text{سود خالص}}{\\text{حقوق صاحبان سهام}}$$',
    },
    'returnonassets': {
        'title_match': ['roa formula', 'how to calculate roa', 'formula', 'calculation'],
        'formula_en': '$$\\text{ROA} = \\frac{\\text{Net Income}}{\\text{Total Assets}}$$',
        'formula_fa': '$$\\text{بازده دارایی‌ها (ROA)} = \\frac{\\text{سود خالص}}{\\text{کل دارایی‌ها}}$$',
    },
    'workingcapital': {
        'title_match': ['working capital formula', 'how to calculate working capital', 'formula', 'calculation'],
        'formula_en': '$$\\text{Working Capital} = \\text{Current Assets} - \\text{Current Liabilities}$$',
        'formula_fa': '$$\\text{سرمایه در گردش} = \\text{دارایی‌های جاری} - \\text{بدهی‌های جاری}$$',
    },
    'enterprisevalue': {
        'title_match': ['enterprise value formula', 'how to calculate enterprise value', 'formula', 'calculation'],
        'formula_en': '$$\\text{Enterprise Value (EV)} = \\text{Market Cap} + \\text{Total Debt} - \\text{Cash and Cash Equivalents}$$',
        'formula_fa': '$$\\text{ارزش کل بنگاه (EV)} = \\text{ارزش بازار سهام} + \\text{مجموع بدهی‌ها} - \\text{وجه نقد و معادل‌های آن}$$',
    },
    'freecashflow': {
        'title_match': ['free cash flow formula', 'how to calculate free cash flow', 'formula', 'calculation'],
        'formula_en': '$$\\text{Free Cash Flow (FCF)} = \\text{Operating Cash Flow} - \\text{Capital Expenditures (CapEx)}$$',
        'formula_fa': '$$\\text{جریان نقد آزاد (FCF)} = \\text{جریان نقد عملیاتی} - \\text{مخارج سرمایه‌ای (CapEx)}$$',
    },
    'ruleof72': {
        'title_match': ['rule of 72 formula', 'how the rule of 72 works', 'formula', 'calculation'],
        'formula_en': '$$\\text{Years to Double} \\approx \\frac{72}{\\text{Interest Rate (\\%)}}$$',
        'formula_fa': '$$\\text{تعداد سال‌ها تا دو برابر شدن سرمایه} \\approx \\frac{۷۲}{\\text{نرخ سود سالانه (به درصد)}}$$',
    }
}

print("Injecting formula standards...", flush=True)
injected = 0
for item in data:
    slug = item.get('slug', '').lower()
    if slug in FORMULA_DB:
        finfo = FORMULA_DB[slug]
        sections = item.get('sections', [])
        applied = False
        for s in sections:
            t_l = s.get('title_en', '').lower()
            if any(m in t_l for m in finfo['title_match']):
                if not any('$$' in p for p in s.get('paragraphs_en', [])):
                    s['paragraphs_en'].insert(1, finfo['formula_en'])
                    s['paragraphs_fa'].insert(1, finfo['formula_fa'])
                    applied = True
                    injected += 1
                    print(f"  + Injected formula: {item['term_en']} ({slug}) -> {s['title_en']}", flush=True)
                    break
        if not applied and sections:
            for s in sections:
                if any(k in s.get('title_en', '').lower() for k in ['formula', 'calculate', 'what is']):
                    s['paragraphs_en'].insert(1, finfo['formula_en'])
                    s['paragraphs_fa'].insert(1, finfo['formula_fa'])
                    applied = True
                    injected += 1
                    print(f"  + Fallback injected formula: {item['term_en']} ({slug}) -> {s['title_en']}", flush=True)
                    break

print(f"Total target formulas injected: {injected}", flush=True)

# 2. Build High-Speed Regex Index
en_dict = {}
fa_dict = {}

STOPWORDS = {
    'rate', 'cost', 'costs', 'bond', 'bonds', 'bank', 'banks', 'term', 'terms', 'plan', 'plans',
    'time', 'times', 'date', 'dates', 'high', 'low', 'long', 'short', 'free', 'real', 'open',
    'firm', 'firms', 'good', 'goods', 'year', 'years', 'lead', 'gain', 'gains', 'loss', 'losses',
    'sale', 'sales', 'fund', 'funds', 'book', 'cash', 'debt', 'risk', 'unit', 'units', 'call',
    'put', 'note', 'notes', 'pool', 'pools', 'par', 'tax', 'taxes', 'fee', 'fees', 'cut', 'cuts',
    'cap', 'caps', 'bar', 'bars', 'gap', 'gaps', 'tip', 'tips', 'bid', 'ask', 'run', 'runs',
    'pay', 'pays', 'buy', 'buys', 'sell', 'sells', 'hold', 'holds', 'mean', 'item', 'items',
    'other', 'value', 'values', 'price', 'prices', 'stock', 'stocks', 'share', 'shares', 'asset',
    'assets', 'money', 'yield', 'yields', 'order', 'orders', 'trade', 'trades', 'loan', 'loans',
    'trend', 'trust', 'trusts', 'gross', 'net', 'swap', 'swaps', 'basis', 'spot', 'strike',
    'spread', 'spreads', 'alpha', 'beta', 'floor', 'float', 'chart', 'index', 'ratio', 'ratios',
    'margin', 'return', 'returns', 'audit', 'audits', 'credit', 'debit', 'equity', 'equities',
    'option', 'options', 'future', 'futures', 'market', 'markets', 'factor', 'factors', 'income',
    'profit', 'profits', 'growth', 'charge', 'charges', 'strike', 'series', 'hybrid', 'target',
    'capital', 'model', 'face value'
}

for item in data:
    slug = item.get('slug', '').strip().lower()
    if not slug:
        continue
    
    t_en = item.get('term_en', '').strip()
    clean_en = re.sub(r'\s*\([^)]*\)', '', t_en).strip().lower()
    if len(clean_en) >= 5 and clean_en not in STOPWORDS:
        en_dict[clean_en] = slug
        
    m_paren = re.search(r'\(([A-Z0-9-]{3,8})\)', t_en)
    if m_paren:
        ac = m_paren.group(1).lower()
        if ac not in STOPWORDS:
            en_dict[ac] = slug
            
    t_fa = item.get('term_fa', '').strip()
    clean_fa = re.sub(r'\s*\([^)]*\)', '', t_fa).strip()
    clean_fa = clean_fa.replace('\u200c', ' ').replace('ي', 'ی').replace('ك', 'ک')
    clean_fa = re.sub(r'\s+', ' ', clean_fa).strip()
    if len(clean_fa) >= 6:
        fa_dict[clean_fa] = slug

sorted_en = sorted(en_dict.keys(), key=lambda x: len(x), reverse=True)[:500]
sorted_fa = sorted(fa_dict.keys(), key=lambda x: len(x), reverse=True)[:500]

# Pre-compile the master regexes
print("Compiling master regexes for English and Persian...", flush=True)
pattern_en = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted_en) + r')\b', re.IGNORECASE)

escaped_fa = [re.escape(k).replace(r'\ ', r'[\s\u200c]+') for k in sorted_fa]
pattern_fa = re.compile(r'(?<![^\s،؛«»()\[\]{}.])(' + '|'.join(escaped_fa) + r')(?![^\s،؛«»()\[\]{}.])', re.IGNORECASE)

print("Pre-compilation finished.", flush=True)

def fast_linkify_en(text, current_slug=None):
    if not text or not isinstance(text, str):
        return text
        
    placeholders = []
    def add_ph(s):
        placeholders.append(s)
        return f"___PH_{len(placeholders)-1}___"
        
    # Protect math blocks
    clean = re.sub(r'\$\$.*?\$\$', lambda m: add_ph(m.group(0)), text, flags=re.DOTALL)
    
    # Normalize existing links
    def norm_a(m):
        full_a = m.group(0)
        m_slug = re.search(r'(?:href=[\'"](?:https?://www\.investopedia\.com)?/terms/[a-z0-9]/([a-z0-9_-]+)\.asp[\'"]|data-slug=[\'"]([a-z0-9_-]+)[\'"]|href=[\'"]#term/([a-z0-9_-]+)[\'"])', full_a)
        if m_slug:
            s = m_slug.group(1) or m_slug.group(2) or m_slug.group(3)
            inner = re.sub(r'<[^>]+>', '', full_a)
            return add_ph(f'<a href="#term/{s}" class="internal-term-link" data-slug="{s}">{inner}</a>')
        return add_ph(full_a)

    clean = re.sub(r'<a\b[^>]*>.*?</a>', norm_a, clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', lambda m: add_ph(m.group(0)), clean)
    
    linked = set()
    if current_slug:
        linked.add(current_slug)
        
    def repl(m):
        if len(linked) >= 5:
            return m.group(0)
        matched_str = m.group(1)
        k = matched_str.lower()
        slug = en_dict.get(k)
        if slug and slug not in linked:
            linked.add(slug)
            tag = f'<a href="#term/{slug}" class="internal-term-link" data-slug="{slug}">{matched_str}</a>'
            return add_ph(tag)
        return m.group(0)

    clean = pattern_en.sub(repl, clean)
    
    for idx in range(len(placeholders) - 1, -1, -1):
        clean = clean.replace(f"___PH_{idx}___", placeholders[idx])
        
    return clean

def fast_linkify_fa(text, current_slug=None):
    if not text or not isinstance(text, str):
        return text
        
    placeholders = []
    def add_ph(s):
        placeholders.append(s)
        return f"___PH_{len(placeholders)-1}___"
        
    clean = re.sub(r'\$\$.*?\$\$', lambda m: add_ph(m.group(0)), text, flags=re.DOTALL)
    
    def norm_a(m):
        full_a = m.group(0)
        m_slug = re.search(r'(?:href=[\'"](?:https?://www\.investopedia\.com)?/terms/[a-z0-9]/([a-z0-9_-]+)\.asp[\'"]|data-slug=[\'"]([a-z0-9_-]+)[\'"]|href=[\'"]#term/([a-z0-9_-]+)[\'"])', full_a)
        if m_slug:
            s = m_slug.group(1) or m_slug.group(2) or m_slug.group(3)
            inner = re.sub(r'<[^>]+>', '', full_a)
            return add_ph(f'<a href="#term/{s}" class="internal-term-link" data-slug="{s}">{inner}</a>')
        return add_ph(full_a)

    clean = re.sub(r'<a\b[^>]*>.*?</a>', norm_a, clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', lambda m: add_ph(m.group(0)), clean)
    
    linked = set()
    if current_slug:
        linked.add(current_slug)
        
    def repl(m):
        if len(linked) >= 5:
            return m.group(0)
        matched_str = m.group(1)
        k = matched_str.replace('\u200c', ' ').replace('ي', 'ی').replace('ك', 'ک')
        k = re.sub(r'\s+', ' ', k).strip()
        slug = fa_dict.get(k)
        if slug and slug not in linked:
            linked.add(slug)
            tag = f'<a href="#term/{slug}" class="internal-term-link" data-slug="{slug}">{matched_str}</a>'
            return add_ph(tag)
        return m.group(0)

    clean = pattern_fa.sub(repl, clean)
    
    for idx in range(len(placeholders) - 1, -1, -1):
        clean = clean.replace(f"___PH_{idx}___", placeholders[idx])
        
    return clean

print("Fast single-pass linking across all articles...", flush=True)
t_link = time.time()
enriched_count = 0

for item in data:
    if not item.get('sections'):
        continue
    enriched_count += 1
    slug = item.get('slug', '').lower()
    
    item['definition_en'] = fast_linkify_en(item.get('definition_en', ''), current_slug=slug)
    item['definition_fa'] = fast_linkify_fa(item.get('definition_fa', ''), current_slug=slug)
    
    if item.get('takeaways_en'):
        item['takeaways_en'] = [fast_linkify_en(t, current_slug=slug) for t in item['takeaways_en']]
    if item.get('takeaways_fa'):
        item['takeaways_fa'] = [fast_linkify_fa(t, current_slug=slug) for t in item['takeaways_fa']]
        
    if item.get('bottom_line_en'):
        item['bottom_line_en'] = fast_linkify_en(item['bottom_line_en'], current_slug=slug)
    if item.get('bottom_line_fa'):
        item['bottom_line_fa'] = fast_linkify_fa(item['bottom_line_fa'], current_slug=slug)
        
    for s in item.get('sections', []):
        s['paragraphs_en'] = [fast_linkify_en(p, current_slug=slug) for p in s.get('paragraphs_en', [])]
        s['paragraphs_fa'] = [fast_linkify_fa(p, current_slug=slug) for p in s.get('paragraphs_fa', [])]

print(f"Finished linking {enriched_count} terms in {time.time() - t_link:.2f}s!", flush=True)

# Write to temp file then atomic rename for safety
print(f"Saving atomically to {DICT_FILE}...", flush=True)
TMP_FILE = DICT_FILE + ".tmp"
with open(TMP_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

if os.path.exists(DICT_FILE):
    os.replace(TMP_FILE, DICT_FILE)
else:
    os.rename(TMP_FILE, DICT_FILE)

print("SUCCESS: bilingual_dictionary.json updated perfectly!", flush=True)
