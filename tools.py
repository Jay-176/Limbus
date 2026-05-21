from duckduckgo_search import DDGS
import asyncio
from crawl4ai import AsyncWebCrawler

def search_web(query, max_results=5):
    """Searches DuckDuckGo and returns a list of URLs and snippets."""
    print(f"Searching the web for: '{query}'")
    results = []
    try:
        # Using the updated DDGS client
        search_results = list(DDGS().text(query, max_results=max_results))
        
        if not search_results:
            print("DuckDuckGo returned no results. It might be rate-limiting.")
            
        for r in search_results:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            })
        return results
    except Exception as e:
        print(f"Error searching web: {e}")
        return []

async def scrape_website(url):
    """Visits a URL and extracts clean Markdown text using Crawl4AI."""
    print(f"Reading website: {url}")
    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(url=url)
            return result.markdown
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return "Could not read this website."

def read_website(url):
    """Helper function to run the async scraper in our sync code."""
    return asyncio.run(scrape_website(url))

if __name__ == "__main__":
    # Test block
    test_query = "What is an AI Agent?"
    print("Testing Search...")
    search_data = search_web(test_query, max_results=2)
    print("Search Results:", search_data)
    
    if search_data:
        print("\nSearch successful! Testing Scraper on the first result...")
        first_url = search_data[0]['url']
        page_text = read_website(first_url)
        print(f"\nExtracted Text (First 500 chars):\n{page_text[:500]}...")
    else:
        print("\nSearch failed to find links. Skipping scraper test.")
