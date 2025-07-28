"""
Story generator module for the AI Emotional Engine for Telugu Story Creation.
"""

import time
import uuid
from loguru import logger

from src.agents.orchestrator import AgentOrchestrator


class StoryGenerator:
    """
    Main story generation class that coordinates the multi-agent system.
    """
    
    def __init__(self, config):
        """
        Initialize the story generator.
        
        Args:
            config (dict): Configuration dictionary.
        """
        self.config = config
        self.orchestrator = AgentOrchestrator(config)
    
    def generate_story(self, request):
        """
        Generate a story based on the provided parameters.
        
        Args:
            request (dict): Story generation request parameters.
        
        Returns:
            dict: Generated story with metadata.
        """
        start_time = time.time()
        story_id = str(uuid.uuid4())
        
        logger.info(f"Starting story generation (ID: {story_id})")
        logger.debug(f"Story parameters: {request['parameters']}")
        
        # Validate parameters
        self._validate_parameters(request["parameters"])
        
        # Generate story using the orchestrator
        story_content = self.orchestrator.generate_story(request["parameters"])
        
        # Calculate metadata
        word_count = len(story_content.split())
        generation_time = time.time() - start_time
        
        # Extract or generate title
        title = self._extract_title(story_content) or self._generate_title(request["parameters"])
        
        # Prepare response
        response = {
            "id": story_id,
            "title": title,
            "content": story_content,
            "metadata": {
                "word_count": word_count,
                "generation_time": generation_time,
                "parameters": request["parameters"]
            }
        }
        
        logger.info(f"Story generation completed (ID: {story_id}, Words: {word_count}, Time: {generation_time:.2f}s)")
        
        return response
    
    def _validate_parameters(self, parameters):
        """
        Validate story generation parameters.
        
        Args:
            parameters (dict): Story parameters.
        
        Raises:
            ValueError: If parameters are invalid.
        """
        required_params = ["length", "genre", "characters", "setting", "theme"]
        
        for param in required_params:
            if param not in parameters:
                raise ValueError(f"Missing required parameter: {param}")
        
        if parameters["length"] < 100 or parameters["length"] > 10000:
            raise ValueError("Story length must be between 100 and 10000 words")
        
        if not parameters["characters"]:
            raise ValueError("At least one character must be defined")
    
    def _extract_title(self, content):
        """
        Extract title from story content if present.
        
        Args:
            content (str): Story content.
        
        Returns:
            str: Extracted title or None.
        """
        lines = content.strip().split("\n")
        if lines and lines[0].startswith("#"):
            return lines[0].lstrip("#").strip()
        return None
    
    def _generate_title(self, parameters):
        """
        Generate a title based on story parameters.
        
        Args:
            parameters (dict): Story parameters.
        
        Returns:
            str: Generated title.
        """
        return f"{parameters['theme']} - A {parameters['genre']} Story"