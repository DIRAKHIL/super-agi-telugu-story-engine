"""
API server for the AI Emotional Engine for Telugu Story Creation.
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from loguru import logger

from src.api.story_generator import StoryGenerator
from src.utils.config.config_manager import ConfigManager


class Character(BaseModel):
    """Character model for story generation."""
    name: str
    age: int
    traits: List[str]
    background: Optional[str] = None


class Setting(BaseModel):
    """Setting model for story generation."""
    location: str
    time_period: str
    social_context: Optional[str] = None


class StoryParameters(BaseModel):
    """Parameters for story generation."""
    length: int = Field(..., gt=100, lt=10000, description="Story length in words")
    genre: str
    emotional_arc: Optional[str] = None
    characters: List[Character]
    setting: Setting
    theme: str
    language_style: Optional[str] = "standard"


class StoryRequest(BaseModel):
    """Story generation request."""
    parameters: StoryParameters


class StoryResponse(BaseModel):
    """Story generation response."""
    id: str
    title: str
    content: str
    metadata: Dict[str, Any]


def create_app(config):
    """
    Create and configure the FastAPI application.
    
    Args:
        config (dict): Configuration dictionary.
    
    Returns:
        FastAPI: Configured FastAPI application.
    """
    app = FastAPI(
        title="AI Emotional Engine for Telugu Story Creation",
        description="A sophisticated multi-agent AI system that generates emotionally resonant, culturally authentic Telugu stories",
        version="0.1.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config["api"]["cors_origins"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create story generator
    story_generator = StoryGenerator(config)
    
    # Dependency to get story generator
    def get_story_generator():
        return story_generator
    
    @app.post("/api/v1/stories", response_model=StoryResponse)
    async def generate_story(
        request: StoryRequest,
        generator: StoryGenerator = Depends(get_story_generator)
    ):
        """
        Generate a story based on the provided parameters.
        """
        try:
            # Use model_dump instead of dict for Pydantic v2 compatibility
            story = generator.generate_story(request.model_dump())
            return story
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @app.get("/api/v1/health")
    async def health_check():
        """
        Health check endpoint.
        """
        return {"status": "healthy"}
    
    return app


def start_server(config):
    """
    Start the API server.
    
    Args:
        config (dict): Configuration dictionary.
    """
    app = create_app(config)
    
    logger.info(f"Starting API server at {config['api']['host']}:{config['api']['port']}")
    
    uvicorn.run(
        app,
        host=config["api"]["host"],
        port=config["api"]["port"],
        log_level="debug" if config["api"]["debug"] else "info"
    )