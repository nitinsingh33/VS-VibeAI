"""
Production-optimized FastAPI configuration for Render deployment
Includes CORS, error handling, and production settings
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Production logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import your existing app
try:
    from main import app as main_app
    logger.info("✅ Successfully imported main application")
except ImportError as e:
    logger.error(f"❌ Failed to import main application: {e}")
    # Create a minimal fallback app
    main_app = FastAPI(title="SolysAI Sentiment Analysis", version="1.0.0")

# Production app configuration
app = FastAPI(
    title="SolysAI Sentiment Analysis - Production",
    description="Advanced sentiment analysis for Indian EV market with optimized performance",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT", "production") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT", "production") != "production" else None,
)

# Production middleware stack
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS for production
allowed_origins = [
    "https://solysai-sentiment-analysis.onrender.com",
    "https://*.onrender.com",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8501",
]

# Add environment-specific origins
if os.getenv("RENDER_EXTERNAL_URL"):
    allowed_origins.append(os.getenv("RENDER_EXTERNAL_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Trusted host middleware for security
trusted_hosts = ["*.onrender.com", "localhost", "127.0.0.1"]
if os.getenv("RENDER_EXTERNAL_HOSTNAME"):
    trusted_hosts.append(os.getenv("RENDER_EXTERNAL_HOSTNAME"))

app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)

# Mount the main application
app.mount("/", main_app)

# Production health check
@app.get("/health")
async def production_health_check():
    """Production health check endpoint"""
    try:
        # Test sentiment classifier
        from services.advanced_sentiment_classifier import AdvancedSentimentClassifier
        classifier = AdvancedSentimentClassifier()
        
        # Test basic functionality
        test_result = await classifier.classify_comment_advanced(
            {"text": "Test comment for health check"}
        )
        
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "environment": os.getenv("ENVIRONMENT", "production"),
            "version": "1.0.0",
            "services": {
                "sentiment_classifier": "operational",
                "api": "operational",
                "health_check": "passed"
            },
            "system_info": {
                "python_version": sys.version_info[:2],
                "platform": sys.platform,
                "cpu_count": os.cpu_count()
            }
        }
        
        # Check for data files
        import glob
        data_files = len(glob.glob("*.json"))
        health_status["data_files_available"] = data_files
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "services": {
                    "sentiment_classifier": "error",
                    "api": "operational",
                    "health_check": "failed"
                }
            }
        )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc} - {request.url}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("🚀 SolysAI Sentiment Analysis starting up...")
    logger.info(f"📅 Startup time: {datetime.now().isoformat()}")
    logger.info(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'production')}")
    logger.info(f"🔗 Port: {os.getenv('PORT', '8000')}")
    
    # Create necessary directories
    directories = ['exports', 'static', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"📂 Ensured directory exists: {directory}")
    
    # Check for data files
    import glob
    data_files = glob.glob("*.json")
    logger.info(f"📊 Found {len(data_files)} data files")
    
    logger.info("✅ Application startup completed successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("🛑 SolysAI Sentiment Analysis shutting down...")
    logger.info(f"📅 Shutdown time: {datetime.now().isoformat()}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"
    
    logger.info(f"🚀 Starting production server on {host}:{port}")
    
    uvicorn.run(
        "production_app:app",
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        use_colors=False,  # Better for production logs
        server_header=False,  # Security
        date_header=False  # Security
    )
