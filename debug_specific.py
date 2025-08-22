#!/usr/bin/env python3
import asyncio
from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def debug_specific():
    classifier = AdvancedSentimentClassifier()
    
    text = "dil se recommend karta hun"
    comment = {'text': text, 'author': 'test'}
    
    print(f"🔍 Debugging: '{text}'")
    print("="*50)
    
    # Get language info
    language_info = classifier.detect_language_mix(text)
    print(f"Language info: {language_info}")
    
    # Get pattern analysis
    pattern_result = classifier.analyze_sentiment_patterns(text, language_info)
    print(f"Pattern analysis:")
    print(f"  Sentiment: {pattern_result['sentiment']}")
    print(f"  Confidence: {pattern_result['confidence']}")
    print(f"  Positive score: {pattern_result['positive_score']}")
    print(f"  Negative score: {pattern_result['negative_score']}")
    print(f"  Is advice request: {pattern_result['is_advice_request']}")
    print(f"  Has strong negative: {pattern_result['has_strong_negative']}")
    print(f"  Sentiment words: {pattern_result['sentiment_words']}")
    
    # Full classification
    print("\nFull classification:")
    result = await classifier.classify_comment_advanced(comment)
    print(f"  Final sentiment: {result['sentiment']}")
    print(f"  Final confidence: {result['confidence']}")

if __name__ == "__main__":
    asyncio.run(debug_specific())
