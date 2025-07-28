"""
Base Agent Class for Telugu Story Engine
Foundation for all real AI agents - NO MOCKS, NO FALLBACKS
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json
from enum import Enum

from ..core.model_manager import get_model_manager
from ..core.config import get_config

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    PROCESSING = "processing"
    COLLABORATING = "collaborating"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentResponse:
    """Response from an agent"""
    agent_id: str
    agent_type: str
    content: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    status: AgentStatus = AgentStatus.COMPLETED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "content": self.content,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "processing_time": self.processing_time,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value
        }

@dataclass
class AgentMemory:
    """Agent memory for context and collaboration"""
    agent_id: str
    conversations: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    collaboration_history: List[Dict[str, Any]] = field(default_factory=list)
    learned_patterns: Dict[str, Any] = field(default_factory=dict)
    
    def add_conversation(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a conversation entry"""
        self.conversations.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })
    
    def update_context(self, key: str, value: Any):
        """Update context information"""
        self.context[key] = value
    
    def add_collaboration(self, other_agent_id: str, interaction_type: str, data: Dict[str, Any]):
        """Record collaboration with another agent"""
        self.collaboration_history.append({
            "other_agent_id": other_agent_id,
            "interaction_type": interaction_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

class BaseAgent(ABC):
    """
    Base class for all Telugu Story Engine agents
    Provides common functionality for real AI processing
    """
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_type = self.__class__.__name__
        self.config = config or {}
        self.global_config = get_config()
        self.model_manager = get_model_manager()
        self.memory = AgentMemory(agent_id=self.agent_id)
        self.status = AgentStatus.IDLE
        
        # Agent-specific configuration
        self.enabled = self.config.get("enabled", True)
        self.weight = self.config.get("weight", 1.0)
        self.relevance_threshold = self.config.get("relevance_threshold", 0.3)
        self.max_iterations = self.config.get("max_iterations", 3)
        
        logger.info(f"Initialized {self.agent_type} with ID: {self.agent_id}")
    
    @abstractmethod
    async def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process input data and return agent response
        Must be implemented by all agents - NO MOCKS ALLOWED
        """
        pass
    
    @abstractmethod
    def get_relevance_score(self, input_data: Dict[str, Any]) -> float:
        """
        Calculate how relevant this agent is for the given input
        Returns score between 0.0 and 1.0
        """
        pass
    
    async def collaborate(
        self,
        other_agents: List['BaseAgent'],
        shared_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Collaborate with other agents
        Real multi-agent interaction - NO MOCKS
        """
        self.status = AgentStatus.COLLABORATING
        collaboration_results = {}
        
        try:
            for agent in other_agents:
                if agent.agent_id != self.agent_id and agent.enabled:
                    # Calculate collaboration relevance
                    relevance = await self._calculate_collaboration_relevance(agent, shared_context)
                    
                    if relevance > self.relevance_threshold:
                        # Perform actual collaboration
                        collab_result = await self._collaborate_with_agent(agent, shared_context)
                        collaboration_results[agent.agent_id] = collab_result
                        
                        # Record collaboration
                        self.memory.add_collaboration(
                            agent.agent_id,
                            "collaboration",
                            collab_result
                        )
            
            return collaboration_results
            
        except Exception as e:
            logger.error(f"Collaboration error in {self.agent_type}: {e}")
            self.status = AgentStatus.ERROR
            raise
        finally:
            self.status = AgentStatus.IDLE
    
    async def _calculate_collaboration_relevance(
        self,
        other_agent: 'BaseAgent',
        context: Dict[str, Any]
    ) -> float:
        """Calculate relevance of collaborating with another agent"""
        # Base implementation - can be overridden by specific agents
        base_relevance = 0.5
        
        # Increase relevance based on complementary capabilities
        if self._has_complementary_capabilities(other_agent):
            base_relevance += 0.3
        
        # Adjust based on context requirements
        if self._context_requires_collaboration(other_agent, context):
            base_relevance += 0.2
        
        return min(base_relevance, 1.0)
    
    def _has_complementary_capabilities(self, other_agent: 'BaseAgent') -> bool:
        """Check if another agent has complementary capabilities"""
        # Define complementary agent pairs
        complementary_pairs = {
            "StoryStructureAgent": ["EmotionalIntelligenceAgent", "CharacterDevelopmentAgent"],
            "EmotionalIntelligenceAgent": ["StoryStructureAgent", "CulturalAdaptationAgent"],
            "CulturalAdaptationAgent": ["EmotionalIntelligenceAgent", "CharacterDevelopmentAgent"],
            "CharacterDevelopmentAgent": ["StoryStructureAgent", "CharacterPsychologistAgent"]
        }
        
        my_type = self.agent_type
        other_type = other_agent.agent_type
        
        return other_type in complementary_pairs.get(my_type, [])
    
    def _context_requires_collaboration(
        self,
        other_agent: 'BaseAgent',
        context: Dict[str, Any]
    ) -> bool:
        """Check if context requires collaboration with specific agent"""
        # Check for specific requirements in context
        required_capabilities = context.get("required_capabilities", [])
        other_capabilities = other_agent.get_capabilities()
        
        return any(cap in other_capabilities for cap in required_capabilities)
    
    async def _collaborate_with_agent(
        self,
        other_agent: 'BaseAgent',
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform actual collaboration with another agent"""
        # Create collaboration prompt
        collaboration_prompt = self._create_collaboration_prompt(other_agent, context)
        
        # Get responses from both agents
        my_response = await self.process(collaboration_prompt, context)
        other_response = await other_agent.process(collaboration_prompt, context)
        
        # Synthesize responses
        synthesis = await self._synthesize_responses(my_response, other_response, context)
        
        return {
            "my_response": my_response.to_dict(),
            "other_response": other_response.to_dict(),
            "synthesis": synthesis,
            "collaboration_score": (my_response.confidence + other_response.confidence) / 2
        }
    
    def _create_collaboration_prompt(
        self,
        other_agent: 'BaseAgent',
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a prompt for collaboration"""
        return {
            "type": "collaboration",
            "collaborating_with": other_agent.agent_type,
            "context": context,
            "my_capabilities": self.get_capabilities(),
            "other_capabilities": other_agent.get_capabilities()
        }
    
    async def _synthesize_responses(
        self,
        my_response: AgentResponse,
        other_response: AgentResponse,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize responses from collaboration"""
        # Weight responses based on confidence and agent weights
        my_weight = self.weight * my_response.confidence
        other_weight = other_response.confidence  # Assuming other agent has weight 1.0
        
        total_weight = my_weight + other_weight
        
        if total_weight == 0:
            return {"synthesis": "No valid responses to synthesize"}
        
        # Create weighted synthesis
        synthesis = {
            "combined_content": self._combine_content(my_response.content, other_response.content),
            "confidence": (my_weight + other_weight) / 2,
            "contributing_agents": [self.agent_id, other_response.agent_id],
            "synthesis_method": "weighted_combination"
        }
        
        return synthesis
    
    def _combine_content(self, my_content: str, other_content: str) -> str:
        """Combine content from two agents"""
        # Base implementation - can be overridden
        return f"{my_content}\n\n[Collaboration with {self.agent_type}]\n{other_content}"
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        # Base capabilities - should be overridden by specific agents
        return ["text_processing", "context_understanding"]
    
    def update_memory(self, key: str, value: Any):
        """Update agent memory"""
        self.memory.update_context(key, value)
    
    def get_memory_context(self) -> Dict[str, Any]:
        """Get current memory context"""
        return self.memory.context
    
    def add_conversation(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add conversation to memory"""
        self.memory.add_conversation(role, content, metadata)
    
    async def learn_from_feedback(self, feedback: Dict[str, Any]):
        """Learn from feedback to improve future performance"""
        # Store feedback in learned patterns
        feedback_id = str(uuid.uuid4())
        self.memory.learned_patterns[feedback_id] = {
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
            "agent_state": self.get_state_snapshot()
        }
        
        # Apply learning (can be overridden by specific agents)
        await self._apply_learning(feedback)
    
    async def _apply_learning(self, feedback: Dict[str, Any]):
        """Apply learning from feedback - can be overridden"""
        # Base implementation: adjust confidence based on feedback
        if "quality_score" in feedback:
            quality_score = feedback["quality_score"]
            if quality_score > 0.8:
                self.weight = min(self.weight * 1.1, 2.0)  # Increase weight
            elif quality_score < 0.5:
                self.weight = max(self.weight * 0.9, 0.1)  # Decrease weight
    
    def get_state_snapshot(self) -> Dict[str, Any]:
        """Get current agent state snapshot"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "weight": self.weight,
            "enabled": self.enabled,
            "memory_size": len(self.memory.conversations),
            "collaboration_count": len(self.memory.collaboration_history),
            "learned_patterns_count": len(self.memory.learned_patterns)
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        # Calculate metrics from memory
        total_conversations = len(self.memory.conversations)
        total_collaborations = len(self.memory.collaboration_history)
        
        # Calculate average processing time (if available)
        processing_times = []
        for conv in self.memory.conversations:
            if "processing_time" in conv.get("metadata", {}):
                processing_times.append(conv["metadata"]["processing_time"])
        
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        return {
            "total_conversations": total_conversations,
            "total_collaborations": total_collaborations,
            "average_processing_time": avg_processing_time,
            "current_weight": self.weight,
            "learned_patterns": len(self.memory.learned_patterns),
            "status": self.status.value
        }
    
    async def reset(self):
        """Reset agent state"""
        self.memory = AgentMemory(agent_id=self.agent_id)
        self.status = AgentStatus.IDLE
        logger.info(f"Reset agent {self.agent_type} ({self.agent_id})")
    
    def __str__(self) -> str:
        return f"{self.agent_type}({self.agent_id})"
    
    def __repr__(self) -> str:
        return f"{self.agent_type}(id={self.agent_id}, weight={self.weight}, enabled={self.enabled})"