"""
SolysAI Simple Interface - ChatGPT-style interface with enhanced AI capabilities
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
import io
import base64

# Page configuration
st.set_page_config(
    page_title="SolysAI - EV Market Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-like appearance
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .user-message {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 1rem;
        margin: 1rem 0;
        margin-left: 3rem;
    }
    
    .assistant-message {
        background-color: white;
        padding: 1rem;
        border-radius: 1rem;
        margin: 1rem 0;
        margin-right: 3rem;
        border: 1px solid #e6e9ef;
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem 2rem;
        border-top: 1px solid #e6e9ef;
        z-index: 1000;
    }
    
    .export-button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.5rem;
        margin: 0.5rem 0.25rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    
    .confidence-badge {
        background-color: #e8f5e8;
        color: #2d5a2d;
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        margin: 0.25rem;
    }
    
    .method-badge {
        background-color: #e8f0ff;
        color: #1a4d80;
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        margin: 0.25rem;
    }
    
    /* Hide Streamlit default elements */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Adjust main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_url' not in st.session_state:
    # Auto-detect if running on public ngrok tunnel
    try:
        import requests
        # Check if we can reach localhost API
        requests.get('http://localhost:8000/api/health', timeout=2)
        st.session_state.api_url = 'http://localhost:8000'
    except:
        # If localhost fails, we might be on a public tunnel, use relative path
        st.session_state.api_url = 'http://localhost:8000'  # Will be overridden by user if needed

# Header
st.markdown("""
<div class="main-header">
    <h1>🚗 SolysAI</h1>
    <h3>EV Market Intelligence with Advanced AI Analysis</h3>
    <p>Powered by Gemini 2.5 Pro • Real YouTube Comments • Statistical Analysis</p>
</div>
""", unsafe_allow_html=True)

# Main chat container
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Parse response for enhanced display
            content = message["content"]
            
            # Check if response contains analysis metadata
            if isinstance(content, dict):
                response_text = content.get('response', '')
                metadata = content.get('metadata', {})
                
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>SolysAI:</strong>
                    {response_text}
                """, unsafe_allow_html=True)
                
                # Display analysis metadata if available
                if metadata:
                    badges_html = ""
                    if 'confidence_level' in metadata:
                        badges_html += f'<span class="confidence-badge">Confidence: {metadata["confidence_level"]}%</span>'
                    if 'analysis_method' in metadata:
                        method = metadata['analysis_method'].replace('_', ' ').title()
                        badges_html += f'<span class="method-badge">Method: {method}</span>'
                    if 'total_comments' in metadata:
                        badges_html += f'<span class="confidence-badge">Comments: {metadata["total_comments"]}</span>'
                    
                    if badges_html:
                        st.markdown(f'<div style="margin-top: 1rem;">{badges_html}</div>', unsafe_allow_html=True)
                
                # Add export buttons if applicable
                if metadata.get('export_available'):
                    st.markdown("""
                    <div style="margin-top: 1rem;">
                        <a href="#" class="export-button" onclick="downloadExcel()">📊 Download Excel</a>
                        <a href="#" class="export-button" onclick="downloadWord()">📄 Download Word</a>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>SolysAI:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input area (fixed at bottom)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Create columns for input and send button
col1, col2 = st.columns([8, 1])

with col1:
    user_input = st.text_input(
        "Ask about EV market insights...",
        placeholder="e.g., How is Ola Electric performing in Q1 2025?",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if send_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show thinking indicator
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("""
    <div class="assistant-message">
        <strong>SolysAI:</strong> 🧠 Analyzing with Gemini 2.5 Pro...
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Make API request
        response = requests.post(
            f"{st.session_state.api_url}/query/enhanced",
            json={"query": user_input},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract response and metadata
            ai_response = result.get('response', 'No response received')
            
            # Check for temporal analysis data
            metadata = {}
            if 'temporal_analysis' in result and result['temporal_analysis']:
                temporal_data = result['temporal_analysis']
                
                # Extract confidence and method info from first OEM's data
                for oem_data in temporal_data.values():
                    if isinstance(oem_data, list) and oem_data:
                        latest = oem_data[-1]
                        sentiment = latest.get('sentiment_metrics', {})
                        if sentiment:
                            metadata['confidence_level'] = sentiment.get('confidence_level', 0)
                            metadata['analysis_method'] = sentiment.get('analysis_method', 'unknown')
                            metadata['total_comments'] = sentiment.get('total_comments', 0)
                            metadata['export_available'] = True
                            break
            
            # Format response with metadata
            response_content = {
                'response': ai_response,
                'metadata': metadata
            }
            
            # Clear thinking indicator and add response
            thinking_placeholder.empty()
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            
            # Trigger rerun to show new message
            st.rerun()
            
        else:
            thinking_placeholder.empty()
            error_msg = f"Error: {response.status_code} - {response.text}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()
            
    except requests.exceptions.Timeout:
        thinking_placeholder.empty()
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "⏰ Request timed out. The AI is processing a complex query. Please try again."
        })
        st.rerun()
        
    except Exception as e:
        thinking_placeholder.empty()
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"❌ Error: {str(e)}"
        })
        st.rerun()

# Auto-scroll to bottom
st.markdown("""
<script>
    window.scrollTo(0, document.body.scrollHeight);
    
    function downloadExcel() {
        // Trigger Excel export
        window.open('/export/excel', '_blank');
    }
    
    function downloadWord() {
        // Trigger Word export
        window.open('/export/word', '_blank');
    }
</script>
""", unsafe_allow_html=True)

# Sample questions (show only if no messages)
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; opacity: 0.7;">
        <h4>Try asking:</h4>
        <p>• "How is Ola Electric performing in Q1 2025?"</p>
        <p>• "Compare sentiment for all EV brands in March 2025"</p>
        <p>• "Give me brand strength analysis for Ather"</p>
        <p>• "What are the top issues with Hero Vida?"</p>
        <p>• "Export Bajaj Chetak comments to Excel"</p>
    </div>
    """, unsafe_allow_html=True)

# Add JavaScript for better UX
st.markdown("""
<script>
    // Auto-focus on input
    setTimeout(function() {
        const input = document.querySelector('[data-testid="stTextInput"] input');
        if (input) input.focus();
    }, 100);
    
    // Handle Enter key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            const sendButton = document.querySelector('button[kind="primary"]');
            if (sendButton && document.activeElement.tagName === 'INPUT') {
                e.preventDefault();
                sendButton.click();
            }
        }
    });
</script>
""", unsafe_allow_html=True)
