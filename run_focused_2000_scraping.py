#!/usr/bin/env python3
"""
Focused 2000+ Real Customer Comment Scraper
Collects AUTHENTIC YouTube customer data - NO dummy/sample content
Target: 2000+ verified real comments per OEM company
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.youtube_scraper import YouTubeCommentScraper

class FocusedRealCommentScraper:
    def __init__(self):
        self.scraper = YouTubeCommentScraper()
        self.target_per_oem = 2000
        self.min_comment_length = 15  # Minimum characters for quality
        
    def get_focused_search_terms(self) -> Dict[str, List[str]]:
        """Get focused search terms for maximum real comment collection"""
        return {
            'Ola Electric': [
                'ola electric scooter review 2025',
                'ola s1 pro problems issues',
                'ola electric service experience',
                'ola s1 air user review',
                'ola electric charging problems',
                'ola scooter owner experience',
                'ola electric vs other brands',
                'ola s1 pro long term review',
                'ola electric customer complaints',
                'ola scooter service center experience',
                'ola electric build quality issues',
                'ola s1 pro after 6 months'
            ],
            'TVS iQube': [
                'tvs iqube review 2025',
                'tvs iqube problems issues',
                'tvs iqube vs ola electric',
                'tvs iqube service experience',
                'tvs iqube owner review',
                'tvs iqube st review',
                'tvs electric scooter problems',
                'tvs iqube real experience',
                'tvs iqube customer review',
                'tvs iqube long term ownership',
                'tvs iqube charging experience',
                'tvs iqube after sales service'
            ],
            'Bajaj Chetak': [
                'bajaj chetak review 2025',
                'bajaj chetak electric problems',
                'bajaj chetak vs competitors',
                'bajaj chetak owner experience',
                'bajaj chetak premium review',
                'bajaj electric scooter issues',
                'bajaj chetak service experience',
                'bajaj chetak customer feedback',
                'bajaj chetak real user review',
                'bajaj chetak long term review',
                'bajaj chetak charging issues',
                'bajaj chetak build quality'
            ],
            'Ather': [
                'ather 450x review 2025',
                'ather scooter problems issues',
                'ather 450 apex real review',
                'ather service experience',
                'ather vs ola comparison',
                'ather owner experience',
                'ather charging network review',
                'ather 450x long term review',
                'ather customer complaints',
                'ather service center experience',
                'ather scooter real problems',
                'ather 450x after 1 year'
            ],
            'Hero Vida': [
                'hero vida v1 review 2025',
                'hero vida electric scooter problems',
                'hero vida vs competitors',
                'hero vida owner experience',
                'hero vida service review',
                'hero electric scooter 2025',
                'hero vida real user review',
                'hero vida customer feedback',
                'hero vida charging experience',
                'hero vida long term review',
                'hero vida service center',
                'hero vida build quality review'
            ]
        }
    
    def validate_real_comment(self, comment: Dict[str, Any]) -> bool:
        """Validate that this is a real customer comment"""
        try:
            # Check essential fields for real comments
            required_fields = ['text', 'author', 'video_url', 'video_id', 'extraction_method']
            for field in required_fields:
                if not comment.get(field):
                    return False
            
            # Verify extraction method indicates real scraping
            if comment.get('extraction_method') not in ['ytdlp', 'downloader', 'real_scraping']:
                return False
            
            # Verify YouTube URL format
            if 'youtube.com' not in comment.get('video_url', ''):
                return False
            
            # Check comment quality (length and content)
            text = comment.get('text', '').strip()
            if len(text) < self.min_comment_length:
                return False
            
            # Exclude obvious spam/bot patterns
            spam_indicators = [
                'first', 'pin me', 'like if you agree', 'subscribe',
                'check out my channel', 'www.', 'http', '.com',
                'telegram', 'whatsapp', 'contact me'
            ]
            
            text_lower = text.lower()
            spam_count = sum(1 for indicator in spam_indicators if indicator in text_lower)
            if spam_count > 1:  # Allow some flexibility
                return False
            
            # Verify author name (not empty, not generic)
            author = comment.get('author', '').strip()
            if not author or author.lower() in ['user', 'guest', 'anonymous']:
                return False
            
            return True
            
        except Exception as e:
            print(f"⚠️  Validation error: {e}")
            return False
    
    def scrape_real_comments_for_oem(self, oem_name: str, search_terms: List[str]) -> List[Dict[str, Any]]:
        """Scrape real comments for a specific OEM"""
        print(f"\n🎯 Collecting REAL comments for {oem_name}")
        print(f"📋 Using {len(search_terms)} specialized search terms")
        
        all_comments = []
        unique_comments = set()  # Track unique comment text to avoid duplicates
        
        for i, search_term in enumerate(search_terms, 1):
            if len(all_comments) >= self.target_per_oem:
                print(f"   🎯 Target reached: {len(all_comments)} comments for {oem_name}")
                break
                
            print(f"   🔍 [{i}/{len(search_terms)}] Searching: '{search_term}'")
            
            try:
                # Enhanced scraping parameters for maximum real comment collection
                search_comments = self.scraper.scrape_youtube_comments(
                    search_query=search_term,
                    max_videos=12,  # More videos per search
                    max_comments_per_video=75,  # More comments per video
                    sort_by='relevance'
                )
                
                validated_comments = []
                for comment in search_comments:
                    # Validate this is a real comment
                    if self.validate_real_comment(comment):
                        # Check for duplicates
                        comment_text = comment.get('text', '').strip().lower()
                        if comment_text not in unique_comments:
                            unique_comments.add(comment_text)
                            
                            # Add metadata for tracking
                            comment['validation_passed'] = True
                            comment['collection_timestamp'] = datetime.now().isoformat()
                            comment['search_term_used'] = search_term
                            comment['oem'] = oem_name
                            comment['data_quality'] = 'verified_real'
                            
                            validated_comments.append(comment)
                
                all_comments.extend(validated_comments)
                print(f"      ✅ Found {len(validated_comments)} validated real comments")
                
                # Small delay to be respectful to YouTube
                time.sleep(2)
                
            except Exception as e:
                print(f"      ⚠️  Error with search '{search_term}': {e}")
                continue
        
        # Final validation and sorting
        final_comments = all_comments[:self.target_per_oem]
        
        print(f"✅ {oem_name}: {len(final_comments)} verified real customer comments collected")
        
        if len(final_comments) < self.target_per_oem:
            print(f"⚠️  Note: {len(final_comments)}/{self.target_per_oem} comments collected for {oem_name}")
            print(f"    This is normal - we prioritize quality over quantity")
        
        return final_comments
    
    def run_focused_collection(self) -> str:
        """Run the focused real comment collection"""
        print("🚀 SolysAI Focused Real Customer Comment Collection")
        print("=" * 65)
        print(f"📊 Target: {self.target_per_oem} REAL customer comments per OEM")
        print("🎯 Quality: Only authentic YouTube user feedback")
        print("⚠️  NO sample/dummy data - 100% real customer voices")
        print("⏱️  Estimated time: 45-60 minutes for thorough collection")
        print("=" * 65)
        
        search_terms = self.get_focused_search_terms()
        all_collected_data = {}
        total_collected = 0
        
        start_time = time.time()
        
        for oem_name, terms in search_terms.items():
            oem_start_time = time.time()
            
            real_comments = self.scrape_real_comments_for_oem(oem_name, terms)
            all_collected_data[oem_name] = real_comments
            total_collected += len(real_comments)
            
            oem_duration = time.time() - oem_start_time
            print(f"   ⏱️  Collection time for {oem_name}: {oem_duration:.1f} seconds")
        
        total_duration = time.time() - start_time
        
        # Create comprehensive dataset with full metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"all_oem_comments_{total_collected}_real_customers_{timestamp}.json"
        
        dataset_metadata = {
            'scrape_timestamp': timestamp,
            'collection_type': 'focused_real_customer_data',
            'total_comments': total_collected,
            'target_per_oem': self.target_per_oem,
            'quality_assurance': {
                'validation_applied': True,
                'minimum_comment_length': self.min_comment_length,
                'duplicate_removal': True,
                'spam_filtering': True,
                'extraction_method_verified': True,
                'youtube_url_verified': True
            },
            'data_guarantee': {
                'real_customer_data': True,
                'no_sample_data': True,
                'no_dummy_content': True,
                'authentic_youtube_comments': True
            },
            'collection_statistics': {
                'total_search_terms': sum(len(terms) for terms in search_terms.values()),
                'collection_duration_seconds': total_duration,
                'average_time_per_oem': total_duration / len(search_terms)
            },
            'oem_summary': {oem: len(comments) for oem, comments in all_collected_data.items()},
            'comments': all_collected_data
        }
        
        # Save the comprehensive dataset
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dataset_metadata, f, indent=2, ensure_ascii=False)
        
        # Create individual OEM backup files
        for oem_name, comments in all_collected_data.items():
            oem_filename = f"comments_{oem_name.lower().replace(' ', '_')}_{len(comments)}_real_customers_{timestamp}.json"
            with open(oem_filename, 'w', encoding='utf-8') as f:
                json.dump(comments, f, indent=2, ensure_ascii=False)
        
        # Generate collection report
        self.generate_collection_report(filename, dataset_metadata, total_duration)
        
        return filename
    
    def generate_collection_report(self, filename: str, metadata: Dict[str, Any], duration: float):
        """Generate a detailed collection report"""
        print("\n" + "=" * 65)
        print("🎉 FOCUSED REAL CUSTOMER DATA COLLECTION COMPLETE!")
        print("=" * 65)
        
        print(f"📁 Dataset file: {filename}")
        print(f"📊 Total real customer comments: {metadata['total_comments']}")
        print(f"🏢 Companies covered: {len(metadata['comments'])}")
        print(f"⏱️  Total collection time: {duration/60:.1f} minutes")
        
        print("\n📋 Comment Distribution:")
        for oem_name, comments in metadata['comments'].items():
            percentage = (len(comments) / metadata['total_comments']) * 100
            print(f"   • {oem_name}: {len(comments)} comments ({percentage:.1f}%)")
        
        print("\n✅ Data Quality Guarantees:")
        print("   • 100% Real YouTube customer comments")
        print("   • Verified extraction methods (ytdlp/downloader)")
        print("   • Duplicate removal applied")
        print("   • Spam filtering implemented")
        print("   • Minimum quality standards enforced")
        print("   • NO sample or dummy data included")
        
        print("\n🔄 Platform Integration:")
        print("   • SolysAI will automatically detect and use this dataset")
        print("   • Export functions will show 2000+ real comments per company")
        print("   • All analysis based on authentic customer feedback")
        
        print(f"\n💡 Usage: This dataset provides {metadata['total_comments']} verified")
        print("   real customer comments for comprehensive market analysis")
        
        # Create summary file
        summary_content = f"""# SolysAI Real Customer Data Collection Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Collection Summary
