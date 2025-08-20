#!/usr/bin/env python3
"""
Example usage of the VibeAI Search Agent
This file demonstrates how to use the agent programmatically
"""

import asyncio
import os
from services.agent_service import AgentService

async def example_usage():
    """Example of how to use the VibeAI Search Agent"""
    
    # Example 1: Basic usage
    print("🤖 VibeAI Search Agent - Example Usage")
    print("=" * 50)
    
    # Check if API keys are configured
    if not os.getenv('SERPER_API_KEY') or not os.getenv('GEMINI_API_KEY'):
        print("⚠️ Please configure your API keys in a .env file:")
        print("SERPER_API_KEY=your_serper_api_key_here")
        print("GEMINI_API_KEY=your_gemini_api_key_here")
        return
    
    # Initialize the agent
    agent = AgentService()
    
    # Example queries to test
    example_queries = [
        "What are the latest developments in artificial intelligence?",
        "How does renewable energy work?",
        "What is the current state of space exploration?",
        "Explain quantum computing in simple terms"
    ]
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n📝 Example {i}: {query}")
        print("-" * 50)
        
        try:
            result = await agent.process_query(query, max_results=3)
            
            print(f"✅ Response generated successfully!")
            print(f"📏 Response length: {len(result['response'])} characters")
            print(f"📚 Sources found: {len(result['sources'])}")
            print(f"⏱️ Processing time: {result.get('processing_time', 0):.2f}ms")
            
            # Show response preview
            preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
            print(f"\n📋 Response preview:\n{preview}")
            
            # Show sources
            if result['sources']:
                print(f"\n📚 Sources:")
                for j, source in enumerate(result['sources'][:2], 1):  # Show first 2 sources
                    print(f"  {j}. {source['title']}")
                    print(f"     🔗 {source['url']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(example_usage())
