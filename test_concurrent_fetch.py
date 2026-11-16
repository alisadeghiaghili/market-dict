import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrape_and_enrich_pipeline import fetch_page_with_retry

urls = [
    'https://www.investopedia.com/terms/1/10-k.asp',
    'https://www.investopedia.com/terms/1/10-q.asp',
    'https://www.investopedia.com/terms/a/accounting-equation.asp',
    'https://www.investopedia.com/terms/a/arr.asp',
    'https://www.investopedia.com/terms/b/breakevenanalysis.asp',
    'https://www.investopedia.com/terms/s/sharperatio.asp',
    'https://www.investopedia.com/terms/c/capm.asp',
    'https://www.investopedia.com/terms/w/wacc.asp',
]

t0 = time.time()
results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futures = {ex.submit(fetch_page_with_retry, u): u for u in urls}
    for f in as_completed(futures):
        u = futures[f]
        try:
            h = f.result()
            results[u] = len(h) if h else 0
        except Exception as e:
            results[u] = str(e)

t1 = time.time()
print(f"Fetched {len(urls)} pages concurrently in {t1-t0:.2f}s:")
for u, r in results.items():
    print(f"  {u.split('/')[-1]}: {r} bytes")
