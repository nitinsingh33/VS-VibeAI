#!/usr/bin/env python3
"""
Test Enhanced YouTube Scraping - Quick Verification
This script tests the enhanced scraping with a small sample to verify it works.
"""

import sys
import os

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.youtube_scraper import YouTubeCommentScraper

def test_enhanced_scraping():
    print("🧪 Testing Enhanced YouTube Comment Scraping")
    print("=" * 50)
    
    scraper = YouTubeCommentScraper()
    
    # Test with small numbers for quick verification
    test_oem = "Ola Electric"
    target_comments = 10  # Small number for quick test
    
    print(f"🎯 Testing {test_oem} scraping (target: {target_comments} comments)")
    print("This should complete in 1-2 minutes...")
    
    try:
        comments = scraper.scrape_oem_comments(
            oem_name=test_oem, 
            target_total=target_comments,
            max_videos=3,  # Limit videos for faster test
            comments_per_video=5  # Limit comments per video
        )
        
        print(f"\n✅ Test Result: {len(comments)} comments collected")
        
        if comments:
            print("\n📋 Sample Comment:")
            sample = comments[0]
            print(f"Text: {sample.get('text', '')[:100]}...")
            print(f"Author: {sample.get('author', 'N/A')}")
            print(f"Likes: {sample.get('likes', 0)}")
            print(f"Video: {sample.get('video_title', 'N/A')[:50]}...")
            
            print(f"\n🎉 SUCCESS: Enhanced scraping is working!")
            print(f"Ready to run full scraping with 500+ comments per OEM")
        else:
            print(f"\n⚠️  WARNING: No comments collected")
            print(f"This could be due to:")
            print(f"- Network connectivity issues")
            print(f"- YouTube API limits")
            print(f"- Limited content for search terms")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"Troubleshooting:")
        print(f"1. Check internet connection")
        print(f"2. Ensure packages installed: pip install youtube-comment-downloader yt-dlp")
        print(f"3. Try again in a few minutes")

if __name__ == "__main__":
    test_enhanced_scraping()
