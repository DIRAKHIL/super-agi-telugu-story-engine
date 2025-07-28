"""
Production configuration for the AI Emotional Engine for Telugu Story Creation.
"""

from src.config.default import load_config as load_default_config


def load_config():
    """Load production configuration."""
    config = load_default_config()
    
    # Override default settings for production
    config["api"]["debug"] = False
    config["api"]["cors_origins"] = [
        "https://story-engine.example.com",
        "https://api.story-engine.example.com"
    ]
    
    # Use PostgreSQL for production
    config["database"]["url"] = "postgresql://user:password@localhost:5432/story_engine"
    
    # Use more powerful models for production
    config["models"]["story_generation"]["model_name"] = "gpt-4"
    
    # Enable all expert agents for full functionality
    for agent in config["agents"]["expert"]:
        config["agents"]["expert"][agent]["enabled"] = True
    
    return config