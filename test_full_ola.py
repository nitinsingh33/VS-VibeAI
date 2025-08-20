#!/usr/bin/env python3
"""
Full test script for Ola market share comment advanced classification
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_full_classification():
    print("🔍 Testing Advanced Sentiment Classification")
    print("=" * 60)
    
    # The comment to analyze
    test_comment = {
        'text': "Ola ka market share badh raha hai💯",
        'likes': 0,
        'replies': 0,
        'shares': 0
    }
    
    print(f"Comment: {test_comment['text']}")
    print("=" * 60)
    
    try:
        # Initialize classifier
        classifier = AdvancedSentimentClassifier()
        print("✅ Classifier initialized")
        
        # Perform advanced classification
        result = await classifier.classify_comment_advanced(test_comment)
        print("✅ Advanced classification completed")
        
        print("\n📊 ADVANCED CLASSIFICATION RESULTS:")
        print("-" * 40)
        
        # Basic sentiment
        print(f"Sentiment: {result.get('sentiment', 'unknown')}")
        print(f"Confidence: {result.get('confidence', 0)}")
        print(f"Category: {result.get('category', 'unknown')}")
        
        # Language analysis
        lang_info = result.get('language_analysis', {})
        print(f"\n🌐 Language Analysis:")
        print(f"  Primary Language: {lang_info.get('primary_language', 'unknown')}")
        print(f"  Is Mixed: {lang_info.get('is_mixed', False)}")
        print(f"  Languages: {lang_info.get('languages', {})}")
        
        # Emoji analysis
        emoji_info = result.get('emoji_analysis', {})
        print(f"\n😊 Emoji Analysis:")
        print(f"  Has Emojis: {emoji_info.get('has_emojis', False)}")
        print(f"  Emoji Count: {emoji_info.get('emoji_count', 0)}")
        print(f"  Emoji Sentiment: {emoji_info.get('emoji_sentiment', 'neutral')}")
        print(f"  Emoji Score: {emoji_info.get('emoji_sentiment_score', 0)}")
        print(f"  Emojis: {emoji_info.get('emojis', [])}")
        
        # Company mentions
        company_info = result.get('company_analysis', {})
        print(f"\n🏢 Company Analysis:")
        print(f"  Has Mentions: {company_info.get('has_mentions', False)}")
        print(f"  Primary Company: {company_info.get('primary_company', 'none')}")
        print(f"  All Mentions: {company_info.get('all_mentions', {})}")
        
        # Pattern analysis
        pattern_info = result.get('pattern_analysis', {})
        print(f"\n🔍 Pattern Analysis:")
        print(f"  Positive Score: {pattern_info.get('positive_score', 0)}")
        print(f"  Negative Score: {pattern_info.get('negative_score', 0)}")
        print(f"  Is Advice Request: {pattern_info.get('is_advice_request', False)}")
        print(f"  Sentiment Words: {pattern_info.get('sentiment_words', [])}")
        
        # Context detection
        context_info = result.get('context_analysis', {})
        print(f"\n📝 Context Analysis:")
        print(f"  Context: {context_info.get('context', 'unknown')}")
        print(f"  Is Question: {context_info.get('is_question', False)}")
        print(f"  Is Comparison: {context_info.get('is_comparison', False)}")
        
        # Final summary
        print(f"\n🎯 FINAL CLASSIFICATION:")
        print(f"  Overall Sentiment: {result.get('sentiment', 'unknown')}")
        print(f"  Confidence: {result.get('confidence', 0)}")
        print(f"  Category: {result.get('category', 'unknown')}")
        
        # Analysis summary for this specific comment
        print(f"\n💡 ANALYSIS SUMMARY:")
        print("  - Hindi-English code-switching: 'Ola ka market share badh raha hai'")
        print("  - Translation: 'Ola's market share is increasing'")
        print("  - 💯 emoji indicates strong approval/satisfaction")
        print("  - 'badh raha hai' (is increasing) = positive business sentiment")
        print("  - Ola Electric company specifically mentioned")
        print("  - Context: Business/market news update")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during classification: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_full_classification())
