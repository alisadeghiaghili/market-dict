from scrape_and_enrich_pipeline import tr
text = 'The <a href="#term/capm" class="internal-term-link" data-slug="capm">capital asset pricing model</a> is used to calculate expected return.'
res = tr(text)
print('Input: ', text)
print('Output:', res)
