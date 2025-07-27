"""
Base Agent for Multi-Agent Orchestration System
"""
import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class AgentMessage(BaseModel):
    """Message format for agent communication"""
    id: str
    sender_id: str
    receiver_id: Optional[str] = None  # None for broadcast
    message_type: str
    content: Any
    timestamp: float
    priority: int = 1  # 1-10, higher is more priority


class AgentTask(BaseModel):
    """Task definition for agents"""
    id: str
    task_type: str
    input_data: Any
    requirements: Dict[str, Any] = {}
    timeout: int = 300  # seconds
    priority: int = 1
    dependencies: List[str] = []  # Task IDs this task depends on


class AgentResult(BaseModel):
    """Result from agent execution"""
    task_id: str
    agent_id: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, agent_id: str, agent_type: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.result_callback: Optional[Callable] = None
        self.capabilities: List[str] = []
        self.created_at = time.time()
        self.last_activity = time.time()
        
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute a specific task"""
        pass
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent"""
        pass
    
    async def start(self):
        """Start the agent's main loop"""
        logger.info(f"Starting agent {self.agent_id} of type {self.agent_type}")
        
        if not await self.initialize():
            logger.error(f"Failed to initialize agent {self.agent_id}")
            return
        
        # Start message processing loop
        asyncio.create_task(self._message_loop())
        
        self.status = AgentStatus.IDLE
        logger.info(f"Agent {self.agent_id} started successfully")
    
    async def stop(self):
        """Stop the agent"""
        logger.info(f"Stopping agent {self.agent_id}")
        self.status = AgentStatus.IDLE
        
        # Clear message queue
        while not self.message_queue.empty():
            try:
                self.message_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
    
    async def send_message(self, message: AgentMessage):
        """Send a message to this agent"""
        await self.message_queue.put(message)
        self.last_activity = time.time()
    
    async def process_task(self, task: AgentTask) -> AgentResult:
        """Process a task with timeout and error handling"""
        if self.status != AgentStatus.IDLE:
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error="Agent is busy",
                execution_time=0.0
            )
        
        self.status = AgentStatus.WORKING
        self.current_task = task
        start_time = time.time()
        
        try:
            # Execute task with timeout
            result = await asyncio.wait_for(
                self.execute_task(task),
                timeout=task.timeout
            )
            
            self.status = AgentStatus.COMPLETED
            execution_time = time.time() - start_time
            
            logger.info(f"Agent {self.agent_id} completed task {task.id} in {execution_time:.2f}s")
            
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=result.success,
                result=result.result,
                error=result.error,
                execution_time=execution_time,
                metadata=result.metadata
            )
            
        except asyncio.TimeoutError:
            self.status = AgentStatus.TIMEOUT
            execution_time = time.time() - start_time
            
            logger.warning(f"Agent {self.agent_id} timed out on task {task.id}")
            
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=f"Task timed out after {task.timeout} seconds",
                execution_time=execution_time
            )
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            execution_time = time.time() - start_time
            
            logger.error(f"Agent {self.agent_id} failed on task {task.id}: {str(e)}")
            
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=execution_time
            )
        
        finally:
            self.current_task = None
            self.status = AgentStatus.IDLE
            self.last_activity = time.time()
    
    async def _message_loop(self):
        """Process incoming messages"""
        while True:
            try:
                # Wait for message with timeout
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=1.0
                )
                
                await self._handle_message(message)
                
            except asyncio.TimeoutError:
                # No message received, continue
                continue
            except Exception as e:
                logger.error(f"Error in message loop for agent {self.agent_id}: {str(e)}")
    
    async def _handle_message(self, message: AgentMessage):
        """Handle incoming message"""
        logger.debug(f"Agent {self.agent_id} received message: {message.message_type}")
        
        if message.message_type == "ping":
            # Respond to ping
            response = AgentMessage(
                id=str(uuid.uuid4()),
                sender_id=self.agent_id,
                receiver_id=message.sender_id,
                message_type="pong",
                content={"status": self.status.value},
                timestamp=time.time()
            )
            
            if self.result_callback:
                await self.result_callback(response)
    
    def can_handle_task(self, task: AgentTask) -> bool:
        """Check if agent can handle the given task"""
        return task.task_type in self.capabilities
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "current_task": self.current_task.id if self.current_task else None,
            "created_at": self.created_at,
            "last_activity": self.last_activity,
            "uptime": time.time() - self.created_at
        }
    
    def set_result_callback(self, callback: Callable):
        """Set callback for sending results/messages"""
        self.result_callback = callback