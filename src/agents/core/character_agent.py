"""
Character agent for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.base_agent import BaseAgent


class CharacterAgent(BaseAgent):
    """
    Agent responsible for character development and consistency.
    """
    
    def __init__(self, config):
        """
        Initialize the character agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        super().__init__(config)
        logger.info("Character agent initialized")
    
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
            return self.develop_characters(input_data, context)
        elif isinstance(input_data, str):
            return self.ensure_character_consistency(input_data, context)
        else:
            raise ValueError("Invalid input data for CharacterAgent")
    
    def develop_characters(self, characters, story_plan=None):
        """
        Develop characters with depth and consistency.
        
        Args:
            characters (list): Basic character definitions.
            story_plan (dict, optional): Story plan for context.
        
        Returns:
            list: Developed characters.
        """
        logger.info(f"Developing {len(characters)} characters")
        
        developed_characters = []
        
        for character in characters:
            # Create a copy of the character to avoid modifying the original
            developed = character.copy()
            
            # Add character development elements
            developed["motivations"] = self._determine_motivations(character)
            developed["arc"] = self._determine_character_arc(character, story_plan)
            developed["relationships"] = self._determine_relationships(character, characters)
            developed["backstory"] = self._expand_backstory(character)
            developed["cultural_context"] = self._determine_cultural_context(character)
            
            developed_characters.append(developed)
            
            logger.debug(f"Developed character: {developed['name']}")
        
        return developed_characters
    
    def ensure_character_consistency(self, story, context=None):
        """
        Ensure character consistency throughout the story.
        
        Args:
            story (str): Story content.
            context (dict, optional): Context information.
        
        Returns:
            str: Story with consistent characters.
        """
        logger.info("Ensuring character consistency")
        
        # In a real implementation, this would use an LLM to check and fix character consistency
        # For now, we'll return the original story
        
        return story
    
    def _determine_motivations(self, character):
        """
        Determine character motivations based on traits and background.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Character motivations.
        """
        traits = [t.lower() for t in character.get("traits", [])]
        background = character.get("background", "").lower()
        
        # Default motivations
        motivations = {
            "primary": "self-improvement",
            "secondary": "connection",
            "hidden": "security"
        }
        
        # Determine primary motivation based on traits
        if any(t in traits for t in ["brave", "determined", "ambitious"]):
            motivations["primary"] = "achievement"
        elif any(t in traits for t in ["loyal", "compassionate", "friendly"]):
            motivations["primary"] = "connection"
        elif any(t in traits for t in ["intelligent", "curious", "creative"]):
            motivations["primary"] = "knowledge"
        elif any(t in traits for t in ["impulsive", "adventurous", "free-spirited"]):
            motivations["primary"] = "freedom"
        
        # Determine secondary motivation based on background
        if any(word in background for word in ["poor", "struggle", "hardship"]):
            motivations["secondary"] = "security"
        elif any(word in background for word in ["isolated", "alone", "rejected"]):
            motivations["secondary"] = "connection"
        elif any(word in background for word in ["oppressed", "controlled", "restricted"]):
            motivations["secondary"] = "freedom"
        elif any(word in background for word in ["failure", "lost", "mistake"]):
            motivations["secondary"] = "redemption"
        
        # Determine hidden motivation (often contrary to primary)
        if motivations["primary"] == "achievement":
            motivations["hidden"] = "fear of failure"
        elif motivations["primary"] == "connection":
            motivations["hidden"] = "fear of rejection"
        elif motivations["primary"] == "knowledge":
            motivations["hidden"] = "fear of ignorance"
        elif motivations["primary"] == "freedom":
            motivations["hidden"] = "fear of confinement"
        
        return motivations
    
    def _determine_character_arc(self, character, story_plan=None):
        """
        Determine character arc based on traits, background, and story plan.
        
        Args:
            character (dict): Character definition.
            story_plan (dict, optional): Story plan for context.
        
        Returns:
            dict: Character arc.
        """
        traits = [t.lower() for t in character.get("traits", [])]
        background = character.get("background", "").lower()
        
        # Default arc
        arc = {
            "type": "growth",
            "starting_state": "unfulfilled",
            "ending_state": "fulfilled",
            "key_moments": []
        }
        
        # Determine arc type based on traits and background
        if any(t in traits for t in ["flawed", "arrogant", "selfish"]):
            arc["type"] = "redemption"
            arc["starting_state"] = "flawed"
            arc["ending_state"] = "redeemed"
        elif any(t in traits for t in ["innocent", "naive", "sheltered"]):
            arc["type"] = "disillusionment"
            arc["starting_state"] = "innocent"
            arc["ending_state"] = "wiser"
        elif any(t in traits for t in ["traumatized", "wounded", "damaged"]):
            arc["type"] = "healing"
            arc["starting_state"] = "wounded"
            arc["ending_state"] = "healed"
        elif any(word in background for word in ["loss", "tragedy", "death"]):
            arc["type"] = "acceptance"
            arc["starting_state"] = "in denial"
            arc["ending_state"] = "accepting"
        
        # If story plan is provided, adjust arc based on plot structure
        if story_plan and "plot_structure" in story_plan:
            plot_structure = story_plan["plot_structure"]
            
            # Create key moments based on plot structure
            for i, plot_point in enumerate(plot_structure):
                key_moment = {
                    "plot_point": plot_point,
                    "character_state": self._get_character_state_for_plot_point(arc["type"], plot_point)
                }
                arc["key_moments"].append(key_moment)
        
        return arc
    
    def _determine_relationships(self, character, all_characters):
        """
        Determine character relationships with other characters.
        
        Args:
            character (dict): Character definition.
            all_characters (list): All characters in the story.
        
        Returns:
            list: Character relationships.
        """
        relationships = []
        
        # Skip if there's only one character
        if len(all_characters) <= 1:
            return relationships
        
        character_name = character.get("name", "")
        
        for other in all_characters:
            other_name = other.get("name", "")
            
            # Skip self
            if other_name == character_name:
                continue
            
            # Generate a relationship
            relationship = {
                "with": other_name,
                "type": self._generate_relationship_type(character, other),
                "dynamics": self._generate_relationship_dynamics(character, other)
            }
            
            relationships.append(relationship)
        
        return relationships
    
    def _expand_backstory(self, character):
        """
        Expand character backstory.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Expanded backstory.
        """
        background = character.get("background", "")
        
        # Default backstory elements
        backstory = {
            "childhood": "Standard childhood",
            "formative_events": [],
            "education": "Basic education",
            "career": "Unspecified",
            "key_relationships": []
        }
        
        # Extract information from background if available
        if background:
            background_lower = background.lower()
            
            # Determine childhood
            if "born in" in background_lower:
                birth_place = background_lower.split("born in")[1].split(",")[0].strip()
                backstory["childhood"] = f"Grew up in {birth_place}"
            
            # Determine education
            if "teacher" in background_lower or "professor" in background_lower:
                backstory["education"] = "Higher education"
            elif "school" in background_lower:
                backstory["education"] = "School education"
            
            # Determine career
            if "teacher" in background_lower:
                backstory["career"] = "Teacher"
            elif "work" in background_lower:
                backstory["career"] = "Working professional"
            elif "fishing" in background_lower:
                backstory["career"] = "Fisher"
            elif "farmer" in background_lower:
                backstory["career"] = "Farmer"
            
            # Determine formative events
            if "left" in background_lower:
                backstory["formative_events"].append("Leaving home")
            if "moved" in background_lower:
                backstory["formative_events"].append("Relocation")
            if "lost" in background_lower:
                backstory["formative_events"].append("Experiencing loss")
        
        return backstory
    
    def _determine_cultural_context(self, character):
        """
        Determine character's cultural context.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Cultural context.
        """
        background = character.get("background", "").lower()
        
        # Default cultural context
        cultural_context = {
            "region": "General Telugu region",
            "socioeconomic_status": "Middle class",
            "religious_background": "Traditional Hindu",
            "urban_rural": "Unspecified"
        }
        
        # Determine region
        if "coastal" in background:
            cultural_context["region"] = "Coastal Andhra"
        elif "rayalaseema" in background:
            cultural_context["region"] = "Rayalaseema"
        elif "telangana" in background:
            cultural_context["region"] = "Telangana"
        elif "hyderabad" in background:
            cultural_context["region"] = "Hyderabad"
        
        # Determine socioeconomic status
        if any(word in background for word in ["poor", "poverty", "struggle"]):
            cultural_context["socioeconomic_status"] = "Lower class"
        elif any(word in background for word in ["wealthy", "rich", "affluent"]):
            cultural_context["socioeconomic_status"] = "Upper class"
        
        # Determine urban/rural background
        if any(word in background for word in ["village", "rural", "countryside"]):
            cultural_context["urban_rural"] = "Rural"
        elif any(word in background for word in ["city", "urban", "town"]):
            cultural_context["urban_rural"] = "Urban"
        
        # Determine religious background
        if "christian" in background:
            cultural_context["religious_background"] = "Christian"
        elif "muslim" in background:
            cultural_context["religious_background"] = "Muslim"
        elif "secular" in background:
            cultural_context["religious_background"] = "Secular"
        
        return cultural_context
    
    def _get_character_state_for_plot_point(self, arc_type, plot_point):
        """
        Get character state for a specific plot point.
        
        Args:
            arc_type (str): Character arc type.
            plot_point (str): Plot point.
        
        Returns:
            str: Character state.
        """
        # Character states for different arc types at different plot points
        arc_states = {
            "growth": {
                "exposition": "comfortable but unfulfilled",
                "inciting_incident": "challenged",
                "rising_action": "struggling",
                "climax": "moment of truth",
                "falling_action": "changed",
                "resolution": "fulfilled"
            },
            "redemption": {
                "exposition": "flawed",
                "inciting_incident": "confronted",
                "rising_action": "resistant",
                "climax": "sacrifice",
                "falling_action": "humbled",
                "resolution": "redeemed"
            },
            "disillusionment": {
                "exposition": "innocent",
                "inciting_incident": "first doubt",
                "rising_action": "questioning",
                "climax": "harsh truth",
                "falling_action": "processing",
                "resolution": "wiser"
            },
            "healing": {
                "exposition": "wounded",
                "inciting_incident": "opportunity to heal",
                "rising_action": "reluctant steps",
                "climax": "confronting trauma",
                "falling_action": "processing",
                "resolution": "healed"
            },
            "acceptance": {
                "exposition": "in denial",
                "inciting_incident": "forced to face reality",
                "rising_action": "bargaining",
                "climax": "emotional breakdown",
                "falling_action": "beginning to accept",
                "resolution": "acceptance"
            }
        }
        
        # Get states for the arc type
        states = arc_states.get(arc_type, arc_states["growth"])
        
        # Map plot point to standard plot points
        standard_plot_point = plot_point
        if plot_point in ["setup", "meeting"]:
            standard_plot_point = "exposition"
        elif plot_point in ["complication", "attraction", "inciting_incident"]:
            standard_plot_point = "inciting_incident"
        elif plot_point in ["confusion", "conflict", "rising_stakes"]:
            standard_plot_point = "rising_action"
        elif plot_point in ["twist", "separation"]:
            standard_plot_point = "climax"
        elif plot_point in ["resolution", "reunion"]:
            standard_plot_point = "resolution"
        
        # Return state for the plot point
        return states.get(standard_plot_point, "unspecified")
    
    def _generate_relationship_type(self, character1, character2):
        """
        Generate relationship type between two characters.
        
        Args:
            character1 (dict): First character.
            character2 (dict): Second character.
        
        Returns:
            str: Relationship type.
        """
        # Default relationship type
        relationship_type = "acquaintance"
        
        # Check for family relationships based on names and backgrounds
        name1 = character1.get("name", "").lower()
        name2 = character2.get("name", "").lower()
        background1 = character1.get("background", "").lower()
        background2 = character2.get("background", "").lower()
        
        # Simple heuristics for relationship types
        if "family" in background1 and name2 in background1:
            relationship_type = "family"
        elif "family" in background2 and name1 in background2:
            relationship_type = "family"
        elif abs(character1.get("age", 30) - character2.get("age", 30)) < 10:
            relationship_type = "peer"
        elif character1.get("age", 30) > character2.get("age", 30) + 15:
            relationship_type = "mentor"
        elif character2.get("age", 30) > character1.get("age", 30) + 15:
            relationship_type = "mentee"
        
        return relationship_type
    
    def _generate_relationship_dynamics(self, character1, character2):
        """
        Generate relationship dynamics between two characters.
        
        Args:
            character1 (dict): First character.
            character2 (dict): Second character.
        
        Returns:
            dict: Relationship dynamics.
        """
        traits1 = [t.lower() for t in character1.get("traits", [])]
        traits2 = [t.lower() for t in character2.get("traits", [])]
        
        # Default dynamics
        dynamics = {
            "trust": 0.5,
            "conflict": 0.5,
            "power_balance": 0.5,
            "emotional_bond": 0.5
        }
        
        # Adjust trust based on traits
        if any(t in traits1 for t in ["loyal", "honest", "trustworthy"]) and any(t in traits2 for t in ["loyal", "honest", "trustworthy"]):
            dynamics["trust"] = 0.8
        elif any(t in traits1 for t in ["deceptive", "manipulative", "dishonest"]) or any(t in traits2 for t in ["deceptive", "manipulative", "dishonest"]):
            dynamics["trust"] = 0.2
        
        # Adjust conflict based on traits
        if any(t in traits1 for t in ["aggressive", "stubborn", "dominant"]) and any(t in traits2 for t in ["aggressive", "stubborn", "dominant"]):
            dynamics["conflict"] = 0.8
        elif any(t in traits1 for t in ["peaceful", "cooperative", "agreeable"]) and any(t in traits2 for t in ["peaceful", "cooperative", "agreeable"]):
            dynamics["conflict"] = 0.2
        
        # Adjust power balance based on traits and age
        age_diff = character1.get("age", 30) - character2.get("age", 30)
        if age_diff > 10 or any(t in traits1 for t in ["dominant", "powerful", "authoritative"]):
            dynamics["power_balance"] = 0.7
        elif age_diff < -10 or any(t in traits2 for t in ["dominant", "powerful", "authoritative"]):
            dynamics["power_balance"] = 0.3
        
        # Adjust emotional bond based on traits
        if any(t in traits1 for t in ["compassionate", "empathetic", "loving"]) and any(t in traits2 for t in ["compassionate", "empathetic", "loving"]):
            dynamics["emotional_bond"] = 0.8
        elif any(t in traits1 for t in ["cold", "distant", "aloof"]) or any(t in traits2 for t in ["cold", "distant", "aloof"]):
            dynamics["emotional_bond"] = 0.2
        
        return dynamics