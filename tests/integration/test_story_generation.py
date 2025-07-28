"""
Integration tests for story generation.
"""

import pytest
from src.api.story_generator import StoryGenerator
from src.utils.config.config_manager import ConfigManager


class TestStoryGeneration:
    """Integration tests for the story generation process."""
    
    @pytest.fixture
    def config(self):
        """Load test configuration."""
        config_manager = ConfigManager()
        return config_manager.load_config("test")
    
    @pytest.fixture
    def story_generator(self, config):
        """Create a story generator for testing."""
        return StoryGenerator(config)
    
    @pytest.fixture
    def story_request(self):
        """Create a test story request."""
        return {
            "parameters": {
                "length": 1000,
                "genre": "drama",
                "emotional_arc": "family_restoration",
                "characters": [
                    {
                        "name": "రాజు",
                        "age": 30,
                        "traits": ["brave", "loyal", "impulsive"],
                        "background": "Born in coastal village, left to city for work"
                    },
                    {
                        "name": "లక్ష్మి",
                        "age": 28,
                        "traits": ["intelligent", "determined", "compassionate"],
                        "background": "Teacher from rural background"
                    }
                ],
                "setting": {
                    "location": "Coastal Andhra Pradesh",
                    "time_period": "Contemporary",
                    "social_context": "Rural fishing community"
                },
                "theme": "Family reconciliation after long separation",
                "language_style": "Simple and direct with regional dialect"
            }
        }
    
    def test_story_generation_end_to_end(self, story_generator, story_request):
        """Test the end-to-end story generation process."""
        # Generate story
        story = story_generator.generate_story(story_request)
        
        # Verify response structure
        assert "id" in story
        assert "title" in story
        assert "content" in story
        assert "metadata" in story
        
        # Verify metadata
        assert "word_count" in story["metadata"]
        assert "generation_time" in story["metadata"]
        assert "parameters" in story["metadata"]
        
        # Verify content
        assert len(story["content"]) > 0
        assert story["metadata"]["word_count"] > 0
    
    def test_parameter_validation(self, story_generator):
        """Test parameter validation."""
        # Missing required parameter
        invalid_request = {
            "parameters": {
                "genre": "drama",
                "theme": "Family reconciliation"
                # Missing other required parameters
            }
        }
        
        with pytest.raises(ValueError):
            story_generator.generate_story(invalid_request)
        
        # Invalid length
        invalid_length_request = {
            "parameters": {
                "length": 50,  # Too short
                "genre": "drama",
                "characters": [{"name": "Test", "age": 30, "traits": ["brave"]}],
                "setting": {"location": "Test", "time_period": "Contemporary"},
                "theme": "Test theme"
            }
        }
        
        with pytest.raises(ValueError):
            story_generator.generate_story(invalid_length_request)
        
        # No characters
        no_characters_request = {
            "parameters": {
                "length": 1000,
                "genre": "drama",
                "characters": [],  # Empty characters list
                "setting": {"location": "Test", "time_period": "Contemporary"},
                "theme": "Test theme"
            }
        }
        
        with pytest.raises(ValueError):
            story_generator.generate_story(no_characters_request)