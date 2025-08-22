#!/usr/bin/env python3
"""
Quick test for the petrol scooter irrelevant content detection
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_petrol_case():
    """Test the specific petrol scooter case"""
    classifier = AdvancedSentimentClassifier()
    
    test_text = "I like petrol scooty❤❤❤"
    
    # Create a mock comment dict
    comment = {
        'text': test_text,
        'likes': 0,
        'replies': 0,
        'shares': 0
    }
    
    # Run classification
    result = await classifier.classify_comment_advanced(comment)
    
    print("🧪 Testing Petrol Scooter Irrelevant Content Detection")
    print("=" * 60)
    print(f"Text: {test_text}")
    print(f"Predicted Sentiment: {result.get('sentiment', 'unknown')}")
    print(f"Confidence: {result.get('confidence', 0.0)}")
    
    # Get pattern analysis details
    pattern_analysis = result.get('pattern_analysis', {})
    print(f"\n🔍 Analysis Details:")
    print(f"   - Is Advice Request: {pattern_analysis.get('is_advice_request', False)}")
    print(f"   - Is Information Seeking: {pattern_analysis.get('is_information_seeking', False)}")
    print(f"   - Is Question: {pattern_analysis.get('is_question', False)}")
    print(f"   - Is Irrelevant (Petrol/Non-EV): {pattern_analysis.get('is_irrelevant', False)}")
    print(f"   - Is Neutral Request: {pattern_analysis.get('is_neutral_request', False)}")
    print(f"   - Positive Score: {pattern_analysis.get('positive_score', 0)}")
    print(f"   - Negative Score: {pattern_analysis.get('negative_score', 0)}")
    
    # Check emoji analysis
    emoji_analysis = result.get('emoji_analysis', {})
    print(f"\n💝 Emoji Analysis:")
    print(f"   - Has Emojis: {emoji_analysis.get('has_emojis', False)}")
    print(f"   - Emoji Count: {emoji_analysis.get('emoji_count', 0)}")
    print(f"   - Emoji Sentiment: {emoji_analysis.get('emoji_sentiment', 'neutral')}")
    print(f"   - Emoji Score: {emoji_analysis.get('emoji_sentiment_score', 0)}")
    
    if result.get('sentiment') == 'neutral':
        print(f"\n✅ SUCCESS: Correctly identified as NEUTRAL despite positive emojis and 'like'")
        print(f"   💡 Reason: Content about petrol scooters is irrelevant to EV sentiment analysis")
    else:
        print(f"\n❌ ISSUE: Should be neutral but got {result.get('sentiment')}")
    
    return result.get('sentiment') == 'neutral'

if __name__ == "__main__":
    success = asyncio.run(test_petrol_case())
    print("\n" + "=" * 60)
    if success:
        print("🎉 Test PASSED! Irrelevant content detection working correctly.")
    else:
        print("❌ Test FAILED! Need to adjust irrelevant content detection.")
