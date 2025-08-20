#!/usr/bin/env python3
"""
Test script to classify the TVS vs Bajaj comparison comment
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_tvs_bajaj_comment():
    """Test the TVS vs Bajaj comparison comment sentiment classification"""
    
    # Initialize the advanced classifier
    classifier = AdvancedSentimentClassifier()
    
    # The comment to analyze
    test_comment = {
        'text': "📌📌📌📌📌📌📌📌📌📌📌\n📌📌📌📌📌📌📌📌📌📌📌\nBroo TVS iqube ST or Bajaj chetak premium 2024   which one is best your opinion plzzz rply",
        'likes': 0,
        'replies': 0,
        'shares': 0
    }
    
    print("🔍 Testing Advanced Sentiment Classification")
    print("=" * 60)
    print(f"Comment: {test_comment['text']}")
    print("=" * 60)
    
    try:
        # Perform advanced classification
        result = await classifier.classify_comment_advanced(test_comment)
        
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
        
        # Company mentions
        company_info = result.get('company_analysis', {})
        print(f"\n🏢 Company Analysis:")
        print(f"  Has Mentions: {company_info.get('has_mentions', False)}")
        print(f"  Primary Company: {company_info.get('primary_company', 'none')}")
        print(f"  Competitor Mentions: {company_info.get('competitor_mentions', [])}")
        print(f"  All Mentions: {company_info.get('all_mentions', {})}")
        
        # Pattern analysis
        pattern_info = result.get('pattern_analysis', {})
        print(f"\n🔍 Pattern Analysis:")
        print(f"  Positive Score: {pattern_info.get('positive_score', 0)}")
        print(f"  Negative Score: {pattern_info.get('negative_score', 0)}")
        print(f"  Is Advice Request: {pattern_info.get('is_advice_request', False)}")
        print(f"  Sentiment Words: {pattern_info.get('sentiment_words', [])}")
        
        # Sarcasm detection
        sarcasm_info = result.get('sarcasm_analysis', {})
        print(f"\n😏 Sarcasm Analysis:")
        print(f"  Sarcasm Detected: {sarcasm_info.get('sarcasm_detected', False)}")
        print(f"  Sarcasm Score: {sarcasm_info.get('sarcasm_score', 0)}")
        print(f"  Sarcasm Indicators: {sarcasm_info.get('sarcasm_indicators', [])}")
        
        # Context detection
        context_info = result.get('context_analysis', {})
        print(f"\n📝 Context Analysis:")
        print(f"  Context: {context_info.get('context', 'unknown')}")
        print(f"  Is Question: {context_info.get('is_question', False)}")
        print(f"  Is Comparison: {context_info.get('is_comparison', False)}")
        
        # Product relevance
        relevance_info = result.get('relevance_analysis', {})
        print(f"\n🎯 Relevance Analysis:")
        print(f"  Product Relevance: {relevance_info.get('product_relevance_score', 0)}")
        print(f"  EV Specific: {relevance_info.get('is_ev_specific', False)}")
        
        # Final classification
        print(f"\n🎯 FINAL CLASSIFICATION:")
        print(f"  Overall Sentiment: {result.get('sentiment', 'unknown')}")
        print(f"  Confidence: {result.get('confidence', 0)}")
        print(f"  Category: {result.get('category', 'unknown')}")
        print(f"  Context: {result.get('context_analysis', {}).get('context', 'unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during classification: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_tvs_bajaj_comment())
