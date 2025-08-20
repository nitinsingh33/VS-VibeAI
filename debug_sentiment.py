#!/usr/bin/env python3
import asyncio
import sys
from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def debug_specific_comment():
    classifier = AdvancedSentimentClassifier()
    
    text = "bhot achhi gadi hai"
    comment = {'text': text, 'author': 'test'}
    
    print(f"🔍 Debugging: '{text}'")
    print("="*50)
    
    # Let's debug step by step
    text_lower = text.lower()
    
    # Check language analysis
    language_info = classifier.detect_language_mix(text)
    print(f"Language info: {language_info}")
    
    # Check pattern analysis
    pattern_result = classifier.analyze_sentiment_patterns(text, language_info)
    print(f"Pattern analysis: {pattern_result}")
    
    # Check full classification
    result = await classifier.classify_comment_advanced(comment)
    print(f"Final result: {result}")
    
    # Let's manually check transliteration patterns
    print("\n🔍 Manual transliteration check:")
    transliteration_corrections = {
        'bhot achhi': 'positive',
        'bhot acchi': 'positive', 
        'bhot achha': 'positive',
        'bahut achhi': 'positive',
        'bahut acchi': 'positive',
        'bahut achha': 'positive',
        'dil se': 'positive',
        'bhot badhiya': 'positive',
        'bahut badhiya': 'positive'
    }
    
    for pattern, sentiment_type in transliteration_corrections.items():
        if pattern in text_lower:
            print(f"Found pattern: '{pattern}' -> {sentiment_type}")

if __name__ == "__main__":
    asyncio.run(debug_specific_comment())
