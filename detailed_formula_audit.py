import json
import re

with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total terms: {len(data)}")

issues = []

for item in data:
    term_en = item['term_en']
    slug = item.get('slug', '')
    sections = item.get('sections', [])
    
    for s_idx, s in enumerate(sections):
        title = s.get('title_en', '')
        title_l = title.lower()
        paras_en = s.get('paragraphs_en', [])
        paras_fa = s.get('paragraphs_fa', [])
        
        # Check if title indicates a formula
        is_formula_heading = any(k in title_l for k in [
            'formula', 'how to calculate', 'calculating', 'equation', 'how is'
        ]) and any(k in title_l for k in ['formula', 'calculate', 'calculating', 'equation'])
        
        has_proper_latex = any('$$' in p for p in paras_en)
        
        # Check for unformatted math or broken math or plain text formula
        has_unformatted_math = False
        for p in paras_en:
            if '\\text{' in p and '$$' not in p:
                has_unformatted_math = True
            elif ' = ' in p and any(sym in p for sym in [' / ', ' + ', ' - ', ' * ']) and len(p) < 120 and '$$' not in p:
                has_unformatted_math = True
                
        if is_formula_heading and not has_proper_latex:
            issues.append({
                'term_en': term_en,
                'slug': slug,
                'section_idx': s_idx,
                'title': title,
                'num_paras': len(paras_en),
                'has_unformatted_math': has_unformatted_math,
                'sample_paras': paras_en[:3]
            })

print(f"Total formula sections needing attention: {len(issues)}")
for iss in issues:
    print(f"\n--- {iss['term_en']} ({iss['slug']}) | Sec: {iss['title']} (unformatted={iss['has_unformatted_math']}) ---")
    for p in iss['sample_paras']:
        print("  *", p[:140])
