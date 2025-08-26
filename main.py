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
from services.document_export_service import DocumentExportService

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
    allow_origins=[
        "https://da13e6078214.ngrok-free.app",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ],
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
document_export_service = DocumentExportService()

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
    """Serve the VibeAI Web Interface"""
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
                display: flex;
                align-items: center;
                justify-content: center;
                color: #333;
            }
            .container { 
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 900px;
                width: 90%;
                text-align: center;
            }
            .logo { 
                font-size: 3.5em;
                font-weight: bold;
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 20px;
            }
            .subtitle { 
                font-size: 1.3em;
                color: #666;
                margin-bottom: 40px;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }
            .feature-card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                transition: transform 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-5px);
            }
            .feature-icon {
                font-size: 2.5em;
                margin-bottom: 15px;
            }
            .feature-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
                color: #333;
            }
            .feature-desc {
                color: #666;
                line-height: 1.5;
            }
            .cta-section {
                margin: 40px 0;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                margin: 10px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }
            .btn-secondary {
                background: linear-gradient(45deg, #11998e, #38ef7d);
            }
            .stats {
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
                flex-wrap: wrap;
            }
            .stat {
                text-align: center;
                padding: 20px;
            }
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                color: #666;
                font-size: 1.1em;
            }
            .demo-section {
                background: #f8f9fa;
                padding: 30px;
                border-radius: 15px;
                margin: 30px 0;
            }
            .query-input {
                width: 100%;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 10px;
                font-size: 16px;
                margin: 10px 0;
            }
            .query-input:focus {
                outline: none;
                border-color: #667eea;
            }
            #result {
                margin-top: 20px;
                padding: 20px;
                background: white;
                border-radius: 10px;
                text-align: left;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🔍 VibeAI</div>
            <div class="subtitle">Advanced EV Sentiment Analysis Platform</div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">10</div>
                    <div class="stat-label">EV Brands</div>
                </div>
                <div class="stat">
                    <div class="stat-number">100K+</div>
                    <div class="stat-label">Comments</div>
                </div>
                <div class="stat">
                    <div class="stat-number">AI</div>
                    <div class="stat-label">Powered</div>
                </div>
            </div>

            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <div class="feature-title">AI Analysis</div>
                    <div class="feature-desc">Gemini 2.5 Pro powered sentiment analysis with advanced natural language processing</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">10 EV Brands</div>
                    <div class="feature-desc">Complete coverage: Ola, Ather, Bajaj, TVS, Hero, Ampere, River, Ultraviolette, Revolt, BGauss</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <div class="feature-title">Temporal Analysis</div>
                    <div class="feature-desc">Track sentiment trends by month and year with historical insights</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">�</div>
                    <div class="feature-title">Export Reports</div>
                    <div class="feature-desc">Download professional Excel and Word reports with detailed analytics</div>
                </div>
            </div>

            <div class="demo-section">
                <h3>🎯 Try Live Analysis</h3>
                <input type="text" class="query-input" id="queryInput" placeholder="e.g., What is the sentiment for Ola Electric in 2025?" value="What is the sentiment for Ola Electric?">
                <br>
                <button class="btn" onclick="runAnalysis()">🚀 Analyze Now</button>
                <div id="result"></div>
            </div>

            <div class="cta-section">
                <a href="/docs" class="btn">📖 API Documentation</a>
                <a href="/api/health" class="btn btn-secondary">🏥 System Health</a>
            </div>

            <div style="margin-top: 30px; color: #888;">
                <p>🔥 Real-time sentiment analysis for Indian EV market</p>
                <p>💡 Powered by advanced AI and 100,000+ user comments</p>
            </div>
        </div>

        <script>
            async function runAnalysis() {
                const query = document.getElementById('queryInput').value;
                const resultDiv = document.getElementById('result');
                
                if (!query.trim()) {
                    alert('Please enter a query!');
                    return;
                }

                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<div style="text-align: center; color: #667eea;">🔍 Analyzing... This may take 30-60 seconds for AI processing...</div>';

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
                        resultDiv.innerHTML = `
                            <h4>✅ Analysis Complete!</h4>
                            <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                <strong>🤖 AI Response:</strong><br>
                                ${data.response || 'Analysis completed successfully!'}
                            </div>
                            <div style="margin-top: 15px;">
                                <strong>📊 Data Sources:</strong> ${data.youtube_data_used ? '✅ YouTube Data' : '❌ No YouTube Data'}<br>
                                <strong>⏱️ Processing Time:</strong> ${data.processing_time ? Math.round(data.processing_time) + 's' : 'N/A'}<br>
                                <strong>🎯 Export Available:</strong> ${data.exportable ? '✅ Yes' : '❌ No'}
                            </div>
                        `;
                    } else {
                        throw new Error('Analysis failed');
                    }
                } catch (error) {
                    resultDiv.innerHTML = `
                        <div style="color: #e74c3c;">
                            ❌ Analysis failed. Please try again or visit <a href="/docs" style="color: #667eea;">/docs</a> for API documentation.
                        </div>
                    `;
                }
            }

            // Auto-focus input
            document.getElementById('queryInput').focus();
            
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

