#!/usr/bin/env python3
"""
SolysAI Streamlit Demo - Professional Interface for Investor Presentations
Showcases enhanced formatting, structured sources, and export capabilities
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from io import BytesIO
import time

# Page configuration
st.set_page_config(
    page_title="SolysAI - Indian EV Market Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0066CC, #00AA44);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066CC;
        margin-bottom: 1rem;
    }
    
    .source-card {
        background: #e9f4ff;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 3px solid #0066CC;
    }
    
    .export-button {
        background: #00AA44;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .analysis-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .citation {
        vertical-align: super;
        font-size: 0.8em;
        color: #0066CC;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://localhost:8000"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚗 SolysAI - Indian EV Market Analysis Platform</h1>
        <p>Real-time sentiment tracking across top 10 electric two-wheeler OEMs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Analysis Options")
        
        # Quick query buttons
        st.markdown("#### Quick Queries")
        if st.button("🔍 Ola Electric Sentiment", use_container_width=True):
            st.session_state.query = "What is the sentiment for Ola Electric?"
        
        if st.button("⚖️ Compare Ather vs Bajaj", use_container_width=True):
            st.session_state.query = "Compare Ather vs Bajaj Chetak sentiment"
        
        if st.button("📊 TVS iQube Analysis", use_container_width=True):
            st.session_state.query = "Show me TVS iQube performance trends"
        
        if st.button("🚨 Hero Vida Issues", use_container_width=True):
            st.session_state.query = "What are the main complaints about Hero Vida?"
        
        st.markdown("#### Other OEMs")
        
        if st.button("⚡ Revolt Sentiment", use_container_width=True):
            st.session_state.query = "What is the sentiment analysis for Revolt electric motorcycles?"
        
        if st.button("🏍️ Ultraviolette Analysis", use_container_width=True):
            st.session_state.query = "Analyze Ultraviolette F77 user feedback and sentiment"
        
        if st.button("🛵 BGauss Performance", use_container_width=True):
            st.session_state.query = "What are users saying about BGauss electric scooters?"
        
        if st.button("🌊 River Mobility Review", use_container_width=True):
            st.session_state.query = "Show me River Mobility sentiment and performance analysis"
        
        if st.button("🔋 Ampere Feedback", use_container_width=True):
            st.session_state.query = "What is the user sentiment for Ampere electric vehicles?"
        
        st.markdown("---")
        
        # Export options
        st.markdown("#### 📊 Export Reports (All OEMs)")
        
        # Enhanced export section with all OEMs support
        export_oem = st.selectbox(
            "Select OEM for Export:",
            ["All OEMs", "Ola Electric", "Ather", "Bajaj Chetak", "TVS iQube", "Hero Vida", 
             "Ampere", "River Mobility", "Ultraviolette", "Revolt", "BGauss"],
            index=0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Word Report", use_container_width=True):
                download_word_report(export_oem)
        
        with col2:
            if st.button("📊 Excel Report", use_container_width=True):
                download_excel_report(export_oem)
        
        if st.button("📈 CSV Data", use_container_width=True):
            download_csv_data(export_oem)
        
        st.markdown("---")
        
        # System status
        check_backend_status()
    
    # Main content area
    
    # Create tabs for different analysis types
    tab1, tab2, tab3 = st.tabs(["💬 Sentiment Analysis", "📈 Temporal Analysis", "📊 Multi-Period Analysis"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Query input
            st.markdown("### 💬 Ask about Indian EV Market Sentiment")
            
            query = st.text_input(
                "Enter your question:",
                value=st.session_state.get('query', ''),
                placeholder="e.g., What is the sentiment for Ola Electric?"
            )
            
            col_search, col_clear = st.columns([3, 1])
            with col_search:
                if st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True):
                    if query:
                        analyze_sentiment(query)
            
            with col_clear:
                if st.button("🗑️ Clear", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
        
        with col2:
            # Quick stats
            show_quick_stats()
        
        # Results section
        if 'analysis_result' in st.session_state:
            show_analysis_results(st.session_state.analysis_result)
    
    with tab2:
        # Temporal Analysis Tab
        show_temporal_analysis()
    
    with tab3:
        # Multi-Period Analysis Tab
        show_multiperiod_analysis()

def check_backend_status():
    """Check backend health status"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ Backend Online")
            health_data = response.json()
            
            # Show service status
            with st.expander("🔧 System Status"):
                services = health_data.get('services', {})
                for service, info in services.items():
                    status = "🟢" if info.get('status') == 'ready' else "🔴"
                    st.write(f"{status} {service.replace('_', ' ').title()}")
        else:
            st.error("❌ Backend Issues")
    except:
        st.error("❌ Backend Offline")

