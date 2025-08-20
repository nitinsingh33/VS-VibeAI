"""
Analytics Dashboard - Real-time Query Monitoring for CEO/Leadership
"""

import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Any

class AnalyticsDashboard:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        
    def load_analytics_data(self) -> Dict[str, Any]:
        """Load analytics data from the API"""
        try:
            response = requests.get(f"{self.api_base}/api/analytics/dashboard")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "No analytics data available"}
        except Exception as e:
            return {"error": f"Failed to load analytics: {str(e)}"}
    
    def load_query_logs(self) -> List[Dict]:
        """Load query logs from file"""
        try:
            if os.path.exists("query_analytics.json"):
                with open("query_analytics.json", 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            st.error(f"Error loading query logs: {e}")
            return []
    
    def create_query_trends_chart(self, logs: List[Dict]):
        """Create query trends over time"""
        if not logs:
            st.warning("No query data available yet")
            return
            
        df = pd.DataFrame(logs)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        
        # Daily query count
        daily_counts = df.groupby('date').size().reset_index(name='queries')
        
        fig = px.line(daily_counts, x='date', y='queries', 
                     title="Daily Query Volume",
                     labels={'queries': 'Number of Queries', 'date': 'Date'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Hourly distribution
        hourly_counts = df.groupby('hour').size().reset_index(name='queries')
        
        fig2 = px.bar(hourly_counts, x='hour', y='queries',
                     title="Query Distribution by Hour",
                     labels={'queries': 'Number of Queries', 'hour': 'Hour of Day'})
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    def create_oem_analysis_chart(self, logs: List[Dict]):
        """Create OEM mention analysis"""
        if not logs:
            return
            
        oem_counts = {'Ola Electric': 0, 'TVS iQube': 0, 'Bajaj Chetak': 0, 'Ather': 0, 'Hero Vida': 0}
        
        for log in logs:
            for oem in log.get('oems_mentioned', []):
                if oem in oem_counts:
                    oem_counts[oem] += 1
        
        if sum(oem_counts.values()) > 0:
            fig = px.pie(values=list(oem_counts.values()), 
                        names=list(oem_counts.keys()),
                        title="OEM Mentions in Queries")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_performance_metrics(self, logs: List[Dict]):
        """Create performance metrics dashboard"""
        if not logs:
            return
            
        df = pd.DataFrame(logs)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_processing_time = df['processing_time'].mean()
            st.metric("Avg Processing Time", f"{avg_processing_time:.1f}ms")
        
        with col2:
            total_queries = len(df)
            st.metric("Total Queries", total_queries)
        
        with col3:
            export_requests = df['export_requested'].sum()
            st.metric("Export Requests", export_requests)
        
        with col4:
            error_rate = (df['error_occurred'].sum() / len(df)) * 100 if len(df) > 0 else 0
            st.metric("Error Rate", f"{error_rate:.1f}%")
        
        # Processing time distribution
        fig = px.histogram(df, x='processing_time', 
                          title="Processing Time Distribution",
                          labels={'processing_time': 'Processing Time (ms)'})
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def show_recent_queries(self, logs: List[Dict], limit: int = 10):
        """Show recent queries table"""
        if not logs:
            st.warning("No recent queries available")
            return
            
        recent_logs = sorted(logs, key=lambda x: x['timestamp'], reverse=True)[:limit]
        
        query_data = []
        for log in recent_logs:
            query_data.append({
                'Timestamp': pd.to_datetime(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                'Query': log['user_query'][:80] + "..." if len(log['user_query']) > 80 else log['user_query'],
                'Processing Time (ms)': f"{log['processing_time']:.1f}",
                'OEMs Mentioned': ', '.join(log.get('oems_mentioned', [])),
                'Export Requested': '✅' if log['export_requested'] else '❌',
                'Error': '⚠️' if log['error_occurred'] else '✅'
            })
        
        df = pd.DataFrame(query_data)
        st.dataframe(df, use_container_width=True, height=400)
    
    def show_query_analysis(self, logs: List[Dict]):
        """Analyze query patterns"""
        if not logs:
            return
            
        # Most common query words
        all_queries = ' '.join([log['user_query'].lower() for log in logs])
        words = all_queries.split()
        
        # Filter out common words
        stop_words = {'what', 'is', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'are', 'vs', 'about', 'how', 'do', 'does', 'did', 'can', 'could', 'should', 'would'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        word_counts = {}
        for word in filtered_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        if word_counts:
            top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:15]
            
            words_df = pd.DataFrame(top_words, columns=['Word', 'Count'])
            
            fig = px.bar(words_df, x='Count', y='Word', orientation='h',
                        title="Most Common Query Terms")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(
        page_title="SolysAI Analytics Dashboard", 
        page_icon="📊", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 SolysAI Analytics Dashboard")
    st.markdown("### Real-time Query Monitoring & Business Intelligence")
    
    dashboard = AnalyticsDashboard()
    
    # Sidebar
    st.sidebar.header("Dashboard Controls")
    
    # Auto-refresh option
    auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)
    if auto_refresh:
        st.rerun()
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    # Export options
    st.sidebar.header("Export Options")
    if st.sidebar.button("📊 Export Analytics Report"):
        try:
            response = requests.get(f"{dashboard.api_base}/api/analytics/export")
            if response.status_code == 200:
                data = response.json()
                if 'download_url' in data:
                    st.sidebar.success("✅ Report exported successfully!")
                    st.sidebar.markdown(f"[📥 Download Report]({data['download_url']})")
            else:
                st.sidebar.error("Failed to export report")
        except Exception as e:
            st.sidebar.error(f"Export error: {e}")
    
    # Load data
    logs = dashboard.load_query_logs()
    analytics_data = dashboard.load_analytics_data()
    
    # Main dashboard
    if logs:
        # Key metrics at the top
        st.header("📈 Key Performance Indicators")
        dashboard.create_performance_metrics(logs)
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Query Trends", 
            "🏢 OEM Analysis", 
            "📝 Recent Queries", 
            "🔍 Query Patterns",
            "⚙️ System Status"
        ])
        
        with tab1:
            st.header("Query Trends Analysis")
            dashboard.create_query_trends_chart(logs)
        
        with tab2:
            st.header("OEM Focus Analysis")
            dashboard.create_oem_analysis_chart(logs)
            
            # Additional OEM insights
            if logs:
                st.subheader("OEM Query Insights")
                oem_queries = {}
                for log in logs:
                    for oem in log.get('oems_mentioned', []):
                        if oem not in oem_queries:
                            oem_queries[oem] = []
                        oem_queries[oem].append(log['user_query'])
                
                for oem, queries in oem_queries.items():
                    with st.expander(f"{oem} - {len(queries)} queries"):
                        for query in queries[-5:]:  # Show last 5 queries
                            st.write(f"• {query}")
        
        with tab3:
            st.header("Recent Query Activity")
            show_limit = st.slider("Number of queries to show", 5, 50, 20)
            dashboard.show_recent_queries(logs, show_limit)
        
        with tab4:
            st.header("Query Pattern Analysis")
            dashboard.show_query_analysis(logs)
        
        with tab5:
            st.header("System Health Status")
            
            # API Health Check
            try:
                health_response = requests.get(f"{dashboard.api_base}/api/health")
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    
                    st.success("✅ API Server: Healthy")
                    
                    # Service status
                    services = health_data.get('services', {})
                    for service_name, service_info in services.items():
                        status = service_info.get('status', 'unknown')
                        emoji = '✅' if status == 'ready' else '⚠️'
                        st.write(f"{emoji} **{service_name.replace('_', ' ').title()}**: {status}")
                        
                        # Additional service details
                        if 'supported_oems' in service_info:
                            st.write(f"   └─ Supported OEMs: {len(service_info['supported_oems'])}")
                        if 'conversation_count' in service_info:
                            st.write(f"   └─ Active conversations: {service_info['conversation_count']}")
                else:
                    st.error("❌ API Server: Unreachable")
            except Exception as e:
                st.error(f"❌ API Connection Error: {e}")
            
            # Data status
            st.subheader("Data Pipeline Status")
            if os.path.exists("all_oem_comments_2500_total_20250816_130830.json"):
                st.success("✅ Comment Database: 2,500 comments loaded")
            else:
                st.warning("⚠️ Comment Database: Limited data available")
            
            # Export status
            export_count = len([f for f in os.listdir("exports") if f.endswith('.xlsx')]) if os.path.exists("exports") else 0
            st.info(f"📊 Export Files: {export_count} reports generated")
    
    else:
        st.warning("⚠️ No analytics data available yet")
        st.info("🚀 Start using the SolysAI platform to generate analytics data!")
        
        # Show system status even without query data
        st.header("🔧 System Status")
        try:
            health_response = requests.get(f"{dashboard.api_base}/api/health")
            if health_response.status_code == 200:
                health_data = health_response.json()
                st.success("✅ SolysAI Platform: Online and Ready")
                
                services = health_data.get('services', {})
                for service_name, service_info in services.items():
                    status = service_info.get('status', 'unknown')
                    emoji = '✅' if status == 'ready' else '⚠️'
                    st.write(f"{emoji} {service_name.replace('_', ' ').title()}: {status}")
            else:
                st.error("❌ SolysAI Platform: Offline")
        except Exception as e:
            st.error(f"❌ Connection Error: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("**SolysAI Analytics Dashboard** | Real-time Business Intelligence for Auto OEMs")
    st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
