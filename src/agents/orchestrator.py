"""
Agent orchestrator for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.core.story_agent import StoryAgent
from src.agents.core.emotion_agent import EmotionAgent
from src.agents.core.cultural_agent import CulturalAgent
from src.agents.core.character_agent import CharacterAgent
from src.agents.core.technical_agent import TechnicalAgent
from src.agents.core.quality_agent import QualityAgent

from src.agents.expert.character_psychologist_agent import CharacterPsychologistAgent
from src.agents.expert.trauma_informed_agent import TraumaInformedAgent
from src.agents.expert.legal_ethics_agent import LegalEthicsAgent
from src.agents.expert.medical_narrative_agent import MedicalNarrativeAgent
from src.agents.expert.spiritual_meaning_agent import SpiritualMeaningAgent
from src.agents.expert.leadership_agent import LeadershipAgent


class AgentOrchestrator:
    """
    Orchestrates the multi-agent system for story generation.
    """
    
    def __init__(self, config):
        """
        Initialize the agent orchestrator.
        
        Args:
            config (dict): Configuration dictionary.
        """
        self.config = config
        self.agents = {}
        
        # Initialize core agents
        self._init_core_agents()
        
        # Initialize expert agents
        self._init_expert_agents()
        
        logger.info(f"Initialized {len(self.agents)} agents")
    
    def _init_core_agents(self):
        """Initialize core agents."""
        core_agents = {
            "story": StoryAgent,
            "emotion": EmotionAgent,
            "cultural": CulturalAgent,
            "character": CharacterAgent,
            "technical": TechnicalAgent,
            "quality": QualityAgent
        }
        
        for name, agent_class in core_agents.items():
            if self.config["agents"].get(name, {}).get("enabled", False):
                self.agents[name] = agent_class(self.config)
                logger.debug(f"Initialized core agent: {name}")
    
    def _init_expert_agents(self):
        """Initialize expert domain agents."""
        expert_agents = {
            "character_psychologist": CharacterPsychologistAgent,
            "trauma_informed": TraumaInformedAgent,
            "legal_ethics": LegalEthicsAgent,
            "medical_narrative": MedicalNarrativeAgent,
            "spiritual_meaning": SpiritualMeaningAgent,
            "leadership": LeadershipAgent
        }
        
        for name, agent_class in expert_agents.items():
            if self.config["agents"]["expert"].get(name, {}).get("enabled", False):
                self.agents[f"expert_{name}"] = agent_class(self.config)
                logger.debug(f"Initialized expert agent: {name}")
    
    def generate_story(self, parameters):
        """
        Generate a story using the multi-agent system.
        
        Args:
            parameters (dict): Story generation parameters.
        
        Returns:
            str: Generated story.
        """
        logger.info("Starting multi-agent story generation process")
        
        # Step 1: Story planning with core agents
        story_plan = self._create_story_plan(parameters)
        
        # Step 2: Character development with expert input
        characters = self._develop_characters(parameters["characters"], story_plan)
        
        # Step 3: Generate initial story draft
        initial_draft = self._generate_initial_draft(story_plan, characters)
        
        # Step 4: Expert agent refinement
        refined_draft = self._refine_with_experts(initial_draft, parameters)
        
        # Step 5: Cultural adaptation
        culturally_adapted = self._adapt_culturally(refined_draft, parameters)
        
        # Step 6: Technical quality improvement
        technically_improved = self._improve_technical_quality(culturally_adapted)
        
        # Step 7: Final quality assurance
        final_story = self._perform_quality_assurance(technically_improved, parameters)
        
        logger.info("Multi-agent story generation process completed")
        
        return final_story
    
    def _create_story_plan(self, parameters):
        """Create a story plan using the story agent."""
        logger.info("Creating story plan")
        if "story" in self.agents:
            return self.agents["story"].create_story_plan(parameters)
        return {"plot": "Default plot structure", "scenes": []}
    
    def _develop_characters(self, character_params, story_plan):
        """Develop characters with psychological depth."""
        logger.info("Developing characters")
        characters = character_params.copy()
        
        # Use character agent if available
        if "character" in self.agents:
            characters = self.agents["character"].develop_characters(characters, story_plan)
        
        # Use character psychologist agent if available
        if "expert_character_psychologist" in self.agents:
            characters = self.agents["expert_character_psychologist"].enhance_characters(characters)
        
        return characters
    
    def _generate_initial_draft(self, story_plan, characters):
        """Generate initial story draft."""
        logger.info("Generating initial draft")
        if "story" in self.agents:
            return self.agents["story"].generate_draft(story_plan, characters)
        return "Default story draft"
    
    def _refine_with_experts(self, draft, parameters):
        """Refine story with expert agents."""
        logger.info("Refining story with expert agents")
        refined = draft
        
        # Apply each expert agent in sequence
        for name, agent in self.agents.items():
            if name.startswith("expert_") and hasattr(agent, "refine_story"):
                refined = agent.refine_story(refined, parameters)
                logger.debug(f"Applied {name} refinement")
        
        return refined
    
    def _adapt_culturally(self, draft, parameters):
        """Adapt story to Telugu cultural context."""
        logger.info("Adapting story culturally")
        if "cultural" in self.agents:
            return self.agents["cultural"].adapt_culturally(draft, parameters)
        return draft
    
    def _improve_technical_quality(self, draft):
        """Improve technical quality of the story."""
        logger.info("Improving technical quality")
        if "technical" in self.agents:
            return self.agents["technical"].improve_quality(draft)
        return draft
    
    def _perform_quality_assurance(self, draft, parameters):
        """Perform final quality assurance."""
        logger.info("Performing quality assurance")
        if "quality" in self.agents:
            return self.agents["quality"].ensure_quality(draft, parameters)
        return draft