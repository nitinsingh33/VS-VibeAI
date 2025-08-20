"""
Standalone Export Handler - Direct export functionality for VibeAI
"""

import asyncio
import os
from services.enhanced_agent_service import EnhancedAgentService
from services.export_service import ExportService

class StandaloneExporter:
    def __init__(self):
        self.agent = EnhancedAgentService()
        self.export_service = ExportService()
        self.youtube_data = None
    
    async def initialize(self):
        """Initialize by loading YouTube data"""
        if not self.youtube_data:
            self.youtube_data = await self.agent.load_youtube_data()
    
    async def export_all_comments(self, oem_name: str, file_format: str = 'excel') -> str:
        """Export all comments for a specific OEM with advanced sentiment analysis"""
        await self.initialize()
        
        if oem_name not in self.youtube_data:
            raise ValueError(f"OEM '{oem_name}' not found. Available: {list(self.youtube_data.keys())}")
        
        comments = self.youtube_data[oem_name]
        
        # Apply advanced sentiment analysis
        enhanced_comments = await self.agent.sentiment_analyzer.analyze_comment_batch(comments, oem_name)
        sentiment_summary = self.agent.sentiment_analyzer.advanced_classifier.get_batch_summary(enhanced_comments)
        
        export_data = {
            'query': f'All {len(comments)} comments for {oem_name} with advanced sentiment analysis',
            'analysis': f'Complete dataset of all {len(comments)} user comments for {oem_name} from real YouTube data with 9-layer sentiment analysis.',
            'comments_data': enhanced_comments,
            'sentiment_summary': sentiment_summary,
            'sources': [
                {
                    'title': f'{oem_name} YouTube Comments (Advanced Analysis)',
                    'url': 'Internal Data Collection',
                    'snippet': f'Real user feedback from {len(comments)} comments with multilingual sentiment analysis'
                }
            ],
            'statistics': [
                {
                    'OEM': oem_name,
                    'Total_Comments': len(comments),
                    'Date_Range': self._get_date_range(comments),
                    'Avg_Likes': round(sum(c.get('likes', 0) for c in comments) / len(comments), 2),
                    'Total_Videos': len(set(c.get('video_id', '') for c in comments)),
                    'Positive_Sentiment': sentiment_summary.get('positive_count', 0),
                    'Negative_Sentiment': sentiment_summary.get('negative_count', 0),
                    'Neutral_Sentiment': sentiment_summary.get('neutral_count', 0),
                    'Confidence_Score': round(sentiment_summary.get('average_confidence', 0), 2),
                    'Extraction_Method': 'YouTube Real Data + Advanced AI Analysis'
                }
            ],
            'summary': f'Complete advanced sentiment analysis of {len(comments)} real user comments for {oem_name}',
            'key_findings': [
                f'Total authentic comments analyzed: {len(comments)}',
                f'Average engagement: {round(sum(c.get("likes", 0) for c in comments) / len(comments), 2)} likes per comment',
                f'Video sources: {len(set(c.get("video_id", "") for c in comments))} unique videos',
                f'Data collection period: August 2025',
                f'Comments with high engagement (5+ likes): {len([c for c in comments if c.get("likes", 0) >= 5])}'
            ]
        }
        
        if file_format.lower() == 'excel':
            return self.export_service.create_excel_export(export_data)
        elif file_format.lower() == 'word':
            return self.export_service.create_word_export(export_data)
        else:
            raise ValueError("Format must be 'excel' or 'word'")
    
    async def export_comparison(self, oem_list: list, file_format: str = 'excel') -> str:
        """Export comparison data for multiple OEMs with advanced sentiment analysis"""
        await self.initialize()
        
        comparison_data = {}
        sentiment_summaries = {}
        
        for oem in oem_list:
            if oem in self.youtube_data:
                comments = self.youtube_data[oem]
                # Apply advanced sentiment analysis for each OEM
                enhanced_comments = await self.agent.sentiment_analyzer.analyze_comment_batch(comments, oem)
                sentiment_summary = self.agent.sentiment_analyzer.advanced_classifier.get_batch_summary(enhanced_comments)
                
                comparison_data[oem] = enhanced_comments
                sentiment_summaries[oem] = sentiment_summary
        
        export_data = {
            'query': f'Advanced sentiment comparison of {", ".join(oem_list)}',
            'analysis': f'Comprehensive comparison analysis across {len(comparison_data)} electric vehicle brands using 9-layer sentiment analysis.',
            'comments_data': [comment for comments in comparison_data.values() for comment in comments],  # Flatten all comments
            'oem_data': comparison_data,  # Keep OEM-specific data for statistics
            'sentiment_summaries': sentiment_summaries,
            'sources': [
                {
                    'title': f'{oem} YouTube Comments (Advanced Analysis)',
                    'url': 'Internal Data Collection',
                    'snippet': f'Real user feedback with multilingual sentiment analysis'
                }
                for oem in comparison_data.keys()
            ],
            'statistics': [
                {
                    'OEM': oem,
                    'Total_Comments': len(comparison_data[oem]),
                    'Avg_Likes': round(sum(c.get('likes', 0) for c in comparison_data[oem]) / len(comparison_data[oem]), 2),
                    'Positive_Sentiment': sentiment_summaries[oem].get('positive_count', 0),
                    'Negative_Sentiment': sentiment_summaries[oem].get('negative_count', 0),
                    'Neutral_Sentiment': sentiment_summaries[oem].get('neutral_count', 0),
                    'Confidence_Score': round(sentiment_summaries[oem].get('average_confidence', 0), 2),
                    'Sentiment_Score': round(sentiment_summaries[oem].get('sentiment_score', 0), 2)
                }
                for oem in comparison_data.keys()
            ],
            'summary': f'Advanced sentiment comparison across {len(comparison_data)} electric vehicle brands',
            'tables': {
                'OEM_Sentiment_Comparison': self._create_advanced_comparison_table(comparison_data, sentiment_summaries)
            }
        }
        
        if file_format.lower() == 'excel':
            return self.export_service.create_excel_export(export_data)
        elif file_format.lower() == 'word':
            return self.export_service.create_word_export(export_data)
        else:
            raise ValueError("Format must be 'excel' or 'word'")
    
    def _create_advanced_comparison_table(self, comparison_data, sentiment_summaries):
        """Create advanced comparison table with sentiment analysis"""
        import pandas as pd
        
        table_data = []
        for oem, comments in comparison_data.items():
            sentiment = sentiment_summaries[oem]
            table_data.append({
                'OEM': oem,
                'Total_Comments': len(comments),
                'Avg_Likes': round(sum(c.get('likes', 0) for c in comments) / len(comments), 2),
                'Positive_%': round((sentiment.get('positive_count', 0) / len(comments)) * 100, 1),
                'Negative_%': round((sentiment.get('negative_count', 0) / len(comments)) * 100, 1),
                'Neutral_%': round((sentiment.get('neutral_count', 0) / len(comments)) * 100, 1),
                'Confidence_Score': round(sentiment.get('average_confidence', 0), 2),
                'Overall_Sentiment': sentiment.get('dominant_sentiment', 'Unknown')
            })
        
        return pd.DataFrame(table_data)
    
    def _get_date_range(self, comments):
        """Get date range for comments"""
        dates = [c.get('date', '') for c in comments if c.get('date')]
        if dates:
            return f"{min(dates)} to {max(dates)}"
        return "Unknown"

