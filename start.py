#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""
import os
import sys
import traceback

def main():
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"🚀 Starting VibeAI on port {port}")
        print(f"🌍 Environment: {os.environ.get('NODE_ENV', 'production')}")
        print(f"🐍 Python version: {sys.version}")
        print(f"📂 Working directory: {os.getcwd()}")
        
        # Import uvicorn after printing initial info
        import uvicorn
        
        # Try to import the main app to check for import errors
        print("🔍 Importing main application...")
        from main import app
        print("✅ Main application imported successfully")
        
        print(f"🌐 Starting server on 0.0.0.0:{port}")
        
        uvicorn.run(
            app,  # Use the imported app directly
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print(f"📜 Full traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
