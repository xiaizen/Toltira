import preload_models
from agents.orchestrator import orchestrate
from utils.perf_tracker import tracker
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import uvicorn

# Create FastAPI app instance first
app = FastAPI(title="Bolt-v0 AI System")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda r, exc: JSONResponse(
    {"error": "Too many requests"}, status_code=429
))
app.add_middleware(SlowAPIMiddleware)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
@limiter.limit("5/minute")
async def process_query(request: Request, prompt: str = Form(...)):
    """Process user queries with rate limiting"""
    try:
        # Ensure prompt is not empty
        prompt = prompt.strip()
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Get AI response
        response = orchestrate(prompt)
        
        # Return formatted HTML response
        return HTMLResponse(f'<div class="message ai-message">🤖 AI: {response}</div>')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    return JSONResponse({"stats": tracker.stats()})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8001))  # Use 8001 as default
    uvicorn.run(app, host="0.0.0.0", port=port)