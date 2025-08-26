"""
Enhanced Agent Service - Combines YouTube Comments with Google Search and Gemini AI
"""

import asyncio
import time
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

from .search_service import SearchService
from .gemini_service import GeminiService
from .youtube_scraper import YouTubeCommentScraper
from .export_service import ExportService
from .temporal_analysis_service import TemporalAnalysisService
from .conversation_memory_service import ConversationMemoryService

class EnhancedAgentService:
    def __init__(self):
        self.search_service = SearchService()
        self.gemini_service = GeminiService()
        self.youtube_scraper = YouTubeCommentScraper()
        self.export_service = ExportService()
        self.temporal_service = TemporalAnalysisService()
        self.memory_service = ConversationMemoryService()
        self.youtube_data_cache = {}

    async def load_youtube_data(self, force_refresh: bool = False, use_enhanced_scraping: bool = False, auto_update: bool = True) -> Dict[str, Any]:
        """Load or refresh YouTube comment data with REAL data priority"""
        
        # Check for newer data files if auto_update is enabled
        if auto_update and self.youtube_data_cache:
            newer_files = self._check_for_newer_data()
            if newer_files:
                print("🔄 Found newer data files, updating cache...")
                force_refresh = True
        
        if not self.youtube_data_cache or force_refresh:
            print("🔄 Loading YouTube comment data...")
            
            if use_enhanced_scraping:
                print("🚀 Running REAL enhanced YouTube scraping for 500+ comments per OEM...")
                print("⚠️  This will collect ACTUAL YouTube comments (10-30 minutes)")
                
                # Run the REAL enhanced scraping
                try:
                    self.youtube_data_cache = self.youtube_scraper.run_enhanced_scraping(target_comments=500)
                    total_comments = sum(len(comments) for comments in self.youtube_data_cache.values())
                    real_comments = sum(len([c for c in comments if c.get('extraction_method') in ['downloader', 'ytdlp']]) 
                                      for comments in self.youtube_data_cache.values())
                    print(f"✅ REAL enhanced scraping completed! Total: {total_comments} comments ({real_comments} confirmed real)")
                except Exception as e:
                    print(f"❌ Enhanced scraping failed: {e}")
                    print("🔄 Falling back to latest scraped data...")
                    existing_files = self._find_latest_scraped_data()
                    if existing_files:
                        self.youtube_data_cache = self._load_latest_scraped_data(existing_files)
                    else:
                        self.youtube_data_cache = self._create_sample_youtube_data()
            else:
                # Try to load existing REAL scraped data first
                existing_files = self._find_latest_scraped_data()
                
                if existing_files:
                    try:
                        self.youtube_data_cache = self._load_latest_scraped_data(existing_files)
                        total_comments = sum(len(comments) for comments in self.youtube_data_cache.values())
                        
                        # Check if this is real scraped data
                        real_comments = 0
                        for comments in self.youtube_data_cache.values():
                            real_comments += len([c for c in comments if (
                                c.get('extraction_method') in ['downloader', 'ytdlp', 'working_scraper'] or
                                c.get('verified_real') == True
                            )])
                        
                        print(f"✅ Loaded latest REAL scraped data: {total_comments} total comments")
                        print(f"🎯 Confirmed real YouTube comments: {real_comments}")
                        
                        if real_comments == 0:
                            print("⚠️  Note: Loaded data may be sample data, not real YouTube comments")
                            print("💡 Run enhanced scraping for real YouTube data")
                        
                    except Exception as e:
                        print(f"⚠️  Error loading scraped data: {e}")
                        self.youtube_data_cache = self._create_sample_youtube_data()
                        print("✅ Using sample data for demonstration")
                else:
                    print("📁 No existing scraped data found")
                    self.youtube_data_cache = self._create_sample_youtube_data()
                    print("✅ Using sample data for demonstration")
                    print("💡 Run 'python run_enhanced_scraping.py' to collect REAL YouTube data")
        
        return self.youtube_data_cache

    def _find_latest_scraped_data(self) -> Optional[Dict[str, str]]:
        """Find the latest scraped data files for each OEM"""
        import os
        import glob
        
        found_files = {}  # Initialize dictionary
        
        # Look for the REAL YouTube comment data (priority order)
        combined_patterns = [
            "all_oem_comments_historical_20250817_170823.json",          # Priority 1: Latest historical data (Aug 17, 5PM)
            "all_oem_comments_historical_*.json",                       # Priority 2: Other historical data files
            "real_youtube_comments_20250817.json",                      # Priority 3: NEW REAL DATA (10,000 authentic comments)
            "real_youtube_comments_*.json",                             # Priority 4: Other real comment files
            "all_oem_comments_7443_real_verified_20250817_013348.json", # Priority 5: Previous real data
            "all_oem_comments_7443_real_verified_*.json",               # Priority 6: Other verified real data
            "all_oem_comments_*_real_verified_*.json",                  # Priority 7: Other verified real data
            "all_oem_comments_2500_total_*.json",                       # Priority 8: Original real data (500 per OEM)  
            "all_oem_comments_*_total_*.json",                          # Priority 9: Other real scraped data
            "all_oem_comments_july2025.json"                            # Priority 10: Legacy real data
        ]
        
        # EXCLUDE enhanced/generated datasets - only use REAL YouTube data
        excluded_patterns = [
            "all_oem_comments_10000_enhanced_*.json",  # Exclude: Enhanced 10K dataset (contains generated data)
            "all_oem_comments_*_enhanced_*.json"       # Exclude: Any enhanced dataset
        ]
        
        # Check for combined files first (REAL data only)
        combined_files = []
        for pattern in combined_patterns:
            potential_files = glob.glob(pattern)
            # Filter out excluded patterns
            for excluded_pattern in excluded_patterns:
                excluded_files = set(glob.glob(excluded_pattern))
                potential_files = [f for f in potential_files if f not in excluded_files]
            combined_files.extend(potential_files)
        
        if combined_files:
            latest_combined = max(combined_files, key=os.path.getctime)
            found_files['_combined'] = latest_combined
            print(f"🎯 Found REAL YouTube data: {latest_combined}")
            print(f"📊 Using authentic user comments only (no generated data)")
        
        # Look for individual OEM files with REAL comments (fallback)
        oem_patterns = {
            'Ola Electric': "comments_ola_electric_*_comments_*.json",
            'TVS iQube': "comments_tvs_iqube_*_comments_*.json", 
            'Bajaj Chetak': "comments_bajaj_chetak_*_comments_*.json",
            'Ather': "comments_ather_*_comments_*.json",
            'Hero Vida': "comments_hero_vida_*_comments_*.json"
        }
        
        # Only load individual files if no combined dataset found
        if '_combined' not in found_files:
            for oem_name, pattern in oem_patterns.items():
                files = glob.glob(pattern)
                if files:
                    # Get the most recent file for this OEM
                    latest_file = max(files, key=os.path.getctime)
                    found_files[oem_name] = latest_file
        
        return found_files if found_files else None

    def _load_latest_scraped_data(self, file_dict: Dict[str, str]) -> Dict[str, List[Dict]]:
        """Load the latest scraped data files with priority for large-scale datasets"""
        combined_data = {}
        
        # Priority 1: Load combined file if available (better for large-scale analysis)
        if '_combined' in file_dict:
            try:
                print(f"📊 Loading large-scale dataset from {file_dict['_combined']}")
                with open(file_dict['_combined'], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle both array format and object format
                if isinstance(data, list):
                    # Array format: group by OEM
                    for comment in data:
                        oem = comment.get('oem', 'Unknown')
                        if oem not in combined_data:
                            combined_data[oem] = []
                        combined_data[oem].append(comment)
                elif isinstance(data, dict):
                    if 'comments' in data:
                        # Metadata format with comments key
                        combined_data = data['comments']
                    else:
                        # Direct OEM mapping or nested historical format
                        combined_data = {}
                        for oem_name, oem_data in data.items():
                            if isinstance(oem_data, list):
                                # Flat format: OEM -> [comments]
                                combined_data[oem_name] = oem_data
                            elif isinstance(oem_data, dict):
                                # Nested format: OEM -> Year -> Month -> [comments]
                                oem_comments = []
                                for year, year_data in oem_data.items():
                                    if isinstance(year_data, dict):
                                        for month, comments in year_data.items():
                                            if isinstance(comments, list):
                                                oem_comments.extend(comments)
                                    elif isinstance(year_data, list):
                                        oem_comments.extend(year_data)
                                combined_data[oem_name] = oem_comments
                
                # Report statistics - focus on REAL comment verification
                total_comments = sum(len(comments) for comments in combined_data.values())
                real_count = 0
                for oem_comments in combined_data.values():
                    # Count ONLY verified real YouTube comments (exclude any generated data)
                    real_count += len([c for c in oem_comments if (
                        c.get('extraction_method') in ['downloader', 'ytdlp', 'real_scraping', 'working_scraper'] or
                        c.get('verified_real') == True or
                        ('youtube.com' in c.get('video_url', '') and c.get('video_id') and len(c.get('video_id', '')) > 5) or
                        (c.get('video_id') and c.get('author') and c.get('text'))  # Real YouTube format
                    )])
                
                print(f"✅ Loaded {total_comments} total comments across {len(combined_data)} OEMs")
                print(f"🎯 VERIFIED REAL YouTube comments: {real_count}")
                print(f"⚠️  Only authentic user feedback included (no generated content)")
                
                # Filter out any potentially enhanced/generated comments if they exist
                filtered_data = {}
                for oem_name, comments in combined_data.items():
                    real_comments = []
                    for comment in comments:
                        # Include if it has proper YouTube metadata, extraction method, or verified_real flag
                        if (comment.get('extraction_method') in ['downloader', 'ytdlp', 'real_scraping', 'working_scraper'] or
                            comment.get('verified_real') == True or
                            ('youtube.com' in comment.get('video_url', '') and 
                             comment.get('video_id') and
                             comment.get('author')) or
                            (comment.get('video_id') and len(comment.get('video_id', '')) > 5 and comment.get('author'))):  # Real YouTube format
                            real_comments.append(comment)
                    
                    if real_comments:
                        filtered_data[oem_name] = real_comments
                        print(f"📊 {oem_name}: {len(real_comments)} verified real comments")
                
                return filtered_data
                
            except Exception as e:
                print(f"⚠️  Error loading combined file: {e}")
        
        # Priority 2: Load individual OEM files (fallback)
        for oem_name, filename in file_dict.items():
            if oem_name == '_combined':
                continue
                
            try:
                print(f"📁 Loading {oem_name} data from {filename}")
                with open(filename, 'r', encoding='utf-8') as f:
                    comments = json.load(f)
                    combined_data[oem_name] = comments
                    real_count = len([c for c in comments if c.get('extraction_method') in ['downloader', 'ytdlp']])
                    print(f"✅ Loaded {len(comments)} comments for {oem_name} ({real_count} confirmed real)")
            except Exception as e:
                print(f"⚠️  Error loading {filename}: {e}")
        
        return combined_data
    
    def _check_for_newer_data(self) -> bool:
        """Check if there are newer data files available"""
        import os
        current_files = self._find_latest_scraped_data()
        
        if not current_files or not hasattr(self, '_last_loaded_files'):
            self._last_loaded_files = current_files
            return True
            
        # Check if any file has been modified
        for oem_name, filename in current_files.items():
            if oem_name not in self._last_loaded_files:
                print(f"🆕 New data file found for {oem_name}: {filename}")
                return True
            
            old_file = self._last_loaded_files[oem_name]
            if filename != old_file:
                print(f"🔄 Updated data file for {oem_name}: {filename}")
                return True
                
            # Check modification time
            try:
                current_mtime = os.path.getmtime(filename)
                if not hasattr(self, '_file_mtimes'):
                    self._file_mtimes = {}
                
                old_mtime = self._file_mtimes.get(filename, 0)
                if current_mtime > old_mtime:
                    print(f"📝 Modified data detected for {oem_name}")
                    self._file_mtimes[filename] = current_mtime
                    return True
                    
            except Exception as e:
                print(f"⚠️  Error checking file time for {filename}: {e}")
                
        return False
    
    def _extract_comments_for_export(self, query: str, youtube_data: Dict[str, List[Dict]]) -> List[Dict]:
        """Extract comments relevant to query for export"""
        relevant_comments = []
        query_lower = query.lower()
        keywords = query_lower.split()
        
        # Check if user wants ALL comments for a specific OEM
        oem_mapping = {
            'ola': 'Ola Electric',
            'ola electric': 'Ola Electric',
            'tvs': 'TVS iQube',
            'tvs iqube': 'TVS iQube',
            'iqube': 'TVS iQube',
            'bajaj': 'Bajaj Chetak',
            'bajaj chetak': 'Bajaj Chetak',
            'chetak': 'Bajaj Chetak',
            'ather': 'Ather',
            'hero': 'Hero Vida',
            'hero vida': 'Hero Vida',
            'vida': 'Hero Vida'
        }
        
        # Check if user wants all comments for a specific OEM
        target_oem = None
        for oem_key, oem_name in oem_mapping.items():
            if oem_key in query_lower:
                target_oem = oem_name
                break
        
        # Check for various patterns indicating user wants ALL comments
        all_comments_patterns = [
            'all comments', 'all 500', '500 comments', 'all 2000', '2000 comments',
            'all 2,000', '2,000 comments', 'all 2500', '2500 comments', 
            'all 2,500', '2,500 comments', 'complete dataset', 'full dataset',
            'entire dataset', 'export all', 'download all', 'all data', 'export data',
            'premium data', 'full export', 'complete export', 'maximum data'
        ]
        
        wants_all_comments = any(phrase in query_lower for phrase in all_comments_patterns)
        
        # If requesting ALL comments for specific OEM
        if target_oem and wants_all_comments:
            if target_oem in youtube_data:
                print(f"📊 Extracting ALL {len(youtube_data[target_oem])} comments for {target_oem}")
                for comment in youtube_data[target_oem]:
                    comment_export = comment.copy()
                    comment_export['relevance_score'] = 10  # High relevance for all comments
                    comment_export['export_timestamp'] = datetime.now().isoformat()
                    relevant_comments.append(comment_export)
                return relevant_comments
        
        # If requesting ALL comments from ALL OEMs (2500 total)
        if wants_all_comments and not target_oem:
            print(f"📊 Extracting ALL comments from ALL OEMs (Full Dataset)")
            for oem_name, comments in youtube_data.items():
                print(f"📁 Adding {len(comments)} comments from {oem_name}")
                for comment in comments:
                    comment_export = comment.copy()
                    comment_export['relevance_score'] = 10  # High relevance for all comments
                    comment_export['export_timestamp'] = datetime.now().isoformat()
                    comment_export['oem'] = oem_name  # Add OEM identifier for full dataset
                    relevant_comments.append(comment_export)
            print(f"✅ Total comments extracted: {len(relevant_comments)}")
            return relevant_comments
        
        # Otherwise, extract relevant comments based on keywords
        for oem_name, comments in youtube_data.items():
            # If specific OEM mentioned, prioritize that OEM
            oem_boost = 5 if target_oem == oem_name else 0
            
            for comment in comments:
                comment_text = comment.get('text', '').lower()
                relevance_score = sum(1 for keyword in keywords if keyword in comment_text) + oem_boost
                
                if relevance_score > 0 or oem_name.lower() in query_lower:
                    comment_export = comment.copy()
                    comment_export['relevance_score'] = relevance_score
                    comment_export['export_timestamp'] = datetime.now().isoformat()
                    comment_export['oem'] = oem_name  # Add OEM identifier
                    relevant_comments.append(comment_export)
        
        # Sort by relevance and return appropriate number
        relevant_comments.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Enhanced logic for determining how many comments to return
        if wants_all_comments:
            print(f"📊 Returning ALL {len(relevant_comments)} relevant comments (user requested full dataset)")
            return relevant_comments  # Return ALL relevant comments
        elif any(phrase in query_lower for phrase in ['2000', 'two thousand', '2,000']):
            return relevant_comments[:2000]  # Return up to 2000
        elif any(phrase in query_lower for phrase in ['1500', 'fifteen hundred', '1,500']):
            return relevant_comments[:1500]  # Return up to 1500
        elif any(phrase in query_lower for phrase in ['1000', 'thousand', '1,000']):
            return relevant_comments[:1000]  # Return up to 1000
        elif any(phrase in query_lower for phrase in ['500', 'five hundred']):
            return relevant_comments[:500]  # Return up to 500
        else:
            return relevant_comments[:2000]  # Default to maximum available for premium experience
    
    def _generate_query_statistics(self, query: str, youtube_data: Dict[str, List[Dict]]) -> List[Dict]:
        """Generate statistics for the query"""
        stats = []
        total_comments = sum(len(comments) for comments in youtube_data.values())
        
        for oem_name, comments in youtube_data.items():
            oem_stats = {
                'OEM': oem_name,
                'Total_Comments': len(comments),
                'Percentage_of_Dataset': round((len(comments) / total_comments) * 100, 2),
                'Avg_Likes': round(sum(c.get('likes', 0) for c in comments) / len(comments), 2) if comments else 0,
                'Latest_Comment': max((c.get('date', '') for c in comments), default='Unknown'),
                'Query_Relevant': len([c for c in comments if any(word in c.get('text', '').lower() 
                                     for word in query.lower().split())])
            }
            stats.append(oem_stats)
        
        return stats
    
    def _generate_export_summary(self, query: str, response: str) -> str:
        """Generate executive summary for export"""
        summary_lines = [
            f"Query Analysis: {query}",
            f"Generated on: {datetime.now().strftime('%B %d, %Y')}",
            "",
            "Key Insights:",
        ]
        
        # Extract key sentences from response (simple approach)
        sentences = response.split('.')
        key_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 20]
        
        for sentence in key_sentences:
            summary_lines.append(f"• {sentence}")
        
        return '\n'.join(summary_lines)

    def _create_sample_youtube_data(self) -> Dict[str, List[Dict]]:
        """Create sample YouTube comment data for demonstration"""
        sample_data = {
            'Ola Electric': [
                {
                    'text': 'The S1 Pro has amazing acceleration but the charging infrastructure needs improvement',
                    'author': 'BikeEnthusiast2025',
                    'likes': 45,
                    'date': '2025-07-15 14:30:00',
                    'video_title': 'Ola S1 Pro Long Term Review',
                    'video_url': 'https://youtube.com/watch?v=sample1',
                    'oem': 'Ola Electric'
                },
                {
                    'text': 'Build quality issues still persist. Had to visit service center 3 times',
                    'author': 'TechReviewer',
                    'likes': 23,
                    'date': '2025-07-20 10:15:00',
                    'video_title': 'Ola Electric Problems',
                    'video_url': 'https://youtube.com/watch?v=sample2',
                    'oem': 'Ola Electric'
                }
            ],
            'TVS iQube': [
                {
                    'text': 'TVS has the most reliable electric scooter. No issues in 6 months',
                    'author': 'DailyCommuter',
                    'likes': 67,
                    'date': '2025-07-12 16:45:00',
                    'video_title': 'TVS iQube Ownership Experience',
                    'video_url': 'https://youtube.com/watch?v=sample3',
                    'oem': 'TVS iQube'
                }
            ],
            'Bajaj Chetak': [
                {
                    'text': 'Chetak has premium feel but range is limited compared to competitors',
                    'author': 'ScooterExpert',
                    'likes': 34,
                    'date': '2025-07-18 09:20:00',
                    'video_title': 'Bajaj Chetak Detailed Review',
                    'video_url': 'https://youtube.com/watch?v=sample4',
                    'oem': 'Bajaj Chetak'
                }
            ],
            'Ather': [
                {
                    'text': 'Ather 450X performance is outstanding. Best in class features',
                    'author': 'ElectricVehicleFan',
                    'likes': 89,
                    'date': '2025-07-25 11:30:00',
                    'video_title': 'Ather 450X Performance Test',
                    'video_url': 'https://youtube.com/watch?v=sample5',
                    'oem': 'Ather'
                }
            ],
            'Hero Vida': [
                {
                    'text': 'New entrant but showing promise. Needs more charging stations',
                    'author': 'MotorCycleNews',
                    'likes': 56,
                    'date': '2025-07-22 13:15:00',
                    'video_title': 'Hero Vida First Impressions',
                    'video_url': 'https://youtube.com/watch?v=sample6',
                    'oem': 'Hero Vida'
                }
            ]
        }
        return sample_data

    async def process_enhanced_query(self, query: str, use_youtube_data: bool = True, max_search_results: int = 5) -> Dict[str, Any]:
        """
        Process query using YouTube comments, Google search, Gemini AI, temporal analysis, and conversation memory
        """
        try:
            start_time = time.time()
            print(f"🚀 Processing enhanced query: \"{query}\"")

            # Step 1: Check conversation memory for context
            conversation_context = self.memory_service.get_conversation_context(last_n=3)
            relevant_history = self.memory_service.get_relevant_history(query, max_relevant=2)
            
            # Step 2: Check for temporal analysis requests
            time_period = self.temporal_service.extract_time_period(query)
            temporal_analysis_data = None
            
            # Step 3: Load YouTube data if requested
            youtube_context = ""
            youtube_summary = ""
            if use_youtube_data:
                youtube_data = await self.load_youtube_data()
                youtube_summary = self.youtube_scraper.get_oem_summary(youtube_data)
                
                # Apply temporal filtering if time period specified
                if time_period:
                    print(f"🕒 Applying temporal filter: {time_period['description']}")
                    filtered_youtube_data = {}
                    
                    for oem_name, comments in youtube_data.items():
                        filtered_comments = self.temporal_service.filter_comments_by_time_period(comments, time_period)
                        if filtered_comments:
                            filtered_youtube_data[oem_name] = filtered_comments
                    
                    if filtered_youtube_data:
                        youtube_data = filtered_youtube_data
                        temporal_analysis_data = self._perform_temporal_analysis(youtube_data, time_period)
                        print(f"📊 Temporal analysis completed for {len(filtered_youtube_data)} OEMs")
                    else:
                        print("⚠️ No comments found for specified time period")
                
                youtube_context = self._extract_relevant_youtube_comments(query, youtube_data)

            # Step 4: Perform Google search
            search_results = []
            search_context = ""
            try:
                search_results = await self.search_service.search(query, max_search_results)
                if search_results:
                    search_data = self.search_service.extract_search_context(search_results)
                    search_context = search_data['context']
            except Exception as e:
                print(f"⚠️ Search failed: {e}")

            # Step 5: Combine contexts with memory and temporal data
            combined_context = self._combine_enhanced_contexts(
                query, youtube_context, search_context, youtube_summary, 
                conversation_context, temporal_analysis_data, time_period
            )

            # Step 6: Generate response using Gemini
            response = await self.gemini_service.generate_response(query, combined_context)

            processing_time = (time.time() - start_time) * 1000

            # Step 7: Prepare sources with improved formatting
            sources = []
            
            # Add search sources
            if search_results:
                search_context_data = self.search_service.extract_search_context(search_results)
                sources.extend(search_context_data['sources'])

            # Add YouTube sources
            if youtube_context:
                youtube_sources = self._extract_youtube_sources(youtube_data, query)
                sources.extend(youtube_sources)

            # Step 8: Check for export opportunities
            export_files = {}
            should_export = self.export_service.detect_tabular_query(query, response)
            
            if should_export:
                # Extract relevant comments for export
                relevant_comments = self._extract_comments_for_export(query, youtube_data)
                
                export_data = {
                    'query': query,
                    'analysis': response,
                    'comments_data': relevant_comments,
                    'sources': sources,
                    'statistics': self._generate_query_statistics(query, youtube_data),
                    'summary': self._generate_export_summary(query, response),
                    'temporal_analysis': temporal_analysis_data,
                    'time_period': time_period,
                    'timestamp': datetime.now().isoformat()
                }
                
                try:
                    # Create Excel export
                    excel_file = self.export_service.create_excel_export(export_data)
                    export_files['excel'] = excel_file
                    
                    # Create Word export
                    word_file = self.export_service.create_word_export(export_data)
                    export_files['word'] = word_file
                    
                    print(f"📊 Export files created: {len(export_files)} files")
                except Exception as e:
                    print(f"⚠️ Export creation failed: {e}")

            # Step 9: Save interaction to memory
            interaction_metadata = {
                'time_period': time_period,
                'temporal_analysis': bool(temporal_analysis_data),
                'export_generated': bool(export_files),
                'youtube_data_used': bool(youtube_context),
                'search_results_count': len(search_results)
            }
            
            self.memory_service.add_interaction(query, response, interaction_metadata)

            result = {
                'query': query,
                'response': response,
                'sources': sources,
                'youtube_data_used': bool(youtube_context),
                'search_results_count': len(search_results),
                'youtube_comments_analyzed': len(youtube_context.split('\n\n')) if youtube_context else 0,
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat(),
                'export_files': export_files,
                'exportable': should_export,
                'temporal_analysis': temporal_analysis_data,
                'time_period': time_period,
                'conversation_context_used': bool(conversation_context),
                'relevant_history_count': len(relevant_history)
            }

            print(f"✅ Enhanced query processed in {processing_time:.2f}ms")
            return result

        except Exception as e:
            print(f"❌ Enhanced processing error: {e}")
            raise

    def _extract_relevant_youtube_comments(self, query: str, youtube_data: Dict[str, List[Dict]], max_comments: int = 50) -> str:
        """Extract relevant YouTube comments based on query with improved relevance scoring"""
        all_relevant_comments = []
        query_lower = query.lower()
        
        # Enhanced keywords extraction
        keywords = query_lower.split()
        
        # Add common variations and synonyms
        keyword_variants = {
            'service': ['support', 'maintenance', 'repair', 'issue', 'problem'],
            'battery': ['range', 'charging', 'charge', 'power', 'electric'],
            'price': ['cost', 'expensive', 'cheap', 'value', 'money'],
            'quality': ['build', 'reliability', 'durable', 'performance'],
            'compare': ['vs', 'versus', 'better', 'best', 'competition']
        }
        
        # Expand keywords with variants
        expanded_keywords = set(keywords)
        for keyword in keywords:
            if keyword in keyword_variants:
                expanded_keywords.update(keyword_variants[keyword])
        
        for oem_name, comments in youtube_data.items():
            oem_mentioned = oem_name.lower() in query_lower
            
            for comment in comments:
                comment_text = comment.get('text', '').lower()
                
                # Calculate relevance score
                relevance_score = 0
                
                # Direct keyword matches (highest weight)
                for keyword in expanded_keywords:
                    if keyword in comment_text:
                        relevance_score += 3
                
                # OEM mention bonus
                if oem_mentioned:
                    relevance_score += 2
                
                # Check for sentiment indicators
                positive_words = ['good', 'great', 'excellent', 'best', 'amazing', 'love', 'recommend']
                negative_words = ['bad', 'worst', 'terrible', 'issue', 'problem', 'defect', 'poor', 'disappointing']
                
                sentiment_score = 0
                for word in positive_words:
                    if word in comment_text:
                        sentiment_score += 1
                for word in negative_words:
                    if word in comment_text:
                        sentiment_score += 1
                
                relevance_score += min(sentiment_score, 2)  # Cap sentiment bonus
                
                # Length bonus for detailed comments
                if len(comment_text) > 100:
                    relevance_score += 1
                
                # Engagement bonus (likes)
                likes = comment.get('likes', 0)
                if likes > 5:
                    relevance_score += 1
                if likes > 20:
                    relevance_score += 1
                
                # Include comment if relevant
                if relevance_score > 0:
                    all_relevant_comments.append({
                        'comment': comment,
                        'oem': oem_name,
                        'relevance': relevance_score
                    })
        
        # Sort by relevance score (descending)
        all_relevant_comments.sort(key=lambda x: x['relevance'], reverse=True)
        
        # Format top comments
        formatted_comments = []
        for item in all_relevant_comments[:max_comments]:
            comment = item['comment']
            oem_name = item['oem']
            
            formatted_comment = (
                f"**{oem_name} User Feedback (Relevance: {item['relevance']}, {comment.get('date', 'Unknown')}):**\n"
                f"Comment: {comment.get('text', '')}\n"
                f"Author: {comment.get('author', 'Anonymous')}\n"
                f"Likes: {comment.get('likes', 0)}\n"
                f"Video: {comment.get('video_title', 'YouTube Video')}\n"
                f"Source: {comment.get('video_url', 'N/A')}"
            )
            formatted_comments.append(formatted_comment)
        
        result = '\n\n---\n\n'.join(formatted_comments)
        
        # Add summary statistics
        if formatted_comments:
            oem_counts = {}
            for item in all_relevant_comments[:max_comments]:
                oem = item['oem']
                oem_counts[oem] = oem_counts.get(oem, 0) + 1
            
            summary = f"\n\n=== ANALYSIS SUMMARY ===\n"
            summary += f"Total relevant comments analyzed: {len(formatted_comments)}\n"
            summary += f"Comments per OEM: {', '.join([f'{oem}: {count}' for oem, count in oem_counts.items()])}\n"
            summary += f"Average relevance score: {sum(item['relevance'] for item in all_relevant_comments[:max_comments]) / len(formatted_comments):.1f}"
            
            result += summary
        
        return result

    def _extract_youtube_sources(self, youtube_data: Dict[str, List[Dict]], query: str) -> List[Dict]:
        """Extract YouTube video sources"""
        sources = []
        seen_urls = set()
        
        for oem_name, comments in youtube_data.items():
            for comment in comments:
                video_url = comment.get('video_url', '')
                video_title = comment.get('video_title', '')
                
                if video_url and video_url not in seen_urls:
                    sources.append({
                        'title': f"{video_title} (YouTube)",
                        'url': video_url,
                        'snippet': f"User comments about {oem_name} from July 2025"
                    })
                    seen_urls.add(video_url)
                    
                    if len(sources) >= 5:  # Limit YouTube sources
                        break
        
        return sources

    def _combine_enhanced_contexts(self, query: str, youtube_context: str, search_context: str, 
                                 youtube_summary: str, conversation_context: str = "", 
                                 temporal_analysis: Dict[str, Any] = None, 
                                 time_period: Dict[str, Any] = None) -> str:
        """Combine all contexts including memory and temporal data for Gemini"""
        
        context_parts = [
            f"USER QUERY: {query}",
            ""
        ]
        
        # Add conversation context if available
        if conversation_context:
            context_parts.extend([
                conversation_context,
                ""
            ])
        
        # Add temporal analysis if available
        if temporal_analysis and time_period:
            temporal_summary = self.temporal_service.generate_temporal_summary(temporal_analysis, time_period)
            context_parts.extend([
                "=== TEMPORAL ANALYSIS RESULTS ===",
                temporal_summary,
                ""
            ])
        
        context_parts.extend([
            "=== REAL YOUTUBE USER FEEDBACK DATA (August 2025) ===",
            f"Dataset: 2,500+ verified comments from Indian EV users",
            youtube_summary if youtube_summary else "No YouTube data available",
            ""
        ])
        
        if youtube_context:
            context_parts.extend([
                "=== RELEVANT USER COMMENTS WITH SOURCES ===",
                youtube_context,
                ""
            ])
        
        if search_context:
            context_parts.extend([
                "=== CURRENT WEB SEARCH RESULTS WITH SOURCES ===",
                search_context,
                ""
            ])
        
        # Enhanced instructions with temporal and memory awareness
        context_parts.append("""
=== ENHANCED RESPONSE INSTRUCTIONS ===
You are an expert Indian electric two-wheeler market analyst with memory and temporal analysis capabilities. Follow these strict guidelines:

1. **QUERY FOCUS**: Answer ONLY the specific question asked. Use conversation context to provide continuity.

2. **TEMPORAL AWARENESS**: If time period is specified, focus analysis on that period. Compare with other periods if relevant.

3. **MANDATORY CITATIONS**: After every factual statement, add source in format:
   - YouTube comments: <YouTube_Comments_[OEM_Name]>
   - Web search: <Web_Search_[Domain]>
   - Video data: <Video_[Title_Summary]>
   - Temporal analysis: <Temporal_Analysis_[Period]>
   - Previous conversation: <Conversation_Context>

4. **RESPONSE STRUCTURE**:
   - Direct answer to query (1-2 sentences)
   - Temporal insights (if time period specified)
   - Supporting evidence with sources
   - Key insights with context from conversation history
   - Conclusion/recommendation (if applicable)

5. **MEMORY INTEGRATION**: Reference previous discussions when relevant. Build on established context.

6. **BRAND STRENGTH ANALYSIS**: When analyzing brand performance, consider temporal trends and conversation history.

7. **TABLE DETECTION**: If query asks for comparison/ranking/list, format as table with clear headers.

EXAMPLE PROPER CITATION WITH TEMPORAL DATA:
"In August 2024, Ola Electric users frequently reported service delays <YouTube_Comments_Ola_Electric><Temporal_Analysis_August_2024>. This represents a 15% increase from our previous discussion about July 2024 performance <Conversation_Context>."

Please provide a focused, well-sourced response that directly addresses the user's specific question with full awareness of conversation history and temporal context.
""")
        
        return '\n'.join(context_parts)

    def _perform_temporal_analysis(self, youtube_data: Dict[str, List[Dict]], 
                                 time_period: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive temporal analysis on filtered data"""
        analysis_results = {}
        
        for oem_name, comments in youtube_data.items():
            # Sentiment analysis for the time period
            sentiment_metrics = self.temporal_service._calculate_sentiment_metrics(comments)
            
            # Brand strength analysis
            brand_strength = self.temporal_service.calculate_brand_strength(comments)
            
            # Comment categorization
            categories = self._categorize_comments(comments)
            
            analysis_results[oem_name] = {
                'comment_count': len(comments),
                'sentiment_metrics': sentiment_metrics,
                'brand_strength': brand_strength,
                'categories': categories,
                'time_period': time_period['description']
            }
        
        return analysis_results

    def _categorize_comments(self, comments: List[Dict]) -> Dict[str, int]:
        """Categorize comments by topic"""
        categories = {
            'service': 0,
            'battery_range': 0,
            'performance': 0,
            'price_value': 0,
            'build_quality': 0,
            'charging': 0,
            'features': 0,
            'comparison': 0,
            'general': 0
        }
        
        category_keywords = {
            'service': ['service', 'support', 'maintenance', 'repair', 'center', 'technician'],
            'battery_range': ['battery', 'range', 'mileage', 'distance', 'km'],
            'performance': ['performance', 'speed', 'acceleration', 'power', 'torque'],
            'price_value': ['price', 'cost', 'expensive', 'cheap', 'value', 'money', 'worth'],
            'build_quality': ['quality', 'build', 'material', 'plastic', 'metal', 'finish'],
            'charging': ['charging', 'charger', 'charge', 'plug', 'station'],
            'features': ['feature', 'technology', 'smart', 'app', 'connectivity'],
            'comparison': ['compare', 'vs', 'versus', 'better', 'best', 'than']
        }
        
        for comment in comments:
            text = comment.get('text', '').lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(keyword in text for keyword in keywords):
                    categories[category] += 1
                    categorized = True
                    break
            
            if not categorized:
                categories['general'] += 1
        
        return categories

    async def get_temporal_brand_analysis(self, oem_name: str, time_periods: List[str]) -> Dict[str, Any]:
        """Get brand analysis across multiple time periods"""
        youtube_data = await self.load_youtube_data()
        
        if oem_name not in youtube_data:
            return {'error': f'OEM {oem_name} not found in dataset'}
        
        results = {}
        
        for period_str in time_periods:
            # Parse time period
            time_period = self.temporal_service.extract_time_period(f"analysis for {period_str}")
            
            if time_period:
                # Filter comments for this period
                filtered_comments = self.temporal_service.filter_comments_by_time_period(
                    youtube_data[oem_name], time_period
                )
                
                if filtered_comments:
                    # Perform analysis
                    sentiment_metrics = self.temporal_service._calculate_sentiment_metrics(filtered_comments)
                    brand_strength = self.temporal_service.calculate_brand_strength(filtered_comments)
                    
                    results[period_str] = {
                        'comment_count': len(filtered_comments),
                        'sentiment_metrics': sentiment_metrics,
                        'brand_strength': brand_strength,
                        'time_period': time_period
                    }
        
        return results

    def get_conversation_summary(self) -> str:
        """Get summary of current conversation"""
        return self.memory_service.get_memory_summary()

    def clear_conversation_memory(self):
        """Clear conversation memory"""
        self.memory_service.clear_session()

    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences based on conversation history"""
        return self.memory_service.get_user_preferences()

    async def get_youtube_analytics(self) -> Dict[str, Any]:
        """Get analytics from YouTube comment data"""
        youtube_data = await self.load_youtube_data()
        
        analytics = {}
        total_comments = 0
        
        for oem_name, comments in youtube_data.items():
            analysis = self.youtube_scraper.analyze_comments(comments)
            analytics[oem_name] = analysis
            total_comments += len(comments)
        
        analytics['overall'] = {
            'total_oems': len(youtube_data),
            'total_comments': total_comments,
            'data_collection_period': 'July 2025'
        }
        
        return analytics

    def get_health_status(self) -> Dict[str, Any]:
        """Get enhanced health status including all services"""
        base_status = {
            'search_service': {
                'configured': self.search_service.is_configured(),
                'status': 'ready' if self.search_service.is_configured() else 'not_configured',
                'api_key_present': bool(self.search_service.api_key)
            },
            'gemini_service': {
                'configured': self.gemini_service.is_configured(),
                'status': 'ready' if self.gemini_service.is_configured() else 'not_configured',
                'api_key_present': bool(self.gemini_service.api_key),
                'model_initialized': bool(self.gemini_service.model)
            },
            'youtube_scraper': {
                'configured': True,
                'status': 'ready',
                'cached_data': bool(self.youtube_data_cache),
                'supported_oems': list(self.youtube_scraper.oems.keys())
            },
            'temporal_analysis': {
                'configured': True,
                'status': 'ready',
                'supported_periods': ['month', 'quarter', 'year', 'duration', 'specific_date'],
                'analysis_types': ['sentiment', 'brand_strength', 'categorization']
            },
            'conversation_memory': {
                'configured': True,
                'status': 'ready',
                'conversation_count': len(self.memory_service.conversation_history),
                'session_active': bool(self.memory_service.session_context),
                'memory_file_exists': os.path.exists(self.memory_service.memory_file)
            }
        }
        
        return base_status
