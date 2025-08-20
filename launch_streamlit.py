#!/usr/bin/env python3
"""
Launcher script for the Enhanced VibeAI Search Agent with Streamlit
"""

import os
import sys
import subprocess

def main():
    """Launch the Streamlit application"""
    
    # Check if .env file exists
    env_file = ".env"
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        print("Please create a .env file with your API keys:")
        print("SERPER_API_KEY=your_serper_api_key_here")
        print("GEMINI_API_KEY=your_gemini_api_key_here")
        return
    
    # Check if required packages are installed
    try:
        import streamlit
        import pandas
        import plotly
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "plotly"])
    
    # Launch Streamlit app
    print("🚀 Launching VibeAI Search Agent with Streamlit...")
    print("📱 Analyzing Indian Electric Two-Wheeler Market")
    print("🌐 Opening browser at http://localhost:8501")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false"
    ])

if __name__ == "__main__":
    main()
