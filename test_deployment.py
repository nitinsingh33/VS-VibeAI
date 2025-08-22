#!/usr/bin/env python3
"""
Quick deployment test script
Tests core functionality before deployment
"""

import asyncio
import json
import time
from typing import Dict, Any

async def test_sentiment_classifier():
    """Test the sentiment classifier functionality"""
    print("🧪 Testing Sentiment Classifier...")
    
    try:
        from services.advanced_sentiment_classifier import AdvancedSentimentClassifier
        classifier = AdvancedSentimentClassifier()
        
        # Test basic classification
        test_comment = {"text": "Excellent electric scooter! Amazing battery life and great performance."}
        result = await classifier.classify_comment_advanced(test_comment)
        
        print(f"✅ Basic classification: {result['sentiment']} (confidence: {result['confidence']:.2f})")
        return True
        
    except Exception as e:
        print(f"❌ Sentiment classifier test failed: {e}")
        return False

async def test_production_optimizer():
    """Test the production optimizer"""
    print("🚀 Testing Production Optimizer...")
    
    try:
        from production_optimizer import ProductionSentimentOptimizer
        optimizer = ProductionSentimentOptimizer()
        
        # Test optimization
        test_comment = {"text": "Please suggest me best electric scooter under 1 lakh"}
        start_time = time.time()
        result = await optimizer.classify_comment_advanced(test_comment)
        processing_time = (time.time() - start_time) * 1000
        
        print(f"✅ Optimization test: {result['sentiment']} in {processing_time:.1f}ms")
        print(f"   Source: {result.get('optimization_layer', 'unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Production optimizer test failed: {e}")
        return False

def test_imports():
    """Test all critical imports"""
    print("📦 Testing Imports...")
    
    import_tests = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "BaseModel"),
        ("requests", "requests"),
        ("google.generativeai", "google-generativeai"),
    ]
    
    passed = 0
    for module_name, display_name in import_tests:
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
            passed += 1
        except ImportError as e:
            print(f"❌ {display_name}: {e}")
    
    return passed == len(import_tests)

def test_data_files():
    """Test for available data files"""
    print("📊 Testing Data Files...")
    
    import glob
    import os
    
    patterns = [
        "all_oem_comments_*.json",
        "comments_*.json"
    ]
    
    total_files = 0
    for pattern in patterns:
        files = glob.glob(pattern)
        total_files += len(files)
        if files:
            print(f"✅ Found {len(files)} files matching {pattern}")
            # Test loading one file
            try:
                with open(files[0], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        print(f"   Sample file has {len(data)} comments")
                    else:
                        print(f"   Sample file format: {type(data)}")
            except Exception as e:
                print(f"   ⚠️  Could not read sample file: {e}")
    
    if total_files == 0:
        print("⚠️  No comment data files found")
        print("   App will work but with limited functionality")
    
    return True  # Non-critical for basic deployment

def test_environment():
    """Test environment setup"""
    print("🌍 Testing Environment...")
    
    import os
    
    # Check Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"✅ Python version: {python_version}")
    
    # Check environment variables (optional)
    env_vars = ["SERPER_API_KEY", "GEMINI_API_KEY"]
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️  {var}: Not set (can be added in Render dashboard)")
    
    # Check required directories
    directories = ["exports", "static", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📂 {directory}: Ready")
    
    return True

async def run_all_tests():
    """Run all deployment tests"""
    print("🚀 SolysAI Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Import Dependencies", test_imports),
        ("Data Files", test_data_files),
        ("Sentiment Classifier", test_sentiment_classifier),
        ("Production Optimizer", test_production_optimizer),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment to Render!")
        deployment_ready = True
    elif passed >= total - 1:
        print("⚠️  Almost ready! Minor issues can be fixed after deployment.")
        deployment_ready = True
    else:
        print("❌ Some critical tests failed. Fix issues before deploying.")
        deployment_ready = False
    
    print("\n📋 Next Steps:")
    if deployment_ready:
        print("1. Push code to GitHub")
        print("2. Create Web Service on Render")
        print("3. Set environment variables in Render dashboard")
        print("4. Deploy and test live endpoints")
    else:
        print("1. Fix failing tests")
        print("2. Run this test script again")
        print("3. Proceed with deployment when tests pass")
    
    return deployment_ready

if __name__ == "__main__":
    try:
        result = asyncio.run(run_all_tests())
        exit_code = 0 if result else 1
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Test suite failed: {e}")
        exit(1)
