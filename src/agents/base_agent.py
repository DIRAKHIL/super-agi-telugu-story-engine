"""
Base agent class for the AI Emotional Engine for Telugu Story Creation.
"""

from abc import ABC, abstractmethod
from loguru import logger


class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    """
    
    def __init__(self, config):
        """
        Initialize the base agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        self.config = config
        self.name = self.__class__.__name__
        logger.debug(f"Initializing agent: {self.name}")
    
    @abstractmethod
    def process(self, input_data, context=None):
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process.
            context: Optional context information.
        
        Returns:
            Processing results.
        """
        pass
    
    def _get_agent_config(self):
        """
        Get agent-specific configuration.
        
        Returns:
            dict: Agent configuration.
        """
        # For core agents
        agent_name = self.name.lower().replace("agent", "")
        if agent_name in self.config["agents"]:
            return self.config["agents"][agent_name]
        
        # For expert agents
        for expert_name, expert_config in self.config["agents"]["expert"].items():
            if expert_name in self.name.lower():
                return expert_config
        
        # Default configuration
        return {"enabled": True, "weight": 1.0}