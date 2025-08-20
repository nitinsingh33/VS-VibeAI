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
        {'text': 'bahut badhiya service', 'expected': 'positive'},    # Should be positive
        {'text': 'please dont buy', 'expected': 'negative'},          # Should be negative
    ]
    
    print("🧪 Testing Enhanced Sentiment Classifier")
    print("="*50)
    
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
            
            if 'reasons' in result and result['reasons']:
                print(f"   Reasons: {result['reasons'][:100]}...")
            
            print()
            
        except Exception as e:
            print(f"{i}. ❌ Error with \"{test_case['text']}\": {e}")
            print()

if __name__ == "__main__":
    asyncio.run(test_sentiment())