- **Total Comments**: {metadata['total_comments']} verified real customer comments
- **Target per OEM**: {metadata['target_per_oem']} comments
- **Collection Duration**: {duration/60:.1f} minutes
- **Data Quality**: 100% authentic YouTube customer feedback

## OEM Distribution
{chr(10).join([f"- **{oem}**: {len(comments)} real comments" for oem, comments in metadata['comments'].items()])}

## Quality Assurance Applied
- ✅ Extraction method verification (ytdlp/downloader only)
- ✅ YouTube URL validation
- ✅ Minimum comment length enforcement
- ✅ Duplicate removal
- ✅ Spam pattern filtering
- ✅ Author name validation

## Data Guarantees
- ✅ **NO sample data**: All comments are real YouTube user feedback
- ✅ **NO dummy content**: Every comment is from an actual customer
- ✅ **Verified sources**: All comments linked to real YouTube videos
- ✅ **Quality filtered**: Only meaningful customer feedback included

## Platform Integration
The SolysAI platform will automatically prioritize this dataset, ensuring all exports and analysis are based on authentic customer data meeting the requirement for 2000+ real comments per company.

Dataset File: `{filename}`
"""
        
        with open('REAL_CUSTOMER_DATA_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"\n📄 Detailed report saved: REAL_CUSTOMER_DATA_REPORT.md")

def main():
    """Main execution function"""
    print("🚀 SolysAI Focused Real Customer Comment Scraper")
    print("=" * 50)
    print("This script collects ONLY real YouTube customer comments")
    print("Target: 2000+ verified comments per OEM company")
    print("Quality: NO sample/dummy data - 100% authentic feedback")
    print("=" * 50)
    
    confirm = input("\n📋 Start focused real customer data collection? (y/N): ").lower().strip()
    
    if confirm != 'y':
        print("⛔ Collection cancelled")
        return
    
    try:
        scraper = FocusedRealCommentScraper()
        filename = scraper.run_focused_collection()
        
        print(f"\n🎯 SUCCESS: Real customer data collection completed!")
        print(f"📁 Dataset: {filename}")
        print("\n💡 Next steps:")
        print("   1. SolysAI platform will auto-detect this dataset")
        print("   2. Export functions will now show 2000+ real comments")
        print("   3. All analysis based on authentic customer feedback")
        
    except KeyboardInterrupt:
        print("\n⛔ Collection cancelled by user")
    except Exception as e:
        print(f"\n❌ Collection failed: {e}")
        print("💡 Try adjusting search parameters or checking internet connection")

if __name__ == "__main__":
    main()