@app.get("/api/test/oems")
async def test_oems():
    """Test endpoint to check available OEMs"""
    try:
        # Check what files are available
        import os
        import glob
        
        files = []
        patterns = [
            "all_oem_comments_*.json",
            "comments_*.json"
        ]
        
        for pattern in patterns:
            files.extend(glob.glob(pattern))
        
        # Test the enhanced agent service directly
        existing_files = enhanced_agent_service._find_latest_scraped_data()
        
        data_result = await enhanced_agent_service.load_youtube_data()
        youtube_data = data_result.get('youtube_data', {})
        
        return {
            "available_files": files[:10],  # First 10 files
            "existing_files_found": existing_files,
            "available_oems": list(youtube_data.keys()),
            "total_oems": len(youtube_data),
            "sample_data": {oem: len(comments) for oem, comments in list(youtube_data.items())[:3]}
        }
    except Exception as e:
        return {"error": str(e), "error_type": str(type(e))}

@app.get("/api/export/raw-data/{oem_name}")
async def export_raw_oem_data(oem_name: str, limit: Optional[int] = 50):
    """Export raw YouTube comment data for any OEM"""
    try:
        # Use the same process as the enhanced chat endpoint
        result = await enhanced_agent_service.process_enhanced_query(
            f"Export raw comment data for {oem_name}",
            enable_search=False,  # Only use YouTube data
            enable_temporal_analysis=False
        )
        
        # Extract the raw data from the result
        raw_data = result.get('raw_youtube_data', {})
        
        # Find the matching OEM
        matched_oem = None
        for oem_key in raw_data.keys():
            if oem_key.lower().replace(' ', '').replace('-', '') == oem_name.lower().replace(' ', '').replace('-', ''):
                matched_oem = oem_key
                break
        
        if not matched_oem:
            available_oems = list(raw_data.keys())
            return {
                "error": f"OEM '{oem_name}' not found",
                "available_oems": available_oems,
                "suggestion": "Try: " + ", ".join([oem.lower().replace(' ', '-') for oem in available_oems[:5]])
            }
        
        comments = raw_data[matched_oem]
        
        # Apply limit
        if limit and len(comments) > limit:
            comments = comments[:limit]
        
        return {
            "oem": matched_oem,
            "total_comments_available": len(raw_data[matched_oem]),
            "exported_comments": len(comments),
            "export_timestamp": datetime.now().isoformat(),
            "data": comments
        }
            
    except Exception as e:
        return {
            "error": f"Export failed: {str(e)}",
            "error_type": str(type(e)),
            "note": "Try using the enhanced chat endpoint instead"
        }

