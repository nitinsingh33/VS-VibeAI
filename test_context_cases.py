#!/usr/bin/env python3
"""
Test specific context-aware sentiment analysis cases
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_context_cases():
    """Test specific context-aware cases"""
    classifier = AdvancedSentimentClassifier()
    
    test_cases = [
        {
            "text": "don't like scooter sound irritating",
            "expected": "negative",
            "description": "Negation + negative descriptor should be negative",
            "target_oem": None
        },
        {
            "text": "Like for ola",
            "expected": "neutral", 
            "description": "Wrong brand mention (Ola in VIDA context) should be neutral",
            "target_oem": "hero vida"
        },
        {
            "text": "Ola is great",
            "expected": "neutral",
            "description": "Positive about wrong brand in VIDA context should be neutral",
            "target_oem": "hero vida"
        },
        {
            "text": "Hero VIDA is great",
            "expected": "positive",
            "description": "Positive about correct brand should remain positive",
            "target_oem": "hero vida"
        }
    ]
    
    print("🧪 Testing Context-Aware Sentiment Analysis")
    print("=" * 60)
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, case in enumerate(test_cases, 1):
        # Create a mock comment dict
        comment = {
            'text': case['text'],
            'likes': 0,
            'replies': 0,
            'shares': 0
        }
        
        # Run classification with target OEM
        if case['target_oem']:
            result = await classifier.classify_comment_advanced(comment, target_oem=case['target_oem'])
        else:
            result = await classifier.classify_comment_advanced(comment)
        
        predicted_sentiment = result.get('sentiment', 'unknown')
        confidence = result.get('confidence', 0.0)
        
        # Check if prediction matches expected
        is_correct = predicted_sentiment == case['expected']
        if is_correct:
            correct_predictions += 1
        
        # Print results
        status_icon = "✅" if is_correct else "❌"
        print(f"\n{status_icon} Test {i}: {case['description']}")
        print(f"   Text: '{case['text']}'")
        if case['target_oem']:
            print(f"   Target OEM: {case['target_oem']}")
        print(f"   Expected: {case['expected']}")
        print(f"   Predicted: {predicted_sentiment} (confidence: {confidence})")
        
        # Show analysis details for wrong predictions
        if not is_correct:
            print(f"   🔍 Analysis Details:")
            pattern_analysis = result.get('pattern_analysis', {})
            print(f"      - Positive Score: {pattern_analysis.get('positive_score', 0)}")
            print(f"      - Negative Score: {pattern_analysis.get('negative_score', 0)}")
            print(f"      - Has Strong Negative: {pattern_analysis.get('has_strong_negative', False)}")
            print(f"      - Has Negative Phrase: {pattern_analysis.get('has_negative_phrase', False)}")
            
            company_analysis = result.get('company_analysis', {})
            if company_analysis.get('has_mentions'):
                print(f"      - Company Mentions: {list(company_analysis.get('all_mentions', {}).keys())}")
            
            factors = result.get('classification_factors', [])
            if factors:
                print(f"      - Classification Factors: {factors}")
    
    print("\n" + "=" * 60)
    accuracy = (correct_predictions / total_tests) * 100
    print(f"📊 Results: {correct_predictions}/{total_tests} correct ({accuracy:.1f}% accuracy)")
    
    if accuracy >= 80:
        print("🎉 Great! Context-aware sentiment analysis is working well!")
    elif accuracy >= 60:
        print("⚠️  Good progress, but some cases need fine-tuning")
    else:
        print("❌ More work needed on context-aware classification logic")
    
    return accuracy

if __name__ == "__main__":
    success = asyncio.run(test_context_cases())
    print("\n" + "=" * 60)
    if success >= 80:
        print("🎉 Context-aware sentiment analysis working correctly!")
    else:
        print("❌ Context-aware sentiment analysis needs improvement.")
