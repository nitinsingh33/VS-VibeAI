#!/usr/bin/env python3
"""
Simple test script for Ola market share comment
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔄 Starting test...")

try:
    print("📦 Importing advanced sentiment classifier...")
    from services.advanced_sentiment_classifier import AdvancedSentimentClassifier
    print("✅ Import successful!")
    
    print("🏗️ Initializing classifier...")
    classifier = AdvancedSentimentClassifier()
    print("✅ Classifier initialized!")
    
    # Simple test first
    print("🧪 Testing basic methods...")
    test_text = "Ola ka market share badh raha hai💯"
    
    # Test language detection
    lang_result = classifier.detect_language_mix(test_text)
    print(f"🌐 Language Analysis: {lang_result}")
    
    # Test emoji analysis  
    emoji_result = classifier.analyze_emojis(test_text)
    print(f"😊 Emoji Analysis: {emoji_result}")
    
    # Test company detection
    company_result = classifier.detect_company_mentions(test_text)
    print(f"🏢 Company Analysis: {company_result}")
    
    print("✅ Basic tests completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
