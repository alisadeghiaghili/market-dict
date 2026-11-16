from scrape_and_enrich_pipeline import fetch_page_with_retry
from bs4 import BeautifulSoup

terms = ['accounting-equation', 'arr', 'breakevenanalysis', 'debtequityratio', 'ebit', 'sharperatio']

for slug in terms:
    url = f'https://www.investopedia.com/terms/{slug[0]}/{slug}.asp'
    html = fetch_page_with_retry(url)
    if not html:
        print(f'{slug}: FAILED TO FETCH')
        continue
    soup = BeautifulSoup(html, 'html.parser')
    print(f'=== {slug} ===')
    for h in soup.find_all(['h2', 'h3']):
        if any(w in h.get_text().lower() for w in ['formula', 'calculate', 'calculating']):
            print('  Heading:', h.get_text().strip())
            curr = h.find_next_sibling()
            count = 0
            while curr and curr.name not in ['h2', 'h3'] and count < 4:
                print('    Tag:', curr.name, 'Class:', curr.get('class'))
                for img in curr.find_all('img'):
                    print('      IMG alt:', img.get('alt'), 'src:', (img.get('src') or img.get('data-src') or '')[:80])
                for k in curr.find_all(class_='katex'):
                    print('      KaTeX found!')
                if curr.name in ['p', 'div', 'table']:
                    txt = curr.get_text(strip=True)[:100]
                    if txt:
                        print('      Text:', txt)
                curr = curr.find_next_sibling()
                count += 1
