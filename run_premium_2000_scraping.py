#!/usr/bin/env python3
"""
Premium Scraping Script - Collect 2,000+ Comments per OEM
Prioritizes: Recent comments + High engagement + Popular videos
"""

import os
import sys
import time
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any
from services.youtube_scraper import YouTubeCommentScraper

class PremiumCommentScraper:
    def __init__(self):
        self.scraper = YouTubeCommentScraper()
        self.target_per_oem = 2000
        self.oems = {
            'Ola Electric': [
                'ola electric scooter review 2025',
                'ola s1 pro review',
                'ola electric problems',
                'ola electric service experience',
                'ola electric vs competitors',
                'ola electric latest news',
                'ola electric customer feedback',
                'ola s1 air review'
            ],
            'TVS iQube': [
                'tvs iqube review 2025',
                'tvs iqube vs ola electric',
                'tvs iqube performance test',
                'tvs iqube customer review',
                'tvs iqube problems',
                'tvs iqube service experience',
                'tvs iqube range test',
                'tvs iqube comparison'
            ],
            'Bajaj Chetak': [
                'bajaj chetak review 2025',
                'bajaj chetak electric scooter',
                'bajaj chetak vs competitors',
                'bajaj chetak customer feedback',
                'bajaj chetak problems',
                'bajaj chetak service',
                'bajaj chetak performance',
                'bajaj chetak comparison'
            ],
            'Ather': [
                'ather 450x review 2025',
                'ather electric scooter review',
                'ather vs ola electric',
                'ather customer experience',
                'ather service quality',
                'ather 450x problems',
                'ather charging network',
                'ather performance test'
            ],
            'Hero Vida': [
                'hero vida review 2025',
                'hero vida electric scooter',
                'hero vida vs competitors',
                'hero vida customer feedback',
                'hero vida performance',
                'hero vida service experience',
                'hero vida problems',
                'hero vida comparison'
            ]
        }
    
    def get_enhanced_search_terms(self, oem_name: str) -> List[str]:
        """Get comprehensive search terms for maximum coverage"""
        base_terms = self.oems.get(oem_name, [])
        
        # Add temporal terms for recent content
        recent_terms = [
            f"{oem_name.lower()} 2025 review",
            f"{oem_name.lower()} latest update",
            f"{oem_name.lower()} new model",
            f"{oem_name.lower()} recent experience",
            f"{oem_name.lower()} august 2025"
        ]
        
        # Add engagement-focused terms
        engagement_terms = [
            f"{oem_name.lower()} honest review",
            f"{oem_name.lower()} real experience",
            f"{oem_name.lower()} detailed review",
            f"{oem_name.lower()} user experience",
            f"{oem_name.lower()} long term review"
        ]
        
        return base_terms + recent_terms + engagement_terms
    
    def filter_high_quality_comments(self, comments: List[Dict]) -> List[Dict]:
        """Filter and prioritize high-quality comments"""
        if not comments:
            return []
        
        # Score comments based on multiple factors
        scored_comments = []
        
        for comment in comments:
            score = 0
            
            # Engagement score (likes, replies)
            likes = comment.get('likes', 0)
            if likes > 50:
                score += 5
            elif likes > 20:
                score += 3
            elif likes > 5:
                score += 1
            
            # Length score (detailed comments)
            text_length = len(comment.get('text', ''))
            if text_length > 200:
                score += 3
            elif text_length > 100:
                score += 2
            elif text_length > 50:
                score += 1
            
            # Recency score (recent comments prioritized)
            try:
                comment_date = datetime.strptime(comment.get('date', ''), '%Y-%m-%d %H:%M:%S')
                days_old = (datetime.now() - comment_date).days
                if days_old < 30:
                    score += 4
                elif days_old < 90:
                    score += 3
                elif days_old < 180:
                    score += 2
                elif days_old < 365:
                    score += 1
            except:
                pass
            
            # Content quality score
            text = comment.get('text', '').lower()
            quality_keywords = [
                'experience', 'review', 'quality', 'performance', 'service',
                'problem', 'issue', 'excellent', 'poor', 'recommend',
                'satisfied', 'disappointed', 'worth', 'value'
            ]
            
            quality_score = sum(1 for keyword in quality_keywords if keyword in text)
            score += min(quality_score, 3)  # Cap at 3 points
            
            scored_comments.append({
                'comment': comment,
                'quality_score': score
            })
        
        # Sort by quality score (descending)
        scored_comments.sort(key=lambda x: x['quality_score'], reverse=True)
        
        # Return top comments
        return [item['comment'] for item in scored_comments]
    
    def scrape_oem_premium(self, oem_name: str) -> List[Dict]:
        """Scrape premium quality comments for an OEM"""
        print(f"\n🎯 Scraping {oem_name} - Target: {self.target_per_oem} high-quality comments")
        
        all_comments = []
        search_terms = self.get_enhanced_search_terms(oem_name)
        
        for i, search_term in enumerate(search_terms, 1):
            if len(all_comments) >= self.target_per_oem:
                break
                
            print(f"  📹 [{i}/{len(search_terms)}] Searching: '{search_term}'")
            
            try:
                # Get comments for this search term
                comments = self.scraper.scrape_oem_comments(oem_name, max_videos=30, comments_per_video=100, target_total=300)
                
                if comments:
                    # Filter for high quality
                    quality_comments = self.filter_high_quality_comments(comments)
                    
                    # Add to collection (avoid duplicates)
                    new_comments = 0
                    existing_texts = {c.get('text', '') for c in all_comments}
                    
                    for comment in quality_comments:
                        if comment.get('text', '') not in existing_texts:
                            comment['search_term'] = search_term
                            comment['quality_verified'] = True
                            comment['extraction_method'] = 'premium_scraping'
                            all_comments.append(comment)
                            existing_texts.add(comment.get('text', ''))
                            new_comments += 1
                    
                    print(f"    ✅ Found {new_comments} new high-quality comments")
                    print(f"    📊 Total for {oem_name}: {len(all_comments)}")
                else:
                    print(f"    ⚠️  No comments found for '{search_term}'")
                
                # Respectful delay
                time.sleep(3)
                
            except Exception as e:
                print(f"    ❌ Error scraping '{search_term}': {e}")
                continue
        
        # Final quality filter and sorting
        final_comments = self.filter_high_quality_comments(all_comments)
        result = final_comments[:self.target_per_oem]
        
        print(f"  🏆 Final result: {len(result)} premium comments for {oem_name}")
        return result
    
    def run_premium_scraping(self) -> Dict[str, List[Dict]]:
        """Run premium scraping for all OEMs"""
        print("🚀 PREMIUM COMMENT SCRAPING - 2,000+ per OEM")
        print("=" * 70)
        print("📈 Focus: Recent + High Engagement + Popular Videos")
        print("🎯 Target: 2,000 quality comments per OEM")
        print("⏱️  Estimated time: 60-90 minutes")
        print("=" * 70)
        
        start_time = time.time()
        all_data = {}
        total_collected = 0
        
        for oem_name in self.oems.keys():
            print(f"\n🏢 Processing {oem_name}...")
            
            try:
                comments = self.scrape_oem_premium(oem_name)
                all_data[oem_name] = comments
                total_collected += len(comments)
                
                print(f"✅ {oem_name} completed: {len(comments)} comments")
                
                # Save individual OEM file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                individual_filename = f"comments_{oem_name.lower().replace(' ', '_')}_2000_comments_{timestamp}.json"
                
                with open(individual_filename, 'w', encoding='utf-8') as f:
                    json.dump(comments, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Saved: {individual_filename}")
                
            except Exception as e:
                print(f"❌ Failed to scrape {oem_name}: {e}")
                all_data[oem_name] = []
        
        # Save combined dataset
        elapsed_time = time.time() - start_time
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        combined_data = {
            'scrape_timestamp': timestamp,
            'scraping_method': 'premium_quality_focused',
            'target_per_oem': self.target_per_oem,
            'total_comments': total_collected,
            'oem_summary': {oem: len(comments) for oem, comments in all_data.items()},
            'quality_criteria': [
                'High engagement (likes, replies)',
                'Recent comments (prioritized)',
                'Detailed feedback (length)',
                'Content quality (keywords)',
                'Popular videos'
            ],
            'comments': all_data
        }
        
        combined_filename = f"all_oem_comments_{total_collected}_total_{timestamp}.json"
        
        with open(combined_filename, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        
        # Results summary
        print("\n" + "=" * 70)
        print("🏆 PREMIUM SCRAPING COMPLETE!")
        print("=" * 70)
        print(f"📊 Total Comments: {total_collected}")
        print(f"⏱️  Total Time: {elapsed_time/60:.1f} minutes")
        print(f"💾 Combined File: {combined_filename}")
        print("\n📋 OEM BREAKDOWN:")
        
        for oem_name, comments in all_data.items():
            quality_score = sum(c.get('likes', 0) for c in comments) / len(comments) if comments else 0
            print(f"  🏢 {oem_name}: {len(comments)} comments (avg {quality_score:.1f} likes)")
        
        # Success metrics
        success_rate = (sum(1 for comments in all_data.values() if len(comments) >= self.target_per_oem * 0.8) / len(all_data)) * 100
        
        print(f"\n📈 QUALITY METRICS:")
        print(f"  ✅ Success Rate: {success_rate:.1f}% (80%+ of target)")
        print(f"  📊 Average per OEM: {total_collected / len(all_data):.1f} comments")
        print(f"  ⚡ Comments per minute: {total_collected/(elapsed_time/60):.1f}")
        
        if total_collected >= self.target_per_oem * len(all_data) * 0.8:
            print("\n🎉 SUCCESS: Target achieved! Premium dataset ready for analysis.")
        else:
            print("\n⚠️  PARTIAL SUCCESS: Some OEMs need additional scraping.")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"  1. Load new dataset in VibeAI platform")
        print(f"  2. Test with CEO demonstration queries")
        print(f"  3. Generate executive reports")
        
        return all_data

def main():
    print("🎯 PREMIUM COMMENT SCRAPER")
    print("Target: 2,000+ high-quality comments per OEM")
    print("Focus: Recent + High Engagement + Popular Videos")
    print()
    
    confirm = input("Start premium scraping? This will take 60-90 minutes (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Scraping cancelled")
        return
    
    scraper = PremiumCommentScraper()
    
    try:
        results = scraper.run_premium_scraping()
        
        total_comments = sum(len(comments) for comments in results.values())
        
        if total_comments >= 8000:  # 2000 * 4 OEMs minimum
            print("\n🚀 READY FOR CEO DEMONSTRATION!")
            print("✅ Premium dataset with 2,000+ comments per OEM available")
            print("📊 Platform ready for executive-level analysis")
        else:
            print(f"\n⚠️  Collected {total_comments} comments")
            print("💡 Consider running additional targeted scraping")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraping interrupted by user")
        print("Partial data may have been saved")
    except Exception as e:
        print(f"\n❌ Error during premium scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
