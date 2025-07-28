"""
Default configuration for the AI Emotional Engine for Telugu Story Creation.
PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!
"""

import os

def load_config():
    """Load default configuration for production-ready real AI system."""
    return {
        "api": {
            "host": "0.0.0.0",
            "port": 8000,
            "debug": False,
            "cors_origins": ["*"],
            "api_prefix": "/api/v1"
        },
        "database": {
            "url": "postgresql://postgres:postgres@localhost:5432/story_engine",
            "echo": False,
            "pool_size": 20,
            "max_overflow": 10
        },
        "agents": {
            "story": {"enabled": True, "weight": 1.0},
            "emotion": {"enabled": True, "weight": 0.9},
            "cultural": {"enabled": True, "weight": 0.8},
            "character": {"enabled": True, "weight": 0.8},
            "technical": {"enabled": True, "weight": 0.7},
            "quality": {"enabled": True, "weight": 0.9},
            "expert": {
                "character_psychologist": {"enabled": True, "weight": 0.8},
                "trauma_informed": {"enabled": True, "weight": 0.7},
                "legal_ethics": {"enabled": True, "weight": 0.7},
                "medical_narrative": {"enabled": True, "weight": 0.7},
                "spiritual_meaning": {"enabled": True, "weight": 0.6},
                "leadership": {"enabled": True, "weight": 0.6}
            }
        },
        "models": {
            "language": {
                "model_name": "ai4bharat/indic-bert",
                "cache_dir": "./models/cache",
                "quantization": "int8",  # Optimize for production
                "batch_size": 16
            },
            "story_generation": {
                # Default to local LLM if available, otherwise use API
                "model_name": os.environ.get("STORY_MODEL", "local:./models/llama-3-8b-telugu-instruct.gguf"),
                "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
                "temperature": 0.7,
                "max_tokens": 4096,
                "top_p": 0.95,
                "frequency_penalty": 0.2,
                "presence_penalty": 0.1
            },
            "embedding": {
                "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                "cache_dir": "./models/cache",
                "dimensions": 384
            }
        },
        "telugu": {
            "transliteration": {
                "enabled": True,
                "service": "ai4bharat",
                "api_key": os.environ.get("AI4BHARAT_API_KEY", ""),
                "fallback_service": "local",  # Use local transliteration if API fails
                "cache_results": True
            },
            "dialect": "standard",
            "regional_variations": True,
            "dictionary_path": "./data/telugu_dictionary.json",
            "grammar_rules_path": "./data/telugu_grammar_rules.json"
        },
        "logging": {
            "level": os.environ.get("LOG_LEVEL", "INFO"),
            "file": "./logs/story_engine.log",
            "rotation": "50 MB",
            "retention": "30 days",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            "backtrace": True,
            "diagnose": True,
            "enqueue": True
        },
        "cache": {
            "enabled": True,
            "ttl": 3600,
            "max_size": 10000,
            "type": "redis",  # Use Redis for production
            "redis_url": os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        },
        "performance": {
            "use_gpu": True,
            "batch_processing": True,
            "max_workers": 8,
            "timeout": 60,
            "rate_limit": 100  # Requests per minute
        },
        "security": {
            "api_key_required": True,
            "api_key": os.environ.get("API_KEY", ""),
            "rate_limiting": True,
            "max_requests_per_minute": 60,
            "content_filtering": True
        },
        "dashboard": {
            "enabled": True,
            "port": 8050,
            "admin_username": os.environ.get("ADMIN_USERNAME", "admin"),
            "admin_password": os.environ.get("ADMIN_PASSWORD", ""),
            "metrics_retention_days": 30
        }
    }