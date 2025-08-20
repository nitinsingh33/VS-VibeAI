#!/usr/bin/env python3
"""
Enhanced YouTube Comment Scraping Script
Run this to scrape 500+ comments per Indian EV OEM
"""

import os
import sys
import time
from datetime import datetime
from services.youtube_scraper import YouTubeCommentScraper

def main():
    print("🏍️ Enhanced VibeAI YouTube Comment Scraper")
    print("=" * 60)
    print("This script will scrape 500+ comments for each Indian EV OEM:")
    print("• Ola Electric")
    print("• TVS iQube") 
    print("• Bajaj Chetak")
    print("• Ather")
    print("• Hero Vida")
    print("=" * 60)
    
    # Get user preferences
    target_comments = input("Enter target comments per OEM (default 500): ").strip()
    target_comments = int(target_comments) if target_comments.isdigit() else 500
    
    print(f"\n🎯 Target: {target_comments} comments per OEM")
    print(f"📊 Expected total: {target_comments * 5} comments")
    
    # Confirm before starting
    confirm = input("\nStart scraping? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Scraping cancelled.")
        return
    
    # Initialize scraper
    print("\n🚀 Initializing YouTube Comment Scraper...")
    scraper = YouTubeCommentScraper()
    
    # Run enhanced scraping
    start_time = time.time()
    print(f"\n⏰ Starting enhanced scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        all_data = scraper.run_enhanced_scraping(target_comments=target_comments)
        
        # Show results
        total_scraped = sum(len(comments) for comments in all_data.values())
        elapsed_time = time.time() - start_time
        
        print("\n🎉 SCRAPING COMPLETED!")
        print("=" * 60)
        print("📈 FINAL RESULTS:")
        
        for oem, comments in all_data.items():
            status = "✅" if len(comments) >= target_comments * 0.8 else "⚠️"  # 80% threshold
            print(f"{status} {oem}: {len(comments)} comments")
        
        print(f"\n📊 Total Comments Scraped: {total_scraped}")
        print(f"⏱️  Total Time: {elapsed_time/60:.1f} minutes")
        print(f"💾 Data saved to timestamped JSON files")
        
        # Performance metrics
        avg_per_oem = total_scraped / len(all_data)
        success_rate = (sum(1 for comments in all_data.values() if len(comments) >= target_comments * 0.8) / len(all_data)) * 100
        
        print(f"\n📋 PERFORMANCE METRICS:")
        print(f"• Average per OEM: {avg_per_oem:.1f} comments")
        print(f"• Success Rate: {success_rate:.1f}% (80%+ of target)")
        print(f"• Comments per minute: {total_scraped/(elapsed_time/60):.1f}")
        
        if total_scraped >= target_comments * len(all_data) * 0.8:
            print("\n🏆 SUCCESS: Target achieved for most OEMs!")
        else:
            print("\n⚠️  PARTIAL SUCCESS: Some OEMs may need additional scraping")
        
        print("\n💡 TIP: Data files are saved with timestamps for easy identification")
        print("    Use these files with your Streamlit app for analysis!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraping interrupted by user")
        print("Partial data may have been saved to JSON files")
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        print("Check your internet connection and try again")
    
    print(f"\n🏁 Script completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
