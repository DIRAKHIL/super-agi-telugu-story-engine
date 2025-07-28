"""
Character Psychologist Agent for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.base_agent import BaseAgent


class CharacterPsychologistAgent(BaseAgent):
    """
    Expert agent that applies psychological frameworks to character development.
    """
    
    def __init__(self, config):
        """
        Initialize the character psychologist agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        super().__init__(config)
        
        # Get agent-specific configuration
        agent_config = self._get_agent_config()
        
        # Configure psychological frameworks
        self.frameworks = {
            "ocean": agent_config.get("frameworks", {}).get("ocean", True),
            "maslow": agent_config.get("frameworks", {}).get("maslow", True),
            "erikson": agent_config.get("frameworks", {}).get("erikson", False),
            "jung": agent_config.get("frameworks", {}).get("jung", False)
        }
        
        logger.info(f"Character Psychologist agent initialized with frameworks: {self.frameworks}")
    
    def process(self, input_data, context=None):
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process.
            context: Optional context information.
        
        Returns:
            Processing results.
        """
        if isinstance(input_data, list):
            return self.enhance_characters(input_data)
        elif isinstance(input_data, str):
            return self.refine_story(input_data, context)
        else:
            raise ValueError("Invalid input data for CharacterPsychologistAgent")
    
    def enhance_characters(self, characters):
        """
        Enhance characters with psychological depth.
        
        Args:
            characters (list): Character definitions.
        
        Returns:
            list: Enhanced characters.
        """
        logger.info(f"Enhancing {len(characters)} characters with psychological frameworks")
        
        enhanced_characters = []
        
        for character in characters:
            enhanced = character.copy()
            
            # Apply OCEAN personality model
            if self.frameworks["ocean"]:
                enhanced["psychology"] = enhanced.get("psychology", {})
                enhanced["psychology"]["ocean"] = self._apply_ocean_model(character)
            
            # Apply Maslow's hierarchy of needs
            if self.frameworks["maslow"]:
                enhanced["psychology"] = enhanced.get("psychology", {})
                enhanced["psychology"]["needs"] = self._apply_maslow_hierarchy(character)
            
            # Apply Erikson's stages of development
            if self.frameworks["erikson"]:
                enhanced["psychology"] = enhanced.get("psychology", {})
                enhanced["psychology"]["development_stage"] = self._apply_erikson_stages(character)
            
            # Apply Jungian archetypes
            if self.frameworks["jung"]:
                enhanced["psychology"] = enhanced.get("psychology", {})
                enhanced["psychology"]["archetype"] = self._apply_jung_archetypes(character)
            
            enhanced_characters.append(enhanced)
        
        logger.debug(f"Enhanced {len(enhanced_characters)} characters with psychological depth")
        
        return enhanced_characters
    
    def refine_story(self, story, parameters=None):
        """
        Refine story with psychological insights.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            str: Refined story.
        """
        logger.info("Refining story with psychological insights")
        
        # In a real implementation, this would use an LLM to refine the story
        # For now, we'll return the original story
        
        return story
    
    def _apply_ocean_model(self, character):
        """
        Apply OCEAN personality model to character.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: OCEAN personality traits.
        """
        # Map character traits to OCEAN dimensions
        traits = character.get("traits", [])
        
        # Default values
        ocean = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }
        
        # Simple trait mapping (in a real implementation, this would be more sophisticated)
        trait_mapping = {
            "creative": {"openness": 0.8},
            "curious": {"openness": 0.7},
            "organized": {"conscientiousness": 0.8},
            "responsible": {"conscientiousness": 0.7},
            "outgoing": {"extraversion": 0.8},
            "sociable": {"extraversion": 0.7},
            "friendly": {"agreeableness": 0.8},
            "cooperative": {"agreeableness": 0.7},
            "anxious": {"neuroticism": 0.8},
            "moody": {"neuroticism": 0.7},
            "brave": {"neuroticism": 0.3, "extraversion": 0.6},
            "loyal": {"agreeableness": 0.7, "conscientiousness": 0.6},
            "impulsive": {"conscientiousness": 0.3, "neuroticism": 0.6},
            "intelligent": {"openness": 0.7},
            "determined": {"conscientiousness": 0.7},
            "compassionate": {"agreeableness": 0.8}
        }
        
        # Apply trait mappings
        for trait in traits:
            trait_lower = trait.lower()
            if trait_lower in trait_mapping:
                for dimension, value in trait_mapping[trait_lower].items():
                    ocean[dimension] = value
        
        return ocean
    
    def _apply_maslow_hierarchy(self, character):
        """
        Apply Maslow's hierarchy of needs to character.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Character needs.
        """
        # Simple implementation based on character background
        background = character.get("background", "").lower()
        
        needs = {
            "physiological": 0.5,
            "safety": 0.5,
            "belonging": 0.5,
            "esteem": 0.5,
            "self_actualization": 0.5
        }
        
        # Adjust needs based on background keywords
        if any(word in background for word in ["poor", "starving", "homeless", "refugee"]):
            needs["physiological"] = 0.9
            needs["safety"] = 0.8
            needs["self_actualization"] = 0.2
        
        if any(word in background for word in ["danger", "war", "threat", "unsafe"]):
            needs["safety"] = 0.9
            needs["self_actualization"] = 0.3
        
        if any(word in background for word in ["lonely", "isolated", "rejected"]):
            needs["belonging"] = 0.9
            needs["esteem"] = 0.4
        
        if any(word in background for word in ["failure", "humiliated", "disrespected"]):
            needs["esteem"] = 0.9
        
        if any(word in background for word in ["successful", "accomplished", "fulfilled"]):
            needs["self_actualization"] = 0.8
            needs["physiological"] = 0.3
            needs["safety"] = 0.3
        
        return needs
    
    def _apply_erikson_stages(self, character):
        """
        Apply Erikson's stages of development to character.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Character's developmental stage.
        """
        age = character.get("age", 30)
        
        # Determine primary developmental stage based on age
        if age < 2:
            stage = "trust_vs_mistrust"
        elif age < 4:
            stage = "autonomy_vs_shame"
        elif age < 6:
            stage = "initiative_vs_guilt"
        elif age < 12:
            stage = "industry_vs_inferiority"
        elif age < 20:
            stage = "identity_vs_role_confusion"
        elif age < 40:
            stage = "intimacy_vs_isolation"
        elif age < 65:
            stage = "generativity_vs_stagnation"
        else:
            stage = "integrity_vs_despair"
        
        return {
            "current_stage": stage,
            "resolved_stages": []  # In a real implementation, this would be determined based on character history
        }
    
    def _apply_jung_archetypes(self, character):
        """
        Apply Jungian archetypes to character.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Character's archetypes.
        """
        traits = [t.lower() for t in character.get("traits", [])]
        background = character.get("background", "").lower()
        
        # Simple archetype mapping
        archetypes = {
            "hero": 0,
            "mentor": 0,
            "threshold_guardian": 0,
            "herald": 0,
            "shapeshifter": 0,
            "shadow": 0,
            "trickster": 0
        }
        
        # Hero traits
        if any(t in traits for t in ["brave", "courageous", "determined", "strong"]):
            archetypes["hero"] += 1
        
        # Mentor traits
        if any(t in traits for t in ["wise", "knowledgeable", "guiding", "teaching"]):
            archetypes["mentor"] += 1
        
        # Threshold Guardian traits
        if any(t in traits for t in ["protective", "testing", "challenging"]):
            archetypes["threshold_guardian"] += 1
        
        # Herald traits
        if any(t in traits for t in ["announcing", "warning", "motivating"]):
            archetypes["herald"] += 1
        
        # Shapeshifter traits
        if any(t in traits for t in ["changing", "unpredictable", "mysterious"]):
            archetypes["shapeshifter"] += 1
        
        # Shadow traits
        if any(t in traits for t in ["dark", "villainous", "antagonistic"]):
            archetypes["shadow"] += 1
        
        # Trickster traits
        if any(t in traits for t in ["mischievous", "playful", "deceiving"]):
            archetypes["trickster"] += 1
        
        # Find primary archetype
        primary_archetype = max(archetypes.items(), key=lambda x: x[1])[0]
        
        return {
            "primary": primary_archetype,
            "scores": archetypes
        }