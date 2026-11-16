import json

with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

enriched = [item for item in data if item.get('deep_enriched')]
print(f"Total enriched terms: {len(enriched)}")

with_links = []
without_links = []

for item in enriched:
    has_link = False
    for s in item.get('sections', []):
        for p in s.get('paragraphs_en', []):
            if 'href=' in p:
                has_link = True
                break
        if has_link:
            break
    if has_link:
        with_links.append(item['term_en'])
    else:
        without_links.append(item['term_en'])

print(f"Enriched WITH links: {len(with_links)}")
print(f"Enriched WITHOUT links: {len(without_links)}")
print("Sample with links:", with_links[:10])
print("Sample without links:", without_links[:10])
