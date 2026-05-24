import os
import asyncio
from tavily import TavilyClient

# Initialize Tavily
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def search_web(query: str, max_results: int = 3):
    """Searches the web using Tavily API with advanced depth for better context."""
    print(f"\n[Limbus] Searching Tavily for: {query}")
    try:
        # Advanced search depth enabled
        response = tavily_client.search(
            query=query, 
            max_results=max_results,
            search_depth="advanced" 
        )
        
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append({
                "title": result.get("title", ""),
                "href": result.get("url", ""),
                "body": result.get("content", "")
            })
            
        return formatted_results
            
    except Exception as e:
        print(f"[ERROR] Tavily Search Failed: {e}")
        return []

# We will leave the async scraper function here just in case you ever 
# upgrade to a paid server and want to use it again later.
async def read_website_async(url: str):
    """Asynchronously scrapes a website (Currently bypassed for speed)."""
    from crawl4ai import AsyncWebCrawler # Imported locally to save memory on boot
    print(f"[Limbus] Scraping URL: {url}")
    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(url=url)
            return result.markdown
    except Exception as e:
        print(f"[ERROR] Scraping Failed for {url}: {e}")
        return "Error: Could not scrape website data."
