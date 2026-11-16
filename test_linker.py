import json
import re

with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def normalize_fa(text):
    if not text: return ""
    text = text.replace('\u200c', ' ')
    text = text.replace('ي', 'ی').replace('ك', 'ک')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

en_terms = {}
fa_terms = {}

STOPWORDS_EN = {
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
    'capital', 'capital asset', 'model', 'asset pricing'
}

STOPWORDS_FA = {
    'نرخ', 'هزینه', 'سود', 'زیان', 'سهام', 'اوراق', 'بانک', 'پول', 'قیمت', 'ارزش', 'بازار',
    'رشد', 'وام', 'وجه', 'نقد', 'دارایی', 'بدهی', 'سرمایه', 'خرید', 'فروش', 'زمان', 'سال',
    'ریسک', 'صندوق', 'کالا', 'حساب', 'درآمد', 'شاخص', 'نسبت', 'بازده', 'واحد', 'سند', 'برگ',
    'طرح', 'کسر', 'اضافه', 'عادی', 'خالص', 'ناخالص', 'ثابت', 'متغیر', 'جاری', 'کوتاه', 'بلند',
    'مدل', 'قیمت گذاری'
}

for item in data:
    slug = item.get('slug', '').strip().lower()
    if not slug:
        continue
    
    t_en = item.get('term_en', '').strip()
    clean_en = re.sub(r'\s*\([^)]*\)', '', t_en).strip().lower()
    if len(clean_en) >= 5 and clean_en not in STOPWORDS_EN:
        en_terms[clean_en] = slug
    
    m_paren = re.search(r'\(([A-Z0-9-]{3,8})\)', t_en)
    if m_paren:
        acronym = m_paren.group(1).lower()
        if acronym not in STOPWORDS_EN and len(acronym) >= 3:
            en_terms[acronym] = slug
            
    t_fa = item.get('term_fa', '').strip()
    clean_fa = re.sub(r'\s*\([^)]*\)', '', t_fa).strip()
    norm_fa = normalize_fa(clean_fa)
    if len(norm_fa) >= 5 and norm_fa not in STOPWORDS_FA:
        fa_terms[norm_fa] = slug

sorted_en_keys = sorted(en_terms.keys(), key=lambda x: len(x), reverse=True)
sorted_fa_keys = sorted(fa_terms.keys(), key=lambda x: len(x), reverse=True)

test_en = "The Sharpe ratio was developed by William Sharpe as an extension of the capital asset pricing model to measure risk-adjusted return using standard deviation."
test_fa = "نسبت شارپ توسط ویلیام شارپ به عنوان توسعه‌ای از مدل قیمت گذاری دارایی های سرمایه ای برای سنجش بازده تعدیل شده با ریسک با استفاده از انحراف معیار ایجاد شد."

def linkify_text(text, is_persian=False, current_slug=None):
    if not text:
        return text
    
    placeholders = []
    def add_ph(s):
        placeholders.append(s)
        return f"___PH_{len(placeholders)-1}___"
    
    # 1. Protect $$...$$ math
    clean = re.sub(r'\$\$.*?\$\$', lambda m: add_ph(m.group(0)), text, flags=re.DOTALL)
    # 2. Protect existing <a> tags
    clean = re.sub(r'<a\b[^>]*>.*?</a>', lambda m: add_ph(m.group(0)), clean, flags=re.DOTALL | re.IGNORECASE)
    # 3. Protect other HTML tags
    clean = re.sub(r'<[^>]+>', lambda m: add_ph(m.group(0)), clean)
    
    keys = sorted_fa_keys if is_persian else sorted_en_keys
    term_dict = fa_terms if is_persian else en_terms
    
    linked_slugs = set()
    if current_slug:
        linked_slugs.add(current_slug)
        
    for k in keys:
        slug = term_dict[k]
        if slug in linked_slugs:
            continue
        
        if is_persian:
            # Flexible pattern matching with optional half-spaces
            pattern_str = r'(?<![^\s،؛«»()\[\]{}.])(' + re.escape(k).replace(r'\ ', r'[\s\u200c]+') + r')(?![^\s،؛«»()\[\]{}.])'
            pattern = re.compile(pattern_str, re.IGNORECASE)
        else:
            pattern = re.compile(r'\b(' + re.escape(k) + r')\b', re.IGNORECASE)
            
        m = pattern.search(clean)
        if m:
            matched_str = m.group(1)
            # Create tag and IMMEDIATELY protect it with a placeholder so nested words inside it are NOT matched!
            tag = f'<a href="#term/{slug}" class="internal-term-link" data-slug="{slug}">{matched_str}</a>'
            clean = pattern.sub(add_ph(tag), clean, count=1)
            linked_slugs.add(slug)
            if len(linked_slugs) >= 6:
                break
                
    # Restore all placeholders in reverse order
    for idx in range(len(placeholders) - 1, -1, -1):
        clean = clean.replace(f"___PH_{idx}___", placeholders[idx])
        
    return clean

print("\n--- English Test ---")
print("Before:", test_en)
print("After :", linkify_text(test_en, is_persian=False, current_slug='sharperatio'))

print("\n--- Persian Test ---")
print("Before:", test_fa)
print("After :", linkify_text(test_fa, is_persian=True, current_slug='sharperatio'))
