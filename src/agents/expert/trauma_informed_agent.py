"""
Trauma-Informed Agent for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.base_agent import BaseAgent


class TraumaInformedAgent(BaseAgent):
    """
    Expert agent that creates authentic trauma and recovery representations.
    """
    
    def __init__(self, config):
        """
        Initialize the trauma-informed agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        super().__init__(config)
        
        # Get agent-specific configuration
        agent_config = self._get_agent_config()
        
        # Configure trauma frameworks
        self.frameworks = {
            "ptsd": agent_config.get("frameworks", {}).get("ptsd", True),
            "grief": agent_config.get("frameworks", {}).get("grief", True),
            "resilience": agent_config.get("frameworks", {}).get("resilience", True),
            "moral_injury": agent_config.get("frameworks", {}).get("moral_injury", False)
        }
        
        logger.info(f"Trauma-Informed agent initialized with frameworks: {self.frameworks}")
    
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
            return self.analyze_character_trauma(input_data)
        elif isinstance(input_data, str):
            return self.refine_story(input_data, context)
        else:
            raise ValueError("Invalid input data for TraumaInformedAgent")
    
    def analyze_character_trauma(self, characters):
        """
        Analyze character trauma and recovery potential.
        
        Args:
            characters (list): Character definitions.
        
        Returns:
            list: Characters with trauma analysis.
        """
        logger.info(f"Analyzing trauma for {len(characters)} characters")
        
        analyzed_characters = []
        
        for character in characters:
            # Create a copy of the character to avoid modifying the original
            analyzed = character.copy()
            
            # Add trauma analysis
            analyzed["trauma"] = self._analyze_trauma(character)
            
            analyzed_characters.append(analyzed)
        
        return analyzed_characters
    
    def refine_story(self, story, parameters=None):
        """
        Refine story with trauma-informed perspective.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            str: Refined story.
        """
        logger.info("Refining story with trauma-informed perspective")
        
        # In a real implementation, this would use an LLM to refine the story
        # For now, we'll return the original story
        
        return story
    
    def _analyze_trauma(self, character):
        """
        Analyze character trauma based on background and traits.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Trauma analysis.
        """
        background = character.get("background", "").lower()
        traits = [t.lower() for t in character.get("traits", [])]
        
        # Default trauma analysis
        trauma_analysis = {
            "trauma_indicators": [],
            "recovery_stage": "resolved",
            "resilience_factors": [],
            "vulnerability_factors": []
        }
        
        # Check for trauma indicators in background
        trauma_indicators = []
        if any(word in background for word in ["loss", "death", "died", "lost"]):
            trauma_indicators.append("loss")
        if any(word in background for word in ["abuse", "violence", "assault"]):
            trauma_indicators.append("interpersonal violence")
        if any(word in background for word in ["accident", "disaster", "catastrophe"]):
            trauma_indicators.append("accident/disaster")
        if any(word in background for word in ["war", "conflict", "battle"]):
            trauma_indicators.append("war/conflict")
        if any(word in background for word in ["rejection", "abandoned", "left"]):
            trauma_indicators.append("abandonment")
        
        trauma_analysis["trauma_indicators"] = trauma_indicators
        
        # Determine recovery stage
        if trauma_indicators:
            trauma_analysis["recovery_stage"] = self._determine_recovery_stage(character)
        
        # Identify resilience factors
        resilience_factors = []
        if any(t in traits for t in ["resilient", "strong", "determined"]):
            resilience_factors.append("personal strength")
        if "support" in background or "family" in background or "friend" in background:
            resilience_factors.append("social support")
        if any(t in traits for t in ["optimistic", "hopeful", "positive"]):
            resilience_factors.append("positive outlook")
        if any(t in traits for t in ["spiritual", "religious", "faithful"]):
            resilience_factors.append("spiritual/religious beliefs")
        if "education" in background or "learned" in background or "study" in background:
            resilience_factors.append("education/knowledge")
        
        trauma_analysis["resilience_factors"] = resilience_factors
        
        # Identify vulnerability factors
        vulnerability_factors = []
        if any(t in traits for t in ["anxious", "fearful", "nervous"]):
            vulnerability_factors.append("anxiety")
        if any(t in traits for t in ["depressed", "sad", "melancholic"]):
            vulnerability_factors.append("depression")
        if "alone" in background or "isolated" in background:
            vulnerability_factors.append("social isolation")
        if any(t in traits for t in ["impulsive", "reckless", "careless"]):
            vulnerability_factors.append("impulsivity")
        if "substance" in background or "alcohol" in background or "drug" in background:
            vulnerability_factors.append("substance use")
        
        trauma_analysis["vulnerability_factors"] = vulnerability_factors
        
        return trauma_analysis
    
    def _determine_recovery_stage(self, character):
        """
        Determine character's trauma recovery stage.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            str: Recovery stage.
        """
        background = character.get("background", "").lower()
        traits = [t.lower() for t in character.get("traits", [])]
        
        # Default to resolved
        recovery_stage = "resolved"
        
        # Check for acute trauma
        if any(word in background for word in ["recent", "just", "new"]) and any(word in background for word in ["trauma", "loss", "accident", "disaster"]):
            recovery_stage = "acute"
        
        # Check for ongoing trauma
        elif "ongoing" in background or "continuing" in background or "current" in background:
            recovery_stage = "ongoing"
        
        # Check for processing trauma
        elif any(t in traits for t in ["processing", "healing", "recovering"]):
            recovery_stage = "processing"
        
        # Check for unresolved trauma
        elif any(t in traits for t in ["traumatized", "haunted", "troubled"]):
            recovery_stage = "unresolved"
        
        # Check for post-traumatic growth
        elif any(t in traits for t in ["transformed", "enlightened", "wise"]) and any(word in background for word in ["trauma", "loss", "accident", "disaster"]):
            recovery_stage = "post_traumatic_growth"
        
        return recovery_stage
    
    def generate_trauma_informed_narrative(self, character, trauma_type):
        """
        Generate trauma-informed narrative elements for a character.
        
        Args:
            character (dict): Character definition.
            trauma_type (str): Type of trauma.
        
        Returns:
            dict: Trauma-informed narrative elements.
        """
        logger.info(f"Generating trauma-informed narrative for trauma type: {trauma_type}")
        
        # Default narrative elements
        narrative_elements = {
            "symptoms": [],
            "coping_mechanisms": [],
            "recovery_arc": [],
            "support_systems": []
        }
        
        # Generate elements based on trauma type
        if trauma_type == "loss":
            narrative_elements = self._generate_loss_narrative(character)
        elif trauma_type == "interpersonal violence":
            narrative_elements = self._generate_violence_narrative(character)
        elif trauma_type == "accident/disaster":
            narrative_elements = self._generate_disaster_narrative(character)
        elif trauma_type == "war/conflict":
            narrative_elements = self._generate_war_narrative(character)
        elif trauma_type == "abandonment":
            narrative_elements = self._generate_abandonment_narrative(character)
        
        return narrative_elements
    
    def _generate_loss_narrative(self, character):
        """
        Generate narrative elements for loss trauma.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Narrative elements.
        """
        # Kübler-Ross grief stages
        grief_stages = [
            "denial - character struggles to accept the loss",
            "anger - character expresses rage at the situation or others",
            "bargaining - character tries to negotiate or find meaning",
            "depression - character experiences profound sadness",
            "acceptance - character comes to terms with the loss"
        ]
        
        # Common symptoms of grief
        symptoms = [
            "emotional numbness",
            "difficulty concentrating",
            "sleep disturbances",
            "appetite changes",
            "social withdrawal"
        ]
        
        # Common coping mechanisms
        coping_mechanisms = [
            "reminiscing about the lost person/thing",
            "creating rituals or memorials",
            "seeking support from others",
            "finding meaning in the loss",
            "engaging in self-care"
        ]
        
        # Support systems
        support_systems = [
            "family members",
            "friends",
            "community groups",
            "religious/spiritual practices",
            "professional counseling"
        ]
        
        return {
            "symptoms": symptoms,
            "coping_mechanisms": coping_mechanisms,
            "recovery_arc": grief_stages,
            "support_systems": support_systems
        }
    
    def _generate_violence_narrative(self, character):
        """
        Generate narrative elements for interpersonal violence trauma.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Narrative elements.
        """
        # Recovery stages for interpersonal violence
        recovery_stages = [
            "safety - establishing physical and emotional security",
            "remembrance - processing traumatic memories",
            "reconnection - rebuilding relationships and identity",
            "integration - incorporating experience into life narrative"
        ]
        
        # Common symptoms
        symptoms = [
            "hypervigilance",
            "intrusive memories",
            "avoidance behaviors",
            "trust issues",
            "emotional dysregulation"
        ]
        
        # Common coping mechanisms
        coping_mechanisms = [
            "establishing boundaries",
            "safety planning",
            "grounding techniques",
            "seeking justice/closure",
            "reclaiming personal power"
        ]
        
        # Support systems
        support_systems = [
            "trauma-informed therapists",
            "support groups",
            "trusted friends/family",
            "advocacy organizations",
            "legal support"
        ]
        
        return {
            "symptoms": symptoms,
            "coping_mechanisms": coping_mechanisms,
            "recovery_arc": recovery_stages,
            "support_systems": support_systems
        }
    
    def _generate_disaster_narrative(self, character):
        """
        Generate narrative elements for accident/disaster trauma.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Narrative elements.
        """
        # Recovery stages for disaster trauma
        recovery_stages = [
            "impact - initial shock and disorientation",
            "rescue - seeking safety and immediate needs",
            "recovery - rebuilding physical resources",
            "reconstruction - rebuilding life and meaning"
        ]
        
        # Common symptoms
        symptoms = [
            "heightened startle response",
            "flashbacks triggered by similar situations",
            "anxiety about future disasters",
            "survivor's guilt",
            "difficulty with uncertainty"
        ]
        
        # Common coping mechanisms
        coping_mechanisms = [
            "preparation and planning",
            "helping others affected",
            "creating new safety measures",
            "finding meaning in survival",
            "gradual exposure to triggers"
        ]
        
        # Support systems
        support_systems = [
            "disaster relief organizations",
            "community rebuilding efforts",
            "fellow survivors",
            "practical support networks",
            "crisis counseling"
        ]
        
        return {
            "symptoms": symptoms,
            "coping_mechanisms": coping_mechanisms,
            "recovery_arc": recovery_stages,
            "support_systems": support_systems
        }
    
    def _generate_war_narrative(self, character):
        """
        Generate narrative elements for war/conflict trauma.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Narrative elements.
        """
        # Recovery stages for war trauma
        recovery_stages = [
            "survival mode - focus on basic safety",
            "reintegration - returning to civilian life",
            "meaning-making - processing moral injuries",
            "identity reconstruction - who am I after war",
            "post-traumatic growth - finding purpose"
        ]
        
        # Common symptoms
        symptoms = [
            "combat hypervigilance",
            "moral injury",
            "survivor's guilt",
            "difficulty with civilian transition",
            "complex grief for lost comrades"
        ]
        
        # Common coping mechanisms
        coping_mechanisms = [
            "connecting with fellow veterans",
            "service to others",
            "ritual and commemoration",
            "creative expression",
            "physical activity"
        ]
        
        # Support systems
        support_systems = [
            "veteran organizations",
            "specialized trauma treatment",
            "peer support groups",
            "family reintegration programs",
            "community recognition"
        ]
        
        return {
            "symptoms": symptoms,
            "coping_mechanisms": coping_mechanisms,
            "recovery_arc": recovery_stages,
            "support_systems": support_systems
        }
    
    def _generate_abandonment_narrative(self, character):
        """
        Generate narrative elements for abandonment trauma.
        
        Args:
            character (dict): Character definition.
        
        Returns:
            dict: Narrative elements.
        """
        # Recovery stages for abandonment trauma
        recovery_stages = [
            "shock and denial - disbelief at abandonment",
            "anger and protest - attempts to reconnect",
            "despair - acceptance of separation",
            "detachment - emotional withdrawal",
            "reorganization - building new attachments"
        ]
        
        # Common symptoms
        symptoms = [
            "fear of rejection",
            "difficulty trusting others",
            "anxious attachment patterns",
            "self-blame",
            "fear of being alone"
        ]
        
        # Common coping mechanisms
        coping_mechanisms = [
            "building secure relationships",
            "developing self-reliance",
            "challenging negative self-beliefs",
            "establishing healthy boundaries",
            "self-compassion practices"
        ]
        
        # Support systems
        support_systems = [
            "consistent relationships",
            "therapy for attachment issues",
            "supportive community",
            "chosen family",
            "self-development resources"
        ]
        
        return {
            "symptoms": symptoms,
            "coping_mechanisms": coping_mechanisms,
            "recovery_arc": recovery_stages,
            "support_systems": support_systems
        }