#!/usr/bin/env python3
"""
Test script for Enhanced VibeAI Search Agent with YouTube Integration
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.enhanced_agent_service import EnhancedAgentService

async def test_enhanced_agent():
    """Test the enhanced agent with YouTube + Google Search + Gemini"""
    print("🧪 Testing Enhanced VibeAI Search Agent")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API keys are configured
    serper_key = os.getenv('SERPER_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    print(f"SERPER_API_KEY configured: {'✅' if serper_key else '❌'}")
    print(f"GEMINI_API_KEY configured: {'✅' if gemini_key else '❌'}")
    
    if not serper_key or not gemini_key:
        print("\n⚠️ Warning: Missing API keys. Some features may not work.")
    
    print("\n" + "=" * 50)
    
    try:
        # Initialize enhanced agent
        agent = EnhancedAgentService()
        
        # Test health status
        print("🏥 Checking enhanced service health...")
        health = agent.get_health_status()
        
        for service, status in health.items():
            if isinstance(status, dict):
                icon = "✅" if status.get('configured', False) else "❌"
                print(f"{icon} {service.replace('_', ' ').title()}: {status.get('status', 'unknown')}")
        
        # Test YouTube data loading
        print(f"\n📱 Testing YouTube data loading...")
        youtube_data = await agent.load_youtube_data()
        print(f"✅ YouTube data loaded for {len(youtube_data)} OEMs")
        
        # Show sample data
        for oem, comments in youtube_data.items():
            print(f"  • {oem}: {len(comments)} comments")
        
        # Test enhanced query processing
        test_queries = [
            "What are users saying about Ola Electric scooters?",
            "Compare TVS iQube vs Ather based on user feedback",
            "What are the charging infrastructure issues for electric scooters?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test Query {i}: '{query}'")
            print("-" * 40)
            
            try:
                result = await agent.process_enhanced_query(query, use_youtube_data=True)
                
                print(f"✅ Enhanced query processed successfully!")
                print(f"📏 Response length: {len(result['response'])} characters")
                print(f"📱 YouTube comments analyzed: {result['youtube_comments_analyzed']}")
                print(f"🔍 Search results used: {result['search_results_count']}")
                print(f"📚 Total sources: {len(result['sources'])}")
                print(f"⏱️ Processing time: {result['processing_time']:.2f}ms")
                
                # Show response preview
                preview = result['response'][:300] + "..." if len(result['response']) > 300 else result['response']
                print(f"\n📋 Response preview:")
                print(preview)
                
                # Show sources
                if result['sources']:
                    print(f"\n📚 Sources found:")
                    for j, source in enumerate(result['sources'][:3], 1):  # Show first 3 sources
                        print(f"  {j}. {source['title']}")
                        print(f"     🔗 {source['url']}")
                
                break  # Test only first query to save time
                
            except Exception as e:
                print(f"❌ Test query failed: {e}")
        
        # Test YouTube analytics
        print(f"\n📊 Testing YouTube analytics...")
        analytics = await agent.get_youtube_analytics()
        
        overall = analytics.get('overall', {})
        print(f"✅ Analytics generated:")
        print(f"  • Total OEMs: {overall.get('total_oems', 0)}")
        print(f"  • Total Comments: {overall.get('total_comments', 0)}")
        print(f"  • Data Period: {overall.get('data_collection_period', 'Unknown')}")
        
        print(f"\n🎉 All enhanced tests completed successfully!")
        print(f"\nNext steps:")
        print(f"1. Run 'python3 launch_streamlit.py' to start the Streamlit interface")
        print(f"2. Visit the web interface for interactive analysis")
        print(f"3. Try different queries about Indian electric two-wheelers")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Enhanced test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_enhanced_agent()
    
    if not success:
        print("\n❌ Tests failed. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
