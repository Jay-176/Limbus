import os
from google import genai
from google.genai import types
from tools import search_web

# Initialize the Gemini Client
client = genai.Client()

async def run_limbus_research(prompt: str) -> str:
    """The main orchestration loop for the Limbus AI Agent."""
    print(f"\n[Limbus Brain] Initialized research goal: '{prompt}'")

    # 1. Search the web using the Tavily tool (now using advanced depth)
    search_results = search_web(prompt, max_results=3)

    if not search_results:
        return "I couldn't find any search results for that topic."

    compiled_research = ""

    # 2. Process the text data Tavily extracted
    for i, result in enumerate(search_results):
        link = result.get('href', result.get('url', ''))
        title = result.get('title', 'Unknown Source')
        
        body_text = result.get('body', 'No content extracted.')

        if not link:
            continue

        print(f"[Limbus Brain] Processing source {i+1}: {title}")

        compiled_research += f"### Source: {title}\n**URL:** {link}\n**Content:**\n{body_text}\n\n---\n\n"

    print("[Limbus Brain] All data collected. Generating final report...")
    
    # UPDATED: We explicitly tell Limbus to write a detailed, multi-paragraph report
    system_instruction = """You are Limbus, an advanced, autonomous AI research assistant. 
    Write a highly detailed, comprehensive, and expansive Markdown report answering the user's prompt based on the provided web data. 
    Ensure the report spans multiple paragraphs, breaks down complex topics, provides deep context, and connects ideas logically.
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
                temperature=0.6, # UPDATED: Raised from 0.3 for more expansive writing
            )
        )
        print("[Limbus Brain] Report generated successfully.")
        return response.text
        
    except Exception as e:
        error_msg = f"[CRITICAL ERROR] Gemini API failed during generation: {e}"
        print(error_msg)
        return "I encountered an error while trying to write the final report. Please check the server logs."