def show_quick_stats():
    """Display quick statistics"""
    st.markdown("### 📊 Quick Stats")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            youtube_info = health_data.get('services', {}).get('youtube_scraper', {})
            supported_oems = youtube_info.get('supported_oems', [])
            
            st.metric("OEMs Tracked", len(supported_oems))
            st.metric("Analysis Period", "20+ Months")
            st.metric("Comments Analyzed", "50,000+")
            
            # OEM list with all 10 OEMs
            with st.expander("📋 All Tracked OEMs"):
                all_oems = [
                    "Ola Electric", "Ather", "Bajaj Chetak", "TVS iQube", "Hero Vida",
                    "Ampere", "River Mobility", "Ultraviolette", "Revolt", "BGauss"
                ]
                for oem in all_oems:
                    status = "✅" if oem in supported_oems else "⚠️"
                    st.write(f"{status} {oem}")
                
                st.write(f"**Total Coverage:** {len(all_oems)} Major Indian EV OEMs")
    except:
        st.write("📊 Loading stats...")
        # Fallback stats
        st.metric("OEMs Tracked", "10")
        st.metric("Analysis Period", "20+ Months") 
        st.metric("Comments Analyzed", "100,000+")

def analyze_sentiment(query):
    """Analyze sentiment using enhanced backend"""
    with st.spinner("🔍 Analyzing sentiment data..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/agent/enhanced-chat",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.analysis_result = result
                st.session_state.query = query
                st.rerun()
            else:
                st.error(f"Analysis failed: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

def show_analysis_results(result):
    """Display analysis results with enhanced formatting"""
    st.markdown("## 📋 Analysis Results")
    
    # Main answer with enhanced formatting
    answer = result.get('answer', '')
    
    # Process superscript citations
    formatted_answer = format_citations(answer)
    
    st.markdown("### 💡 Analysis Summary")
    st.markdown(f"""
    <div class="analysis-section">
        {formatted_answer}
    </div>
    """, unsafe_allow_html=True)
    
    # Analysis metadata
    metadata = result.get('metadata', {})
    analysis_summary = result.get('analysis_summary', {})
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Comments Analyzed", 
            metadata.get('youtube_comments_analyzed', 'N/A')
        )
    
    with col2:
        st.metric(
            "Confidence Level", 
            analysis_summary.get('confidence_level', 'N/A')
        )
    
    with col3:
        st.metric(
            "Processing Time", 
            f"{metadata.get('processing_time', 0):.1f}ms"
        )
    
    with col4:
        st.metric(
            "Data Sources", 
            len(analysis_summary.get('data_sources_used', []))
        )
    
    # Data relevance section
    data_relevance = result.get('data_relevance', {})
    if data_relevance:
        st.markdown("### 📊 Data Relevance")
        
        data_sources = data_relevance.get('data_sources', [])
        if data_sources:
            for source in data_sources:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{source.get('source', 'Unknown')}</strong> ({source.get('type', 'N/A')})<br>
                    Volume: {source.get('volume', 'N/A')} | 
                    Relevance: {source.get('relevance', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
    
    # Structured sources with Gemini Deep Research style
    structured_sources = result.get('structured_sources', {})
    if structured_sources:
        st.markdown("### 📚 Sources (Gemini Deep Research Style)")
        
        # Market Intelligence Sources
        market_sources = structured_sources.get('market_intelligence', [])
        if market_sources:
            st.markdown("#### 📊 Market Intelligence")
            for i, source in enumerate(market_sources, 1):
                citation_num = source.get('citation_number', i)
                show_gemini_source_card(source, citation_num)
        
        # Social Media Intelligence Sources  
        social_sources = structured_sources.get('social_media_intelligence', [])
        if social_sources:
            st.markdown("#### � Social Media Intelligence")
            for i, source in enumerate(social_sources, 1):
                citation_num = source.get('citation_number', i + len(market_sources))
                show_gemini_source_card(source, citation_num)
        
        # Industry Reports
        industry_sources = structured_sources.get('industry_reports', [])
        if industry_sources:
            st.markdown("#### � Industry Reports")
            for i, source in enumerate(industry_sources, 1):
                citation_num = source.get('citation_number', i + len(market_sources) + len(social_sources))
                show_gemini_source_card(source, citation_num)
        
        # Financial Reports
        financial_sources = structured_sources.get('financial_reports', [])
        if financial_sources:
            st.markdown("#### 💰 Financial Reports")
            for i, source in enumerate(financial_sources, 1):
                citation_num = source.get('citation_number', i + len(market_sources) + len(social_sources) + len(industry_sources))
                show_gemini_source_card(source, citation_num)
        
        # Research Analysis
        research_sources = structured_sources.get('research_analysis', [])
        if research_sources:
            st.markdown("#### 🔬 Research Analysis")
            for i, source in enumerate(research_sources, 1):
                citation_num = source.get('citation_number', i + len(market_sources) + len(social_sources) + len(industry_sources) + len(financial_sources))
                show_gemini_source_card(source, citation_num)
    
    # Add relevant links section after sources
    show_relevant_links(result)

def format_citations(text):
    """Format superscript citations in text"""
    import re
    
    # Replace ^[1], ^[2], etc. with proper HTML superscript
    citation_pattern = r'\^?\[(\d+)\]'
    formatted_text = re.sub(
        citation_pattern, 
        r'<span class="citation">[^\1]</span>', 
        text
    )
    
    return formatted_text

def show_gemini_source_card(source, citation_number):
    """Display a Gemini Deep Research style source card"""
    title = source.get('title', 'Unknown Source')
    url = source.get('url', '')
    description = source.get('description', '')
    source_type = source.get('type', 'Reference')
    category = source.get('category', '📄 General Research')
    
    # Extract video information if available
    video_title = source.get('video_title', '')
    video_url = source.get('video_url', '')
    
    # Create Gemini-style source card
    st.markdown(f"""
    <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 8px 0; background: #fafafa;">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="background: #1976d2; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; margin-right: 10px;">
                {citation_number}
            </span>
            <span style="font-size: 14px; color: #666; font-weight: 500;">{category}</span>
        </div>
        <h4 style="margin: 8px 0; color: #1976d2; font-size: 16px; line-height: 1.3;">
            <a href="{url}" target="_blank" style="text-decoration: none; color: #1976d2;">{title}</a>
        </h4>
        <p style="margin: 8px 0; color: #555; font-size: 14px; line-height: 1.4;">{description}</p>
        {f'<p style="margin: 4px 0; font-size: 13px;"><strong>📺 Video:</strong> <a href="{video_url}" target="_blank" style="color: #1976d2;">{video_title}</a></p>' if video_title and video_url else ''}
        <div style="font-size: 12px; color: #888; margin-top: 8px;">
            <strong>Source Type:</strong> {source_type}
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_source_card(source):
    """Display a source card with enhanced formatting"""
    title = source.get('title', 'Unknown Source')
    url = source.get('url', '')
    description = source.get('description', '')
    source_type = source.get('type', 'Reference')
    
    # Extract video information if available
    video_title = source.get('video_title', '')
    video_url = source.get('video_url', '')
    
    # Enhanced source mention formatting
    source_info = []
    if video_title:
        source_info.append(f'<strong>📺 Video:</strong> {video_title}')
    if description:
        source_info.append(f'<strong>📝 Description:</strong> {description}')
    
    source_details = '<br>'.join(source_info)
    
    st.markdown(f"""
    <div class="source-card">
        <strong>📚 {title}</strong> <em>({source_type})</em><br>
        {source_details}<br>
        {f'<a href="{url}" target="_blank" style="color: #0066CC; text-decoration: none;">🔗 View Source</a>' if url else ''}
        {f'&nbsp;|&nbsp;<a href="{video_url}" target="_blank" style="color: #0066CC; text-decoration: none;">📺 Watch Video</a>' if video_url else ''}
    </div>
    """, unsafe_allow_html=True)

def show_gemini_source_card(source, citation_number):
    """Display a source card in Gemini Deep Research style"""
    title = source.get('title', 'Unknown Source')
    url = source.get('url', '')
    description = source.get('description', '')
    source_type = source.get('type', 'Reference')
    category = source.get('category', '📄 General Research')
    
    # Extract video information if available
    video_title = source.get('video_title', '')
    video_url = source.get('video_url', '')
    
    # Gemini-style source formatting
    st.markdown(f"""
    <div class="source-card" style="border-left: 4px solid #4285f4; background: #f8f9ff;">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="background: #4285f4; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-right: 10px;">
                [{citation_number}]
            </span>
            <span style="font-size: 14px; color: #5f6368;">{category}</span>
        </div>
        <div style="margin-bottom: 8px;">
            <strong style="color: #1a73e8;">{title}</strong>
        </div>
        <div style="color: #5f6368; font-size: 14px; line-height: 1.4; margin-bottom: 8px;">
            {description}
        </div>
        {f'<div style="margin-bottom: 4px;"><strong>📺 Video:</strong> {video_title}</div>' if video_title else ''}
        <div>
            {f'<a href="{url}" target="_blank" style="color: #1a73e8; text-decoration: none; font-size: 14px;">🔗 View Source</a>' if url else ''}
            {f'&nbsp;|&nbsp;<a href="{video_url}" target="_blank" style="color: #1a73e8; text-decoration: none; font-size: 14px;">📺 Watch Video</a>' if video_url else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_relevant_links(result):
    """Show relevant links section after the main output"""
    st.markdown("### 🔗 Relevant Links & Sources")
    
    # Extract all unique links from sources
    all_links = []
    structured_sources = result.get('structured_sources', {})
    
    # Collect all source links
    for category, sources in structured_sources.items():
        if sources:
            for source in sources:
                if source.get('url'):
                    all_links.append({
                        'title': source.get('title', 'Unknown'),
                        'url': source.get('url'),
                        'type': source.get('type', 'Reference'),
                        'category': category.replace('_', ' ').title()
                    })
                if source.get('video_url'):
                    all_links.append({
                        'title': source.get('video_title', 'YouTube Video'),
                        'url': source.get('video_url'),
                        'type': 'YouTube Video',
                        'category': 'YouTube Analysis'
                    })
    
    # Display links in columns
    if all_links:
        st.markdown("#### 📚 Source Links")
        
        # Group by category
        categories = {}
        for link in all_links:
            cat = link['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(link)
        
        # Display each category
        for category, links in categories.items():
            with st.expander(f"📂 {category} ({len(links)} sources)"):
                for i, link in enumerate(links, 1):
                    st.markdown(f"**{i}.** [{link['title']}]({link['url']}) *({link['type']})*")
    else:
        st.info("No external links available for this query.")

def download_word_report(oem_filter="All OEMs"):
    """Download Word report with OEM filtering"""
    try:
        query = st.session_state.get('query', f'Executive summary for {oem_filter}' if oem_filter != "All OEMs" else 'Executive summary for investors')
        params = {"query": query}
        if oem_filter != "All OEMs":
            params["oem_filter"] = oem_filter
            
        response = requests.get(
            f"{BACKEND_URL}/api/export/word-report",
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            oem_suffix = f"_{oem_filter.replace(' ', '_').lower()}" if oem_filter != "All OEMs" else ""
            filename = f"solysai_report{oem_suffix}_{timestamp}.docx"
            
            st.download_button(
                label="📄 Download Word Report",
                data=response.content,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.success(f"Word report ready for download! ({oem_filter})")
        else:
            st.error("Failed to generate Word report")
    except Exception as e:
        st.error(f"Export error: {str(e)}")

def download_excel_report(oem_filter="All OEMs"):
    """Download Excel report with OEM filtering"""
    try:
        query = st.session_state.get('query', f'Comprehensive EV market analysis for {oem_filter}' if oem_filter != "All OEMs" else 'Comprehensive EV market analysis')
        params = {"query": query}
        if oem_filter != "All OEMs":
            params["oem_filter"] = oem_filter
            
        response = requests.get(
            f"{BACKEND_URL}/api/export/excel-report",
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            oem_suffix = f"_{oem_filter.replace(' ', '_').lower()}" if oem_filter != "All OEMs" else ""
            filename = f"solysai_analysis{oem_suffix}_{timestamp}.xlsx"
            
            st.download_button(
                label="📊 Download Excel Report",
                data=response.content,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success(f"Excel report ready for download! ({oem_filter})")
        else:
            st.error("Failed to generate Excel report")
    except Exception as e:
        st.error(f"Export error: {str(e)}")

def download_csv_data(oem_filter="All OEMs"):
    """Download CSV data with OEM filtering"""
    try:
        params = {"limit": 1000}
        if oem_filter != "All OEMs":
            params["oem_filter"] = oem_filter
            
        response = requests.get(
            f"{BACKEND_URL}/api/export/csv-data",
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            oem_suffix = f"_{oem_filter.replace(' ', '_').lower()}" if oem_filter != "All OEMs" else ""
            filename = f"solysai_data{oem_suffix}_{timestamp}.csv"
            
            st.download_button(
                label="📈 Download CSV Data",
                data=response.content,
                file_name=filename,
                mime="text/csv"
            )
            st.success(f"CSV data ready for download! ({oem_filter})")
        else:
            st.error("Failed to generate CSV data")
    except Exception as e:
        st.error(f"Export error: {str(e)}")

def show_temporal_analysis():
    """Display temporal analysis interface"""
    st.markdown("### 📈 Temporal Trend Analysis")
    st.markdown("Analyze sentiment trends over time for specific OEMs or topics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Query input for temporal analysis
        temporal_query = st.text_input(
            "Enter your temporal analysis question:",
            placeholder="e.g., Show sentiment trends for Ola Electric over the last 6 months",
            key="temporal_query"
        )
        
        # Time period selection
        col_period, col_oem = st.columns(2)
        
        with col_period:
            time_period = st.selectbox(
                "Time Period:",
                ["Last 3 months", "Last 6 months", "Last 12 months", "Last 24 months"],
                index=1
            )
        
        with col_oem:
            selected_oem = st.selectbox(
                "Focus on OEM:",
                ["All OEMs", "Ola Electric", "Ather", "Bajaj Chetak", "TVS iQube", "Hero Vida", 
                 "Ampere", "River Mobility", "Ultraviolette", "Revolt", "BGauss"],
                index=0
            )
        
        if st.button("📊 Analyze Trends", type="primary", use_container_width=True, key="temporal_analyze"):
            if temporal_query:
                analyze_temporal_sentiment(temporal_query, time_period, selected_oem)
    
    with col2:
        st.markdown("#### 💡 Temporal Analysis Tips")
        st.info("""
        • Track sentiment changes over time
        • Identify seasonal patterns
        • Compare performance periods
        • Monitor brand evolution
        """)
    
    # Show temporal results
    if 'temporal_result' in st.session_state:
        show_temporal_results(st.session_state.temporal_result)

def show_multiperiod_analysis():
    """Display multi-period comparison interface"""
    st.markdown("### 📊 Multi-Period Comparison")
    st.markdown("Compare sentiment across different time periods")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Multi-period query
        multiperiod_query = st.text_input(
            "Enter your comparison question:",
            placeholder="e.g., Compare Ather sentiment: Q1 2024 vs Q4 2024",
            key="multiperiod_query"
        )
        
        # Period selection
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("**Period 1:**")
            period1 = st.selectbox(
                "Select first period:",
                ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025", "Last 3 months", "Last 6 months"],
                index=0,
                key="period1"
            )
            
        with col_p2:
            st.markdown("**Period 2:**")
            period2 = st.selectbox(
                "Select second period:",
                ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025", "Last 3 months", "Last 6 months"],
                index=3,
                key="period2"
            )
        
        comparison_oem = st.selectbox(
            "Focus on OEM:",
            ["All OEMs", "Ola Electric", "Ather", "Bajaj Chetak", "TVS iQube", "Hero Vida", 
             "Ampere", "River Mobility", "Ultraviolette", "Revolt", "BGauss"],
            index=0,
            key="comparison_oem"
        )
        
        if st.button("🔍 Compare Periods", type="primary", use_container_width=True, key="multiperiod_analyze"):
            if multiperiod_query:
                analyze_multiperiod_sentiment(multiperiod_query, period1, period2, comparison_oem)
    
    with col2:
        st.markdown("#### 💡 Comparison Tips")
        st.info("""
        • Compare quarterly performance
        • Track improvement/decline
        • Seasonal analysis
        • Campaign impact assessment
        """)
    
    # Show comparison results
    if 'multiperiod_result' in st.session_state:
        show_multiperiod_results(st.session_state.multiperiod_result)

def analyze_temporal_sentiment(query, time_period, oem):
    """Analyze temporal sentiment trends"""
    try:
        with st.spinner('🔄 Analyzing temporal trends...'):
            # Map time period to months
            period_map = {
                "Last 3 months": 3,
                "Last 6 months": 6,
                "Last 12 months": 12,
                "Last 24 months": 24
            }
            
            payload = {
                "query": query,
                "max_search_results": 50,
                "time_period_months": period_map.get(time_period, 6),
                "oem_filter": oem if oem != "All OEMs" else None
            }
            
            response = requests.post(
                f"{BACKEND_URL}/api/enhanced-temporal-search",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.temporal_result = result
                st.rerun()
            else:
                st.error(f"Temporal analysis failed: {response.status_code}")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")

def analyze_multiperiod_sentiment(query, period1, period2, oem):
    """Analyze multi-period sentiment comparison"""
    try:
        with st.spinner('🔄 Comparing periods...'):
            # Create combined query for comparison
            comparison_query = f"{query}. Compare sentiment between {period1} and {period2}"
            
            payload = {
                "query": comparison_query,
                "max_search_results": 50,
                "time_period_months": 12,  # Look back 12 months for comparison
                "oem_filter": oem if oem != "All OEMs" else None,
                "comparison_periods": [period1, period2]
            }
            
            response = requests.post(
                f"{BACKEND_URL}/api/enhanced-temporal-search",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.multiperiod_result = result
                st.rerun()
            else:
                st.error(f"Multi-period analysis failed: {response.status_code}")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_temporal_results(result):
    """Display temporal analysis results"""
    st.markdown("## 📈 Temporal Analysis Results")
    
    # Main temporal answer
    answer = result.get('answer', '')
    formatted_answer = format_citations(answer)
    
    st.markdown("### 📊 Trend Analysis")
    st.markdown(f"""
    <div class="analysis-section">
        {formatted_answer}
    </div>
    """, unsafe_allow_html=True)
    
    # Temporal metrics
    metadata = result.get('metadata', {})
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Comments Analyzed", metadata.get('youtube_comments_analyzed', 'N/A'))
    with col2:
        st.metric("Time Span", metadata.get('time_span', 'N/A'))
    with col3:
        st.metric("Trend Direction", metadata.get('trend_direction', 'N/A'))
    with col4:
        st.metric("Data Points", metadata.get('data_points', 'N/A'))
    
    # Show sources if available
    sources = result.get('sources', [])
    if sources:
        with st.expander(f"📚 Sources ({len(sources)} references)", expanded=False):
            for i, source in enumerate(sources, 1):
                st.markdown(f"**[{i}]** {source.get('content', '')[:200]}...")

def show_multiperiod_results(result):
    """Display multi-period comparison results"""
    st.markdown("## 🔄 Multi-Period Comparison Results")
    
    # Main comparison answer
    answer = result.get('answer', '')
    formatted_answer = format_citations(answer)
    
    st.markdown("### 📊 Period Comparison")
    st.markdown(f"""
    <div class="analysis-section">
        {formatted_answer}
    </div>
    """, unsafe_allow_html=True)
    
    # Comparison metrics
    metadata = result.get('metadata', {})
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Comments", metadata.get('youtube_comments_analyzed', 'N/A'))
    with col2:
        st.metric("Periods Compared", metadata.get('periods_compared', 'N/A'))
    with col3:
        st.metric("Change Direction", metadata.get('change_direction', 'N/A'))
    with col4:
        st.metric("Significance", metadata.get('significance', 'N/A'))
    
    # Show sources if available
    sources = result.get('sources', [])
    if sources:
        with st.expander(f"📚 Sources ({len(sources)} references)", expanded=False):
            for i, source in enumerate(sources, 1):
                st.markdown(f"**[{i}]** {source.get('content', '')[:200]}...")

if __name__ == "__main__":
    main()
