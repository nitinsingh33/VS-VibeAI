"""
Production Sentiment Optimizer
Ultra-fast sentiment analysis for high-throughput environments
"""

import asyncio
from typing import Dict, Any
from services.advanced_sentiment_classifier import AdvancedSentimentClassifier

class ProductionSentimentOptimizer:
    """
    Production-optimized sentiment classifier
    - Ultra-fast processing
    - Optimized for high-throughput
    - Maintains accuracy while maximizing speed
    """
    
    def __init__(self):
        self.base_classifier = AdvancedSentimentClassifier()
        self.cache = {}  # Simple cache for common patterns
        
    async def classify_comment_advanced(self, comment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ultra-fast comment classification
        
        Args:
            comment: Dictionary containing comment data
            
        Returns:
            Dictionary with sentiment analysis results
        """
        text = comment.get('text', comment.get('comment', ''))
        
        # Quick cache lookup for exact matches
        if text in self.cache:
            return self.cache[text]
        
        # Use the base classifier for analysis
        result = self.base_classifier.enhanced_sentiment_analysis(
            text, 
            comment.get('likes', 0),
            comment.get('replies', 0), 
            comment.get('shares', 0)
        )
        
        # Add source identifier
        result['source'] = 'ultra_fast'
        
        # Cache results for future use (limit cache size)
        if len(self.cache) < 1000:
            self.cache[text] = result
        
        return result

    def clear_cache(self):
        """Clear the internal cache"""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            'cache_size': len(self.cache),
            'max_cache_size': 1000
        }
