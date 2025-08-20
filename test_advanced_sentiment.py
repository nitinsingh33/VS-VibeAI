#!/usr/bin/env python3
"""
Test script for Advanced Sentiment Classification
Tests: Language detection, Emoji analysis, Company attribution, Sarcasm detection
"""

import asyncio
import sys
import os
sys.path.append('/Users/amanmathur/Downloads/VS-VibeAI')

from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

async def test_advanced_classification():
    """Test all advanced sentiment classification features"""
    
    classifier = AdvancedSentimentClassifier()
    
    # Test comments covering all features
    test_comments = [
        {
            'text': 'Ola S1 Pro is absolutely amazing! 😍 Love the acceleration and range. Perfect for daily commute!',
            'likes': 45,
            'author': 'EVLover2025'
        },
        {
            'text': 'Great service from Ola service center 🙄 Visited 3 times already for the same issue! Best experience ever!!!',
            'likes': 12,
            'author': 'FrustratedCustomer'
        },
        {
            'text': 'Ather 450X ka performance बहुत अच्छा है! Battery range भी मस्त है। Highly recommend! 👍⚡',
            'likes': 67,
            'author': 'BikeReviewer'
        },
        {
            'text': 'TVS iQube is धमाकेदार! Quality and service दोनों बेहतरीन। चार्जिंग भी fast है।',
            'likes': 23,
            'author': 'DailyCommuter'
        },
        {
            'text': 'Bajaj Chetak looks premium but range is disappointing. Service quality needs improvement.',
            'likes': 8,
            'author': 'HonestReviewer'
        },
        {
            'text': 'Hero Vida is good but charging infrastructure needs expansion. Overall satisfied with purchase.',
            'likes': 15,
            'author': 'NewOwner'
        },
        {
            'text': 'This movie was fantastic! Weather is also nice today. Planning to visit relatives.',
            'likes': 2,
            'author': 'RandomUser'
        },
        {
            'text': 'Perfect Revolt service! Thanks for nothing... Money well spent on repairs 💸😤',
            'likes': 34,
            'author': 'SarcasticRider'
        }
    ]
    
    print("🚀 Testing Advanced Multi-Layer Sentiment Classification")
    print("=" * 60)
    
    # Test individual comment classification
    for i, comment in enumerate(test_comments, 1):
        print(f"\n📝 TEST COMMENT {i}:")
        print(f"Text: {comment['text']}")
        print(f"Likes: {comment['likes']}")
        
        result = await classifier.classify_comment_advanced(comment, target_oem='Ola Electric')
        
        print(f"\n🎯 ADVANCED CLASSIFICATION RESULTS:")
        print(f"   Sentiment: {result['sentiment']} (confidence: {result['confidence']})")
        print(f"   Sarcasm: {'YES' if result['sarcasm_detected'] else 'NO'} (score: {result['sarcasm_score']})")
        print(f"   Language: {result['language_analysis']['primary_language']} | Mixed: {result['language_analysis']['is_mixed']}")
        print(f"   Product Relevance: {result['product_relevance']} (score: {result['relevance_score']})")
        print(f"   Context: {result['context']}")
        
        # Emoji analysis
        emoji_info = result['emoji_analysis']
        if emoji_info['has_emojis']:
            print(f"   Emojis: {emoji_info['emoji_count']} found, sentiment: {emoji_info['emoji_sentiment']} (score: {emoji_info['emoji_sentiment_score']})")
        
        # Company analysis
        company_info = result['company_analysis']
        if company_info['has_mentions']:
            print(f"   Companies: Primary={company_info['primary_company']}, Competitors={company_info['competitor_mentions']}")
        
        # Engagement analysis
        engagement_info = result['engagement_analysis']
        print(f"   Engagement: {engagement_info['engagement_level']} (score: {engagement_info['engagement_score']})")
        
        # Language breakdown
        lang_info = result['language_analysis']
        if lang_info['languages']:
            print(f"   Language breakdown: {lang_info['languages']}")
        
        print("-" * 40)
    
    print(f"\n📊 BATCH ANALYSIS TEST")
    print("=" * 30)
    
    # Test batch analysis
    enhanced_comments = await classifier.analyze_comment_batch(test_comments, target_oem='Ola Electric')
    
    # Generate summary
    summary = classifier.get_batch_summary(enhanced_comments)
    
    print(f"✅ BATCH SUMMARY:")
    print(f"   Total comments: {summary['total_comments']}")
    print(f"   Sentiment distribution: {summary['sentiment_distribution']}")
    print(f"   Language distribution: {summary['language_distribution']}")
    print(f"   Emoji usage: {summary['emoji_usage']}")
    print(f"   Sarcasm detected: {summary['sarcasm_statistics']['detected']} ({summary['sarcasm_percentage']}%)")
    print(f"   Multilingual comments: {summary['multilingual_percentage']}%")
    print(f"   Company mentions: {summary['company_mentions']}")
    print(f"   Average confidence: {summary['average_confidence']}")
    print(f"   Average engagement: {summary['average_engagement_score']}")
    
    print(f"\n🎯 SPECIFIC FEATURE TESTS")
    print("=" * 25)
    
    # Test 1: Language Detection
    print("1. LANGUAGE DETECTION TEST:")
    lang_test = "Ola S1 Pro बहुत अच्छा है but range could be better"
    lang_result = classifier.detect_language_mix(lang_test)
    print(f"   Text: {lang_test}")
    print(f"   Primary language: {lang_result['primary_language']}")
    print(f"   Is mixed: {lang_result['is_mixed']}")
    print(f"   Language breakdown: {lang_result['languages']}")
    
    # Test 2: Emoji Analysis
    print("\n2. EMOJI ANALYSIS TEST:")
    emoji_test = "Love my Ather 450X! 😍👍⚡🔥 But service needs improvement 😤"
    emoji_result = classifier.analyze_emojis(emoji_test)
    print(f"   Text: {emoji_test}")
    print(f"   Emoji count: {emoji_result['emoji_count']}")
    print(f"   Emoji sentiment: {emoji_result['emoji_sentiment']} (score: {emoji_result['emoji_sentiment_score']})")
    print(f"   Emojis found: {[e['emoji'] for e in emoji_result['emojis']]}")
    
    # Test 3: Company Detection
    print("\n3. COMPANY MENTION DETECTION TEST:")
    company_test = "Comparing Ola S1 Pro vs Ather 450X vs TVS iQube"
    company_result = classifier.detect_company_mentions(company_test)
    print(f"   Text: {company_test}")
    print(f"   Primary company: {company_result['primary_company']}")
    print(f"   All mentions: {list(company_result['all_mentions'].keys())}")
    print(f"   Competitor mentions: {company_result['competitor_mentions']}")
    
    # Test 4: Sarcasm Detection
    print("\n4. SARCASM DETECTION TEST:")
    sarcasm_tests = [
        "Great service! Visited the center 4 times already...",
        "Perfect experience with Ola! Money well spent on repairs 🙄",
        "Amazing product quality! Totally worth the investment!"
    ]
    
    for text in sarcasm_tests:
        emoji_info = classifier.analyze_emojis(text)
        company_info = classifier.detect_company_mentions(text)
        sarcasm_result = classifier.detect_sarcasm_advanced(text, emoji_info, company_info)
        
        print(f"   Text: {text}")
        print(f"   Sarcasm detected: {'YES' if sarcasm_result['sarcasm_detected'] else 'NO'} (score: {sarcasm_result['sarcasm_score']})")
        if sarcasm_result['sarcasm_indicators']:
            print(f"   Indicators: {sarcasm_result['sarcasm_indicators']}")
        print()
    
    print("🎉 ALL ADVANCED SENTIMENT CLASSIFICATION TESTS COMPLETED!")
    print("✅ Features tested: Language detection, Emoji analysis, Company attribution, Sarcasm detection, Engagement weighting")

if __name__ == "__main__":
    asyncio.run(test_advanced_classification())
