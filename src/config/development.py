"""
Development configuration for the AI Emotional Engine for Telugu Story Creation.
"""

from src.config.default import load_config as load_default_config


def load_config():
    """Load development configuration."""
    config = load_default_config()
    
    # Override default settings for development
    config["api"]["debug"] = True
    config["database"]["echo"] = True
    config["logging"]["level"] = "DEBUG"
    
    # Disable some expert agents for faster development
    config["agents"]["expert"]["legal_ethics"]["enabled"] = False
    config["agents"]["expert"]["medical_narrative"]["enabled"] = False
    config["agents"]["expert"]["leadership"]["enabled"] = False
    
    # Use smaller models for faster development
    config["models"]["story_generation"]["model_name"] = "gpt-3.5-turbo"
    
    return config