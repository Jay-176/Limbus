import asyncio
from duckduckgo_search import DDGS
from crawl4ai import AsyncWebCrawler

def search_web(query: str, max_results: int = 3):
    """Searches DuckDuckGo using the HTML backend to bypass Render IP blocks."""
    print(f"\n[Limbus] Searching web for: {query}")
    try:
        with DDGS() as ddgs:
            # backend="html" is the secret to bypassing datacenter restrictions
            results = list(ddgs.text(query, backend="html", max_results=max_results))
            
            if not results:
                print(f"[WARNING] DuckDuckGo returned empty for query: {query}")
            return results
            
    except Exception as e:
        print(f"[ERROR] DuckDuckGo Search Failed: {e}")
        return []

async def read_website_async(url: str):
    """Asynchronously scrapes a website using crawl4ai."""
    print(f"[Limbus] Scraping URL: {url}")
    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(url=url)
            return result.markdown
    except Exception as e:
        print(f"[ERROR] Scraping Failed for {url}: {e}")
        return "Error: Could not scrape website data."

def read_website(url: str):
    """Synchronous wrapper so your agent.py can call it easily without await."""
    try:
        return asyncio.run(read_website_async(url))
    except RuntimeError:
        # Handles cases where the FastAPI event loop is already running
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(read_website_async(url))
