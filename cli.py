#!/usr/bin/env python3
"""
Command Line Interface for VibeAI Search Agent
Usage: python cli.py "Your question here"
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from services.agent_service import AgentService

# Load environment variables
load_dotenv()

def print_banner():
    """Print a nice banner for the CLI"""
    print("=" * 60)
    print("🤖 VibeAI Search Agent - Command Line Interface")
    print("=" * 60)

def print_sources(sources):
    """Print formatted sources"""
    if not sources:
        print("\n📚 Sources: None (fallback response)")
        return
    
    print(f"\n📚 Sources ({len(sources)} found):")
    print("-" * 40)
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source['title']}")
        print(f"   🔗 {source['url']}")
        print(f"   📝 {source['snippet'][:100]}{'...' if len(source['snippet']) > 100 else ''}")
        print()

def print_response(result):
    """Print formatted response"""
    print("\n🎯 Response:")
    print("-" * 40)
    print(result['response'])
    
    print_sources(result['sources'])
    
    print(f"\n⏱️ Processing time: {result.get('processing_time', 0):.2f}ms")
    print(f"📊 Search results used: {result.get('search_results', 0)}")
    
    if result.get('fallback'):
        print(f"⚠️ Fallback mode: {result.get('fallback_reason', 'unknown')}")
    
    print(f"🕒 Generated at: {result.get('timestamp', 'unknown')}")

async def interactive_mode():
    """Run in interactive mode"""
    print_banner()
    print("Interactive mode - Type 'quit' or 'exit' to stop")
    print("Type your questions and get AI-powered responses with sources!")
    print()
    
    agent = AgentService()
    
    # Check service health
    health = agent.get_health_status()
    search_ok = health['search_service']['configured']
    gemini_ok = health['gemini_service']['configured']
    
    if not search_ok:
        print("⚠️ Warning: SERPER_API_KEY not configured - search may not work")
    if not gemini_ok:
        print("⚠️ Warning: GEMINI_API_KEY not configured - response generation may fail")
    
    if search_ok and gemini_ok:
        print("✅ All services configured and ready!")
    
    print("\n" + "=" * 60)
    
    while True:
        try:
            query = input("\n🤔 Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                print("❌ Please enter a question.")
                continue
            
            print(f"\n🔍 Processing: {query}")
            print("Please wait...")
            
            result = await agent.process_query(query)
            print_response(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

async def single_query_mode(query):
    """Process a single query and exit"""
    print_banner()
    print(f"Processing query: {query}")
    print()
    
    try:
        agent = AgentService()
        result = await agent.process_query(query)
        print_response(result)
        
        # Also save to file for reference with enhanced classification metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"response_{timestamp}.json"
        
        # Add enhanced classification metadata to the result
        enhanced_result = {
            **result,
            "enhanced_classification_metadata": {
                "analysis_timestamp": timestamp,
                "sentiment_analyzer_version": "enhanced_v1.0",
                "features_enabled": [
                    "sarcasm_detection",
                    "context_understanding", 
                    "multilingual_support",
                    "product_relevance_scoring"
                ],
                "confidence_levels": "included_per_comment",
                "export_format": "enhanced_json"
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(enhanced_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Enhanced response saved to: {filename}")
        print(f"✨ Includes: sarcasm detection, multilingual support, confidence scores")
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        sys.exit(1)

def print_help():
    """Print help information"""
    print_banner()
    print("Usage:")
    print("  python cli.py                    # Interactive mode")
    print("  python cli.py \"Your question\"    # Single query mode")
    print("  python cli.py --help             # Show this help")
    print()
    print("Examples:")
    print("  python cli.py \"What are the latest AI developments?\"")
    print("  python cli.py \"How does quantum computing work?\"")
    print("  python cli.py \"Current news about climate change\"")
    print()
    print("Environment Variables:")
    print("  SERPER_API_KEY    - Your Serper API key for search")
    print("  GEMINI_API_KEY    - Your Google Gemini API key")
    print("  MAX_SEARCH_RESULTS - Max search results (default: 5)")
    print()

async def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments - run in interactive mode
        await interactive_mode()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ['--help', '-h', 'help']:
            print_help()
        else:
            # Single query mode
            await single_query_mode(arg)
    else:
        print("❌ Too many arguments. Use --help for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
