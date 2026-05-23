import os
from google import genai
from google.genai import types
from tools import search_web

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

    # 2. Process the text data Tavily ALREADY extracted
    for i, result in enumerate(search_results):
        link = result.get('href', result.get('url', ''))
        title = result.get('title', 'Unknown Source')
        
        # Grab the pre-scraped content provided by Tavily!
        body_text = result.get('body', 'No content extracted.')

        if not link:
            continue

        print(f"[Limbus Brain] Processing source {i+1}: {title}")

        # Append to our giant research document instantly
        compiled_research += f"### Source: {title}\n**URL:** {link}\n**Content:**\n{body_text}\n\n---\n\n"

    # 3. Analyze the data and generate the final report
    print("[Limbus Brain] All data collected. Generating final report...")
    
    system_instruction = """You are Limbus, an advanced, autonomous AI research assistant. 
    Your job is to read the provided web search data and synthesize it into a clean, highly readable Markdown report answering the user's prompt.
    Always cite your sources at the bottom using inline links, like [Source Name](URL)."""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Content(role="user", parts=[
                    types.Part.from_text(text=f"User Request: {prompt}\n\nRaw Web Data:\n{compiled_research}")
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
