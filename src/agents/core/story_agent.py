"""
Story agent for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.base_agent import BaseAgent


class StoryAgent(BaseAgent):
    """
    Agent responsible for story structure and plot development.
    """
    
    def __init__(self, config):
        """
        Initialize the story agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        super().__init__(config)
        self.model_config = config["models"]["story_generation"]
        logger.info(f"Story agent initialized with model: {self.model_config['model_name']}")
    
    def process(self, input_data, context=None):
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process.
            context: Optional context information.
        
        Returns:
            Processing results.
        """
        if isinstance(input_data, dict) and "parameters" in input_data:
            return self.create_story_plan(input_data["parameters"])
        elif isinstance(input_data, str):
            return self.enhance_story(input_data, context)
        else:
            raise ValueError("Invalid input data for StoryAgent")
    
    def create_story_plan(self, parameters):
        """
        Create a story plan based on parameters.
        
        Args:
            parameters (dict): Story parameters.
        
        Returns:
            dict: Story plan.
        """
        logger.info("Creating story plan")
        
        # Extract relevant parameters
        genre = parameters.get("genre", "drama")
        theme = parameters.get("theme", "")
        setting = parameters.get("setting", {})
        
        # Create basic plot structure based on genre
        plot_structure = self._get_plot_structure(genre)
        
        # Create scenes based on plot structure
        scenes = self._create_scenes(plot_structure, theme, setting)
        
        story_plan = {
            "genre": genre,
            "theme": theme,
            "setting": setting,
            "plot_structure": plot_structure,
            "scenes": scenes
        }
        
        logger.debug(f"Created story plan with {len(scenes)} scenes")
        
        return story_plan
    
    def generate_draft(self, story_plan, characters):
        """
        Generate initial story draft.
        
        Args:
            story_plan (dict): Story plan.
            characters (list): Developed characters.
        
        Returns:
            str: Initial story draft.
        """
        logger.info("Generating initial story draft")
        
        # In a real implementation, this would use an LLM to generate the draft
        # For now, we'll return a placeholder
        
        scenes_text = []
        for scene in story_plan["scenes"]:
            scene_text = f"## {scene['title']}\n\n{scene['description']}\n\n"
            scenes_text.append(scene_text)
        
        draft = f"# {story_plan['theme']}\n\n" + "\n".join(scenes_text)
        
        logger.debug(f"Generated initial draft with {len(draft.split())} words")
        
        return draft
    
    def enhance_story(self, story, context=None):
        """
        Enhance an existing story.
        
        Args:
            story (str): Existing story.
            context (dict, optional): Context information.
        
        Returns:
            str: Enhanced story.
        """
        logger.info("Enhancing story")
        
        # In a real implementation, this would use an LLM to enhance the story
        # For now, we'll return the original story
        
        return story
    
    def _get_plot_structure(self, genre):
        """
        Get plot structure based on genre.
        
        Args:
            genre (str): Story genre.
        
        Returns:
            list: Plot structure.
        """
        plot_structures = {
            "drama": ["exposition", "rising_action", "climax", "falling_action", "resolution"],
            "comedy": ["setup", "complication", "confusion", "resolution", "epilogue"],
            "thriller": ["setup", "inciting_incident", "rising_stakes", "twist", "climax", "resolution"],
            "romance": ["meeting", "attraction", "conflict", "separation", "reunion"]
        }
        
        return plot_structures.get(genre.lower(), plot_structures["drama"])
    
    def _create_scenes(self, plot_structure, theme, setting):
        """
        Create scenes based on plot structure.
        
        Args:
            plot_structure (list): Plot structure.
            theme (str): Story theme.
            setting (dict): Story setting.
        
        Returns:
            list: Scenes.
        """
        scenes = []
        
        for i, plot_point in enumerate(plot_structure):
            scene = {
                "id": i + 1,
                "title": f"Scene {i + 1}: {plot_point.replace('_', ' ').title()}",
                "plot_point": plot_point,
                "description": f"This scene represents the {plot_point.replace('_', ' ')} of the story.",
                "setting": setting.get("location", ""),
                "characters": []
            }
            scenes.append(scene)
        
        return scenes