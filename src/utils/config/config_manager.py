"""
Configuration manager for the AI Emotional Engine for Telugu Story Creation.
"""

import os
import importlib
from loguru import logger


class ConfigManager:
    """
    Manages configuration loading and access for the story engine.
    """
    
    def __init__(self):
        """Initialize the config manager."""
        self.config = None
        self.env = os.environ.get("STORY_ENGINE_ENV", "development")
    
    def load_config(self, env=None):
        """
        Load configuration for the specified environment.
        
        Args:
            env (str, optional): Environment name. Defaults to None.
        
        Returns:
            dict: Configuration dictionary.
        """
        if env:
            self.env = env
        
        logger.info(f"Loading configuration for environment: {self.env}")
        
        # Try to load environment-specific config
        try:
            config_module = importlib.import_module(f"src.config.{self.env}")
            self.config = config_module.load_config()
            logger.info(f"Loaded configuration from src.config.{self.env}")
        except (ImportError, AttributeError) as e:
            logger.warning(f"Failed to load config for {self.env}: {e}")
            logger.info("Falling back to default configuration")
            
            # Fall back to default config
            from src.config.default import load_config
            self.config = load_config()
        
        # Override with environment variables
        self._override_from_env()
        
        return self.config
    
    def get_config(self):
        """
        Get the current configuration.
        
        Returns:
            dict: Configuration dictionary.
        """
        if not self.config:
            return self.load_config()
        return self.config
    
    def _override_from_env(self):
        """Override configuration values from environment variables."""
        # API configuration
        if os.environ.get("API_HOST"):
            self.config["api"]["host"] = os.environ.get("API_HOST")
        
        if os.environ.get("API_PORT"):
            self.config["api"]["port"] = int(os.environ.get("API_PORT"))
        
        if os.environ.get("API_DEBUG"):
            self.config["api"]["debug"] = os.environ.get("API_DEBUG").lower() == "true"
        
        # Database configuration
        if os.environ.get("DATABASE_URL"):
            self.config["database"]["url"] = os.environ.get("DATABASE_URL")
        
        # Model configuration
        if os.environ.get("LANGUAGE_MODEL"):
            self.config["models"]["language"]["model_name"] = os.environ.get("LANGUAGE_MODEL")
        
        if os.environ.get("STORY_MODEL"):
            self.config["models"]["story_generation"]["model_name"] = os.environ.get("STORY_MODEL")
        
        # Logging configuration
        if os.environ.get("LOG_LEVEL"):
            self.config["logging"]["level"] = os.environ.get("LOG_LEVEL")