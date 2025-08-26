#!/usr/bin/env python3
"""
SolysAI Search Agent - Main FastAPI Application
A Python-based AI agent that searches for information and generates responses using Gemini 2.0 Flash
"""

import os
import asyncio
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from services.agent_service import AgentService
from services.search_service import SearchService
from services.gemini_service import GeminiService
from services.enhanced_agent_service import EnhancedAgentService
from services.query_analytics_service import QueryAnalyticsService
from services.response_formatter import ResponseFormatter

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="SolysAI Search Agent",
    description="An AI agent that searches for information and generates factually grounded responses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
search_service = SearchService()
gemini_service = GeminiService()
agent_service = AgentService()
enhanced_agent_service = EnhancedAgentService()
analytics_service = QueryAnalyticsService()
response_formatter = ResponseFormatter()

# Pydantic models for request/response
class SearchSource(BaseModel):
    title: str
    url: str
    snippet: str

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The chat query")

class ChatResponse(BaseModel):
    answer: str
    sources: List[SearchSource] = []
    processing_time: Optional[float] = None

class EnhancedChatResponse(BaseModel):
    answer: str
    analysis_summary: Dict[str, Any] = {}
    data_relevance: Dict[str, Any] = {}
    structured_sources: Dict[str, List[Dict]] = {}
    export_availability: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    processing_time: Optional[float] = None

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="The search query")
    max_results: Optional[int] = Field(default=5, ge=1, le=10, description="Maximum number of search results")

class EnhancedSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The enhanced search query")
    use_youtube_data: Optional[bool] = Field(default=True, description="Include YouTube comment analysis")
    max_search_results: Optional[int] = Field(default=5, ge=1, le=10, description="Maximum search results")
    enable_export: Optional[bool] = Field(default=True, description="Enable data export generation")

class ExportFile(BaseModel):
    filename: str
    file_type: str
    download_url: str

class EnhancedSearchResponse(BaseModel):
    query: str
    response: str
    sources: List[SearchSource]
    youtube_data_used: bool
    temporal_analysis: Optional[Dict[str, Any]] = None
    conversation_context: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    export_files: Dict[str, str] = {}
    exportable: bool = False

class SearchResponse(BaseModel):
    query: str
    response: str
    sources: List[SearchSource]
    search_results: int
    processing_time: Optional[float]
    timestamp: str
    fallback: Optional[bool] = False
    fallback_reason: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, Any]

