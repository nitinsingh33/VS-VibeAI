"""
YouTube Comments Viewer - Browse Real Comments Data
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import glob
import os

st.set_page_config(
    page_title="📱 YouTube Comments Viewer", 
    page_icon="📱",
    layout="wide"
)

st.title("📱 Real YouTube Comments Viewer")
st.markdown("Browse and analyze real YouTube comments collected from Indian electric scooter videos")

# Find all comment files
@st.cache_data
def load_comment_files():
    """Load all available comment files"""
    files = []
    
    # Individual OEM files
    oem_files = glob.glob("comments_*_comments_*.json")
    for file in oem_files:
        files.append({
            'file': file,
            'type': 'individual',
            'size': os.path.getsize(file),
            'modified': datetime.fromtimestamp(os.path.getmtime(file))
        })
    
    # Combined files
    combined_files = glob.glob("all_oem_comments_*.json")
    for file in combined_files:
        files.append({
            'file': file,
            'type': 'combined',
            'size': os.path.getsize(file),
            'modified': datetime.fromtimestamp(os.path.getmtime(file))
        })
    
    return sorted(files, key=lambda x: x['modified'], reverse=True)

@st.cache_data
def load_comments_from_file(filename):
    """Load comments from a specific file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different file formats
        if 'comments' in data:
            # New format with metadata
            return data['comments'], data.get('total_comments', 0), data.get('scrape_timestamp', 'Unknown')
        else:
            # Old format - direct OEM data
            total = sum(len(comments) for comments in data.values())
            return data, total, 'Unknown'
            
    except Exception as e:
        st.error(f"Error loading file {filename}: {e}")
        return {}, 0, 'Error'

# Sidebar - File Selection
with st.sidebar:
    st.header("📁 Comment Files")
    
    files = load_comment_files()
    
    if not files:
        st.warning("No comment files found. Run scraping first.")
        st.stop()
    
    # Show file information
    st.subheader("Available Files:")
    for file_info in files:
        file_type_icon = "📊" if file_info['type'] == 'combined' else "🏭"
        size_mb = file_info['size'] / (1024 * 1024)
        st.write(f"{file_type_icon} `{file_info['file']}`")
        st.write(f"   📦 {size_mb:.1f}MB - {file_info['modified'].strftime('%m/%d %H:%M')}")
    
    st.divider()
    
    # File selector
    selected_file = st.selectbox(
        "Select file to view:",
        [f['file'] for f in files],
        format_func=lambda x: f"{'📊' if 'all_oem' in x else '🏭'} {x}"
    )

# Load selected file
if selected_file:
    comments_data, total_comments, timestamp = load_comments_from_file(selected_file)
    
    # File information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Comments", total_comments)
    with col2:
        st.metric("🏭 OEMs Covered", len(comments_data))
    with col3:
        st.metric("📅 Scraped", timestamp)
    
    st.divider()
    
    # OEM selector
    selected_oem = st.selectbox(
        "🏭 Select OEM to view comments:",
        list(comments_data.keys()),
        index=0
    )
    
    if selected_oem and comments_data[selected_oem]:
        oem_comments = comments_data[selected_oem]
        
        st.subheader(f"📱 {selected_oem} Comments ({len(oem_comments)} total)")
        
        # Comment statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_likes = sum(c.get('likes', 0) for c in oem_comments) / len(oem_comments)
            st.metric("👍 Avg Likes", f"{avg_likes:.1f}")
        
        with col2:
            unique_authors = len(set(c.get('author', 'Unknown') for c in oem_comments))
            st.metric("👤 Unique Users", unique_authors)
        
        with col3:
            real_comments = len([c for c in oem_comments if c.get('extraction_method') in ['downloader', 'ytdlp']])
            st.metric("✅ Real Comments", real_comments)
        
        with col4:
            unique_videos = len(set(c.get('video_title', 'Unknown') for c in oem_comments))
            st.metric("📺 Videos", unique_videos)
        
        st.divider()
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            min_likes = st.slider("Minimum likes", 0, 100, 0)
            
        with col2:
            search_text = st.text_input("🔍 Search in comments", placeholder="Enter keywords...")
        
        # Filter comments
        filtered_comments = oem_comments
        
        if min_likes > 0:
            filtered_comments = [c for c in filtered_comments if c.get('likes', 0) >= min_likes]
        
        if search_text:
            filtered_comments = [c for c in filtered_comments if search_text.lower() in c.get('text', '').lower()]
        
        st.write(f"📋 Showing {len(filtered_comments)} of {len(oem_comments)} comments")
        
        # Display comments
        for i, comment in enumerate(filtered_comments[:20]):  # Show first 20
            with st.expander(f"💬 Comment {i+1}: {comment.get('text', '')[:60]}..."):
                
                # Comment details
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Comment:** {comment.get('text', 'No text')}")
                    st.markdown(f"**Author:** {comment.get('author', 'Unknown')}")
                    st.markdown(f"**Video:** {comment.get('video_title', 'Unknown')}")
                    
                    if comment.get('video_url'):
                        st.markdown(f"**Video URL:** [{comment['video_url']}]({comment['video_url']})")
                
                with col2:
                    st.metric("👍 Likes", comment.get('likes', 0))
                    st.write(f"📅 {comment.get('date', 'Unknown date')}")
                    
                    extraction_method = comment.get('extraction_method', 'Unknown')
                    if extraction_method in ['downloader', 'ytdlp']:
                        st.success(f"✅ Real ({extraction_method})")
                    else:
                        st.info(f"ℹ️ {extraction_method}")
        
        if len(filtered_comments) > 20:
            st.info(f"📄 Showing first 20 comments. Total filtered: {len(filtered_comments)}")
        
        # Download option
        st.divider()
        
        if st.button("📥 Download Comments as CSV"):
            df = pd.DataFrame(filtered_comments)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{selected_oem}_comments.csv",
                mime="text/csv"
            )
        
        # Comment analytics
        st.divider()
        st.subheader("📊 Comment Analytics")
        
        # Sentiment word analysis
        all_text = ' '.join([c.get('text', '') for c in filtered_comments]).lower()
        
        # Simple keyword analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'best', 'love', 'perfect', 'awesome']
        negative_words = ['bad', 'worst', 'terrible', 'problem', 'issue', 'disappointing', 'poor', 'hate']
        
        positive_count = sum(word in all_text for word in positive_words)
        negative_count = sum(word in all_text for word in negative_words)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("😊 Positive Keywords", positive_count)
        
        with col2:
            st.metric("😞 Negative Keywords", negative_count)
        
        # Top videos by comment count
        video_counts = {}
        for comment in filtered_comments:
            video = comment.get('video_title', 'Unknown')[:50] + "..."
            video_counts[video] = video_counts.get(video, 0) + 1
        
        if video_counts:
            st.subheader("📺 Top Videos by Comment Count")
            video_df = pd.DataFrame(list(video_counts.items()), columns=['Video', 'Comments'])
            video_df = video_df.sort_values('Comments', ascending=False).head(10)
            
            fig = px.bar(video_df, x='Comments', y='Video', orientation='h')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 Select a comment file from the sidebar to start viewing real YouTube comments!")

# Footer
st.divider()
st.markdown("""
### 💡 How to Use This Viewer

1. **Select a file** from the sidebar (📊 = combined data, 🏭 = individual OEM)
2. **Choose an OEM** to view their specific comments
3. **Filter comments** by likes or search for keywords
4. **Click on comments** to see full details and video links
5. **Download data** as CSV for further analysis

**Data Sources:** All comments are real YouTube user feedback collected from actual videos about Indian electric scooters.
""")
