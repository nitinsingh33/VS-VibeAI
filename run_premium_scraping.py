#!/usr/bin/env python3
"""
Premium YouTube Comment Scraping Script - 2,000 Recent & High-Engagement Comments per OEM
Enhanced with smart filtering for most recent and relevant comments
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from services.youtube_scraper import YouTubeCommentScraper

class PremiumCommentScraper(YouTubeCommentScraper):
    """Enhanced scraper focused on recent and high-engagement comments"""
    
    def __init__(self):
        super().__init__()
        
        # Enhanced search strategies for better content discovery
        self.premium_search_strategies = {
            'Ola Electric': [
                # Recent reviews and updates
                'ola electric scooter 2024 review',
                'ola s1 pro 2024 update',
                'ola electric latest news',
                'ola s1 pro real owner review',
                'ola electric service center experience',
                'ola electric charging network 2024',
                'ola s1 pro vs competition',
                'ola electric range test 2024',
                'ola scooter problems 2024',
                'ola electric price increase',
                # High engagement content
                'ola electric vs petrol scooter',
                'should you buy ola electric',
                'ola electric after 1 year',
                'ola electric honest review',
                'ola electric buyers guide'
            ],
            'TVS iQube': [
                # Recent content
                'tvs iqube 2024 model',
                'tvs iqube latest review',
                'tvs iqube vs ola electric',
                'tvs iqube real range test',
                'tvs iqube service experience',
                'tvs iqube smartconnect features',
                'tvs iqube price 2024',
                'tvs iqube long term review',
                'tvs iqube charging time',
                'tvs iqube build quality',
                # High engagement
                'best electric scooter tvs iqube',
                'tvs iqube honest opinion',
                'tvs iqube worth buying',
                'tvs iqube vs bajaj chetak'
            ],
            'Bajaj Chetak': [
                # Recent updates
                'bajaj chetak 2024 model',
                'chetak electric latest review',
                'bajaj chetak vs competitors',
                'chetak electric real world range',
                'bajaj chetak service quality',
                'chetak electric premium features',
                'bajaj chetak price worth it',
                'chetak electric build quality',
                'bajaj chetak charging infrastructure',
                'chetak electric performance test',
                # Popular comparisons
                'chetak vs ola electric',
                'chetak vs ather 450x',
                'bajaj chetak honest review'
            ],
            'Ather': [
                # Recent content
                'ather 450x 2024 review',
                'ather energy latest updates',
                'ather grid charging network',
                'ather 450x real world range',
                'ather service center experience',
                'ather 450x software updates',
                'ather 450x performance test',
                'ather energy subscription cost',
                'ather 450x build quality',
                'ather dashboard features 2024',
                # High engagement topics
                'ather 450x vs ola s1 pro',
                'ather 450x worth the price',
                'ather energy honest review',
                'best features ather 450x'
            ],
            'Hero Vida': [
                # Recent developments
                'hero vida 2024 review',
                'vida electric scooter update',
                'hero vida v1 pro features',
                'vida electric real range test',
                'hero vida service network',
                'vida electric app connectivity',
                'hero vida vs competition',
                'vida electric build quality',
                'hero vida charging speed',
                'vida electric price analysis',
                # Trending comparisons
                'hero vida vs ola electric',
                'vida electric honest review',
                'hero vida worth buying 2024'
            ]
        }
    
    def get_comment_engagement_score(self, comment: Dict) -> float:
        """Calculate engagement score for comment prioritization"""
        score = 0.0
        
        # Likes contribute significantly
        likes = comment.get('likes', 0)
        score += min(likes * 2, 100)  # Cap likes contribution at 100
        
        # Comment length (detailed comments often more valuable)
        text_length = len(comment.get('text', ''))
        if 50 <= text_length <= 500:  # Sweet spot for detailed comments
            score += 20
        elif text_length > 500:
            score += 10
        
        # Recency bonus (newer comments get priority)
        if 'time' in comment and comment['time']:
            try:
                comment_date = datetime.fromtimestamp(comment['time'])
                days_old = (datetime.now() - comment_date).days
                
                if days_old <= 30:
                    score += 50  # Very recent
                elif days_old <= 90:
                    score += 30  # Recent
                elif days_old <= 180:
                    score += 15  # Moderately recent
                elif days_old <= 365:
                    score += 5   # Within a year
            except:
                pass
        
        # Quality indicators
        text = comment.get('text', '').lower()
        
        # Positive indicators
        quality_words = [
            'experience', 'review', 'months', 'service', 'performance', 
            'range', 'charging', 'comparison', 'recommend', 'honest',
            'detailed', 'update', 'after', 'real', 'actual'
        ]
        for word in quality_words:
            if word in text:
                score += 5
        
        # Negative indicators (reduce score)
        spam_words = ['first', 'subscribe', 'like if', 'check out']
        for word in spam_words:
            if word in text:
                score -= 20
        
        # Video engagement (popular videos often have better comments)
        video_views = comment.get('video_views', 0)
        if video_views > 100000:
            score += 10
        elif video_views > 50000:
            score += 5
        
        return max(score, 0)  # Ensure non-negative score
    
    def filter_and_rank_comments(self, comments: List[Dict], target_count: int = 2000) -> List[Dict]:
        """Filter and rank comments by engagement and recency"""
        if not comments:
            return []
        
        print(f"📊 Filtering {len(comments)} comments to top {target_count}...")
        
        # Calculate engagement scores
        for comment in comments:
            comment['_engagement_score'] = self.get_comment_engagement_score(comment)
        
        # Sort by engagement score (descending)
        sorted_comments = sorted(comments, key=lambda x: x['_engagement_score'], reverse=True)
        
        # Remove duplicates based on text similarity
        unique_comments = []
        seen_texts = set()
        
        for comment in sorted_comments:
            text = comment.get('text', '').strip().lower()
            # Create a simple fingerprint for duplicate detection
            text_fingerprint = ' '.join(sorted(text.split()[:10]))  # First 10 words, sorted
            
            if text_fingerprint not in seen_texts and len(text) >= 20:
                unique_comments.append(comment)
                seen_texts.add(text_fingerprint)
                
                if len(unique_comments) >= target_count:
                    break
        
        print(f"✅ Selected {len(unique_comments)} high-quality, unique comments")
        return unique_comments
    
    def scrape_premium_oem_comments(self, oem_name: str, target_count: int = 2000) -> List[Dict]:
        """Scrape high-quality comments for an OEM with focus on recent and engaging content"""
        
        if oem_name not in self.premium_search_strategies:
            print(f"❌ OEM {oem_name} not configured for premium scraping")
            return []
        
        print(f"🚀 Starting PREMIUM scraping for {oem_name}")
        print(f"🎯 Target: {target_count} recent & high-engagement comments")
        
        all_comments = []
        search_terms = self.premium_search_strategies[oem_name]
        
        # Enhanced scraping with more videos per search
        videos_per_search = 15
        comments_per_video = 150
        
        for i, search_term in enumerate(search_terms):
            if len(all_comments) >= target_count * 1.5:  # Get 150% to ensure good filtering
                break
                
            print(f"🔍 [{i+1}/{len(search_terms)}] Searching: {search_term}")
            
            try:
                # Search for videos
                videos = self.search_youtube_videos_multiple_methods(search_term, max_results=videos_per_search)
                
                if not videos:
                    print(f"   ⚠️ No videos found for: {search_term}")
                    continue
                
                print(f"   📺 Found {len(videos)} videos")
                
                # Sort videos by view count (prioritize popular videos)
                videos.sort(key=lambda x: x.get('view_count', 0), reverse=True)
                
                for j, video in enumerate(videos):
                    if len(all_comments) >= target_count * 1.5:
                        break
                    
                    video_id = video['video_id']
                    if not video_id or len(video_id) != 11:
                        continue
                    
                    print(f"   📹 [{j+1}/{len(videos)}] Processing: {video['title'][:60]}...")
                    
                    # Extract comments with enhanced limit
                    video_comments = self.extract_comments_with_fallback(video_id, limit=comments_per_video)
                    
                    if not video_comments:
                        print(f"       ⚠️ No comments extracted")
                        continue
                    
                    # Add metadata
                    for comment in video_comments:
                        comment.update({
                            'oem': oem_name,
                            'search_query': search_term,
                            'video_title': video['title'],
                            'video_url': video['url'],
                            'video_uploader': video.get('uploader', 'Unknown'),
                            'video_views': video.get('view_count', 0),
                            'video_duration': video.get('duration', 0)
                        })
                    
                    # Filter for quality and recency
                    quality_comments = []
                    for comment in video_comments:
                        text = comment.get('text', '').strip()
                        
                        # Basic quality filters
                        if (len(text) >= 20 and 
                            not self._is_spam_comment(text) and
                            self._is_relevant_to_oem(text, oem_name)):
                            quality_comments.append(comment)
                    
                    all_comments.extend(quality_comments)
                    print(f"       ✅ Added {len(quality_comments)} quality comments (Total: {len(all_comments)})")
                    
                    # Small delay between videos
                    time.sleep(0.3)
                
                # Delay between search terms
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error processing search term '{search_term}': {e}")
                continue
        
        print(f"📊 Raw collection complete: {len(all_comments)} comments before filtering")
        
        # Apply premium filtering and ranking
        premium_comments = self.filter_and_rank_comments(all_comments, target_count)
        
        # Sort final selection by date (most recent first)
        def get_comment_date(comment):
            try:
                return comment.get('time', 0)
            except:
                return 0
        
        premium_comments.sort(key=get_comment_date, reverse=True)
        
        print(f"🎉 PREMIUM scraping completed for {oem_name}")
        print(f"✨ Final selection: {len(premium_comments)} high-quality comments")
        
        return premium_comments
    
    def _is_relevant_to_oem(self, text: str, oem_name: str) -> bool:
        """Check if comment is relevant to the OEM"""
        text_lower = text.lower()
        oem_keywords = {
            'Ola Electric': ['ola', 's1', 'electric'],
            'TVS iQube': ['tvs', 'iqube', 'electric'],
            'Bajaj Chetak': ['bajaj', 'chetak', 'electric'],
            'Ather': ['ather', '450x', 'energy'],
            'Hero Vida': ['hero', 'vida', 'electric']
        }
        
        keywords = oem_keywords.get(oem_name, [])
        return any(keyword in text_lower for keyword in keywords)
    
    def run_premium_scraping(self, target_per_oem: int = 2000) -> Dict[str, List[Dict]]:
        """Run premium scraping for all OEMs"""
        print("🌟 PREMIUM VIBEAI COMMENT SCRAPING - 2,000 Comments per OEM")
        print("=" * 80)
        print("✨ Focus: RECENT & HIGH-ENGAGEMENT comments only")
        print(f"🎯 Target: {target_per_oem} premium comments per OEM")
        print(f"📊 Total Expected: {target_per_oem * 5} premium comments")
        print("=" * 80)
        
        start_time = time.time()
        all_oem_data = {}
        total_scraped = 0
        
        for oem_name in self.oems.keys():
            try:
                print(f"\n🔥 Processing {oem_name}...")
                comments = self.scrape_premium_oem_comments(oem_name, target_per_oem)
                all_oem_data[oem_name] = comments
                total_scraped += len(comments)
                
                # Save individual OEM file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"premium_{oem_name.replace(' ', '_').lower()}_{len(comments)}_comments_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(comments, f, ensure_ascii=False, indent=2)
                print(f"💾 Saved to: {filename}")
                
                # Show engagement stats
                if comments:
                    avg_engagement = sum(c.get('_engagement_score', 0) for c in comments) / len(comments)
                    recent_count = len([c for c in comments if self._is_recent_comment(c)])
                    print(f"📈 Avg Engagement Score: {avg_engagement:.1f}")
                    print(f"🕒 Recent Comments: {recent_count}/{len(comments)}")
                
                # Delay between OEMs
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error scraping {oem_name}: {e}")
                all_oem_data[oem_name] = []
        
        # Save combined premium dataset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_filename = f"premium_all_oems_{total_scraped}_total_{timestamp}.json"
        
        metadata = {
            'scrape_type': 'premium_quality',
            'scrape_timestamp': timestamp,
            'total_comments': total_scraped,
            'target_per_oem': target_per_oem,
            'focus': 'recent_and_high_engagement',
            'oem_summary': {oem: len(comments) for oem, comments in all_oem_data.items()},
            'quality_metrics': self._calculate_quality_metrics(all_oem_data),
            'comments': all_oem_data
        }
        
        with open(combined_filename, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # Final summary
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 80)
        print("🎉 PREMIUM SCRAPING COMPLETED!")
        print("=" * 80)
        
        for oem, comments in all_oem_data.items():
            success_rate = (len(comments) / target_per_oem) * 100 if target_per_oem > 0 else 0
            status = "✅" if success_rate >= 80 else "⚠️" if success_rate >= 50 else "❌"
            print(f"{status} {oem}: {len(comments)}/{target_per_oem} comments ({success_rate:.1f}%)")
        
        print(f"\n📊 Total Premium Comments: {total_scraped}")
        print(f"⏱️  Total Time: {elapsed_time/60:.1f} minutes")
        print(f"💾 Saved to: {combined_filename}")
        print(f"✨ Average Quality: Premium selection with engagement scoring")
        
        return all_oem_data
    
    def _is_recent_comment(self, comment: Dict) -> bool:
        """Check if comment is from the last 6 months"""
        try:
            if 'time' in comment and comment['time']:
                comment_date = datetime.fromtimestamp(comment['time'])
                return (datetime.now() - comment_date).days <= 180
        except:
            pass
        return False
    
    def _calculate_quality_metrics(self, all_data: Dict) -> Dict:
        """Calculate quality metrics for the scraped data"""
        metrics = {}
        
        for oem, comments in all_data.items():
            if not comments:
                metrics[oem] = {'avg_engagement': 0, 'recent_percentage': 0}
                continue
            
            avg_engagement = sum(c.get('_engagement_score', 0) for c in comments) / len(comments)
            recent_count = len([c for c in comments if self._is_recent_comment(c)])
            recent_percentage = (recent_count / len(comments)) * 100
            
            metrics[oem] = {
                'avg_engagement_score': round(avg_engagement, 2),
                'recent_percentage': round(recent_percentage, 1),
                'total_comments': len(comments),
                'avg_likes': round(sum(c.get('likes', 0) for c in comments) / len(comments), 1)
            }
        
        return metrics

def main():
    print("🌟 VibeAI Premium Comment Scraper")
    print("=" * 60)
    print("Focused on RECENT & HIGH-ENGAGEMENT comments")
    print("Target: 2,000 premium comments per OEM")
    print("=" * 60)
    
    # Get user confirmation
    target_comments = input("Enter target comments per OEM (default 2000): ").strip()
    target_comments = int(target_comments) if target_comments.isdigit() else 2000
    
    print(f"\n🎯 Target: {target_comments} premium comments per OEM")
    print(f"📊 Expected total: {target_comments * 5} premium comments")
    print("\n✨ Premium Features:")
    print("  • Most recent comments (prioritized)")
    print("  • High engagement (likes, replies)")
    print("  • Popular video sources")
    print("  • Quality content filtering")
    print("  • Duplicate removal")
    
    # Confirm before starting
    confirm = input("\n🚀 Start premium scraping? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Scraping cancelled.")
        return
    
    # Initialize premium scraper
    print("\n🔥 Initializing Premium Comment Scraper...")
    scraper = PremiumCommentScraper()
    
    # Run premium scraping
    try:
        all_data = scraper.run_premium_scraping(target_per_oem=target_comments)
        
        # Show final results
        total_scraped = sum(len(comments) for comments in all_data.values())
        
        if total_scraped > 0:
            print(f"\n🏆 SUCCESS: {total_scraped} premium comments collected!")
            print("💡 TIP: These comments are sorted by engagement and recency")
            print("    Perfect for high-quality market intelligence analysis!")
        else:
            print("\n❌ No comments could be collected. Check internet connection.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during premium scraping: {e}")
    
    print(f"\n🏁 Premium scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
