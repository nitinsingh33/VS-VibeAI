#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting VibeAI on port {port}")
    print(f"🌍 Environment: {os.environ.get('NODE_ENV', 'production')}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=1,
        log_level="info",
        access_log=True
    )