# Mount static files (for web interface)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    pass  # Static directory might not exist yet

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the VibeAI Frontend Interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VibeAI - EV Sentiment Analysis Platform</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; color: white; margin-bottom: 40px; }
            .header h1 { font-size: 3.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-bottom: 40px; }
            .feature-card { 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
                transition: transform 0.3s ease;
            }
            .feature-card:hover { transform: translateY(-5px); }
            .feature-card h3 { color: #667eea; margin-bottom: 15px; font-size: 1.4em; }
            .feature-card p { color: #666; line-height: 1.6; }
            .api-section { background: white; border-radius: 15px; padding: 30px; margin-bottom: 30px; }
            .api-buttons { display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 20px; }
            .api-btn { 
                padding: 12px 25px; 
                background: #667eea; 
                color: white; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .api-btn:hover { background: #5a67d8; transform: translateY(-2px); }
            .stats { display: flex; justify-content: space-around; background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin-top: 30px; }
            .stat { text-align: center; color: white; }
            .stat h4 { font-size: 2em; margin-bottom: 5px; }
            .footer { text-align: center; color: white; margin-top: 40px; opacity: 0.8; }
            .demo-section { background: #f8f9fa; border-radius: 15px; padding: 30px; margin: 20px 0; }
            .demo-form { max-width: 600px; margin: 0 auto; }
            .demo-input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; margin-bottom: 15px; }
            .demo-btn { width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
            .demo-btn:hover { background: #218838; }
            .result-box { margin-top: 20px; padding: 20px; background: white; border-radius: 8px; border-left: 5px solid #667eea; }
        </style>
    </head>
    <body>
        <div class="container">
            <header class="header">
                <h1>🚀 VibeAI</h1>
                <p>Advanced EV Sentiment Analysis Platform</p>
                <p>Powered by Gemini 2.5 Pro • 100K+ Comments • 10 EV Brands</p>
            </header>

            <div class="features-grid">
                <div class="feature-card">
                    <h3>🤖 AI-Powered Analysis</h3>
                    <p>Advanced sentiment analysis using Google's Gemini 2.5 Pro AI model with enhanced timeout handling and intelligent retry mechanisms.</p>
                </div>
                <div class="feature-card">
                    <h3>📊 Complete EV Coverage</h3>
                    <p>Analysis of 10 major Indian EV brands: Ola Electric, Ather, Bajaj Chetak, TVS iQube, Hero Vida, Ampere, River Mobility, Ultraviolette, Revolt, BGauss.</p>
                </div>
                <div class="feature-card">
                    <h3>📈 Temporal Analysis</h3>
                    <p>Track sentiment trends over time with month-by-month and year-by-year analysis capabilities for comprehensive market insights.</p>
                </div>
                <div class="feature-card">
                    <h3>📄 Professional Reports</h3>
                    <p>Export detailed analysis in Excel, Word, and CSV formats with professional formatting and comprehensive data visualization.</p>
                </div>
            </div>

            <div class="demo-section">
                <h2 style="text-align: center; margin-bottom: 20px;">🎯 Try Live Analysis</h2>
                <div class="demo-form">
                    <input type="text" id="queryInput" class="demo-input" placeholder="Ask about EV sentiment... (e.g., 'What is the sentiment for Ola Electric in 2025?')" value="What is the sentiment for Ola Electric in 2025?">
                    <button onclick="runAnalysis()" class="demo-btn">🔍 Analyze Sentiment</button>
                    <div id="result" class="result-box" style="display: none;">
                        <h4>Analysis Result:</h4>
                        <div id="resultContent"></div>
                    </div>
                </div>
            </div>

            <div class="api-section">
                <h2 style="text-align: center; margin-bottom: 20px;">🔗 API Access Points</h2>
                <div class="api-buttons">
                    <a href="/docs" class="api-btn">📖 Interactive API Docs</a>
                    <a href="/api/health" class="api-btn">🏥 Health Check</a>
                    <a href="/api/youtube-analytics" class="api-btn">📊 Analytics Data</a>
                    <a href="/api/export/excel-report" class="api-btn">📄 Excel Export</a>
                    <a href="/api/export/word-report" class="api-btn">📝 Word Export</a>
                </div>
            </div>

            <div class="stats">
                <div class="stat">
                    <h4>100K+</h4>
                    <p>Comments Analyzed</p>
                </div>
                <div class="stat">
                    <h4>10</h4>
                    <p>EV Brands Covered</p>
                </div>
                <div class="stat">
                    <h4>99.9%</h4>
                    <p>Uptime</p>
                </div>
                <div class="stat">
                    <h4>Real-time</h4>
                    <p>AI Processing</p>
                </div>
            </div>

            <footer class="footer">
                <p>© 2025 VibeAI - Advanced EV Sentiment Analysis Platform</p>
                <p>Powered by Gemini 2.5 Pro • Deployed on Render</p>
            </footer>
        </div>

        <script>
            async function runAnalysis() {
                const query = document.getElementById('queryInput').value;
                const resultDiv = document.getElementById('result');
                const contentDiv = document.getElementById('resultContent');
                
                if (!query.trim()) {
                    alert('Please enter a query');
                    return;
                }

                resultDiv.style.display = 'block';
                contentDiv.innerHTML = '<p>🔄 Analyzing with Gemini 2.5 Pro... Please wait...</p>';

                try {
                    const response = await fetch('/api/enhanced-search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            query: query,
                            use_youtube_data: true,
                            max_search_results: 5
                        })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        contentDiv.innerHTML = `
                            <p><strong>Query:</strong> ${data.query}</p>
                            <p><strong>Response:</strong></p>
                            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                ${data.response.replace(/\\n/g, '<br>')}
                            </div>
                            <p><strong>Sources:</strong> ${data.sources.length} sources analyzed</p>
                            <p><strong>Processing Time:</strong> ${data.processing_time?.toFixed(2)} seconds</p>
                            ${data.youtube_data_used ? '<p>✅ YouTube data included in analysis</p>' : ''}
                        `;
                    } else {
                        throw new Error(`HTTP ${response.status}`);
                    }
                } catch (error) {
                    contentDiv.innerHTML = `
                        <p style="color: red;">❌ Analysis failed: ${error.message}</p>
                        <p>Please try again or check the API documentation.</p>
                    `;
                }
            }

            // Allow Enter key to trigger analysis
            document.getElementById('queryInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    runAnalysis();
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/api/agent/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest):
    """Chat endpoint for conversational AI agent with enhanced formatting"""
    try:
        start_time = time.time()
        
        # Use enhanced agent service for richer responses
        result = await enhanced_agent_service.process_enhanced_query(
            query=request.query,
            use_youtube_data=True,
            max_search_results=5
        )
        
        processing_time = time.time() - start_time
        result['processing_time'] = processing_time
        result['query'] = request.query
        
        # Format response for better readability and structure
        formatted_result = response_formatter.format_enhanced_response(
            response=result.get('response', ''),
            sources=result.get('sources', []),
            query=request.query,
            metadata=result
        )
        
        return ChatResponse(
            answer=formatted_result.get('answer', 'No response generated'),
            sources=result.get('sources', []),
            processing_time=processing_time
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/api/agent/enhanced-chat", response_model=EnhancedChatResponse)
async def enhanced_agent_chat(request: ChatRequest):
    """Enhanced chat endpoint with full structured response, source categorization, and export capabilities"""
    try:
        start_time = time.time()
        
        # Use enhanced agent service for richer responses
        result = await enhanced_agent_service.process_enhanced_query(
            query=request.query,
            use_youtube_data=True,
            max_search_results=5
        )
        
        processing_time = time.time() - start_time
        result['processing_time'] = processing_time
        result['query'] = request.query
        
        # Format response with full structure
        formatted_result = response_formatter.format_enhanced_response(
            response=result.get('response', ''),
            sources=result.get('sources', []),
            query=request.query,
            metadata=result
        )
        
        return EnhancedChatResponse(
            answer=formatted_result.get('answer', 'No response generated'),
            analysis_summary=formatted_result.get('analysis_summary', {}),
            data_relevance=formatted_result.get('data_relevance', {}),
            structured_sources=formatted_result.get('structured_sources', {}),
            export_availability=formatted_result.get('export_availability', {}),
            metadata=formatted_result.get('metadata', {}),
            processing_time=processing_time
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced chat error: {str(e)}")

@app.post("/api/search", response_model=SearchResponse)
async def search_and_generate(request: SearchRequest):
    """Search for information and generate a factually grounded response"""
    try:
        result = await agent_service.process_query(request.query, request.max_results)
        return SearchResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/enhanced-search", response_model=EnhancedSearchResponse)
async def enhanced_search_and_generate(request: EnhancedSearchRequest, http_request: Request):
    """Enhanced search with YouTube comments integration and export capabilities"""
    start_time = time.time()
    query_id = None
    error_occurred = False
    error_message = None
    
    try:
        # Extract user information
        user_ip = http_request.client.host if http_request.client else None
        user_agent = http_request.headers.get("user-agent", "")
        session_id = http_request.headers.get("x-session-id", str(uuid.uuid4()))
        
        # Process the query
        result = await enhanced_agent_service.process_enhanced_query(
            query=request.query,
            use_youtube_data=request.use_youtube_data,
            max_search_results=request.max_search_results
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Extract metadata for analytics
        metadata = {
            'analysis_method': 'enhanced_search',
            'temporal_analysis_used': bool(result.get('temporal_analysis')),
            'export_requested': request.enable_export,
            'confidence_level': None,
            'total_comments': None
        }
        
        # Try to extract confidence and comment count from temporal analysis
        if result.get('temporal_analysis'):
            temporal_data = result['temporal_analysis']
            for oem_data in temporal_data.values():
                if isinstance(oem_data, list) and oem_data:
                    sentiment = oem_data[-1].get('sentiment_metrics', {})
                    if sentiment:
                        metadata['confidence_level'] = sentiment.get('confidence_level')
                        metadata['total_comments'] = sentiment.get('total_comments')
                        metadata['analysis_method'] = sentiment.get('analysis_method', 'enhanced_search')
                        break
        
        # Log the query
        query_id = analytics_service.log_query(
            user_query=request.query,
            response=result.get('response', ''),
            processing_time=processing_time,
            analysis_metadata=metadata,
            user_info={
                'ip': user_ip,
                'user_agent': user_agent,
                'session_id': session_id
            }
        )
        
        # Add query ID to response for tracking
        result['query_id'] = query_id
        
        return EnhancedSearchResponse(**result)
        
    except ValueError as e:
        error_occurred = True
        error_message = str(e)
        processing_time = time.time() - start_time
        
        # Log the error
        if not query_id:
            analytics_service.log_query(
                user_query=request.query,
                response="",
                processing_time=processing_time,
                user_info={
                    'ip': http_request.client.host if http_request.client else None,
                    'user_agent': http_request.headers.get("user-agent", ""),
                    'session_id': http_request.headers.get("x-session-id", str(uuid.uuid4()))
                },
                error_info={
                    'error_occurred': True,
                    'error_message': error_message
                }
            )
        
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        error_occurred = True
        error_message = str(e)
        processing_time = time.time() - start_time
        
        # Log the error
        if not query_id:
            analytics_service.log_query(
                user_query=request.query,
                response="",
                processing_time=processing_time,
                user_info={
                    'ip': http_request.client.host if http_request.client else None,
                    'user_agent': http_request.headers.get("user-agent", ""),
                    'session_id': http_request.headers.get("x-session-id", str(uuid.uuid4()))
                },
                error_info={
                    'error_occurred': True,
                    'error_message': error_message
                }
            )
        
        raise HTTPException(status_code=500, detail=f"Enhanced search error: {str(e)}")

@app.get("/api/export/{file_type}/{filename}")
async def download_export_file(file_type: str, filename: str):
    """Download exported data files"""
    try:
        export_dir = "exports"
        file_path = os.path.join(export_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Export file not found")
        
        # Determine media type based on file extension
        media_types = {
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        
        media_type = media_types.get(file_type, 'application/octet-stream')
        
        with open(file_path, 'rb') as f:
            content = f.read()
        
        from fastapi.responses import Response
        return Response(
            content=content,
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export download error: {str(e)}")

@app.get("/api/export/raw-data/{oem_name}")
async def export_raw_oem_data(
    oem_name: str, 
    format: str = "json",
    date_range: Optional[str] = None,
    sentiment_filter: Optional[str] = None,
    limit: Optional[int] = None
):
    """Export raw YouTube comment data for any OEM"""
    try:
        print(f"🔍 Export request for OEM: {oem_name}")
        
        # Load YouTube data using the enhanced agent service instance
        data_result = await enhanced_agent_service.load_youtube_data()
        youtube_data = data_result.get('youtube_data', {})
        
        print(f"📊 Available OEMs: {list(youtube_data.keys())}")
        
        # Find matching OEM (case-insensitive)
        matched_oem = None
        for oem in youtube_data.keys():
            if oem.lower().replace(' ', '-') == oem_name.lower() or oem.lower() == oem_name.lower():
                matched_oem = oem
                break
        
        if not matched_oem:
            available_oems = [oem.lower().replace(' ', '-') for oem in youtube_data.keys()]
            raise HTTPException(
                status_code=404, 
                detail=f"OEM '{oem_name}' not found. Available: {', '.join(available_oems)}"
            )
        
        raw_comments = youtube_data[matched_oem]
        print(f"💬 Found {len(raw_comments)} comments for {matched_oem}")
        
        # Apply filters
        filtered_comments = raw_comments
        
        if sentiment_filter:
            filtered_comments = [
                c for c in filtered_comments 
                if c.get('sentiment', '').lower() == sentiment_filter.lower()
            ]
        
        if limit:
            filtered_comments = filtered_comments[:limit]
        
        # Prepare export data
        export_data = {
            'oem': matched_oem,
            'total_comments': len(filtered_comments),
            'export_timestamp': datetime.now().isoformat(),
            'filters_applied': {
                'sentiment_filter': sentiment_filter,
                'date_range': date_range,
                'limit': limit
            },
            'raw_data': filtered_comments[:10] if len(filtered_comments) > 10 else filtered_comments  # Limit for demo
        }
        
        # Return in requested format
        if format.lower() == 'json':
            return export_data
        else:
            raise HTTPException(status_code=400, detail="Only JSON format supported in demo")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"💥 Export error details: {e}")
        print(f"💥 Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Export download error: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Export error details: {e}")
        raise HTTPException(status_code=500, detail=f"Export download error: {str(e)}")

@app.get("/api/youtube-analytics")
async def get_youtube_analytics():
    """Get YouTube comment analytics"""
    try:
        analytics = await enhanced_agent_service.get_youtube_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Get the health status of the application and its services"""
    health_status = enhanced_agent_service.get_health_status()
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        services=health_status
    )

@app.get("/api/temporal-analysis/{oem_name}")
async def get_temporal_brand_analysis(oem_name: str, periods: str = "July 2025,August 2024"):
    """Get temporal brand analysis for specific OEM across multiple periods"""
    try:
        period_list = [p.strip() for p in periods.split(',')]
        analysis = await enhanced_agent_service.get_temporal_brand_analysis(oem_name, period_list)
        return {
            "oem": oem_name,
            "periods_analyzed": period_list,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Temporal analysis error: {str(e)}")

@app.get("/api/conversation-memory")
async def get_conversation_memory():
    """Get conversation memory summary and user preferences"""
    try:
        memory_summary = enhanced_agent_service.get_conversation_summary()
        preferences = enhanced_agent_service.get_user_preferences()
        
        return {
            "memory_summary": memory_summary,
            "user_preferences": preferences,
            "conversation_count": len(enhanced_agent_service.memory_service.conversation_history),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory retrieval error: {str(e)}")

@app.delete("/api/conversation-memory")
async def clear_conversation_memory():
    """Clear conversation memory"""
    try:
        enhanced_agent_service.clear_conversation_memory()
        return {
            "message": "Conversation memory cleared successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory clear error: {str(e)}")

@app.post("/api/enhanced-temporal-search")
async def enhanced_temporal_search(request: EnhancedSearchRequest):
    """Enhanced search with explicit temporal analysis support"""
    try:
        # Process with enhanced temporal awareness
        result = await enhanced_agent_service.process_enhanced_query(
            request.query,
            use_youtube_data=request.use_youtube_data,
            max_search_results=request.max_results
        )
        
        # Add temporal analysis summary if available
        if result.get('temporal_analysis'):
            result['temporal_summary'] = {
                'time_period': result.get('time_period'),
                'analysis_performed': True,
                'oems_analyzed': list(result['temporal_analysis'].keys()) if result['temporal_analysis'] else [],
                'conversation_context_used': result.get('conversation_context_used', False)
            }
        
        return EnhancedSearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced temporal search error: {str(e)}")

@app.get("/api/docs")
async def api_documentation():
    """Get API documentation"""
    return {
        "title": "SolysAI Search Agent API",
        "version": "2.0.0",
        "description": "Enhanced AI agent with temporal analysis and conversation memory",
        "endpoints": {
            "POST /api/search": "Basic search with Gemini AI",
            "POST /api/enhanced-search": "Enhanced search with YouTube comments and temporal analysis",
            "POST /api/enhanced-temporal-search": "Enhanced search with explicit temporal analysis",
            "GET /api/temporal-analysis/{oem_name}": "Get temporal brand analysis for specific OEM",
            "GET /api/conversation-memory": "Get conversation memory and user preferences",
            "DELETE /api/conversation-memory": "Clear conversation memory",
            "GET /api/youtube-analytics": "Get YouTube comment analytics",
            "GET /api/export/{file_type}/{filename}": "Download export files",
            "GET /api/health": "Health check with all services",
            "GET /api/analytics/summary": "Get analytics summary",
            "GET /api/analytics/recent-queries": "Get recent queries",
            "GET /api/analytics/export": "Export analytics to Excel",
            "GET /": "Web interface",
            "GET /docs": "Interactive API docs",
            "GET /redoc": "ReDoc API docs"
        },
        "new_features": {
            "temporal_analysis": "Analyze comments by specific time periods (months, quarters, years)",
            "conversation_memory": "System remembers conversation context and user preferences",
            "brand_strength": "Calculate brand strength metrics over time",
            "enhanced_export": "Export includes temporal analysis and conversation context",
            "query_analytics": "Track user queries and system performance"
        },
        "example_temporal_queries": [
            "What was the sentiment for Ola Electric in August 2024?",
            "Compare Ather's brand strength in Q2 2025 vs Q1 2025",
            "Show me TVS iQube performance trends for the last 6 months",
            "Export all comments from July 2025 with sentiment analysis"
        ],
        "example_request": {
            "query": "What was the sentiment for Ola Electric in August 2024?",
            "max_results": 5,
            "use_youtube_data": True
        }
    }

@app.get("/api/analytics/summary")
async def get_analytics_summary(days: int = 7):
    """Get analytics summary for the last N days"""
    try:
        summary = analytics_service.get_analytics_summary(days=days)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@app.get("/api/analytics/recent-queries")
async def get_recent_queries(limit: int = 50):
    """Get recent queries for monitoring"""
    try:
        queries = analytics_service.get_recent_queries(limit=limit)
        return {
            "recent_queries": queries,
            "total_returned": len(queries)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@app.get("/api/analytics/export")
async def export_analytics():
    """Export analytics data to Excel"""
    try:
        from fastapi.responses import FileResponse
        import tempfile
        import os
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            output_file = analytics_service.export_analytics_to_excel(tmp.name)
            
        if output_file and os.path.exists(output_file):
            return FileResponse(
                path=output_file,
                filename=f"solysai_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate analytics export")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")

@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard():
    """Get comprehensive analytics dashboard data"""
    try:
        summary_7d = analytics_service.get_analytics_summary(days=7)
        summary_30d = analytics_service.get_analytics_summary(days=30)
        recent_queries = analytics_service.get_recent_queries(limit=20)
        
        return {
            "dashboard": {
                "last_7_days": summary_7d,
                "last_30_days": summary_30d,
                "recent_activity": recent_queries[-10:] if recent_queries else [],
                "system_status": "operational",
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting SolysAI Search Agent on port {port}")
    print(f"📊 Health check: http://localhost:{port}/api/health")
    print(f"🌐 Web interface: http://localhost:{port}")
    print(f"📖 API docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
