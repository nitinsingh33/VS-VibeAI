"""
Agent Service - Main orchestrator that coordinates search and response generation
"""

import asyncio
import time
from typing import Dict, Any, Optional
from datetime import datetime

from .search_service import SearchService
from .gemini_service import GeminiService

class AgentService:
    def __init__(self):
        self.search_service = SearchService()
        self.gemini_service = GeminiService()

    async def process_query(self, query: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """
        Process a user query by searching for information and generating a response
        
        Args:
            query: The user's query
            max_results: Maximum number of search results to use
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Validate the query
            validated_query = self.validate_query(query)
            
            print(f"🚀 Processing query: \"{validated_query}\"")
            start_time = time.time()

            # Step 1: Search for relevant information
            try:
                search_results = await self.search_service.search(validated_query, max_results)
            except Exception as search_error:
                print(f"🔄 Search failed: {search_error}")
                return await self._generate_fallback_response(validated_query, str(search_error))

            # Step 2: Check if we got any results
            if not search_results:
                print('⚠️ No search results found, generating response from LLM knowledge only')
                return await self._generate_fallback_response(validated_query, "No search results found")

            # Step 3: Extract context from search results
            search_context_data = self.search_service.extract_search_context(search_results)
            search_context = search_context_data['context']
            sources = search_context_data['sources']

            # Step 4: Generate response using Gemini with search context
            try:
                response = await self.gemini_service.generate_response(validated_query, search_context)
            except Exception as gemini_error:
                print(f"❌ Gemini generation failed: {gemini_error}")
                raise ValueError(f"Response generation failed: {str(gemini_error)}")

            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            print(f"✅ Query processed successfully in {processing_time:.2f}ms")

            return {
                'query': validated_query,
                'response': response,
                'sources': sources,
                'search_results': len(search_results),
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat(),
                'fallback': False
            }

        except Exception as error:
            print(f"❌ Agent processing error: {error}")
            
            # Try to provide a fallback response if possible
            try:
                return await self._generate_fallback_response(query, str(error))
            except:
                raise ValueError(f"Complete processing failure: {str(error)}")

    async def _generate_fallback_response(self, query: str, error_message: str) -> Dict[str, Any]:
        """
        Generate a fallback response when search or normal processing fails
        
        Args:
            query: The user's query
            error_message: Description of what went wrong
            
        Returns:
            Dictionary containing fallback response and metadata
        """
        try:
            print(f"🔄 Generating fallback response due to: {error_message}")
            
            start_time = time.time()
            
            # Determine fallback reason
            if "search" in error_message.lower():
                fallback_reason = "search_failed"
                context = f"Web search was unavailable due to: {error_message}"
            elif "no" in error_message.lower() and "results" in error_message.lower():
                fallback_reason = "no_results"
                context = "No relevant search results were found for your query."
            else:
                fallback_reason = "processing_error"
                context = f"An error occurred during processing: {error_message}"

            response = await self.gemini_service.generate_fallback_response(query, context)
            
            processing_time = (time.time() - start_time) * 1000
            
            return {
                'query': query,
                'response': response,
                'sources': [],
                'search_results': 0,
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat(),
                'fallback': True,
                'fallback_reason': fallback_reason
            }

        except Exception as fallback_error:
            print(f"❌ Fallback response generation failed: {fallback_error}")
            raise ValueError("Both search and fallback response generation failed")

    def validate_query(self, query: str) -> str:
        """
        Validate and sanitize the user query
        
        Args:
            query: The raw query string
            
        Returns:
            Cleaned and validated query
            
        Raises:
            ValueError: If query is invalid
        """
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        cleaned_query = query.strip()
        
        if not cleaned_query:
            raise ValueError("Query cannot be empty")

        if len(cleaned_query) > 500:
            raise ValueError("Query is too long (maximum 500 characters)")

        # Basic sanitization - remove excessive whitespace
        cleaned_query = ' '.join(cleaned_query.split())
        
        return cleaned_query

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get the health status of all services
        
        Returns:
            Dictionary containing service status information
        """
        return {
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
            }
        }
