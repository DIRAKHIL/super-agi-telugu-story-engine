"""
Emotion agent for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.base_agent import BaseAgent


class EmotionAgent(BaseAgent):
    """
    Agent responsible for emotional consistency and impact in stories.
    """
    
    def __init__(self, config):
        """
        Initialize the emotion agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        super().__init__(config)
        logger.info("Emotion agent initialized")
    
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
            return self.plan_emotional_arc(input_data["parameters"])
        elif isinstance(input_data, str):
            return self.enhance_emotional_impact(input_data, context)
        else:
            raise ValueError("Invalid input data for EmotionAgent")
    
    def plan_emotional_arc(self, parameters):
        """
        Plan the emotional arc of the story.
        
        Args:
            parameters (dict): Story parameters.
        
        Returns:
            dict: Emotional arc plan.
        """
        logger.info("Planning emotional arc")
        
        # Extract relevant parameters
        genre = parameters.get("genre", "drama")
        theme = parameters.get("theme", "")
        emotional_arc = parameters.get("emotional_arc", "")
        
        # Determine emotional arc type
        if not emotional_arc:
            emotional_arc = self._determine_default_arc(genre, theme)
        
        # Create emotional beats based on arc type
        emotional_beats = self._create_emotional_beats(emotional_arc)
        
        arc_plan = {
            "arc_type": emotional_arc,
            "emotional_beats": emotional_beats,
            "emotional_intensity": self._calculate_intensity_curve(emotional_arc, len(emotional_beats))
        }
        
        logger.debug(f"Created emotional arc plan: {arc_plan['arc_type']}")
        
        return arc_plan
    
    def enhance_emotional_impact(self, story, context=None):
        """
        Enhance the emotional impact of a story.
        
        Args:
            story (str): Story content.
            context (dict, optional): Context information.
        
        Returns:
            str: Emotionally enhanced story.
        """
        logger.info("Enhancing emotional impact of story")
        
        # In a real implementation, this would use an LLM to enhance emotional impact
        # For now, we'll return the original story
        
        return story
    
    def _determine_default_arc(self, genre, theme):
        """
        Determine default emotional arc based on genre and theme.
        
        Args:
            genre (str): Story genre.
            theme (str): Story theme.
        
        Returns:
            str: Default emotional arc type.
        """
        # Map genres to default emotional arcs
        genre_arc_map = {
            "drama": "rise_fall_rise",
            "comedy": "fall_rise",
            "thriller": "rise_fall",
            "romance": "rise_fall_rise",
            "action": "steady_rise",
            "tragedy": "steady_fall"
        }
        
        # Check for specific themes that override genre defaults
        if "reconciliation" in theme.lower() or "reunion" in theme.lower():
            return "fall_rise"
        elif "loss" in theme.lower() or "tragedy" in theme.lower():
            return "fall"
        elif "triumph" in theme.lower() or "victory" in theme.lower():
            return "rise"
        elif "journey" in theme.lower() or "quest" in theme.lower():
            return "rise_fall_rise"
        
        # Default to genre-based arc
        return genre_arc_map.get(genre.lower(), "rise_fall_rise")
    
    def _create_emotional_beats(self, arc_type):
        """
        Create emotional beats based on arc type.
        
        Args:
            arc_type (str): Emotional arc type.
        
        Returns:
            list: Emotional beats.
        """
        beats = []
        
        # Define emotional beats based on arc type
        if arc_type == "rise":
            beats = [
                {"position": 0.0, "emotion": "neutral", "intensity": 0.2},
                {"position": 0.3, "emotion": "hopeful", "intensity": 0.4},
                {"position": 0.6, "emotion": "determined", "intensity": 0.6},
                {"position": 0.8, "emotion": "excited", "intensity": 0.8},
                {"position": 1.0, "emotion": "triumphant", "intensity": 1.0}
            ]
        elif arc_type == "fall":
            beats = [
                {"position": 0.0, "emotion": "content", "intensity": 0.8},
                {"position": 0.3, "emotion": "concerned", "intensity": 0.6},
                {"position": 0.6, "emotion": "worried", "intensity": 0.4},
                {"position": 0.8, "emotion": "distressed", "intensity": 0.3},
                {"position": 1.0, "emotion": "devastated", "intensity": 0.1}
            ]
        elif arc_type == "rise_fall":
            beats = [
                {"position": 0.0, "emotion": "neutral", "intensity": 0.2},
                {"position": 0.3, "emotion": "hopeful", "intensity": 0.5},
                {"position": 0.5, "emotion": "triumphant", "intensity": 0.9},
                {"position": 0.7, "emotion": "concerned", "intensity": 0.6},
                {"position": 0.9, "emotion": "distressed", "intensity": 0.3},
                {"position": 1.0, "emotion": "resigned", "intensity": 0.4}
            ]
        elif arc_type == "fall_rise":
            beats = [
                {"position": 0.0, "emotion": "content", "intensity": 0.7},
                {"position": 0.2, "emotion": "concerned", "intensity": 0.5},
                {"position": 0.4, "emotion": "distressed", "intensity": 0.2},
                {"position": 0.6, "emotion": "determined", "intensity": 0.4},
                {"position": 0.8, "emotion": "hopeful", "intensity": 0.6},
                {"position": 1.0, "emotion": "triumphant", "intensity": 0.9}
            ]
        elif arc_type == "rise_fall_rise":
            beats = [
                {"position": 0.0, "emotion": "neutral", "intensity": 0.3},
                {"position": 0.2, "emotion": "hopeful", "intensity": 0.5},
                {"position": 0.4, "emotion": "triumphant", "intensity": 0.8},
                {"position": 0.5, "emotion": "shocked", "intensity": 0.4},
                {"position": 0.6, "emotion": "distressed", "intensity": 0.2},
                {"position": 0.8, "emotion": "determined", "intensity": 0.6},
                {"position": 1.0, "emotion": "fulfilled", "intensity": 0.9}
            ]
        else:  # Default to a balanced arc
            beats = [
                {"position": 0.0, "emotion": "neutral", "intensity": 0.5},
                {"position": 0.25, "emotion": "curious", "intensity": 0.6},
                {"position": 0.5, "emotion": "concerned", "intensity": 0.4},
                {"position": 0.75, "emotion": "determined", "intensity": 0.7},
                {"position": 1.0, "emotion": "satisfied", "intensity": 0.8}
            ]
        
        return beats
    
    def _calculate_intensity_curve(self, arc_type, num_points=20):
        """
        Calculate emotional intensity curve.
        
        Args:
            arc_type (str): Emotional arc type.
            num_points (int): Number of points in the curve.
        
        Returns:
            list: Emotional intensity values.
        """
        intensity = []
        
        if arc_type == "rise":
            # Linear rise
            for i in range(num_points):
                intensity.append(0.2 + (0.8 * i / (num_points - 1)))
        elif arc_type == "fall":
            # Linear fall
            for i in range(num_points):
                intensity.append(0.8 - (0.7 * i / (num_points - 1)))
        elif arc_type == "rise_fall":
            # Rise then fall
            peak = num_points // 2
            for i in range(num_points):
                if i <= peak:
                    intensity.append(0.2 + (0.7 * i / peak))
                else:
                    intensity.append(0.9 - (0.5 * (i - peak) / (num_points - peak - 1)))
        elif arc_type == "fall_rise":
            # Fall then rise
            trough = num_points // 2
            for i in range(num_points):
                if i <= trough:
                    intensity.append(0.7 - (0.5 * i / trough))
                else:
                    intensity.append(0.2 + (0.7 * (i - trough) / (num_points - trough - 1)))
        elif arc_type == "rise_fall_rise":
            # Rise, fall, then rise again
            first_peak = num_points // 3
            trough = 2 * num_points // 3
            for i in range(num_points):
                if i <= first_peak:
                    intensity.append(0.3 + (0.5 * i / first_peak))
                elif i <= trough:
                    intensity.append(0.8 - (0.6 * (i - first_peak) / (trough - first_peak)))
                else:
                    intensity.append(0.2 + (0.7 * (i - trough) / (num_points - trough - 1)))
        else:
            # Default balanced curve
            for i in range(num_points):
                position = i / (num_points - 1)
                intensity.append(0.5 + 0.3 * (0.5 - abs(position - 0.5)))
        
        return intensity