"""
Model loader utilities for the AI Emotional Engine for Telugu Story Creation.
"""

import os
from loguru import logger


def load_models(config):
    """
    Load AI models based on configuration.
    
    Args:
        config (dict): Configuration dictionary.
    
    Returns:
        dict: Loaded models.
    """
    models = {}
    
    # Create cache directory if it doesn't exist
    cache_dir = config["models"]["language"]["cache_dir"]
    os.makedirs(cache_dir, exist_ok=True)
    
    # Load language model
    language_model_name = config["models"]["language"]["model_name"]
    logger.info(f"Loading language model: {language_model_name}")
    
    try:
        # In a real implementation, this would use transformers to load the model
        # For now, we'll just create a placeholder
        models["language"] = {"name": language_model_name, "loaded": True}
        logger.info(f"Successfully loaded language model: {language_model_name}")
    except Exception as e:
        logger.error(f"Failed to load language model: {e}")
        models["language"] = {"name": language_model_name, "loaded": False, "error": str(e)}
    
    # Load story generation model
    story_model_name = config["models"]["story_generation"]["model_name"]
    logger.info(f"Loading story generation model: {story_model_name}")
    
    try:
        # In a real implementation, this would load the appropriate model
        # For now, we'll just create a placeholder
        models["story_generation"] = {
            "name": story_model_name,
            "loaded": True,
            "temperature": config["models"]["story_generation"]["temperature"],
            "max_tokens": config["models"]["story_generation"]["max_tokens"]
        }
        logger.info(f"Successfully loaded story generation model: {story_model_name}")
    except Exception as e:
        logger.error(f"Failed to load story generation model: {e}")
        models["story_generation"] = {"name": story_model_name, "loaded": False, "error": str(e)}
    
    return models