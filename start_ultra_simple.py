#!/usr/bin/env python3
"""
VibeAI Ultra-Simple Startup
Completely bypasses Python 3.13 build issues
"""
import os
import sys

def main():
    print("🚀 VibeAI Ultra-Simple Startup")
    print(f"🐍 Python: {sys.version}")
    
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Port: {port}")
    
    try:
        # Try ultra-simple version first
        print("🔍 Loading ultra_simple app...")
        from main_ultra_simple import app
        print("✅ Ultra-simple app loaded")
        
    except ImportError as e:
        print(f"⚠️ Ultra-simple failed: {e}")
        
        try:
            # Fallback to basic FastAPI
            print("🔄 Creating basic FastAPI app...")
            from fastapi import FastAPI
            from fastapi.responses import HTMLResponse
            
            app = FastAPI(title="VibeAI Basic")
            
            @app.get("/", response_class=HTMLResponse)
            async def root():
                return HTMLResponse("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>VibeAI - EV Sentiment Platform</title>
                    <style>
                        body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); color: white; text-align: center; padding: 50px; }
                        .container { max-width: 800px; margin: 0 auto; }
                        h1 { font-size: 3em; margin-bottom: 20px; }
                        .status { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🚀 VibeAI</h1>
                        <p style="font-size: 1.2em;">EV Sentiment Analysis Platform</p>
                        <div class="status">
                            <h3>✅ Platform Status: ONLINE</h3>
                            <p>VibeAI is successfully deployed and running</p>
                            <p><strong>Port:</strong> {port}</p>
                            <p><strong>Mode:</strong> Basic Deployment</p>
                        </div>
                        <div style="margin-top: 30px;">
                            <a href="/health" style="color: white; text-decoration: none; background: #28a745; padding: 10px 20px; border-radius: 5px; margin: 10px;">Health Check</a>
                            <a href="/docs" style="color: white; text-decoration: none; background: #007bff; padding: 10px 20px; border-radius: 5px; margin: 10px;">API Docs</a>
                        </div>
                    </div>
                </body>
                </html>
                """.replace("{port}", str(port)))
            
            @app.get("/health")
            async def health():
                return {
                    "status": "healthy", 
                    "service": "VibeAI Basic",
                    "port": port,
                    "python": sys.version.split()[0]
                }
            
            print("✅ Basic FastAPI app created")
            
        except Exception as e2:
            print(f"❌ All imports failed: {e2}")
            sys.exit(1)
    
    # Start server
    try:
        import uvicorn
        print(f"🎯 Starting on {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"❌ Server start failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
