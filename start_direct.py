#!/usr/bin/env python3
"""
Direct uvicorn startup - simplest possible solution
"""
import os
import subprocess
import sys

def main():
    port = os.environ.get("PORT", "8000")
    print(f"🚀 Direct uvicorn start on port {port}")
    
    # Direct uvicorn command
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "main_minimal:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--log-level", "info"
    ]
    
    print(f"📋 Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
