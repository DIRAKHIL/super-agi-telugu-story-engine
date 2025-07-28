"""
Unit tests for the Story Agent.
"""

import pytest
from src.agents.core.story_agent import StoryAgent


class TestStoryAgent:
    """Test cases for the Story Agent."""
    
    @pytest.fixture
    def config(self):
        """Provide a test configuration."""
        return {
            "agents": {
                "story": {"enabled": True, "weight": 1.0}
            },
            "models": {
                "story_generation": {
                    "model_name": "gpt-3.5-turbo-test",
                    "temperature": 0.7,
                    "max_tokens": 2048
                }
            }
        }
    
    @pytest.fixture
    def story_agent(self, config):
        """Create a story agent for testing."""
        return StoryAgent(config)
    
    @pytest.fixture
    def story_parameters(self):
        """Provide test story parameters."""
        return {
            "length": 1000,
            "genre": "drama",
            "theme": "Overcoming adversity",
            "setting": {
                "location": "Coastal Andhra Pradesh",
                "time_period": "Contemporary",
                "social_context": "Rural fishing community"
            },
            "characters": [
                {
                    "name": "రాజు",
                    "age": 30,
                    "traits": ["brave", "loyal", "impulsive"],
                    "background": "Born in coastal village, left to city for work"
                }
            ]
        }
    
    def test_initialization(self, story_agent, config):
        """Test agent initialization."""
        assert story_agent.name == "StoryAgent"
        assert story_agent.model_config == config["models"]["story_generation"]
    
    def test_create_story_plan(self, story_agent, story_parameters):
        """Test story plan creation."""
        story_plan = story_agent.create_story_plan(story_parameters)
        
        assert isinstance(story_plan, dict)
        assert "genre" in story_plan
        assert story_plan["genre"] == "drama"
        assert "theme" in story_plan
        assert "plot_structure" in story_plan
        assert "scenes" in story_plan
        assert len(story_plan["scenes"]) > 0
    
    def test_get_plot_structure(self, story_agent):
        """Test plot structure generation for different genres."""
        drama_structure = story_agent._get_plot_structure("drama")
        comedy_structure = story_agent._get_plot_structure("comedy")
        thriller_structure = story_agent._get_plot_structure("thriller")
        romance_structure = story_agent._get_plot_structure("romance")
        
        assert len(drama_structure) > 0
        assert len(comedy_structure) > 0
        assert len(thriller_structure) > 0
        assert len(romance_structure) > 0
        
        assert drama_structure != comedy_structure
        assert "climax" in drama_structure
        assert "complication" in comedy_structure
        assert "twist" in thriller_structure
        assert "reunion" in romance_structure
    
    def test_create_scenes_with_ai(self, story_agent):
        """Test scene creation with AI."""
        plot_structure = ["exposition", "rising_action", "climax", "resolution"]
        theme = "Overcoming adversity"
        setting = {"location": "Coastal village"}
        characters = [
            {
                "name": "రాజు",
                "age": 30,
                "traits": ["brave", "loyal", "impulsive"]
            }
        ]
        
        scenes = story_agent._create_scenes_with_ai(plot_structure, theme, setting, characters)
        
        assert len(scenes) == len(plot_structure)
        assert scenes[0]["plot_point"] == "exposition"
        assert scenes[2]["plot_point"] == "climax"
        assert "title" in scenes[0]
        assert "description" in scenes[0]
    
    def test_generate_draft(self, story_agent):
        """Test draft generation."""
        story_plan = {
            "title": "Test Story",
            "theme": "Family reconciliation",
            "genre": "drama",
            "plot_structure": ["exposition", "rising_action", "climax", "falling_action", "resolution"],
            "scenes": [
                {
                    "id": 1,
                    "title": "Scene 1: Exposition",
                    "plot_point": "exposition",
                    "description": "Introduction to the village and characters.",
                    "setting": "Coastal village",
                    "characters": ["రాజు", "లక్ష్మి"]
                },
                {
                    "id": 2,
                    "title": "Scene 2: Rising Action",
                    "plot_point": "rising_action",
                    "description": "Conflict emerges as the protagonist faces challenges.",
                    "setting": "Coastal village",
                    "characters": ["రాజు", "లక్ష్మి"]
                }
            ]
        }
        
        characters = [
            {
                "name": "రాజు",
                "age": 30,
                "traits": ["brave", "loyal", "impulsive"]
            },
            {
                "name": "లక్ష్మి",
                "age": 28,
                "traits": ["intelligent", "determined", "compassionate"]
            }
        ]
        
        draft = story_agent.generate_draft(story_plan, characters)
        
        assert isinstance(draft, str)
        assert len(draft) > 0
        # The test model returns a response
        assert "story" in draft.lower() or "test" in draft.lower() or "scene" in draft.lower() or "కుటుంబ" in draft