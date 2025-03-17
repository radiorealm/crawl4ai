from duckduckgo_search import DDGS

def get_grant_urls():
    query = "grant OR grants OR funding"
    urls = [r["href"] for r in DDGS().text(query)]
    return urls

URL_TO_SCRAPE = get_grant_urls()
for url in URL_TO_SCRAPE:
    print(url)