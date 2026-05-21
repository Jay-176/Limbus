import os
import time
from datetime import datetime
from google import genai
from dotenv import load_dotenv
from tools import search_web, read_website

# 1. Load the API key from your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key not found! Check your .env file.")
    exit()

# 2. Configure the AI Engine using the NEW SDK
client = genai.Client(api_key=api_key)

def run_limbus_research(topic):
    """The core logic loop of the Limbus Agent."""
    print(f"\nLimbus initialized. Goal: Research '{topic}'")
    
    # Step 1: Search the web
    search_results = search_web(topic, max_results=2)
    if not search_results:
        return "I couldn't find any search results for that topic."
        
    # Step 2: Read the websites it found
    compiled_knowledge = ""
    for idx, result in enumerate(search_results):
        url = result['url']
        print(f"Absorbing data from source {idx + 1}: {url}...")
        
        page_text = read_website(url)
        
        # Grab up to 60,000 characters per page to feed to the AI
        compiled_knowledge += f"\n\n--- Source: {url} ---\n{page_text[:60000]}" 
        
    # Step 3: Synthesize and Write the Report
    print("Processing data and drafting final report...")
    
    # Grab the actual current date from your computer for temporal grounding
    today_date = datetime.now().strftime("%B %d, %Y")
    
    system_prompt = f"""
    You are Limbus, an elite, autonomous research agent.
    Today's date is {today_date}. You must use this as the current date for all context.
    
    Your current assignment is to research: "{topic}"
    
    Below is the live data you just scraped from the internet:
    {compiled_knowledge}
    
    Your task:
    1. Read the data carefully.
    2. Write a highly detailed, professional report answering the user's prompt.
    3. Use clean Markdown formatting (Headings, bullet points, bold text).
    4. If the data mentions specific facts or numbers, include them.
    5. Always cite your sources at the bottom using the URLs provided.
    """
    
    # --- Exponential Backoff & Retry Logic ---
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=system_prompt
            )
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            print(f"API Error on attempt {attempt + 1}: {error_msg}")
            
            # If it's a 503 error, or any other temporary glitch, we wait and retry
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt  # Waits 1s, then 2s, then 4s
                print(f"Server busy. Waiting {sleep_time} seconds before retrying...")
                time.sleep(sleep_time)
            else:
                # If it fails all 3 times, then we finally tell the user
                return f" **AI Network Error:** The servers are currently experiencing extreme traffic. Limbus attempted to connect {max_retries} times but was rejected. Please try your search again in a few moments."