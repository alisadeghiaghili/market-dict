import json
import re

with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total terms: {len(data)}")

# 1. Terms with section titles containing formula/calculation/equation/ratio calculation
formula_section_terms = []
# 2. Terms with plain text equations (e.g. "X = Y / Z" or "X = Y - Z" or "X = Y + Z" or "X = ... x ...")
plain_eq_terms = []
# 3. Terms already having LaTeX $$
latex_terms = []

eq_pattern = re.compile(r'([A-Za-z\s()/-]{2,30}\s*=\s*[A-Za-z0-9\s()/*+-]{3,50})')

for item in data:
    term_en = item['term_en']
    slug = item.get('slug', '')
    sections = item.get('sections', [])
    
    has_latex = False
    has_formula_sec = False
    has_plain_eq = False
    
    sec_info = []
    for s in sections:
        t = s.get('title_en', '')
        t_l = t.lower()
        paras = s.get('paragraphs_en', [])
        
        has_l = any('$$' in p for p in paras)
        if has_l:
            has_latex = True
            
        if any(w in t_l for w in ['formula', 'how to calculate', 'calculating', 'how is', 'equation', 'computation']):
            has_formula_sec = True
            sec_info.append((t, has_l, len(paras)))
            
        for p in paras:
            if ' = ' in p and not '$$' in p:
                # check if looks like a formula e.g. "Ratio = A / B" or "Margin = (A - B) / A"
                if any(sym in p for sym in [' / ', ' + ', ' - ', ' * ', ' \times ']) and len(p) < 150:
                    has_plain_eq = True
                    
    if has_latex:
        latex_terms.append(term_en)
    if has_formula_sec and not has_latex:
        formula_section_terms.append((term_en, slug, sec_info))
    if has_plain_eq and not has_latex:
        plain_eq_terms.append((term_en, slug))

print(f"Terms with LaTeX formulas: {len(latex_terms)}")
print(f"Terms with formula section BUT NO LaTeX: {len(formula_section_terms)}")
print(f"Terms with plain text equations: {len(plain_eq_terms)}")

print("\n--- Sample terms with formula section but NO LaTeX: ---")
for t, s, info in formula_section_terms[:30]:
    print(f"{t} ({s}): {info}")
