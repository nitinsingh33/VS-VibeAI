"""
Streamlit Frontend for Indian Electric Two-Wheeler Market Analysis
"""

import streamlit as st
import asyncio
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.enhanced_agent_service import EnhancedAgentService
from services.youtube_scraper import YouTubeCommentScraper

# Page configuration
st.set_page_config(
    page_title="🏍️ Indian Electric Two-Wheeler Market Intelligence",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .oem-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .source-link {
        background: #e1f5fe;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        border-left: 3px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load sample data for demonstration"""
    return {
        'Ola Electric': [
            {'sentiment': 'Mixed', 'engagement': 45, 'issues': ['Charging', 'Service'], 'positives': ['Performance', 'Design']},
        ],
        'TVS iQube': [
            {'sentiment': 'Positive', 'engagement': 67, 'issues': ['Range'], 'positives': ['Reliability', 'Build Quality']},
        ],
        'Bajaj Chetak': [
            {'sentiment': 'Neutral', 'engagement': 34, 'issues': ['Range', 'Features'], 'positives': ['Premium Feel', 'Brand Trust']},
        ],
        'Ather': [
            {'sentiment': 'Positive', 'engagement': 89, 'issues': ['Price'], 'positives': ['Performance', 'Features', 'Tech']},
        ],
        'Hero Vida': [
            {'sentiment': 'Cautious', 'engagement': 56, 'issues': ['New Brand', 'Network'], 'positives': ['Potential', 'Hero Brand']},
        ]
    }

async def run_async_query(agent, query, use_youtube):
    """Run async query in Streamlit"""
    return await agent.process_enhanced_query(query, use_youtube_data=use_youtube)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏍️ Indian Electric Two-Wheeler Market Intelligence</h1>
        <p>Analyze market trends using YouTube user feedback + Google search + AI insights</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'agent' not in st.session_state:
        st.session_state.agent = EnhancedAgentService()
    
    if 'youtube_data_loaded' not in st.session_state:
        st.session_state.youtube_data_loaded = False

    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Status Check
        with st.expander("📡 API Status"):
            health_status = st.session_state.agent.get_health_status()
            
            for service, status in health_status.items():
                if isinstance(status, dict) and 'configured' in status:
                    icon = "✅" if status['configured'] else "❌"
                    st.write(f"{icon} {service.replace('_', ' ').title()}: {status['status']}")
        
        # Data Sources
        st.header("📊 Data Sources")
        use_youtube = st.checkbox("📱 YouTube Comments", value=True, help="Include user feedback from YouTube")
        use_search = st.checkbox("🔍 Google Search", value=True, help="Include current web search results")
        max_results = st.slider("Max Search Results", 1, 10, 5)
        
        # Enhanced Scraping Options
        with st.expander("🚀 Enhanced YouTube Scraping"):
            st.write("**Current Status:**")
            if st.session_state.youtube_data_loaded:
                st.success("✅ YouTube data loaded")
            else:
                st.info("ℹ️ Using sample data")
            
            st.write("**Options:**")
            if st.button("🔄 Load Latest Scraped Data", help="Load most recent scraped data if available"):
                with st.spinner("Loading latest data..."):
                    try:
                        asyncio.run(st.session_state.agent.load_youtube_data(force_refresh=True))
                        st.session_state.youtube_data_loaded = True
                        st.success("✅ Latest data loaded successfully!")
                    except Exception as e:
                        st.error(f"❌ Error loading data: {e}")
            
            if st.button("🚀 Run Enhanced Scraping (500+ comments)", help="This will take 10-30 minutes"):
                if st.checkbox("⚠️ I understand this takes time", key="confirm_scraping"):
                    with st.spinner("Running enhanced scraping... This may take 10-30 minutes"):
                        try:
                            asyncio.run(st.session_state.agent.load_youtube_data(force_refresh=True, use_enhanced_scraping=True))
                            st.session_state.youtube_data_loaded = True
                            st.success("🎉 Enhanced scraping completed!")
                        except Exception as e:
                            st.error(f"❌ Scraping failed: {e}")
                else:
                    st.warning("Please confirm you understand the time requirement")
            
            st.info("💡 **Tip:** Run `python run_enhanced_scraping.py` in terminal for better progress tracking")
        
        # OEM Selection
        st.header("🏭 OEM Focus")
        oems = ['Ola Electric', 'TVS iQube', 'Bajaj Chetak', 'Ather', 'Hero Vida']
        selected_oems = st.multiselect("Select OEMs to analyze", oems, default=oems)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Ask Your Question")
        
        # Sample questions
        sample_questions = [
            "What are users saying about Ola Electric scooters in July 2025?",
            "Compare the reliability of TVS iQube vs Ather 450X based on user feedback",
            "What are the main charging infrastructure concerns for electric scooters?",
            "Which electric scooter has the best performance according to users?",
            "What are the latest updates on Indian electric two-wheeler market?"
        ]
        
        selected_sample = st.selectbox("🎯 Quick Questions:", ["Custom Question"] + sample_questions)
        
        if selected_sample != "Custom Question":
            query = selected_sample
        else:
            query = st.text_input("🤔 Your Question:", placeholder="Ask anything about Indian electric two-wheelers...")
        
        # Query button
        if st.button("🚀 Analyze", type="primary") and query:
            with st.spinner("🔍 Analyzing data sources..."):
                try:
                    # Run the enhanced query
                    result = asyncio.run(run_async_query(st.session_state.agent, query, use_youtube))
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    # Response
                    st.header("🎯 AI Analysis")
                    st.markdown(result['response'])
                    
                    # Metrics
                    col_metrics = st.columns(4)
                    with col_metrics[0]:
                        st.metric("🕐 Processing Time", f"{result['processing_time']:.0f}ms")
                    with col_metrics[1]:
                        st.metric("🔍 Search Results", result['search_results_count'])
                    with col_metrics[2]:
                        st.metric("📱 YouTube Comments", result['youtube_comments_analyzed'])
                    with col_metrics[3]:
                        st.metric("📚 Total Sources", len(result['sources']))
                    
                    # Sources
                    if result['sources']:
                        st.header("📚 Sources")
                        for i, source in enumerate(result['sources'], 1):
                            with st.expander(f"📄 {i}. {source['title']}", expanded=False):
                                st.markdown(f"**URL:** [{source['url']}]({source['url']})")
                                st.markdown(f"**Preview:** {source['snippet']}")
                    
                    # Store result in session state for further analysis
                    st.session_state.last_result = result
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.error("Please check your API keys in the .env file")

    with col2:
        st.header("📊 Market Overview")
        
        # Load sample data for visualization
        sample_data = load_sample_data()
        
        # OEM Sentiment Analysis
        if sample_data:
            sentiment_data = []
            engagement_data = []
            
            for oem, data in sample_data.items():
                if oem in selected_oems:
                    sentiment_data.append({'OEM': oem, 'Sentiment': data[0]['sentiment']})
                    engagement_data.append({'OEM': oem, 'Engagement': data[0]['engagement']})
            
            if sentiment_data:
                # Engagement Chart
                df_engagement = pd.DataFrame(engagement_data)
                fig_engagement = px.bar(
                    df_engagement, 
                    x='OEM', 
                    y='Engagement',
                    title="📈 User Engagement Score",
                    color='Engagement',
                    color_continuous_scale='viridis'
                )
                fig_engagement.update_layout(height=400)
                st.plotly_chart(fig_engagement, use_container_width=True)
                
                # Top Issues and Positives
                st.subheader("🔍 Key Insights")
                
                all_issues = []
                all_positives = []
                
                for oem, data in sample_data.items():
                    if oem in selected_oems:
                        all_issues.extend(data[0]['issues'])
                        all_positives.extend(data[0]['positives'])
                
                # Count frequencies
                issue_counts = pd.Series(all_issues).value_counts()
                positive_counts = pd.Series(all_positives).value_counts()
                
                col_insights = st.columns(2)
                
                with col_insights[0]:
                    st.markdown("**⚠️ Top Concerns:**")
                    for issue, count in issue_counts.head(3).items():
                        st.markdown(f"• {issue} ({count} mentions)")
                
                with col_insights[1]:
                    st.markdown("**✅ Top Strengths:**")
                    for positive, count in positive_counts.head(3).items():
                        st.markdown(f"• {positive} ({count} mentions)")

    # YouTube Data Management Section
    st.header("📱 YouTube Data Management")
    
    col_yt1, col_yt2, col_yt3 = st.columns(3)
    
    with col_yt1:
        if st.button("🔄 Refresh YouTube Data"):
            with st.spinner("📱 Loading YouTube comment data..."):
                try:
                    asyncio.run(st.session_state.agent.load_youtube_data(force_refresh=True))
                    st.success("✅ YouTube data refreshed!")
                    st.session_state.youtube_data_loaded = True
                except Exception as e:
                    st.error(f"❌ Error loading YouTube data: {e}")
    
    with col_yt2:
        if st.button("📊 View YouTube Analytics"):
            with st.spinner("📊 Generating analytics..."):
                try:
                    analytics = asyncio.run(st.session_state.agent.get_youtube_analytics())
                    
                    # Display analytics
                    st.subheader("📈 YouTube Comment Analytics")
                    
                    overall = analytics.get('overall', {})
                    st.metric("Total Comments Analyzed", overall.get('total_comments', 0))
                    st.metric("OEMs Covered", overall.get('total_oems', 0))
                    
                    # Per OEM breakdown
                    for oem, data in analytics.items():
                        if oem != 'overall' and isinstance(data, dict):
                            with st.expander(f"📊 {oem} Analytics"):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.metric("Comments", data.get('total_comments', 0))
                                    st.metric("Unique Users", data.get('unique_authors', 0))
                                with col_b:
                                    st.metric("Avg Likes", f"{data.get('avg_likes', 0):.1f}")
                                
                                # Top keywords
                                keywords = data.get('sentiment_keywords', {})
                                if keywords:
                                    st.write("**Top Keywords:**")
                                    st.write(", ".join(list(keywords.keys())[:5]))
                    
                except Exception as e:
                    st.error(f"❌ Error generating analytics: {e}")
    
    with col_yt3:
        # Download data option
        if st.session_state.youtube_data_loaded:
            youtube_data = asyncio.run(st.session_state.agent.load_youtube_data())
            if youtube_data:
                json_data = json.dumps(youtube_data, indent=2, ensure_ascii=False)
                st.download_button(
                    "💾 Download YouTube Data",
                    data=json_data,
                    file_name=f"youtube_comments_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Powered by Gemini 2.0 Flash | 🔍 Serper API | 📱 YouTube API</p>
        <p>Analyzing Indian Electric Two-Wheeler Market Trends with AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
