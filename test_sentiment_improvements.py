#!/usr/bin/env python3
"""
Test script to verify sentiment analysis improvements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_sentiment_cases():
    """Test specific cases that were misclassified"""
    classifier = AdvancedSentimentClassifier()
    
    test_cases = [
        {
            "text": "I am interested to know the sales of those companies which are in the number range of 11 to 20. Information about top 5 or top 10 is everywhere. Nothing new. Try to give sales number of lesser known companies like Benin, Bounce infinity, Tunwal, iscoot etc",
            "expected": "neutral",
            "description": "Information seeking request - should be neutral"
        },
        {
            "text": "📌📌📌📌📌📌📌📌📌📌📌\n📌📌📌📌📌📌📌📌📌📌📌\nBroo TVS iqube ST or Bajaj chetak premium 2024 which one is best your opinion plzzz rply",
            "expected": "neutral", 
            "description": "Comparison question with opinion request - should be neutral"
        },
        {
            "text": "Which scooter is best for daily commute suggest me please",
            "expected": "neutral",
            "description": "Advice request - should be neutral"
        },
        {
            "text": "Ola electric is fraud company dont buy",
            "expected": "negative",
            "description": "Strong negative opinion - should be negative"
        },
        {
            "text": "Amazing service! Had to visit service center 5 times for same issue",
            "expected": "negative",  # This should be detected as sarcasm
            "description": "Sarcastic comment - should be negative"
        },
        {
            "text": "Ola S1 Pro is absolutely amazing. Love the performance and range!",
            "expected": "positive",
            "description": "Genuine positive review - should be positive"
        },
        {
            "text": "Help me choose between Ather 450X and TVS iQube",
            "expected": "neutral",
            "description": "Choice help request - should be neutral"
        },
        {
            "text": "Sales figures batao yaar for all EV companies",
            "expected": "neutral",
            "description": "Data request in Hindi-English mix - should be neutral"
        },
        {
            "text": "I like petrol scooty❤❤❤",
            "expected": "neutral",
            "description": "Irrelevant petrol preference in EV context - should be neutral"
        },
        {
            "text": "don't like scooter sound irritating",
            "expected": "negative",
            "description": "Negation with negative descriptor - should be negative"
        },
        {
            "text": "Like for ola",
            "expected": "neutral",
            "description": "Wrong brand mention in different brand context - should be neutral (when target is VIDA)"
        }
    ]
    
    print("🧪 Testing Sentiment Analysis Improvements")
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
        
        # Run classification
        result = await classifier.classify_comment_advanced(comment)
        
        # Handle the result structure
        predicted_sentiment = result.get('sentiment', 'unknown')
        confidence = result.get('confidence', 0.0)
        
        # Check if prediction matches expected
        is_correct = predicted_sentiment == case['expected']
        if is_correct:
            correct_predictions += 1
        
        # Print results
        status_icon = "✅" if is_correct else "❌"
        print(f"\n{status_icon} Test {i}: {case['description']}")
        print(f"   Text: {case['text'][:80]}{'...' if len(case['text']) > 80 else ''}")
        print(f"   Expected: {case['expected']}")
        print(f"   Predicted: {predicted_sentiment} (confidence: {confidence})")
        
        # Show additional details for wrong predictions
        if not is_correct:
            print(f"   🔍 Analysis Details:")
            pattern_analysis = result.get('pattern_analysis', {})
            print(f"      - Is Advice Request: {pattern_analysis.get('is_advice_request', False)}")
            print(f"      - Is Information Seeking: {pattern_analysis.get('is_information_seeking', False)}")
            print(f"      - Is Question: {pattern_analysis.get('is_question', False)}")
            print(f"      - Is Irrelevant: {pattern_analysis.get('is_irrelevant', False)}")
            print(f"      - Is Neutral Request: {pattern_analysis.get('is_neutral_request', False)}")
            print(f"      - Positive Score: {pattern_analysis.get('positive_score', 0)}")
            print(f"      - Negative Score: {pattern_analysis.get('negative_score', 0)}")
            
            if result.get('sarcasm_detected'):
                print(f"      - Sarcasm Detected: {result.get('sarcasm_detected', False)}")
                print(f"      - Sarcasm Score: {result.get('sarcasm_score', 0)}")
    
    print("\n" + "=" * 60)
    accuracy = (correct_predictions / total_tests) * 100
    print(f"📊 Results: {correct_predictions}/{total_tests} correct ({accuracy:.1f}% accuracy)")
    
    if accuracy >= 80:
        print("🎉 Great! Sentiment analysis improvements are working well!")
    elif accuracy >= 60:
        print("⚠️  Good progress, but some cases need fine-tuning")
    else:
        print("❌ More work needed on sentiment classification logic")
    
    return accuracy

async def main():
    """Main test function"""
    print("🚀 Starting Sentiment Analysis Test Suite")
    accuracy = await test_sentiment_cases()
    
    if accuracy >= 80:
        print("\n✨ All tests completed successfully!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review the logic for improvement.")
        return 1

if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
