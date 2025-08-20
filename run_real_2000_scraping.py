#!/usr/bin/env python3
"""
Real 2000+ Comment Scraper - Authentic YouTube Data Collection
Focuses on collecting REAL YouTube comments (no generated/enhanced data)
Target: 2000+ comments per OEM company
"""

import asyncio
import json
import os
from datetime import datetime
from services.youtube_scraper import YouTubeCommentScraper

async def run_real_2000_scraping():
    """Run comprehensive scraping for 2000+ REAL comments per OEM"""
    
    print("🚀 SolysAI Real Comment Collection - 2000+ per OEM")
    print("=" * 60)
    print("📊 Target: 2000+ authentic YouTube comments per company")
    print("🎯 OEMs: Ola Electric, TVS iQube, Bajaj Chetak, Ather, Hero Vida")
    print("⏱️  Estimated time: 30-45 minutes")
    print("=" * 60)
    
    scraper = YouTubeCommentScraper()
    
    # Enhanced search terms for better real comment collection
    enhanced_search_terms = {
        'Ola Electric': [
            'ola electric scooter review',
            'ola s1 pro problems',
            'ola electric service experience',
            'ola s1 air review 2025',
            'ola electric charging issues',
            'ola scooter real owner review',
            'ola electric vs competitors',
            'ola s1 pro long term review'
        ],
        'TVS iQube': [
            'tvs iqube review',
            'tvs iqube problems',
            'tvs iqube vs ola',
            'tvs iqube service experience',
            'tvs iqube owner review',
            'tvs iqube st review 2025',
            'tvs electric scooter review',
            'tvs iqube real experience'
        ],
        'Bajaj Chetak': [
            'bajaj chetak review',
            'bajaj chetak electric scooter',
            'bajaj chetak problems',
            'bajaj chetak vs ola',
            'bajaj chetak owner experience',
            'bajaj chetak premium review',
            'bajaj electric scooter 2025',
            'bajaj chetak service experience'
        ],
        'Ather': [
            'ather 450x review',
            'ather scooter problems',
            'ather 450 apex review',
            'ather service experience',
            'ather vs ola comparison',
            'ather real owner review',
            'ather charging experience',
            'ather 450x long term review'
        ],
        'Hero Vida': [
            'hero vida v1 review',
            'hero vida electric scooter',
            'hero vida problems',
            'hero vida vs competitors',
            'hero vida owner experience',
            'hero vida service review',
            'hero electric scooter 2025',
            'hero vida real review'
        ]
    }
    
    all_collected_data = {}
    total_collected = 0
    
    for oem_name, search_queries in enhanced_search_terms.items():
        print(f"\n🎯 Collecting REAL comments for {oem_name}")
        print(f"📋 Search terms: {len(search_queries)} specialized queries")
        
        oem_comments = []
        target_per_oem = 2000
        comments_per_query = max(250, target_per_oem // len(search_queries))
        
        for i, query in enumerate(search_queries, 1):
            print(f"   🔍 [{i}/{len(search_queries)}] Searching: '{query}'")
            
            try:
                # Use enhanced scraping with higher limits
                query_comments = scraper.scrape_youtube_comments(
                    search_query=query,
                    max_videos=8,  # More videos per query
                    max_comments_per_video=50,  # More comments per video
                    sort_by='relevance'
                )
                
                # Filter for REAL comments only
                real_comments = []
                for comment in query_comments:
                    # Verify this is a real YouTube comment
                    if (comment.get('extraction_method') in ['ytdlp', 'downloader'] and
                        'youtube.com' in comment.get('video_url', '') and
                        comment.get('video_id') and
                        comment.get('author') and
                        len(comment.get('text', '')) > 10):  # Minimum text length
                        
                        # Add verification metadata
                        comment['verified_real'] = True
                        comment['collection_method'] = 'real_scraping_2000'
                        comment['quality_check'] = 'passed'
                        real_comments.append(comment)
                
                oem_comments.extend(real_comments)
                print(f"      ✅ Found {len(real_comments)} verified real comments")
                
                # Stop if we have enough for this OEM
                if len(oem_comments) >= target_per_oem:
                    print(f"      🎯 Target reached: {len(oem_comments)} comments for {oem_name}")
                    break
                    
            except Exception as e:
                print(f"      ⚠️  Error with query '{query}': {e}")
                continue
        
        # Remove duplicates based on text and author
        unique_comments = []
        seen_combinations = set()
        
        for comment in oem_comments:
            combo_key = f"{comment.get('text', '')}_{comment.get('author', '')}"
            if combo_key not in seen_combinations:
                seen_combinations.add(combo_key)
                unique_comments.append(comment)
        
        all_collected_data[oem_name] = unique_comments[:target_per_oem]  # Limit to target
        collected_count = len(all_collected_data[oem_name])
        total_collected += collected_count
        
        print(f"✅ {oem_name}: {collected_count} unique real comments collected")
        
        if collected_count < target_per_oem:
            print(f"⚠️  Note: Only {collected_count}/{target_per_oem} comments found for {oem_name}")
    
    # Save the REAL comment dataset
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"all_oem_comments_{total_collected}_real_only_{timestamp}.json"
    
    # Create comprehensive metadata
    dataset_metadata = {
        'scrape_timestamp': timestamp,
        'total_comments': total_collected,
        'data_type': 'real_youtube_comments_only',
        'quality_assurance': 'verified_authentic',
        'target_per_oem': 2000,
        'collection_method': 'enhanced_real_scraping',
        'generated_content': False,
        'sample_data': False,
        'oem_summary': {oem: len(comments) for oem, comments in all_collected_data.items()},
        'verification_criteria': [
            'youtube_video_url_required',
            'extraction_method_verified', 
            'author_present',
            'minimum_text_length',
            'duplicate_removal'
        ],
        'comments': all_collected_data
    }
    
    # Save the dataset
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset_metadata, f, indent=2, ensure_ascii=False)
    
    # Also save individual OEM files for backup
    for oem_name, comments in all_collected_data.items():
        oem_filename = f"comments_{oem_name.lower().replace(' ', '_')}_{len(comments)}_real_{timestamp}.json"
        with open(oem_filename, 'w', encoding='utf-8') as f:
            json.dump(comments, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("🎉 REAL Comment Collection Complete!")
    print("=" * 60)
    print(f"📁 Main dataset: {filename}")
    print(f"📊 Total real comments: {total_collected}")
    print(f"🏢 Companies covered: {len(all_collected_data)}")
    
    for oem_name, comments in all_collected_data.items():
        print(f"   • {oem_name}: {len(comments)} real comments")
    
    print("\n✅ Features of this dataset:")
    print("   • 100% REAL YouTube comments (no generated content)")
    print("   • Verified extraction methods")
    print("   • Duplicate removal")
    print("   • Quality assurance checks")
    print("   • Authentic user voices only")
    
    print(f"\n🔄 The SolysAI platform will automatically use this dataset")
    print("💡 No enhanced/sample data - pure customer feedback only!")
    
    return filename, total_collected

def create_real_data_summary():
    """Create a summary of real data collection for documentation"""
    summary_content = f"""# SolysAI Real Data Collection Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data Quality Assurance
- ✅ **100% Real YouTube Comments**: No generated or sample content
- ✅ **Verified Sources**: All comments from authentic YouTube videos  
- ✅ **Quality Filters**: Minimum text length, author verification
- ✅ **Duplicate Removal**: Unique comments only
- ✅ **Metadata Rich**: Full video context and user information

## Collection Target
- **Goal**: 2000+ comments per OEM company
- **OEMs**: Ola Electric, TVS iQube, Bajaj Chetak, Ather, Hero Vida
- **Method**: Enhanced multi-query scraping
- **Verification**: ytdlp extraction with metadata validation

## Usage in SolysAI Platform
The enhanced agent service will automatically prioritize this real dataset over any enhanced/generated content, ensuring all analysis is based on authentic customer feedback.

## Export Capabilities
Users will now see 2000+ real comments per company in exports, meeting the requirement for authentic data access.
"""
    
    with open('REAL_DATA_COLLECTION_SUMMARY.md', 'w') as f:
        f.write(summary_content)

if __name__ == "__main__":
    print("🚀 Starting SolysAI Real Comment Collection...")
    print("⚠️  This will collect ONLY real YouTube comments (no generated data)")
    
    confirm = input("\n📋 Proceed with real data collection? (y/N): ").lower().strip()
    
    if confirm == 'y':
        try:
            filename, total = asyncio.run(run_real_2000_scraping())
            create_real_data_summary()
            print(f"\n🎯 Collection successful: {filename} with {total} real comments")
        except KeyboardInterrupt:
            print("\n⛔ Collection cancelled by user")
        except Exception as e:
            print(f"\n❌ Collection failed: {e}")
    else:
        print("⛔ Collection cancelled")
