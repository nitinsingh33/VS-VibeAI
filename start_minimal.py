#!/usr/bin/env python3
"""
Minimal startup script for testing
"""
import os
import sys

def main():
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"🚀 Testing VibeAI on port {port}")
        print(f"🌍 Environment: {os.environ.get('NODE_ENV', 'production')}")
        print(f"🐍 Python: {sys.version}")
        
        import uvicorn
        from main_minimal import app
        
        print(f"✅ App imported successfully")
        print(f"🌐 Starting on 0.0.0.0:{port}")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