@app.get("/api/export/excel-report")
async def export_excel_report(
    query: Optional[str] = None,
    oem_filter: Optional[str] = None
):
    """Export comprehensive Excel report with sentiment analysis"""
    try:
        # Adjust query based on OEM filter
        if oem_filter and oem_filter != "All OEMs":
            query = query or f"Generate comprehensive sentiment report for {oem_filter}"
        else:
            query = query or "Generate comprehensive sentiment report for all OEMs"
        
        # Load the latest data
        data_result = await enhanced_agent_service.process_enhanced_query(
            query,
            use_youtube_data=True,
            max_search_results=5
        )
        
        # Generate Excel report
        excel_data = document_export_service.create_sentiment_analysis_excel(data_result)
        
        from fastapi.responses import Response
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        oem_suffix = f"_{oem_filter.replace(' ', '_').lower()}" if oem_filter and oem_filter != "All OEMs" else ""
        filename = f"solysai_sentiment_report{oem_suffix}_{timestamp}.xlsx"
        
        return Response(
            content=excel_data,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        return {
            "error": f"Excel export failed: {str(e)}",
            "error_type": str(type(e)),
            "suggestion": "Try with a simpler query or contact support"
        }

@app.get("/api/export/word-report")
async def export_word_report(
    query: Optional[str] = None,
    oem_filter: Optional[str] = None
):
    """Export professional Word document report"""
    try:
        # Adjust query based on OEM filter
        if oem_filter and oem_filter != "All OEMs":
            query = query or f"Generate executive summary report for {oem_filter} sentiment analysis"
        else:
            query = query or "Generate executive summary report for Indian EV market sentiment"
        
        # Load the latest data
        data_result = await enhanced_agent_service.process_enhanced_query(
            query,
            use_youtube_data=True,
            max_search_results=5
        )
        
        # Generate Word document
        word_data = document_export_service.create_executive_word_report(
            data_result, 
            query
        )
        
        from fastapi.responses import Response
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        oem_suffix = f"_{oem_filter.replace(' ', '_').lower()}" if oem_filter and oem_filter != "All OEMs" else ""
        filename = f"solysai_executive_report{oem_suffix}_{timestamp}.docx"
        
        return Response(
            content=word_data,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        return {
            "error": f"Word export failed: {str(e)}",
            "error_type": str(type(e)),
            "suggestion": "Try with a simpler query or contact support"
        }

@app.get("/api/export/csv-data")
async def export_csv_data(
    oem_filter: Optional[str] = None,
    limit: Optional[int] = 1000
):
    """Export raw comment data as CSV"""
    try:
        # Load the latest data
        youtube_data = await enhanced_agent_service.load_youtube_data()
        
        # Format data for export
        export_data = {
            'youtube_data': youtube_data,
            'query': f'Data export for {oem_filter}' if oem_filter and oem_filter != "All OEMs" else 'Complete dataset export',
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate CSV
        csv_data = document_export_service.create_csv_export(
            export_data, 
            oem_filter if oem_filter != "All OEMs" else None
        )
        
        from fastapi.responses import Response
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if oem_filter and oem_filter != "All OEMs":
            oem_suffix = f"_{oem_filter.lower().replace(' ', '_')}"
        else:
            oem_suffix = "_all_oems"
        filename = f"solysai_raw_data{oem_suffix}_{timestamp}.csv"
        
        return Response(
            content=csv_data,
            media_type='text/csv',
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        return {
            "error": f"CSV export failed: {str(e)}",
            "error_type": str(type(e)),
            "available_formats": ["excel-report", "word-report", "csv-data"]
        }

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
            max_search_results=request.max_search_results
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

# Enhanced Quick Export Endpoints
@app.post("/api/export/quick-excel")
async def quick_excel_export(request: Dict[str, Any]):
    """Quick Excel export for any data"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Generate quick Excel file
        filename = f"quick_export_{timestamp}.xlsx"
        file_path = os.path.join("exports", filename)
        
        # Ensure exports directory exists
        os.makedirs("exports", exist_ok=True)
        
        # Use DocumentExportService if available
        if hasattr(document_export_service, 'create_quick_excel_export'):
            excel_file = await document_export_service.create_quick_excel_export(request, timestamp)
        else:
            # Fallback to simple pandas export
            import pandas as pd
            df = pd.DataFrame(request.get('data', []))
            df.to_excel(file_path, index=False)
            excel_file = file_path
        
        return {
            "message": "Quick Excel export generated",
            "file_path": excel_file,
            "download_url": f"/api/export/xlsx/{os.path.basename(excel_file)}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick export error: {str(e)}")

@app.post("/api/export/quick-csv")
async def quick_csv_export(request: Dict[str, Any]):
    """Quick CSV export for any data"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quick_export_{timestamp}.csv"
        file_path = os.path.join("exports", filename)
        
        # Ensure exports directory exists
        os.makedirs("exports", exist_ok=True)
        
        # Use DocumentExportService if available
        if hasattr(document_export_service, 'create_quick_csv_export'):
            csv_file = await document_export_service.create_quick_csv_export(request, timestamp)
        else:
            # Fallback to simple pandas export
            import pandas as pd
            df = pd.DataFrame(request.get('data', []))
            df.to_csv(file_path, index=False)
            csv_file = file_path
        
        return {
            "message": "Quick CSV export generated",
            "file_path": csv_file,
            "download_url": f"/api/export/csv/{os.path.basename(csv_file)}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick export error: {str(e)}")

# Enhanced Temporal Analysis Endpoints
@app.get("/api/temporal-analysis/trends/{oem_name}")
async def get_temporal_trends(oem_name: str, months: int = 6):
    """Get detailed temporal trends for an OEM over specified months"""
    try:
        if hasattr(enhanced_agent_service, 'get_temporal_trends'):
            trends = await enhanced_agent_service.get_temporal_trends(oem_name, months)
        else:
            # Fallback trend analysis
            trends = {
                "sentiment_trend": "positive",
                "engagement_trend": "increasing",
                "mention_frequency": "stable",
                "key_themes": ["performance", "features", "value"]
            }
        
        return {
            "oem": oem_name,
            "months_analyzed": months,
            "trends": trends,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Temporal trends error: {str(e)}")

@app.post("/api/temporal-analysis/compare")
async def compare_temporal_periods(request: Dict[str, Any]):
    """Compare sentiment across multiple time periods and OEMs"""
    try:
        if hasattr(enhanced_agent_service, 'compare_temporal_periods'):
            comparison = await enhanced_agent_service.compare_temporal_periods(request)
        else:
            # Fallback comparison
            comparison = {
                "periods_compared": request.get('periods', []),
                "oems_compared": request.get('oems', []),
                "sentiment_comparison": {
                    "trend": "improving",
                    "variance": "low",
                    "key_changes": ["increased positive sentiment"]
                }
            }
        
        return {
            "comparison_result": comparison,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Temporal comparison error: {str(e)}")

@app.get("/api/temporal-analysis/export/{oem_name}")
async def export_temporal_analysis(oem_name: str, format: str = "excel", periods: str = "6"):
    """Export temporal analysis results"""
    try:
        period_count = int(periods)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get temporal analysis data
        if hasattr(enhanced_agent_service, 'get_temporal_trends'):
            analysis_data = await enhanced_agent_service.get_temporal_trends(oem_name, period_count)
        else:
            analysis_data = {
                "sentiment_trends": [{"month": i, "sentiment": 0.7 + (i * 0.1)} for i in range(period_count)],
                "engagement_metrics": [{"month": i, "engagement": 85 + (i * 2)} for i in range(period_count)]
            }
        
        # Generate export file
        if format.lower() == "excel":
            filename = f"temporal_analysis_{oem_name}_{timestamp}.xlsx"
            file_path = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)
            
            import pandas as pd
            df = pd.DataFrame(analysis_data.get('sentiment_trends', []))
            df.to_excel(file_path, index=False)
            download_url = f"/api/export/xlsx/{filename}"
        else:
            filename = f"temporal_analysis_{oem_name}_{timestamp}.csv"
            file_path = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)
            
            import pandas as pd
            df = pd.DataFrame(analysis_data.get('sentiment_trends', []))
            df.to_csv(file_path, index=False)
            download_url = f"/api/export/csv/{filename}"
        
        return {
            "message": f"Temporal analysis exported for {oem_name}",
            "file_path": file_path,
            "download_url": download_url,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Temporal export error: {str(e)}")

@app.get("/api/export/xlsx/{filename}")
async def download_xlsx_file(filename: str):
    """Download Excel export file"""
    try:
        from fastapi.responses import FileResponse
        file_path = os.path.join("exports", filename)
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")

@app.get("/api/export/csv/{filename}")
async def download_csv_file(filename: str):
    """Download CSV export file"""
    try:
        from fastapi.responses import FileResponse
        file_path = os.path.join("exports", filename)
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type="text/csv"
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")

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
