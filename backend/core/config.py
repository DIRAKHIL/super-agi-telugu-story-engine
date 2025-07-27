"""
Core configuration for the Telugu Film Story Generation System
"""
import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Super-AGI Emotional Brain Engine"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 12000
    WORKERS: int = 4
    
    # Security
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/telugu_stories"
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI Models Configuration
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
    # Telugu Language Models
    TELUGU_SENTIMENT_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    TELUGU_EMOTION_MODEL: str = "j-hartmann/emotion-english-distilroberta-base"
    TELUGU_STORY_MODEL: str = "microsoft/DialoGPT-large"
    
    # Story Generation Settings
    MAX_STORY_LENGTH: int = 5000
    MIN_STORY_LENGTH: int = 500
    DEFAULT_TEMPERATURE: float = 0.8
    DEFAULT_TOP_P: float = 0.9
    DEFAULT_TOP_K: int = 50
    
    # Multi-Agent Settings
    MAX_AGENTS: int = 10
    AGENT_TIMEOUT: int = 300  # 5 minutes
    
    # Cultural Processing
    TELUGU_CULTURAL_KEYWORDS: List[str] = [
        "కుటుంబం", "సంస్కృతి", "పండుగ", "వివాహం", "గ్రామం", 
        "నగరం", "ప్రేమ", "స్నేహం", "గౌరవం", "న్యాయం"
    ]
    
    # Production Planning
    BUDGET_ESTIMATION_ENABLED: bool = True
    TIMELINE_ESTIMATION_ENABLED: bool = True
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    SENTRY_DSN: Optional[str] = None
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://work-1-lgnjybaibjmwkfyv.prod-runtime.all-hands.dev",
        "https://work-2-lgnjybaibjmwkfyv.prod-runtime.all-hands.dev"
    ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()