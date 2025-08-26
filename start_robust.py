#!/usr/bin/env python3
"""
VibeAI Robust Production Startup
Handles missing dependencies and files gracefully
"""
import os
import sys

def main():
    print("🚀 Starting VibeAI Platform...")
    
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Port: {port}")
    
    try:
        # Try to import uvicorn first
        import uvicorn
        print("✅ uvicorn available")
        
        # Try main_complete first
        try:
            from main_complete import app
            print("✅ main_complete.py loaded successfully")
            print("🎯 Starting complete VibeAI platform with all features")
            
        except ImportError as e:
            print(f"⚠️ main_complete import failed: {e}")
            print("🔄 Trying main_minimal...")
            
            try:
                from main_minimal import app
                print("✅ main_minimal.py loaded as fallback")
                
            except ImportError as e2:
                print(f"❌ main_minimal import failed: {e2}")
                
                # Last resort - create minimal app
                print("🆘 Creating emergency minimal app...")
                from fastapi import FastAPI
                app = FastAPI(title="VibeAI Emergency Mode")
                
                @app.get("/")
                async def root():
                    return {"message": "VibeAI Emergency Mode", "status": "Limited functionality available"}
                    
                @app.get("/health")
                async def health():
                    return {"status": "emergency_mode", "message": "VibeAI running in emergency mode"}
        
        # Start the server
        print(f"🎯 Starting server on 0.0.0.0:{port}")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Critical error - uvicorn not available: {e}")
        print("🆘 Cannot start server")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
