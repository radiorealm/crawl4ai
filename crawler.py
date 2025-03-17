import asyncio
import json
from typing import List

from crawl4ai import *
from pydantic import BaseModel

API_KEY = "put your api key here"

class GrantInfo(BaseModel):
    site: str
    name: str
    country: List[str]
    grantor: str
    facts: List[str]


#TOD: def to automatically find related urls
#Testing duckduckgo_search in DDGS file (ddgs doesnt need NOT FREE serp_api_key)
URL_TO_SCRAPE = "https://track2training.com/2023/12/01/top-10-research-grants-for-international-scholars/"

INSTRUCTION_TO_LLM = """
Extract all grants listed on the page as objects with the following fields:
- 'site': the source URL
- 'name': the name of the grant
- 'country': a list of countries where the grant is available. global if worldwide or not mentioned if not mentioned
- 'grantor': the name of the organization or person who grants the grant
- 'facts': a list of various details about the grant, like for who, requirements, what it gives and so on.
"""

async def main():
    llm_strategy = LLMExtractionStrategy(
        provider="groq/llama3-8b-8192",
        api_token=API_KEY,
        schema=GrantInfo.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION_TO_LLM,
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",
        extra_args={"temperature": 0.0, "max_tokens": 800},
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        process_iframes=False,
        remove_overlay_elements=True,
        exclude_external_links=True,
    )

    browser_cfg = BrowserConfig(headless=True, verbose=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url=URL_TO_SCRAPE, config=crawl_config)

        if result.success:
            data = json.loads(result.extracted_content)
            for d in data:
                print(d)
            llm_strategy.show_usage()
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())