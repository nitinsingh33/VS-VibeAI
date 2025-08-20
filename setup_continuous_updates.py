#!/usr/bin/env python3
"""
Setup Continuous YouTube Data Updates for VibeAI
"""

import schedule
import time
import asyncio
import subprocess
import sys
from datetime import datetime
from services.youtube_scraper import YouTubeCommentScraper

class ContinuousDataUpdater:
    def __init__(self):
        self.scraper = YouTubeCommentScraper()
        self.is_running = False
    
    def run_incremental_update(self):
        """Run incremental data collection"""
        if self.is_running:
            print("⏳ Update already in progress, skipping...")
            return
            
        self.is_running = True
        try:
            print(f"🔄 Starting incremental update at {datetime.now()}")
            
            # Run enhanced scraping for latest comments
            updated_data = self.scraper.run_enhanced_scraping(
                target_comments=100,  # Smaller incremental updates
                incremental=True
            )
            
            total_new = sum(len(comments) for comments in updated_data.values())
            print(f"✅ Incremental update completed: {total_new} new comments collected")
            
        except Exception as e:
            print(f"❌ Update failed: {e}")
        finally:
            self.is_running = False
    
    def run_full_refresh(self):
        """Run full data refresh (weekly)"""
        if self.is_running:
            print("⏳ Update already in progress, skipping full refresh...")
            return
            
        self.is_running = True
        try:
            print(f"🚀 Starting full data refresh at {datetime.now()}")
            
            # Run full enhanced scraping
            updated_data = self.scraper.run_enhanced_scraping(
                target_comments=500,
                incremental=False
            )
            
            total_comments = sum(len(comments) for comments in updated_data.values())
            print(f"✅ Full refresh completed: {total_comments} total comments")
            
        except Exception as e:
            print(f"❌ Full refresh failed: {e}")
        finally:
            self.is_running = False
    
    def start_scheduler(self):
        """Start the continuous update scheduler"""
        print("🚀 Starting VibeAI Continuous Data Updater")
        print("📅 Schedule:")
        print("   - Incremental updates: Every 4 hours")
        print("   - Full refresh: Every Sunday at 2 AM")
        print("   - Health check: Every 30 minutes")
        
        # Schedule incremental updates every 4 hours
        schedule.every(4).hours.do(self.run_incremental_update)
        
        # Schedule full refresh weekly (Sunday 2 AM)
        schedule.every().sunday.at("02:00").do(self.run_full_refresh)
        
        # Schedule health checks
        schedule.every(30).minutes.do(self.health_check)
        
        print("✅ Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Stopping continuous updater...")
            print("✅ Updater stopped")
    
    def health_check(self):
        """Check system health and data freshness"""
        try:
            import os
            import glob
            from datetime import datetime, timedelta
            
            # Check for data files
            recent_files = glob.glob("comments_*_500_*.json")
            if not recent_files:
                print("⚠️  No data files found")
                return
            
            # Check file ages
            now = datetime.now()
            old_files = []
            
            for file in recent_files:
                file_time = datetime.fromtimestamp(os.path.getmtime(file))
                age = now - file_time
                
                if age > timedelta(days=1):
                    old_files.append((file, age.days))
            
            if old_files:
                print(f"📊 Health Check: {len(old_files)} files are older than 1 day")
                for file, days in old_files[:3]:  # Show first 3
                    print(f"   - {file}: {days} days old")
            else:
                print("✅ Health Check: All data files are recent")
                
        except Exception as e:
            print(f"⚠️  Health check error: {e}")

def main():
    """Main function to run the continuous updater"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        updater = ContinuousDataUpdater()
        
        if command == "start":
            updater.start_scheduler()
        elif command == "update":
            print("🔄 Running one-time incremental update...")
            updater.run_incremental_update()
        elif command == "refresh":
            print("🚀 Running one-time full refresh...")
            updater.run_full_refresh()
        elif command == "health":
            print("🏥 Running health check...")
            updater.health_check()
        else:
            print("❌ Unknown command. Use: start, update, refresh, or health")
    else:
        print("📋 VibeAI Continuous Data Updater")
        print("Usage:")
        print("  python setup_continuous_updates.py start    # Start continuous scheduler")
        print("  python setup_continuous_updates.py update   # Run one-time update")
        print("  python setup_continuous_updates.py refresh  # Run full refresh")
        print("  python setup_continuous_updates.py health   # Check system health")

if __name__ == "__main__":
    main()
