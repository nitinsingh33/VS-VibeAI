"""
Enhanced Temporal Analysis Page - Streamlit interface for time-based analysis
"""

import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.enhanced_agent_service import EnhancedAgentService

# Page config
st.set_page_config(
    page_title="📈 Temporal Analysis",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .analysis-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .temporal-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'enhanced_service' not in st.session_state:
    st.session_state.enhanced_service = None

async def load_service():
    """Load the enhanced agent service"""
    if st.session_state.enhanced_service is None:
        st.session_state.enhanced_service = EnhancedAgentService()
    return st.session_state.enhanced_service

def main():
    # Header
    st.markdown("""
    <div class="temporal-header">
        <h1>📈 Temporal Analysis Dashboard</h1>
        <p>Analyze brand sentiment and performance across time periods</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize service
    if st.button("🚀 Initialize Analysis Engine", type="primary"):
        with st.spinner("Loading temporal analysis capabilities..."):
            asyncio.run(load_service())
            st.success("✅ Temporal analysis engine loaded!")
    
    if st.session_state.enhanced_service is None:
        st.info("👆 Please click 'Initialize Analysis Engine' first.")
        return
    
    # Main analysis interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Analysis Configuration")
        
        # OEM selection
        oem_options = ["Ola Electric", "TVS iQube", "Bajaj Chetak", "Ather", "Hero Vida"]
        selected_oem = st.selectbox("Select OEM for Analysis:", oem_options)
        
        # Time period selection
        analysis_type = st.radio(
            "Analysis Type:",
            ["Single Period", "Multi-Period Comparison", "Trend Analysis"]
        )
        
        if analysis_type == "Single Period":
            period_input = st.text_input(
                "Time Period:",
                placeholder="e.g., August 2024, Q2 2025, July 2025",
                help="Enter a specific month, quarter, or year"
            )
            
            if st.button("🔍 Analyze Period", key="single_analysis"):
                if period_input:
                    with st.spinner(f"Analyzing {selected_oem} for {period_input}..."):
                        try:
                            query = f"What was the sentiment and brand strength for {selected_oem} in {period_input}?"
                            result = asyncio.run(
                                st.session_state.enhanced_service.process_enhanced_query(query)
                            )
                            
                            # Display results in col2
                            with col2:
                                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                                st.markdown(f"### 📊 Analysis Results: {selected_oem}")
                                st.markdown(f"**Period:** {period_input}")
                                
                                if result.get('temporal_analysis'):
                                    temporal_data = result['temporal_analysis'].get(selected_oem, {})
                                    
                                    if temporal_data:
                                        # Metrics display
                                        sentiment = temporal_data.get('sentiment_metrics', {})
                                        brand_strength = temporal_data.get('brand_strength', {})
                                        
                                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                                        
                                        with metrics_col1:
                                            st.metric(
                                                "Comments Analyzed",
                                                temporal_data.get('comment_count', 0)
                                            )
                                        
                                        with metrics_col2:
                                            st.metric(
                                                "Sentiment Score",
                                                f"{sentiment.get('sentiment_score', 0)}/100"
                                            )
                                        
                                        with metrics_col3:
                                            st.metric(
                                                "Brand Strength",
                                                f"{brand_strength.get('brand_strength_score', 0)}/100"
                                            )
                                        
                                        # Detailed breakdown
                                        st.markdown("#### 📈 Detailed Metrics")
                                        
                                        # Sentiment breakdown
                                        st.markdown("**Sentiment Distribution:**")
                                        sentiment_data = {
                                            'Positive': sentiment.get('positive_percentage', 0),
                                            'Negative': sentiment.get('negative_percentage', 0),
                                            'Neutral': sentiment.get('neutral_percentage', 0)
                                        }
                                        
                                        # Create pie chart
                                        fig = px.pie(
                                            values=list(sentiment_data.values()),
                                            names=list(sentiment_data.keys()),
                                            title="Sentiment Distribution"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                        
                                        # Category breakdown
                                        if 'categories' in temporal_data:
                                            categories = temporal_data['categories']
                                            st.markdown("**Comment Categories:**")
                                            
                                            category_df = pd.DataFrame([
                                                {'Category': k.replace('_', ' ').title(), 'Comments': v}
                                                for k, v in categories.items()
                                                if v > 0
                                            ])
                                            
                                            if not category_df.empty:
                                                fig_bar = px.bar(
                                                    category_df,
                                                    x='Category',
                                                    y='Comments',
                                                    title="Comments by Category"
                                                )
                                                st.plotly_chart(fig_bar, use_container_width=True)
                                
                                # AI Response
                                st.markdown("#### 🤖 AI Analysis")
                                st.write(result['response'])
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")
        
        elif analysis_type == "Multi-Period Comparison":
            periods = st.text_area(
                "Time Periods (one per line):",
                placeholder="August 2024\nJuly 2025\nQ2 2025",
                help="Enter multiple time periods to compare"
            )
            
            if st.button("📊 Compare Periods", key="multi_analysis"):
                if periods:
                    period_list = [p.strip() for p in periods.split('\n') if p.strip()]
                    
                    with st.spinner(f"Comparing {selected_oem} across {len(period_list)} periods..."):
                        try:
                            # Use the temporal brand analysis API
                            analysis = asyncio.run(
                                st.session_state.enhanced_service.get_temporal_brand_analysis(
                                    selected_oem, period_list
                                )
                            )
                            
                            with col2:
                                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                                st.markdown(f"### 📊 Multi-Period Analysis: {selected_oem}")
                                
                                if 'error' not in analysis:
                                    # Create comparison charts
                                    comparison_data = []
                                    
                                    for period, data in analysis.items():
                                        if 'error' not in data:
                                            comparison_data.append({
                                                'Period': period,
                                                'Sentiment Score': data['sentiment_metrics']['sentiment_score'],
                                                'Brand Strength': data['brand_strength']['brand_strength_score'],
                                                'Comments': data['comment_count'],
                                                'Positive %': data['sentiment_metrics']['positive_percentage'],
                                                'Negative %': data['sentiment_metrics']['negative_percentage']
                                            })
                                    
                                    if comparison_data:
                                        df_comparison = pd.DataFrame(comparison_data)
                                        
                                        # Sentiment trends
                                        fig_sentiment = px.line(
                                            df_comparison,
                                            x='Period',
                                            y='Sentiment Score',
                                            title='Sentiment Score Trends',
                                            markers=True
                                        )
                                        st.plotly_chart(fig_sentiment, use_container_width=True)
                                        
                                        # Brand strength trends
                                        fig_brand = px.line(
                                            df_comparison,
                                            x='Period',
                                            y='Brand Strength',
                                            title='Brand Strength Trends',
                                            markers=True
                                        )
                                        st.plotly_chart(fig_brand, use_container_width=True)
                                        
                                        # Data table
                                        st.markdown("#### 📋 Detailed Comparison")
                                        st.dataframe(df_comparison, use_container_width=True)
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        except Exception as e:
                            st.error(f"Comparison failed: {e}")
        
        else:  # Trend Analysis
            st.markdown("**🔄 Trend Analysis**")
            trend_query = st.text_area(
                "Trend Analysis Query:",
                placeholder="Show me sentiment trends for Ola Electric over the last 6 months",
                help="Ask about trends, patterns, or changes over time"
            )
            
            if st.button("📈 Analyze Trends", key="trend_analysis"):
                if trend_query:
                    with st.spinner("Performing trend analysis..."):
                        try:
                            result = asyncio.run(
                                st.session_state.enhanced_service.process_enhanced_query(trend_query)
                            )
                            
                            with col2:
                                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                                st.markdown("### 📈 Trend Analysis Results")
                                st.write(result['response'])
                                
                                if result.get('export_files'):
                                    st.markdown("#### 📁 Export Options")
                                    for file_type, filepath in result['export_files'].items():
                                        if filepath and os.path.exists(filepath):
                                            with open(filepath, 'rb') as f:
                                                st.download_button(
                                                    label=f"📊 Download {file_type.upper()} Report",
                                                    data=f.read(),
                                                    file_name=os.path.basename(filepath),
                                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if file_type == 'excel' else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                                )
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        except Exception as e:
                            st.error(f"Trend analysis failed: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversation memory section
    st.markdown("---")
    st.markdown("### 🧠 Conversation Memory")
    
    if st.button("📚 Show Conversation History"):
        try:
            memory_summary = st.session_state.enhanced_service.get_conversation_summary()
            preferences = st.session_state.enhanced_service.get_user_preferences()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💭 Memory Summary")
                st.text(memory_summary)
            
            with col2:
                st.markdown("#### 🎯 User Preferences")
                for key, value in preferences.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        except Exception as e:
            st.error(f"Memory retrieval failed: {e}")
    
    if st.button("🗑️ Clear Memory", type="secondary"):
        try:
            st.session_state.enhanced_service.clear_conversation_memory()
            st.success("✅ Conversation memory cleared!")
        except Exception as e:
            st.error(f"Memory clear failed: {e}")

if __name__ == "__main__":
    main()
