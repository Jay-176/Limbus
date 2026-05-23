import os
import asyncio
from tavily import TavilyClient
from crawl4ai import AsyncWebCrawler
import subprocess

# Initialize Tavily
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def ensure_playwright_installed():
    """Forces Playwright to install the browser (Kept for fallback purposes)."""
    print("[Limbus] Checking Playwright browser installation...")
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True)
        print("[Limbus] Playwright browser is ready.")
    except Exception as e:
        print(f"[ERROR] Failed to install Playwright browser: {e}")

def search_web(query: str, max_results: int = 3):
    """Searches the web using Tavily API with advanced depth for better context."""
    
    # We keep this just in case you ever want to switch back to deep scraping
    ensure_playwright_installed()
    
    print(f"\n[Limbus] Searching Tavily for: {query}")
    try:
        # ADDED search_depth="advanced" right here
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

async def read_website_async(url: str):
    """Asynchronously scrapes a website using crawl4ai (Currently bypassed for speed)."""
    print(f"[Limbus] Scraping URL: {url}")
    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(url=url)
            return result.markdown
    except Exception as e:
        print(f"[ERROR] Scraping Failed for {url}: {e}")
        return "Error: Could not scrape website data."
