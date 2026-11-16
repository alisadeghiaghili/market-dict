import json

with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

item = data[460]
print("Term:", item['term_en'])
for s_idx, s in enumerate(item['sections']):
    print(f"Sec {s_idx}: {s['title_en']} (paras_en={len(s['paragraphs_en'])} paras_fa={len(s['paragraphs_fa'])})")
    for p_idx, p in enumerate(s['paragraphs_en']):
        print(f"   EN[{p_idx}]: {p[:120]}")
    for p_idx, p in enumerate(s['paragraphs_fa']):
        print(f"   FA[{p_idx}]: {p[:120]}")
