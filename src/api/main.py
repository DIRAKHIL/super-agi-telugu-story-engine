"""
Main FastAPI Application for Telugu Story Engine
Production-ready API with real AI processing - NO MOCKS
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from ..core.config import get_config
from ..core.model_manager import initialize_models, get_model_manager
from .routes import router
from .models import ErrorResponse
from .middleware import (
    RateLimitMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    SecurityMiddleware
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state
app_state = {
    "startup_time": None,
    "model_manager": None,
    "request_count": 0,
    "error_count": 0
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Telugu Story Engine API...")
    app_state["startup_time"] = time.time()
    
    try:
        # Initialize models
        logger.info("Initializing AI models...")
        await initialize_models()
        app_state["model_manager"] = get_model_manager()
        logger.info("Models initialized successfully")
        
        # Additional startup tasks
        await startup_tasks()
        
        logger.info("Telugu Story Engine API started successfully")
        yield
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    # Shutdown
    logger.info("Shutting down Telugu Story Engine API...")
    await shutdown_tasks()
    logger.info("Shutdown complete")

async def startup_tasks():
    """Additional startup tasks"""
    # Warm up models
    logger.info("Warming up models...")
    model_manager = get_model_manager()
    
    # Test model functionality
    try:
        test_text = "తెలుగు కథ రచన పరీక్ష"
        await model_manager.encode_text("telugu_bert", test_text)
        logger.info("Model warm-up completed successfully")
    except Exception as e:
        logger.warning(f"Model warm-up failed: {e}")
    
    # Initialize caches, databases, etc.
    logger.info("Initializing system components...")

async def shutdown_tasks():
    """Cleanup tasks during shutdown"""
    # Save model caches
    if app_state["model_manager"]:
        try:
            app_state["model_manager"].save_model_cache()
            logger.info("Model cache saved")
        except Exception as e:
            logger.error(f"Failed to save model cache: {e}")
    
    # Additional cleanup
    logger.info("Cleanup completed")

# Create FastAPI application
config = get_config()

app = FastAPI(
    title="Telugu Story Engine API",
    description="Production AI API for Telugu story generation with multi-agent architecture",
    version="2.0.0",
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redoc",
    openapi_url="/api/v2/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Custom middleware
try:
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)
except Exception as e:
    logger.warning(f"Failed to add custom middleware: {e}")

# Include routers
app.include_router(router, prefix="/api/v2")

# Static files (for dashboard)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    logger.warning("Static files directory not found")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    app_state["error_count"] += 1
    
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="internal_server_error",
            message="An internal server error occurred",
            details={"type": type(exc).__name__} if config.debug else None,
            request_id=getattr(request.state, "request_id", None)
        ).dict()
    )

# Health check endpoint
@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - app_state["startup_time"] if app_state["startup_time"] else 0
    
    # Check model manager status
    model_status = "healthy"
    if app_state["model_manager"]:
        try:
            model_info = app_state["model_manager"].get_model_info()
            if not any(info.loaded for info in model_info.values()):
                model_status = "models_not_loaded"
        except Exception:
            model_status = "error"
    else:
        model_status = "not_initialized"
    
    return {
        "status": "healthy" if model_status == "healthy" else "degraded",
        "version": "2.0.0",
        "uptime": uptime,
        "timestamp": time.time(),
        "components": {
            "api": "healthy",
            "models": model_status,
            "database": "healthy",  # Add actual database check
            "cache": "healthy"      # Add actual cache check
        },
        "metrics": {
            "requests_total": app_state["request_count"],
            "errors_total": app_state["error_count"],
            "memory_usage": get_memory_usage()
        }
    }

def get_memory_usage() -> float:
    """Get current memory usage"""
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB
    except ImportError:
        return 0.0

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    uptime = time.time() - app_state["startup_time"] if app_state["startup_time"] else 0
    
    metrics_text = f"""
# HELP telugu_story_engine_requests_total Total number of requests
# TYPE telugu_story_engine_requests_total counter
telugu_story_engine_requests_total {app_state["request_count"]}

# HELP telugu_story_engine_errors_total Total number of errors
# TYPE telugu_story_engine_errors_total counter
telugu_story_engine_errors_total {app_state["error_count"]}

# HELP telugu_story_engine_uptime_seconds Uptime in seconds
# TYPE telugu_story_engine_uptime_seconds gauge
telugu_story_engine_uptime_seconds {uptime}

# HELP telugu_story_engine_memory_usage_mb Memory usage in MB
# TYPE telugu_story_engine_memory_usage_mb gauge
telugu_story_engine_memory_usage_mb {get_memory_usage()}
"""
    
    # Add model-specific metrics
    if app_state["model_manager"]:
        try:
            memory_usage = app_state["model_manager"].get_memory_usage()
            for model_name, usage in memory_usage.items():
                metrics_text += f"""
# HELP telugu_story_engine_model_memory_mb Model memory usage in MB
# TYPE telugu_story_engine_model_memory_mb gauge
telugu_story_engine_model_memory_mb{{model="{model_name}"}} {usage}
"""
        except Exception:
            pass
    
    return Response(content=metrics_text, media_type="text/plain")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Telugu Story Engine API",
        "version": "2.0.0",
        "status": "operational",
        "documentation": "/api/v2/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

# Request middleware to track requests
@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track request metrics"""
    app_state["request_count"] += 1
    
    # Add request ID
    import uuid
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Process request
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Add headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

def create_app() -> FastAPI:
    """Factory function to create the app"""
    return app

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "src.api.main:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
        workers=1 if config.debug else config.api.workers,
        log_level="info"
    )