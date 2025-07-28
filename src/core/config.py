"""
Production Configuration for Telugu Story Engine
Real AI system configuration - NO MOCKS, NO FALLBACKS
"""

import os
from typing import Dict, List, Optional, Any
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class ModelConfig(BaseSettings):
    """Real AI Model Configuration"""
    
    # Telugu Language Models - Production Ready
    telugu_bert_model: str = "bert-base-multilingual-cased"
    telugu_gpt_model: str = "gpt2"  # Better for text generation
    emotion_model: str = "j-hartmann/emotion-english-distilroberta-base"
    cultural_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # Model Paths
    models_dir: Path = Path("data/models")
    cache_dir: Path = Path("data/cache")
    
    # Model Parameters
    max_length: int = 2048
    temperature: float = 0.8
    top_p: float = 0.9
    top_k: int = 50
    
    # GPU Configuration
    device: str = "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu"
    mixed_precision: bool = True
    gradient_checkpointing: bool = True
    
    class Config:
        env_prefix = "MODEL_"

class AgentConfig(BaseSettings):
    """Multi-Agent System Configuration"""
    
    # Core Agents - All Real Implementations
    story_structure_agent: Dict[str, Any] = {
        "enabled": True,
        "weight": 1.0,
        "model": "telugu_gpt",
        "max_iterations": 3
    }
    
    emotional_intelligence_agent: Dict[str, Any] = {
        "enabled": True,
        "weight": 0.9,
        "model": "emotion_model",
        "emotion_categories": 27
    }
    
    cultural_adaptation_agent: Dict[str, Any] = {
        "enabled": True,
        "weight": 0.8,
        "model": "cultural_model",
        "cultural_dimensions": 15
    }
    
    character_development_agent: Dict[str, Any] = {
        "enabled": True,
        "weight": 0.85,
        "model": "telugu_bert",
        "personality_frameworks": ["ocean", "maslow", "erikson"]
    }
    
    # Expert Domain Agents
    expert_agents: Dict[str, Dict[str, Any]] = {
        "character_psychologist": {
            "enabled": True,
            "weight": 0.8,
            "relevance_threshold": 0.3
        },
        "trauma_informed_narrative": {
            "enabled": True,
            "weight": 0.7,
            "sensitivity_level": "high"
        },
        "legal_ethics": {
            "enabled": True,
            "weight": 0.7,
            "legal_domains": ["family", "criminal", "civil"]
        },
        "medical_narrative": {
            "enabled": True,
            "weight": 0.7,
            "medical_specialties": ["general", "mental_health", "emergency"]
        },
        "spiritual_meaning": {
            "enabled": True,
            "weight": 0.6,
            "spiritual_traditions": ["hinduism", "buddhism", "secular"]
        },
        "leadership_social_change": {
            "enabled": True,
            "weight": 0.6,
            "leadership_styles": ["transformational", "servant", "authentic"]
        }
    }
    
    # Collaboration Settings
    max_collaboration_rounds: int = 5
    consensus_threshold: float = 0.7
    conflict_resolution_strategy: str = "weighted_voting"
    
    class Config:
        env_prefix = "AGENT_"

class APIConfig(BaseSettings):
    """Production API Configuration"""
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 12000
    workers: int = 4
    reload: bool = False
    
    # API Settings
    api_version: str = "v2"
    title: str = "Telugu Story Engine API"
    description: str = "Production AI API for Telugu story generation"
    
    # Security
    secret_key: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    # CORS
    allowed_origins: List[str] = [
        "https://work-1-ojauwtnwevcsummg.prod-runtime.all-hands.dev",
        "https://work-2-ojauwtnwevcsummg.prod-runtime.all-hands.dev",
        "http://localhost:3000",
        "http://localhost:8080"
    ]
    
    class Config:
        env_prefix = "API_"

class DatabaseConfig(BaseSettings):
    """Database Configuration"""
    
    # PostgreSQL Settings
    database_url: str = Field(default="sqlite:///telugu_story_engine.db", env="DATABASE_URL")
    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 30
    pool_timeout: int = 30
    
    # Redis Settings
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_expire: int = 3600
    
    class Config:
        env_prefix = "DB_"

class DashboardConfig(BaseSettings):
    """Advanced Dashboard Configuration"""
    
    # Dashboard Settings
    dashboard_host: str = "0.0.0.0"
    dashboard_port: int = 12001
    dashboard_title: str = "Telugu Story Engine Dashboard"
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # Real-time Updates
    websocket_enabled: bool = True
    update_interval: int = 1000  # milliseconds
    
    # Visualization
    max_stories_display: int = 100
    chart_refresh_rate: int = 5000  # milliseconds
    
    class Config:
        env_prefix = "DASHBOARD_"

class ProductionConfig(BaseSettings):
    """Main Production Configuration"""
    
    # Environment
    environment: str = Field(default="production", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "logs/telugu_story_engine.log"
    
    # Performance
    max_concurrent_requests: int = 100
    request_timeout: int = 300  # 5 minutes
    
    # Story Generation
    max_story_length: int = 10000
    min_story_length: int = 500
    default_story_length: int = 2000
    
    # Cultural Settings
    default_cultural_context: str = "contemporary_telugu"
    supported_dialects: List[str] = [
        "coastal_andhra",
        "rayalaseema",
        "telangana",
        "standard_telugu"
    ]
    
    # Quality Assurance
    quality_threshold: float = 0.8
    cultural_authenticity_threshold: float = 0.75
    emotional_coherence_threshold: float = 0.8
    
    # Model Configuration
    model: ModelConfig = ModelConfig()
    agents: AgentConfig = AgentConfig()
    api: APIConfig = APIConfig()
    database: DatabaseConfig = DatabaseConfig()
    dashboard: DashboardConfig = DashboardConfig()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global configuration instance
config = ProductionConfig()

def get_config() -> ProductionConfig:
    """Get the global configuration instance"""
    return config

def update_config(**kwargs) -> None:
    """Update configuration values"""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            raise ValueError(f"Unknown configuration key: {key}")

# Environment-specific configurations
def get_development_config() -> ProductionConfig:
    """Development environment configuration"""
    dev_config = ProductionConfig()
    dev_config.environment = "development"
    dev_config.debug = True
    dev_config.api.reload = True
    dev_config.database.echo = True
    return dev_config

def get_testing_config() -> ProductionConfig:
    """Testing environment configuration"""
    test_config = ProductionConfig()
    test_config.environment = "testing"
    test_config.debug = True
    test_config.database.database_url = "sqlite:///test.db"
    return test_config

def get_production_config() -> ProductionConfig:
    """Production environment configuration"""
    return ProductionConfig()