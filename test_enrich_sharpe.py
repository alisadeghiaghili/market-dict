import json
from bs4 import BeautifulSoup
from scrape_and_enrich_pipeline import fetch_page_with_retry, clean_element_html, tr, tr_chunks, classify_category

# Formula DB for image-based formulas in Investopedia
FORMULA_IMAGE_DB = {
    'sharperatio': {
        'formula_en': '$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Return of portfolio} \\\\ &R_f = \\text{Risk-free rate} \\\\ &\\sigma_p = \\text{Standard deviation of portfolio excess return} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت شارپ} = \\frac{R_p - R_f}{\\sigma_p}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده سبد سرمایه‌گذاری (پرتفوی)} \\\\ &R_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\sigma_p = \\text{انحراف معیار بازده مازاد پرتفوی} \\end{aligned}$$'
    },
    'sortinoratio': {
        'formula_en': '$$\\text{Sortino Ratio} = \\frac{R_p - r_f}{\\sigma_d}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &R_p = \\text{Actual or expected portfolio return} \\\\ &r_f = \\text{Risk-free rate} \\\\ &\\sigma_d = \\text{Standard deviation of the downside} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت سورتینو} = \\frac{R_p - r_f}{\\sigma_d}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &R_p = \\text{بازده واقعی یا مورد انتظار پرتفوی} \\\\ &r_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\sigma_d = \\text{انحراف معیار بازده‌های نزولی (ریسک منفی)} \\end{aligned}$$'
    },
    'treynorratio': {
        'formula_en': '$$\\text{Treynor Ratio} = \\frac{r_p - r_f}{\\beta_p}$$\n$$\\begin{aligned} &\\textbf{where:} \\\\ &r_p = \\text{Portfolio return} \\\\ &r_f = \\text{Risk-free rate} \\\\ &\\beta_p = \\text{Beta of the portfolio} \\end{aligned}$$',
        'formula_fa': '$$\\text{نسبت ترینور} = \\frac{r_p - r_f}{\\beta_p}$$\n$$\\begin{aligned} &\\textbf{تعریف متغیرها:} \\\\ &r_p = \\text{بازده سبد سرمایه‌گذاری} \\\\ &r_f = \\text{نرخ بازده بدون ریسک} \\\\ &\\beta_p = \\text{بتای پرتفوی (ریسک سیستماتیک)} \\end{aligned}$$'
    },
    'accounting-equation': {
        'formula_en': '$$\\text{Assets} = \\text{Liabilities} + \\text{Shareholders\' Equity}$$',
        'formula_fa': '$$\\text{دارایی‌ها} = \\text{بدهی‌ها} + \\text{حقوق صاحبان سهام}$$'
    },
    'breakevenanalysis': {
        'formula_en': '$$\\text{Break-Even Point (BEP)} = \\frac{\\text{Total Fixed Costs}}{\\text{Price per Unit} - \\text{Variable Cost per Unit}}$$',
        'formula_fa': '$$\\text{نقطه سربه‌سر (BEP)} = \\frac{\\text{کل هزینه‌های ثابت}}{\\text{قیمت فروش هر واحد} - \\text{هزینه متغیر هر واحد}}$$'
    },
    'debtequityratio': {
        'formula_en': '$$\\text{Debt / Equity Ratio} = \\frac{\\text{Total Liabilities}}{\\text{Total Shareholders\' Equity}}$$',
        'formula_fa': '$$\\text{نسبت بدهی به حقوق صاحبان سهام (D/E)} = \\frac{\\text{مجموع بدهی‌ها}}{\\text{مجموع حقوق صاحبان سهام}}$$'
    }
}

slug = 'sharperatio'
url = 'https://www.investopedia.com/terms/s/sharperatio.asp'
html = fetch_page_with_retry(url)
soup = BeautifulSoup(html, 'html.parser')
body = soup.find('div', class_='article-body-content') or soup

sections = []
current_sec = None

for el in body.children:
    if not hasattr(el, 'name') or not el.name:
        continue
    h = el if el.name in ['h2', 'h3'] else el.find(['h2', 'h3'])
    if h:
        htitle = h.get_text(strip=True)
        if not any(skip in htitle.lower() for skip in ['key takeaways', 'related articles', 'article sources', 'trending', 'newsletter']):
            if current_sec and (current_sec['paragraphs_en'] or current_sec['items_en']):
                sections.append(current_sec)
            current_sec = {
                'title_en': htitle,
                'title_fa': tr(htitle),
                'paragraphs_en': [],
                'paragraphs_fa': [],
                'items_en': [],
                'items_fa': []
            }
    
    # Check for formula figures/images
    if current_sec and (el.name == 'figure' or el.find('figure')):
        fig = el if el.name == 'figure' else el.find('figure')
        img = fig.find('img')
        if img:
            alt = (img.get('alt') or '').lower()
            src = (img.get('src') or img.get('data-src') or '').lower()
            if any(w in alt for w in ['formula', 'calculation', 'ratio displayed']) or any(w in src for w in ['formula', 'ratio']):
                if slug in FORMULA_IMAGE_DB:
                    f_en = FORMULA_IMAGE_DB[slug]['formula_en']
                    if f_en not in current_sec['paragraphs_en']:
                        current_sec['paragraphs_en'].append(f_en)
                        print(f"Detected formula image and converted to LaTeX: {f_en[:50]}...")

    ps = el.find_all('p') if el.name != 'p' else [el]
    for p in ps:
        ptxt = clean_element_html(p)
        if len(ptxt) > 20 and not any(skip in ptxt for skip in [
            'Investopedia /', 'Fact checked by', 'Get personalized', 'Our team of vetted', 'Subscribe to'
        ]):
            if current_sec:
                current_sec['paragraphs_en'].append(ptxt)

if current_sec and (current_sec['paragraphs_en'] or current_sec['items_en']):
    sections.append(current_sec)

for sec in sections:
    sec['paragraphs_fa'] = tr_chunks(sec['paragraphs_en'])

print(f"\nTotal sections for {slug}: {len(sections)}")
for s in sections:
    print('Section:', s['title_en'])
    for p in s['paragraphs_en']:
        if '$$' in p:
            print('  -> EN Math:', p[:80])
    for p in s['paragraphs_fa']:
        if '$$' in p:
            print('  -> FA Math:', p[:80])
    link_count = sum(p.count('internal-term-link') for p in s['paragraphs_en'])
    if link_count > 0:
        print(f'  -> Internal links in section: {link_count}')
