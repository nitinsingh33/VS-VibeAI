"""
Test script for new VibeAI capabilities:
1. Temporal analysis
2. Brand strength analysis  
3. Conversation memory
"""

import asyncio
from services.enhanced_agent_service import EnhancedAgentService

async def demonstrate_new_features():
    print("🚀 VibeAI Enhanced Capabilities Demo")
    print("="*50)
    
    service = EnhancedAgentService()
    
    # Test 1: Temporal Analysis
    print("\n1️⃣ TEMPORAL ANALYSIS DEMO")
    print("-" * 30)
    
    queries = [
        "What was the sentiment for Ola Electric in August 2024?",
        "Show me Ather's performance in Q2 2025",
        "Compare sentiment trends for the last 6 months",
        "Brand strength analysis for Hero Vida in July 2025"
    ]
    
    for i, query in enumerate(queries):
        print(f"\n📊 Query {i+1}: {query}")
        response = await service.process_enhanced_query(query)
        
        print(f"⏰ Time Period Detected: {response.get('time_period', {}).get('description', 'None')}")
        print(f"📈 Temporal Analysis: {'✅ Yes' if response.get('temporal_analysis') else '❌ No'}")
        print(f"💬 Response: {response['response'][:200]}...")
        
        if response.get('export_files'):
            print(f"📁 Export Files: {list(response['export_files'].keys())}")
    
    # Test 2: Conversation Memory Demo
    print("\n\n2️⃣ CONVERSATION MEMORY DEMO")
    print("-" * 35)
    
    follow_up_queries = [
        "How does this compare to previous months?",
        "What about the same analysis for TVS iQube?",
        "Can you export this comparison data?",
        "What were we discussing about Ola Electric earlier?"
    ]
    
    for i, query in enumerate(follow_up_queries):
        print(f"\n🧠 Follow-up {i+1}: {query}")
        response = await service.process_enhanced_query(query)
        
        print(f"📚 Context Used: {'✅ Yes' if response.get('conversation_context_used') else '❌ No'}")
        print(f"🔗 Relevant History: {response.get('relevant_history_count', 0)} interactions")
        print(f"💬 Response: {response['response'][:200]}...")
    
    # Test 3: User Preferences & Memory Summary
    print("\n\n3️⃣ USER PREFERENCES & MEMORY ANALYSIS")
    print("-" * 45)
    
    memory_summary = service.get_conversation_summary()
    print("📊 Conversation Memory Summary:")
    print(memory_summary)
    
    preferences = service.get_user_preferences()
    print("\n🎯 User Preferences Analysis:")
    for key, value in preferences.items():
        print(f"  • {key}: {value}")
    
    # Test 4: Temporal Brand Analysis API
    print("\n\n4️⃣ ADVANCED TEMPORAL BRAND ANALYSIS")
    print("-" * 45)
    
    try:
        brand_analysis = await service.get_temporal_brand_analysis(
            'Ather', 
            ['July 2025', 'August 2024', 'Q2 2025']
        )
        
        print("📊 Multi-Period Brand Analysis for Ather:")
        for period, data in brand_analysis.items():
            if 'error' not in data:
                sentiment = data['sentiment_metrics']
                brand_strength = data['brand_strength']
                print(f"\n  📅 {period}:")
                print(f"    💬 Comments: {data['comment_count']}")
                print(f"    😊 Sentiment Score: {sentiment['sentiment_score']}/100")
                print(f"    💪 Brand Strength: {brand_strength['brand_strength_score']}/100")
    except Exception as e:
        print(f"⚠️ Advanced analysis error: {e}")
    
    # Test 5: Health Status with New Services
    print("\n\n5️⃣ SYSTEM HEALTH STATUS")
    print("-" * 30)
    
    health = service.get_health_status()
    print("🏥 Enhanced System Health:")
    for service_name, status in health.items():
        print(f"\n  🔧 {service_name}:")
        for key, value in status.items():
            print(f"    • {key}: {value}")
    
    print(f"\n\n✅ Demo completed! Total conversation interactions: {len(service.memory_service.conversation_history)}")

if __name__ == "__main__":
    asyncio.run(demonstrate_new_features())
