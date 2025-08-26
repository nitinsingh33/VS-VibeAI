#!/usr/bin/env python3
"""
VibeAI Ultra-Robust Production Startup
Handles Python 3.13, missing dependencies, and all edge cases
"""
import os
import sys

def main():
    print("🚀 Starting VibeAI Platform (Ultra-Robust Mode)...")
    print(f"🐍 Python version: {sys.version}")
    
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Port: {port}")
    
    # Set environment variables for better compatibility
    os.environ.setdefault("PYTHONPATH", ".")
    
    try:
        # Try to import uvicorn first
        print("🔍 Checking uvicorn availability...")
        import uvicorn
        print("✅ uvicorn available")
        
        # Try main_complete first, then simple, then minimal
        try:
            print("🔍 Loading main_complete.py...")
            from main_complete import app
            print("✅ main_complete.py loaded successfully")
            print("🎯 Starting complete VibeAI platform with all features")
            
        except ImportError as e:
            print(f"⚠️ main_complete import failed: {e}")
            print("🔄 Trying main_simple...")
            
            try:
                from main_simple import app
                print("✅ main_simple.py loaded successfully")
                print("🎯 Starting simple VibeAI platform")
                
            except ImportError as e2:
                print(f"⚠️ main_simple import failed: {e2}")
                print("🔄 Trying main_minimal...")
                
                try:
                    from main_minimal import app
                    print("✅ main_minimal.py loaded as fallback")
                    
                except ImportError as e3:
                    print(f"⚠️ main_minimal import failed: {e3}")
                    print("🆘 Creating emergency minimal app...")
                
                # Create ultra-minimal emergency app
                from fastapi import FastAPI
                from fastapi.responses import JSONResponse, HTMLResponse
                
                app = FastAPI(title="VibeAI Emergency Mode", version="1.0.0")
                
                @app.get("/", response_class=HTMLResponse)
                async def root():
                    return HTMLResponse("""
                    <!DOCTYPE html>
                    <html>
                    <head><title>VibeAI Emergency Mode</title></head>
                    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
                        <h1>🚀 VibeAI Emergency Mode</h1>
                        <p>Service is running in emergency mode</p>
                        <p>Limited functionality available</p>
                        <a href="/health">Health Check</a> | <a href="/docs">API Docs</a>
                    </body>
                    </html>
                    """)
                    
                @app.get("/health")
                async def health():
                    return {"status": "emergency_mode", "message": "VibeAI running in emergency mode", "port": port}
                    
                @app.get("/api/status")
                async def status():
                    return {"service": "VibeAI", "mode": "emergency", "python_version": sys.version}
        
        # Start the server with robust error handling
        print(f"🎯 Starting server on 0.0.0.0:{port}")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        print(f"❌ Critical error - uvicorn not available: {e}")
        print("🆘 Cannot start server - missing core dependencies")
        
        # Last resort - basic HTTP server
        try:
            print("🔄 Attempting basic HTTP server fallback...")
            from http.server import HTTPServer, BaseHTTPRequestHandler
            
            class VibeAIHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<h1>VibeAI Basic Mode</h1><p>Service is running</p>')
            
            server = HTTPServer(('0.0.0.0', port), VibeAIHandler)
            print(f"🎯 Basic HTTP server started on port {port}")
            server.serve_forever()
            
        except Exception as fallback_error:
            print(f"❌ All fallbacks failed: {fallback_error}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
