import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import run_limbus_research

# Initialize FastAPI App
app = FastAPI(title="Limbus AI API")

# Define the request data model
class ResearchRequest(BaseModel):
    prompt: str

# --- 1. FRONTEND ROUTE: Serve the UI ---
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serves the index.html file when someone visits the main URL."""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: index.html not found. Ensure it is in the root directory.</h1>"

# --- 2. BACKEND ROUTE: Connect to the Brain ---
@app.post("/api/research")
async def api_research(request: ResearchRequest):
    """Takes the prompt from the frontend, runs the AI agent, and returns the report."""
    try:
        # AWAIT the async agent function
        result = await run_limbus_research(request.prompt)
        return {"response": result}
    except Exception as e:
        print(f"[CRITICAL ERROR] API failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
