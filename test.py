#!/usr/bin/env python3
"""
Test script for VibeAI Search Agent
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.agent_service import AgentService

async def test_agent():
    """Test the agent with a simple query"""
    print("🧪 Testing VibeAI Search Agent")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API keys are configured
    serper_key = os.getenv('SERPER_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    print(f"SERPER_API_KEY configured: {'✅' if serper_key else '❌'}")
    print(f"GEMINI_API_KEY configured: {'✅' if gemini_key else '❌'}")
    
    if not serper_key or not gemini_key:
        print("\n⚠️ Warning: Missing API keys. Create a .env file with:")
        print("SERPER_API_KEY=your_serper_api_key_here")
        print("GEMINI_API_KEY=your_gemini_api_key_here")
        print("\nContinuing with test (may fail)...")
    
    print("\n" + "=" * 40)
    
    try:
        # Initialize agent
        agent = AgentService()
        
        # Test health status
        print("🏥 Checking service health...")
        health = agent.get_health_status()
        print(f"Search service: {'✅' if health['search_service']['configured'] else '❌'}")
        print(f"Gemini service: {'✅' if health['gemini_service']['configured'] else '❌'}")
        
        # Test query processing
        test_query = "What is artificial intelligence?"
        print(f"\n🔍 Testing query: '{test_query}'")
        
        result = await agent.process_query(test_query)
        
        print(f"\n✅ Test completed successfully!")
        print(f"Response length: {len(result['response'])} characters")
        print(f"Sources found: {len(result['sources'])}")
        print(f"Processing time: {result.get('processing_time', 0):.2f}ms")
        print(f"Fallback mode: {result.get('fallback', False)}")
        
        print("\n📝 Response preview:")
        print("-" * 40)
        preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
        print(preview)
        
        if result['sources']:
            print(f"\n📚 First source: {result['sources'][0]['title']}")
            print(f"URL: {result['sources'][0]['url']}")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True

async def main():
    """Main test function"""
    success = await test_agent()
    
    if success:
        print("\n🎉 All tests passed! The agent is working correctly.")
        print("\nNext steps:")
        print("1. Run 'python main.py' to start the web server")
        print("2. Run 'python cli.py' for interactive mode")
        print("3. Visit http://localhost:8000 for the web interface")
    else:
        print("\n❌ Tests failed. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
