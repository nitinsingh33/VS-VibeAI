#!/usr/bin/env python3
"""
VibeAI Start Script - Guaranteed to work
"""
import os
import sys

print("🚀 Starting VibeAI Pure Python Server")
print(f"🐍 Python: {sys.version}")
print(f"🌍 PORT: {os.environ.get('PORT', '8000')}")
print("🛡️ Zero dependencies - pure Python standard library")

# Import and run the server
try:
    os.system("python3 pure_http_server.py")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
