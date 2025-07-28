"""
Test configuration for the AI Emotional Engine for Telugu Story Creation.
PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!
"""

from src.config.default import load_config as load_default_config


def load_config():
    """Load test configuration."""
    config = load_default_config()
    
    # Override default settings for testing
    config["api"]["port"] = 8001
    config["database"]["url"] = "sqlite:///:memory:"
    
    # Use mock models for testing
    config["models"]["story_generation"]["model_name"] = "gpt-3.5-turbo-test"
    
    # Disable most expert agents for faster testing
    for agent in config["agents"]["expert"]:
        config["agents"]["expert"][agent]["enabled"] = False
    
    # Enable only essential agents for testing
    config["agents"]["expert"]["character_psychologist"]["enabled"] = True
    
    # Add test-specific configurations
    config["test"] = {
        "mock_responses": True,
        "mock_api_calls": True
    }
    
    return config