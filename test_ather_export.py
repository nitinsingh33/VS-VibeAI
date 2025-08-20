#!/usr/bin/env python3
"""
Direct Test Script for Ather Export Issue
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.enhanced_agent_service import EnhancedAgentService

async def test_ather_export_direct():
    """Test the exact Ather export scenario"""
    print("🚀 Testing Ather Export - Direct Simulation")
    print("=" * 50)
    
    # Initialize the enhanced agent
    agent = EnhancedAgentService()
    
    # Test the exact query you mentioned
    query = "Give me all 500 comments on Ather in a downloadable format (Excel)"
    
    print(f"📝 Query: {query}")
    print("\n🔄 Processing...")
    
    try:
        # Process the enhanced query
        result = await agent.process_enhanced_query(
            query=query,
            use_youtube_data=True,
            max_search_results=3
        )
        
        print("\n📊 Results:")
        print(f"✅ Response generated: {len(result.get('response', ''))} characters")
        print(f"📋 Comments analyzed: {result.get('youtube_comments_analyzed', 0)}")
        print(f"🔗 Sources found: {len(result.get('sources', []))}")
        print(f"📁 Export files: {len(result.get('export_files', {}))}")
        print(f"📊 Exportable: {result.get('exportable', False)}")
        print(f"⏱️ Processing time: {result.get('processing_time', 0):.2f}ms")
        
        # Check export files
        if result.get('export_files'):
            print("\n📁 Export Files Generated:")
            for file_type, file_path in result['export_files'].items():
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    print(f"  ✅ {file_type.upper()}: {file_path} ({size} bytes)")
                else:
                    print(f"  ❌ {file_type.upper()}: {file_path} (NOT FOUND)")
        else:
            print("\n❌ No export files generated")
        
        # Show response preview
        print(f"\n💬 Response Preview (first 300 chars):")
        print(f"'{result.get('response', '')[:300]}...'")
        
        # Test export service directly
        print(f"\n🔍 Testing Export Service Directly:")
        is_exportable = agent.export_service.detect_tabular_query(query, result.get('response', ''))
        print(f"  Export detected: {is_exportable}")
        
        # Test comment extraction
        youtube_data = await agent.load_youtube_data()
        extracted_comments = agent._extract_comments_for_export(query, youtube_data)
        print(f"  Comments extracted: {len(extracted_comments)}")
        
        if extracted_comments:
            ather_comments = [c for c in extracted_comments if c.get('oem') == 'Ather']
            print(f"  Ather-specific comments: {len(ather_comments)}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_ather_export_direct())
