from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from agent import run_limbus_research

app = FastAPI()

# This defines what the frontend will send to us
class Query(BaseModel):
    prompt: str

# 1. When you open the browser, serve the HTML file
@app.get("/")
def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# 2. When you type in the chat box, run the AI Agent
@app.post("/api/research")
def research(query: Query):
    print(f"Incoming request from UI: {query.prompt}")
    result = run_limbus_research(query.prompt)
    return {"response": result}

if __name__ == "__main__":
    print("Starting Limbus Backend Server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)