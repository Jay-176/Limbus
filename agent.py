import os
from google import genai
from google.genai import types
from tools import search_web, read_website_async

# Initialize the Gemini Client
client = genai.Client()

async def run_limbus_research(prompt: str) -> str:
    """The main orchestration loop for the Limbus AI Agent."""
    print(f"\n[Limbus Brain] Initialized research goal: '{prompt}'")

    # 1. Search the web using the Tavily tool
    search_results = search_web(prompt, max_results=3)

    if not search_results:
        return "I couldn't find any search results for that topic."

    compiled_research = ""

    # 2. Scrape the content from the discovered websites
    for i, result in enumerate(search_results):
        link = result.get('href', result.get('url', ''))
        title = result.get('title', 'Unknown Source')

        if not link:
            continue

        print(f"[Limbus Brain] Scraping source {i+1}: {title} ({link})")
        
        # AWAIT the asynchronous scraper
        page_content = await read_website_async(link)

        # Truncate to ~5000 characters so we don't overwhelm Gemini's context window
        if len(page_content) > 5000:
            page_content = page_content[:5000] + "... [Content Truncated]"

        # Append to our giant research document
        compiled_research += f"### Source: {title}\n**URL:** {link}\n**Content:**\n{page_content}\n\n---\n\n"

    # 3. Analyze the data and generate the final report
    print("[Limbus Brain] All data collected. Generating final report...")
    
    system_instruction = """You are Limbus, an advanced, autonomous AI research assistant. 
    Your job is to read the provided raw web scraping data and synthesize it into a clean, highly readable Markdown report answering the user's prompt.
    Do not mention the scraping process. Just provide the final answer.
    Always cite your sources at the bottom using inline links, like [Source Name](URL)."""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Content(role="user", parts=[
                    types.Part.from_text(f"User Request: {prompt}\n\nRaw Web Data:\n{compiled_research}")
                ])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
            )
        )
        print("[Limbus Brain] Report generated successfully.")
        return response.text
        
    except Exception as e:
        error_msg = f"[CRITICAL ERROR] Gemini API failed during generation: {e}"
        print(error_msg)
        return "I encountered an error while trying to write the final report. Please check the server logs."
