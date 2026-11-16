import json

with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

terms_with_real_math = []
terms_with_links = []
total_links_en = 0
total_links_fa = 0

for item in data:
    has_math = False
    has_links = False
    
    # check lead
    for fld in ['definition_en', 'bottom_line_en']:
        text = item.get(fld, '')
        if '$$' in text: has_math = True
        c = text.count('class="internal-term-link"')
        if c > 0:
            has_links = True
            total_links_en += c

    for fld in ['definition_fa', 'bottom_line_fa']:
        text = item.get(fld, '')
        if '$$' in text: has_math = True
        c = text.count('class="internal-term-link"')
        if c > 0:
            total_links_fa += c

    for s in item.get('sections', []):
        for p in s.get('paragraphs_en', []):
            if '$$' in p: has_math = True
            c = p.count('class="internal-term-link"')
            if c > 0:
                has_links = True
                total_links_en += c
        for p in s.get('paragraphs_fa', []):
            if '$$' in p: has_math = True
            c = p.count('class="internal-term-link"')
            if c > 0:
                total_links_fa += c

    if has_math:
        terms_with_real_math.append((item['term_en'], item['slug']))
    if has_links:
        terms_with_links.append((item['term_en'], item['slug']))

print(f"Total terms with KaTeX Math ($$): {len(terms_with_real_math)}")
print(f"Total terms with internal links: {len(terms_with_links)}")
print(f"Total English internal links: {total_links_en}")
print(f"Total Persian internal links: {total_links_fa}")

# Check Sharpe Ratio specifically
for item in data:
    if item['slug'] == 'sharperatio':
        print("\n--- Sharpe Ratio Check ---")
        for s in item.get('sections', []):
            if 'Formula' in s['title_en']:
                print(f"Section: {s['title_en']}")
                for p in s['paragraphs_en']:
                    if '$$' in p:
                        print("EN Formula:", p[:100])
                for p in s['paragraphs_fa']:
                    if '$$' in p:
                        print("FA Formula:", p[:100])
