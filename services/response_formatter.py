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
        Format the response with improved readability, proper citations, and structured output
        """
        # Reset source counter for each response
        self.source_counter = 1
        self.source_registry = {}
        
        # Process and format the main response
        formatted_response = self._format_main_content(response)
        
        # Create source citations and references
        formatted_response = self._add_source_citations(formatted_response, sources)
        
        # Add relevance indicators
        relevance_info = self._generate_relevance_info(metadata)
        
        # Create structured sources section
        sources_section = self._create_sources_section(sources, metadata)
        
        # Detect and format tables
        formatted_response = self._format_tables(formatted_response)
        
        # Create final structured output
        final_output = self._create_structured_output(
            formatted_response, sources_section, relevance_info, metadata
        )
        
        return final_output
    
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