# Quick export functions for direct use
async def quick_export_oem(oem_name: str, format: str = 'excel') -> str:
    """Quick export function for single OEM"""
    exporter = StandaloneExporter()
    return await exporter.export_all_comments(oem_name, format)

async def quick_export_comparison(oems: list, format: str = 'excel') -> str:
    """Quick export function for OEM comparison"""
    exporter = StandaloneExporter()
    return await exporter.export_comparison(oems, format)

# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python standalone_exporter.py <OEM_NAME> [excel|word]")
        print("  python standalone_exporter.py compare <OEM1,OEM2,OEM3> [excel|word]")
        print("\nAvailable OEMs: Ola Electric, TVS iQube, Bajaj Chetak, Ather, Hero Vida")
        sys.exit(1)
    
    command = sys.argv[1]
    file_format = sys.argv[2] if len(sys.argv) > 2 else 'excel'
    
    async def main():
        exporter = StandaloneExporter()
        
        if command == 'compare':
            if len(sys.argv) < 3:
                print("Error: Please specify OEMs to compare (comma-separated)")
                return
            oems = [oem.strip() for oem in sys.argv[2].split(',')]
            format_arg = sys.argv[3] if len(sys.argv) > 3 else 'excel'
            
            print(f"Exporting comparison of {', '.join(oems)} as {format_arg}...")
            filepath = await exporter.export_comparison(oems, format_arg)
            print(f"✅ Comparison export created: {filepath}")
        else:
            oem_name = command
            format_arg = file_format
            print(f"Exporting all {oem_name} comments as {format_arg}...")
            filepath = await exporter.export_all_comments(oem_name, format_arg)
            print(f"✅ Export created: {filepath}")
    
    asyncio.run(main())
