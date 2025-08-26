#!/usr/bin/env python3
"""
VibeAI Complete Production Startup Script
Handles complete feature integration with graceful fallbacks
"""
import os
import sys

def main():
    """Start VibeAI Complete with all features"""
    print("🚀 Starting VibeAI Complete Production Platform...")
    print("✨ Features: Analytics • Premium • API • Real-time AI")
    
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Starting on port: {port}")
    
    # Import and run the complete app
    try:
        import uvicorn
        from main_complete import app
        
        print("🎯 All features loaded successfully!")
        print("📊 Analytics dashboard available at /analytics") 
        print("💎 Premium features available at /premium")
        print("📖 API docs available at /docs")
        
        uvicorn.run(
            app,
            host="0.0.0.0", 
            port=port,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔄 Falling back to minimal version...")
        
        # Fallback to minimal version
        try:
            from main_minimal import app
            uvicorn.run(app, host="0.0.0.0", port=port)
        except Exception as fallback_error:
            print(f"❌ Fallback failed: {fallback_error}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
