"""
Response Formatting Service for Enhanced Output Readability
Formats responses with proper paragraphs, tables, superscript sources, and structured output
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime


class ResponseFormatter:
    def __init__(self):
        self.source_counter = 1
        self.source_registry = {}
    
    def format_enhanced_response(self, response: str, sources: List[Dict], 
                                query: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the response with Gemini Deep Research style citations and structured output
        """
        # Reset source counter for each response
        self.source_counter = 1
        self.source_registry = {}
        
        # Process and format the main response with Gemini-style citations
        formatted_response, source_references = self._format_gemini_style_response(response, sources)
        
        # Add relevance indicators
        relevance_info = self._generate_relevance_info(metadata)
        
        # Create Gemini-style structured sources section
        sources_section = self._create_gemini_style_sources(sources, source_references, metadata)
        
        # Detect and format tables
        formatted_response = self._format_tables(formatted_response)
        
        # Create final structured output
        final_output = self._create_structured_output(
            formatted_response, sources_section, relevance_info, metadata
        )
        
        return final_output
    
    def _format_gemini_style_response(self, response: str, sources: List[Dict]) -> tuple:
        """Format response with Gemini Deep Research style numbered citations"""
        # Clean existing citation patterns
        response = re.sub(r'<[^>]+>', '', response)
        response = re.sub(r'\^?\[\d+\]', '', response)
        
        # Create source registry with proper categorization
        source_references = {}
        source_counter = 1
        
        # Add numbered citations in Gemini style
        # Pattern: Add citations after factual statements
        citation_patterns = [
            # Market data patterns
            (r'(\d+\.?\d*\s*(?:units?|sales?|revenue|crore|lakh|percent|%)\s*(?:sold|sales?|revenue|growth))', 'Market Intelligence'),
            (r'(market share|sales figures?|revenue growth|financial performance)', 'Market Intelligence'),
            (r'(stock price|IPO|market cap|valuation)', 'Financial Reports'),
            
            # User feedback patterns  
            (r'(users? (?:report|mention|complain|praise)|sentiment analysis|user feedback)', 'Social Media Intelligence'),
            (r'(YouTube comments?|user experiences?|customer reviews?)', 'Social Media Intelligence'),
            (r'(service (?:issues?|problems?|complaints?)|build quality concerns?)', 'Social Media Intelligence'),
            
            # Industry analysis patterns
            (r'(industry (?:reports?|analysis|trends?)|market research)', 'Industry Reports'),
            (r'(electric vehicle (?:market|industry|sector))', 'Industry Reports'),
        ]
        
        formatted_response = response
        used_citations = set()
        
        for pattern, source_type in citation_patterns:
            matches = re.finditer(pattern, formatted_response, re.IGNORECASE)
            for match in matches:
                matched_text = match.group(1)
                if matched_text.lower() not in used_citations:
                    # Add numbered citation
                    citation_key = f"[{source_counter}]"
                    source_references[source_counter] = {
                        'type': source_type,
                        'context': matched_text,
                        'sources': [s for s in sources if source_type.lower() in s.get('type', '').lower()][:1]
                    }
                    
                    # Replace the first occurrence
                    formatted_response = formatted_response.replace(
                        matched_text, 
                        f"{matched_text}{citation_key}", 
                        1
                    )
                    
                    used_citations.add(matched_text.lower())
                    source_counter += 1
                    
                    if source_counter > 10:  # Limit citations
                        break
        
        return formatted_response, source_references
    
    def _format_main_content(self, response: str) -> str:
        """Format the main response content with proper paragraphs and structure"""
        # Split into sentences and create proper paragraphs
        sentences = re.split(r'(?<=[.!?])\s+', response)
        
        formatted_paragraphs = []
        current_paragraph = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            current_paragraph.append(sentence)
            
            # Start new paragraph after sentiment data, conclusions, or transitions
            if any(indicator in sentence.lower() for indicator in [
                'based on analysis', 'in conclusion', 'however', 'furthermore',
                'additionally', 'on the other hand', 'in contrast'
            ]) and len(current_paragraph) >= 2:
                formatted_paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        
        # Add remaining sentences
        if current_paragraph:
            formatted_paragraphs.append(' '.join(current_paragraph))
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _add_source_citations(self, response: str, sources: List[Dict]) -> str:
        """Add superscript citations to the response"""
        # Remove existing citation patterns
        response = re.sub(r'<[^>]+>', '', response)
        
        # Add citations for specific data points
        citation_patterns = [
            (r'(\d+\.?\d*%\s+(?:positive|negative|neutral))', self._get_youtube_citation()),
            (r'(sentiment (?:analysis|data|metrics))', self._get_youtube_citation()),
            (r'(recent (?:feedback|comments|analysis))', self._get_youtube_citation()),
            (r'(YouTube (?:user|comment))', self._get_youtube_citation()),
            (r'(market (?:sentiment|analysis|data))', self._get_search_citation()),
            (r'(stock (?:price|performance|forecast))', self._get_search_citation()),
            (r'(industry (?:report|analysis|trend))', self._get_search_citation()),
        ]
        
        for pattern, citation in citation_patterns:
            response = re.sub(pattern, f'\\1{citation}', response, flags=re.IGNORECASE)
        
        return response
    
    def _get_youtube_citation(self) -> str:
        """Get citation for YouTube sources"""
        if 'youtube' not in self.source_registry:
            self.source_registry['youtube'] = self.source_counter
            self.source_counter += 1
        return f"^[{self.source_registry['youtube']}]"
    
    def _get_search_citation(self) -> str:
        """Get citation for search sources"""
        if 'search' not in self.source_registry:
            self.source_registry['search'] = self.source_counter
            self.source_counter += 1
        return f"^[{self.source_registry['search']}]"
    
    def _format_tables(self, response: str) -> str:
        """Detect and properly format tables in the response"""
        # Look for table patterns and enhance formatting
        table_pattern = r'(\|[^|]+\|(?:\n\|[^|]+\|)*)'
        
        def format_table(match):
            table = match.group(1)
            lines = table.strip().split('\n')
            
            if len(lines) < 2:
                return table
            
            # Enhanced table formatting
            formatted_lines = []
            for i, line in enumerate(lines):
                if i == 0:  # Header
                    formatted_lines.append(f"**{line}**")
                elif i == 1 and '---' in line:  # Separator
                    formatted_lines.append(line)
                else:  # Data rows
                    formatted_lines.append(line)
            
            return '\n' + '\n'.join(formatted_lines) + '\n'
        
        return re.sub(table_pattern, format_table, response, flags=re.MULTILINE)
    
    def _generate_relevance_info(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate information about data sources and relevance"""
        relevance = {
            'data_sources': [],
            'analysis_depth': 'Standard',
            'confidence_level': 'High'
        }
        
        # YouTube data relevance
        if metadata.get('youtube_data_used'):
            comments_count = metadata.get('youtube_comments_analyzed', 0)
            relevance['data_sources'].append({
                'source': 'YouTube Comments',
                'type': 'User Feedback',
                'volume': f"{comments_count:,} comments analyzed",
                'relevance': 'High - Direct customer sentiment'
            })
        
        # Search data relevance  
        if metadata.get('search_results_count', 0) > 0:
            relevance['data_sources'].append({
                'source': 'Google Search (Serper API)',
                'type': 'Industry Intelligence',
                'volume': f"{metadata['search_results_count']} sources",
                'relevance': 'High - Current market data'
            })
        
        # Temporal analysis
        if metadata.get('temporal_analysis'):
            relevance['analysis_depth'] = 'Advanced - Temporal Analysis'
        
        # Conversation context
        if metadata.get('conversation_context_used'):
            relevance['analysis_depth'] = 'Enhanced - Contextual Memory'
        
        return relevance
    
    def _create_sources_section(self, sources: List[Dict], metadata: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Create a structured sources section"""
        structured_sources = {
            'youtube_analysis': [],
            'market_intelligence': [],
            'industry_reports': [],
            'llm_analysis': []
        }
        
        # Categorize sources
        for source in sources:
            url = source.get('url', '').lower()
            title = source.get('title', '').lower()
            
            if 'youtube' in url or 'video' in title:
                structured_sources['youtube_analysis'].append({
                    'title': source.get('title', 'YouTube Analysis'),
                    'description': source.get('snippet', 'User comment analysis'),
                    'type': 'Social Media Intelligence'
                })
            elif any(term in title for term in ['stock', 'price', 'market', 'investment']):
                structured_sources['market_intelligence'].append({
                    'title': source.get('title'),
                    'url': source.get('url'),
                    'description': source.get('snippet'),
                    'type': 'Market Data'
                })
            else:
                structured_sources['industry_reports'].append({
                    'title': source.get('title'),
                    'url': source.get('url'),
                    'description': source.get('snippet'),
                    'type': 'Industry Analysis'
                })
        
        # Add LLM analysis info
        if metadata.get('youtube_data_used') or metadata.get('search_results_count'):
            structured_sources['llm_analysis'].append({
                'title': 'Gemini 2.0 Flash AI Analysis',
                'description': 'Advanced language model analysis combining multiple data sources for comprehensive insights',
                'type': 'AI Intelligence'
            })
        
        return structured_sources
    
    def _create_gemini_style_sources(self, sources: List[Dict], source_references: Dict, 
                                   metadata: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Create Gemini Deep Research style source categorization"""
        structured_sources = {
            'market_intelligence': [],
            'social_media_intelligence': [], 
            'industry_reports': [],
            'financial_reports': [],
            'research_analysis': []
        }
        
        # Process source references from citations
        for ref_num, ref_data in source_references.items():
            source_type = ref_data['type']
            context = ref_data['context']
            source_list = ref_data['sources']
            
            # Create Gemini-style source entry
            for source in source_list:
                gemini_source = {
                    'title': source.get('title', 'Research Source'),
                    'description': f"Referenced for: {context}",
                    'url': source.get('url', ''),
                    'type': source_type,
                    'citation_number': ref_num,
                    'category': self._get_source_category(source_type)
                }
                
                # Add video information if available
                if 'video_title' in source:
                    gemini_source['video_title'] = source['video_title']
                if 'video_url' in source:
                    gemini_source['video_url'] = source['video_url']
                
                # Categorize into appropriate section
                if source_type == 'Market Intelligence':
                    structured_sources['market_intelligence'].append(gemini_source)
                elif source_type == 'Social Media Intelligence':
                    structured_sources['social_media_intelligence'].append(gemini_source)
                elif source_type == 'Industry Reports':
                    structured_sources['industry_reports'].append(gemini_source)
                elif source_type == 'Financial Reports':
                    structured_sources['financial_reports'].append(gemini_source)
        
        # Add remaining uncategorized sources
        for source in sources:
            if not any(source.get('title') == ref_source.get('title') 
                      for ref_data in source_references.values() 
                      for ref_source in ref_data['sources']):
                
                # Determine category based on content
                if 'youtube' in source.get('title', '').lower() or 'comment' in source.get('snippet', '').lower():
                    category = 'social_media_intelligence'
                    source_type = 'Social Media Intelligence'
                elif any(keyword in source.get('title', '').lower() 
                        for keyword in ['market', 'sales', 'revenue', 'industry']):
                    category = 'market_intelligence'
                    source_type = 'Market Intelligence'
                elif any(keyword in source.get('title', '').lower() 
                        for keyword in ['report', 'analysis', 'research']):
                    category = 'industry_reports' 
                    source_type = 'Industry Reports'
                else:
                    category = 'research_analysis'
                    source_type = 'Research Analysis'
                
                structured_sources[category].append({
                    'title': source.get('title', 'Research Source'),
                    'description': source.get('snippet', 'Additional research source'),
                    'url': source.get('url', ''),
                    'type': source_type,
                    'category': self._get_source_category(source_type)
                })
        
        # Add AI analysis metadata
        if metadata.get('youtube_data_used') or metadata.get('search_results_count'):
            structured_sources['research_analysis'].append({
                'title': 'SolysAI Enhanced Analysis',
                'description': f"AI-powered analysis combining {metadata.get('youtube_comments_analyzed', 0)} user comments with {metadata.get('search_results_count', 0)} market intelligence sources",
                'type': 'AI Research Analysis',
                'category': 'AI Intelligence',
                'processing_time': f"{metadata.get('processing_time', 0):.1f}ms"
            })
        
        return structured_sources
    
    def _get_source_category(self, source_type: str) -> str:
        """Get display category for source type"""
        category_mapping = {
            'Market Intelligence': '📊 Market Data',
            'Social Media Intelligence': '💬 User Feedback', 
            'Industry Reports': '📋 Industry Analysis',
            'Financial Reports': '💰 Financial Data',
            'Research Analysis': '🔬 AI Analysis',
            'AI Research Analysis': '🤖 AI Intelligence'
        }
        return category_mapping.get(source_type, '📄 General Research')
    
    def _create_structured_output(self, formatted_response: str, sources_section: Dict, 
                                 relevance_info: Dict, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create the final structured output"""
        return {
            'answer': formatted_response,
            'analysis_summary': {
                'query_type': self._detect_query_type(metadata.get('query', '')),
                'data_sources_used': [ds['source'] for ds in relevance_info['data_sources']],
                'analysis_depth': relevance_info['analysis_depth'],
                'confidence_level': relevance_info['confidence_level'],
                'processing_time_ms': metadata.get('processing_time', 0)
            },
            'data_relevance': relevance_info,
            'structured_sources': sources_section,
            'export_availability': {
                'can_export': metadata.get('exportable', False),
                'export_formats': ['Excel', 'Word'] if metadata.get('exportable') else [],
                'export_description': 'Raw data and detailed analysis available for download'
            },
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'youtube_comments_analyzed': metadata.get('youtube_comments_analyzed', 0),
                'search_sources': metadata.get('search_results_count', 0),
                'temporal_analysis_applied': bool(metadata.get('temporal_analysis')),
                'conversation_context': bool(metadata.get('conversation_context_used'))
            }
        }
    
    def _detect_query_type(self, query: str) -> str:
        """Detect the type of query for better categorization"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['compare', 'vs', 'versus', 'difference']):
            return 'Comparative Analysis'
        elif any(word in query_lower for word in ['sentiment', 'opinion', 'feedback']):
            return 'Sentiment Analysis'
        elif any(word in query_lower for word in ['trend', 'over time', 'historical']):
            return 'Temporal Analysis'
        elif any(word in query_lower for word in ['export', 'download', 'data']):
            return 'Data Export Request'
        else:
            return 'General Intelligence Query'


def create_raw_data_export_endpoint(oem_name: str, format_type: str = 'json') -> Dict[str, Any]:
    """Create an endpoint for raw data export for any OEM"""
    return {
        'endpoint': f'/api/export/raw-data/{oem_name.lower().replace(" ", "-")}',
        'formats': ['json', 'csv', 'excel'],
        'description': f'Export raw YouTube comment data for {oem_name}',
        'parameters': {
            'format': 'Response format (json/csv/excel)',
            'date_range': 'Optional date range filter (YYYY-MM to YYYY-MM)',
            'sentiment_filter': 'Optional sentiment filter (positive/negative/neutral)',
            'limit': 'Maximum number of comments (default: all)'
        }
    }
