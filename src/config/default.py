"""
Default configuration for the AI Emotional Engine for Telugu Story Creation.
"""

def load_config():
    """Load default configuration."""
    return {
        "api": {
            "host": "0.0.0.0",
            "port": 8000,
            "debug": False,
            "cors_origins": ["*"],
            "api_prefix": "/api/v1"
        },
        "database": {
            "url": "sqlite:///./story_engine.db",
            "echo": False
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
                "cache_dir": "./models/cache"
            },
            "story_generation": {
                "model_name": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 2048
            }
        },
        "telugu": {
            "transliteration": {
                "enabled": True,
                "service": "ai4bharat"
            },
            "dialect": "standard",
            "regional_variations": True
        },
        "logging": {
            "level": "INFO",
            "file": "./logs/story_engine.log",
            "rotation": "10 MB"
        },
        "cache": {
            "enabled": True,
            "ttl": 3600,
            "max_size": 1000
        }
    }