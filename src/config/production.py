"""
Production configuration for the AI Emotional Engine for Telugu Story Creation.
PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!
"""

import os
from src.config.default import load_config as load_default_config


def load_config():
    """Load production configuration for real AI system."""
    config = load_default_config()
    
    # Override default settings for production
    config["api"]["debug"] = False
    config["api"]["port"] = 12000  # Use the port assigned by the runtime environment
    config["api"]["cors_origins"] = [
        "https://story-engine.telugu-ai.org",
        "https://api.telugu-ai.org",
        "https://work-1-chhvgapckwzayelh.prod-runtime.all-hands.dev",
        "https://work-2-chhvgapckwzayelh.prod-runtime.all-hands.dev"
    ]
    
    # Use PostgreSQL for production with connection pooling
    config["database"]["url"] = os.environ.get(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/story_engine"
    )
    config["database"]["pool_size"] = 20
    config["database"]["max_overflow"] = 10
    config["database"]["pool_timeout"] = 30
    config["database"]["pool_recycle"] = 1800
    
    # Use high-performance models for production
    if os.environ.get("USE_LOCAL_MODELS", "true").lower() == "true":
        # Use local models for production
        config["models"]["story_generation"]["model_name"] = "local:./models/llama-3-70b-telugu-instruct.gguf"
        config["models"]["language"]["model_name"] = "ai4bharat/indic-bert-large"
        config["models"]["embedding"]["model_name"] = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    else:
        # Use API-based models for production
        config["models"]["story_generation"]["model_name"] = "gpt-4-turbo"
    
    # Optimize model parameters for production
    config["models"]["story_generation"]["temperature"] = 0.8
    config["models"]["story_generation"]["max_tokens"] = 8192
    config["models"]["story_generation"]["top_p"] = 0.92
    
    # Enable all expert agents for full functionality
    for agent in config["agents"]["expert"]:
        config["agents"]["expert"][agent]["enabled"] = True
    
    # Configure Redis for caching and session management
    config["cache"]["type"] = "redis"
    config["cache"]["redis_url"] = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    config["cache"]["ttl"] = 7200  # 2 hours
    
    # Configure performance settings
    config["performance"]["use_gpu"] = os.environ.get("USE_GPU", "true").lower() == "true"
    config["performance"]["batch_processing"] = True
    config["performance"]["max_workers"] = int(os.environ.get("MAX_WORKERS", "8"))
    
    # Configure security settings
    config["security"]["api_key_required"] = True
    config["security"]["rate_limiting"] = True
    config["security"]["max_requests_per_minute"] = 120  # Higher limit for production
    
    # Configure dashboard
    config["dashboard"]["enabled"] = True
    config["dashboard"]["port"] = 12001  # Use second port for dashboard
    
    # Configure logging
    config["logging"]["level"] = os.environ.get("LOG_LEVEL", "INFO")
    config["logging"]["rotation"] = "100 MB"
    config["logging"]["retention"] = "90 days"
    
    return config