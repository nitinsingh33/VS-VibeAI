#!/usr/bin/env python3
"""
Test script for the specific user comment classification issue
"""

import asyncio
import sys
import os
sys.path.append('/Users/amanmathur/Downloads/VS-VibeAI')

from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_specific_comment():
    """Test the specific problematic comment"""
    
    classifier = AdvancedSentimentClassifier()
    
    # The problematic comment from user
    test_comment = {
        'text': '''Bhaiya please mujhe suggest kar dijiye kaunsi electric scooty Leni chahiye qki mujhe 90 to 110 km me jaane ke liye .....
mujhe facility nhi chahiye bas scooty ka battery backup acha hona chahiye aur range km se km 90 to 100km ke liye ...
Aur mujhe sporty look , normal look digital metre, charging station ye na na mile toh bhi chalega mai ghar me lakar charge kar lunga Mai prayagraj me rahta mere nearby ka ola showroom hai ....

Please bhaiya bta dijiye mere liye koi badhiya electric scooty.🥲

Mera range 80k to 110k 🥲''',
        'likes': 5,
        'author': 'HelpSeeker',
        'oem': 'General'
    }
    
    print("🧪 TESTING SPECIFIC COMMENT CLASSIFICATION")
    print("=" * 50)
    print(f"Comment: {test_comment['text'][:100]}...")
    print()
    
    # Test with advanced classifier
    result = await classifier.classify_comment_advanced(test_comment)
    
    print("🎯 ADVANCED CLASSIFICATION RESULTS:")
    print(f"   Sentiment: {result['sentiment']} (confidence: {result['confidence']})")
    print(f"   Sarcasm: {'YES' if result['sarcasm_detected'] else 'NO'} (score: {result['sarcasm_score']})")
    print(f"   Language: {result['language_analysis']['primary_language']} | Mixed: {result['language_analysis']['is_mixed']}")
    print(f"   Product Relevance: {result['product_relevance']} (score: {result['relevance_score']})")
    print(f"   Context: {result['context']}")
    
    # Check language breakdown
    print("\n🌐 LANGUAGE ANALYSIS:")
    lang_info = result['language_analysis']
    if lang_info['languages']:
        for lang, ratio in lang_info['languages'].items():
            print(f"   {lang}: {ratio:.3f} ({ratio*100:.1f}%)")
    
    # Check pattern analysis
    pattern_info = result['pattern_analysis']
    print(f"\n📊 PATTERN ANALYSIS:")
    print(f"   Sentiment: {pattern_info['sentiment']} (conf: {pattern_info['confidence']})")
    print(f"   Positive score: {pattern_info['positive_score']}")
    print(f"   Negative score: {pattern_info['negative_score']}")
    if pattern_info['sentiment_words']:
        print(f"   Sentiment words found: {pattern_info['sentiment_words']}")
    
    # Check emoji analysis
    emoji_info = result['emoji_analysis']
    if emoji_info['has_emojis']:
        print(f"\n😊 EMOJI ANALYSIS:")
        print(f"   Emojis found: {emoji_info['emoji_count']}")
        print(f"   Emoji sentiment: {emoji_info['emoji_sentiment']} (score: {emoji_info['emoji_sentiment_score']})")
        for emoji_detail in emoji_info['emojis']:
            print(f"   {emoji_detail['emoji']}: {emoji_detail['score']}")
    
    # Check why it might be classified incorrectly
    print(f"\n🔍 DETAILED ANALYSIS:")
    print(f"   Classification factors: {result['classification_factors']}")
    
    # Test with different target OEMs
    print(f"\n🏢 TESTING WITH DIFFERENT TARGET OEMs:")
    for oem in ['Ola Electric', 'Ather', 'Bajaj Chetak']:
        oem_result = await classifier.classify_comment_advanced(test_comment, target_oem=oem)
        print(f"   {oem}: {oem_result['sentiment']} (conf: {oem_result['confidence']:.3f})")
    
    print(f"\n✅ EXPECTED: This comment should be classified as NEUTRAL")
    print(f"   - It's a request for advice/suggestion")
    print(f"   - Contains product requirements (range, price)")
    print(f"   - Uses polite language ('bhaiya please')")
    print(f"   - No negative sentiment about existing products")
    print(f"   - Mixed language but positive intent")

if __name__ == "__main__":
    asyncio.run(test_specific_comment())
