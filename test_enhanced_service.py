#!/usr/bin/env python3
"""
Test script to identify the exact error in enhanced sentiment analysis
"""

import asyncio
import sys
import traceback

async def test_enhanced_service():
    try:
        from services.enhanced_agent_service import EnhancedAgentService
        
        print("🧪 Testing enhanced agent service...")
        service = EnhancedAgentService()
        
        # Test with minimal query
        query = "Show me sarcastic comments about Ola Electric"
        print(f"Query: {query}")
        
        result = await service.process_enhanced_query(
            query=query,
            use_youtube_data=True,
            max_search_results=1
        )
        
        print("✅ Test completed successfully!")
        print(f"Response length: {len(result.get('response', ''))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n=== FULL TRACEBACK ===")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_enhanced_service())
    sys.exit(0 if success else 1)
