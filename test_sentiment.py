#!/usr/bin/env python3
import asyncio
import sys
from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_sentiment():
    classifier = AdvancedSentimentClassifier()
    
    test_cases = [
        {'text': 'froud company hai', 'expected': 'negative'},        # Should be negative (typo)
        {'text': 'bhot achhi gadi hai', 'expected': 'positive'},      # Should be positive (informal Hindi)
        {'text': 'company frawd kar rahi', 'expected': 'negative'},   # Should be negative (typo)
        {'text': 'dil se recommend karta hun', 'expected': 'positive'}, # Should be positive (heart recommend)
        {'text': 'dil se mana karta hun', 'expected': 'negative'},    # Should be negative (heart refusal)
        {'text': 'dil se mat lo yaar', 'expected': 'negative'},       # Should be negative (heartfelt warning)
        {'text': 'bahut badhiya service', 'expected': 'positive'},    # Should be positive
        {'text': 'please dont buy', 'expected': 'negative'},          # Should be negative
        {'text': 'dont recommend this brand', 'expected': 'negative'}, # Should be negative (negative recommend)
        {'text': 'great service but problem hai', 'expected': 'negative'}, # Should be negative (sarcastic)
        {'text': 'achha nahi hai quality', 'expected': 'negative'},   # Should be negative (good negated)
    ]
    
    print("🧪 Testing Enhanced Contextual Sentiment Classifier")
    print("="*60)
    
    for i, test_case in enumerate(test_cases, 1):
        comment = {'text': test_case['text'], 'author': 'test'}
        
        try:
            result = await classifier.classify_comment_advanced(comment)
            sentiment = result['sentiment']
            confidence = result['confidence']
            
            status = "✅" if sentiment == test_case['expected'] else "❌"
            
            print(f"{i}. {status} Text: \"{test_case['text']}\"")
            print(f"   Expected: {test_case['expected']}")
            print(f"   Got: {sentiment} (confidence: {confidence:.2f})")
            
            if 'pattern_analysis' in result:
                pattern_info = result['pattern_analysis']
                print(f"   Scores: +{pattern_info.get('positive_score', 0)} / -{pattern_info.get('negative_score', 0)}")
            
            print()
            
        except Exception as e:
            print(f"{i}. ❌ Error with \"{test_case['text']}\": {e}")
            print()

if __name__ == "__main__":
    asyncio.run(test_sentiment())
