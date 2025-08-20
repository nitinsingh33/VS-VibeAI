"""
Search Service - Handles Google/Serper API integration for web search
"""

import os
import requests
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source: str

class SearchService:
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        self.base_url = 'https://google.serper.dev/search'
        self.max_results = int(os.getenv('MAX_SEARCH_RESULTS', 5))
        self.timeout = int(os.getenv('SEARCH_TIMEOUT', 10))
        
        if not self.api_key:
            print("⚠️ SERPER_API_KEY not found in environment variables")

    async def search(self, query: str, max_results: Optional[int] = None) -> List[SearchResult]:
        """
        Search for information using Serper API
        
        Args:
            query: The search query
            max_results: Maximum number of results to return (optional)
            
        Returns:
            List of SearchResult objects
        """
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not configured")

        try:
            print(f"🔍 Searching for: \"{query}\"")
            
            results_limit = max_results or self.max_results
            
            payload = {
                'q': query,
                'num': results_limit,
                'hl': 'en',
                'gl': 'us'
            }
            
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            results = self._format_search_results(data)
            print(f"✅ Found {len(results)} search results")
            
            return results[:results_limit]
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Search API error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response data: {e.response.text}")
            raise ValueError(f"Search failed: {str(e)}")

    def _format_search_results(self, data: Dict[str, Any]) -> List[SearchResult]:
        """Format raw search results from Serper API"""
        results = []

        # Process knowledge graph if available (highest priority)
        if 'knowledgeGraph' in data:
            kg = data['knowledgeGraph']
            results.append(SearchResult(
                title=kg.get('title', 'Knowledge Graph'),
                url=kg.get('website') or kg.get('source', {}).get('url', ''),
                snippet=kg.get('description', ''),
                source='knowledge_graph'
            ))

        # Process featured snippet if available
        if 'answerBox' in data:
            answer_box = data['answerBox']
            results.append(SearchResult(
                title=answer_box.get('title', 'Featured Snippet'),
                url=answer_box.get('link', ''),
                snippet=answer_box.get('snippet') or answer_box.get('answer', ''),
                source='featured'
            ))

        # Process organic results
        if 'organic' in data:
            for result in data['organic']:
                results.append(SearchResult(
                    title=result.get('title', ''),
                    url=result.get('link', ''),
                    snippet=result.get('snippet', ''),
                    source='organic'
                ))

        return results

    def extract_search_context(self, results: List[SearchResult]) -> Dict[str, Any]:
        """
        Extract context information from search results for LLM processing
        
        Args:
            results: List of SearchResult objects
            
        Returns:
            Dictionary containing context and sources
        """
        if not results:
            return {
                'context': 'No search results found.',
                'sources': []
            }

        # Create context string for LLM
        context_parts = []
        sources = []
        
        for i, result in enumerate(results, 1):
            if result.title and result.snippet:
                context_parts.append(
                    f"Source {i}:\n"
                    f"Title: {result.title}\n"
                    f"Content: {result.snippet}\n"
                    f"URL: {result.url}\n"
                )
                
                sources.append({
                    'title': result.title,
                    'url': result.url,
                    'snippet': result.snippet
                })

        context = '\n---\n'.join(context_parts)
        
        return {
            'context': context,
            'sources': sources
        }

    def is_configured(self) -> bool:
        """Check if the service is properly configured"""
        return bool(self.api_key)
