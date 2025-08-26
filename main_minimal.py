#!/usr/bin/env python3
"""
Minimal FastAPI app for testing Render deployment
"""
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="VibeAI Test", version="1.0.0")

@app.get("/")
async def root():
    return HTMLResponse("""
    <h1>🚀 VibeAI is Live!</h1>
    <p>Port: {}</p>
    <p>Environment: {}</p>
    <a href="/health">Health Check</a>
    """.format(
        os.environ.get("PORT", "8000"),
        os.environ.get("NODE_ENV", "production")
    ))

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "port": os.environ.get("PORT", "8000"),
        "host": "0.0.0.0"
    }

@app.get("/api/health")
async def api_health():
    return {
        "status": "healthy",
        "port": os.environ.get("PORT", "8000"),
        "host": "0.0.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
