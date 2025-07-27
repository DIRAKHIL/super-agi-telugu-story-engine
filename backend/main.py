"""
Main FastAPI application for Telugu Film Story Generation System
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .core.config import settings
from .api.v1.api import api_router
from .agents.orchestrator import AgentOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator: AgentOrchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global orchestrator
    
    # Startup
    logger.info("Starting Telugu Film Story Generation System")
    
    try:
        # Initialize orchestrator
        orchestrator = AgentOrchestrator(config={
            "max_concurrent_tasks": 10,
            "story_agent": {"model_config": {}},
            "emotion_agent": {"model_config": {}},
            "cultural_agent": {"model_config": {}}
        })
        
        # Start orchestrator
        await orchestrator.start()
        
        # Store orchestrator in app state
        app.state.orchestrator = orchestrator
        
        logger.info("System startup completed successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Telugu Film Story Generation System")
    
    try:
        if orchestrator:
            await orchestrator.stop()
        logger.info("System shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Advanced AI system for Telugu film story generation with real AI models",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Super-AGI Emotional Brain Engine - Telugu Film Story Generation System",
        "version": settings.APP_VERSION,
        "status": "operational",
        "features": [
            "Advanced Story Generation",
            "Real AI-Powered Emotion Analysis", 
            "Sentiment Analysis",
            "Multi-Agent Orchestration",
            "Telugu Cultural Processing",
            "Character Development Engine",
            "Production Planning"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        orchestrator_stats = None
        if hasattr(app.state, 'orchestrator') and app.state.orchestrator:
            orchestrator_stats = app.state.orchestrator.get_orchestrator_stats()
        
        return {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "orchestrator": orchestrator_stats
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
        log_level="info"
    )