"""
Multi-Agent Orchestration System
Manages and coordinates multiple AI agents for Telugu film story generation
"""
import asyncio
import time
import uuid
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict, deque
import logging

from .base_agent import BaseAgent, AgentTask, AgentResult, AgentMessage, AgentStatus
from .story_agent import StoryAgent
from .emotion_agent import EmotionAgent
from .cultural_agent import CulturalAgent
from ..core.config import settings

logger = logging.getLogger(__name__)


class WorkflowStep:
    """Represents a step in a workflow"""
    def __init__(self, step_id: str, agent_type: str, task_type: str, 
                 input_mapping: Dict[str, str], dependencies: List[str] = None):
        self.step_id = step_id
        self.agent_type = agent_type
        self.task_type = task_type
        self.input_mapping = input_mapping  # Maps workflow data to task input
        self.dependencies = dependencies or []
        self.completed = False
        self.result: Optional[AgentResult] = None


class Workflow:
    """Defines a complete workflow for story generation"""
    def __init__(self, workflow_id: str, name: str, steps: List[WorkflowStep]):
        self.workflow_id = workflow_id
        self.name = name
        self.steps = {step.step_id: step for step in steps}
        self.execution_order = self._calculate_execution_order()
        self.status = "pending"
        self.results: Dict[str, Any] = {}
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
    
    def _calculate_execution_order(self) -> List[str]:
        """Calculate the execution order based on dependencies"""
        order = []
        completed = set()
        
        while len(completed) < len(self.steps):
            for step_id, step in self.steps.items():
                if step_id in completed:
                    continue
                
                # Check if all dependencies are completed
                if all(dep in completed for dep in step.dependencies):
                    order.append(step_id)
                    completed.add(step_id)
                    break
            else:
                # Circular dependency or other issue
                remaining = set(self.steps.keys()) - completed
                logger.error(f"Cannot resolve dependencies for steps: {remaining}")
                break
        
        return order


class AgentOrchestrator:
    """Orchestrates multiple AI agents for complex story generation tasks"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_types: Dict[str, List[str]] = defaultdict(list)  # type -> agent_ids
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[str, AgentTask] = {}
        self.completed_tasks: Dict[str, AgentResult] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.active_workflows: Dict[str, Workflow] = {}
        
        # Statistics
        self.total_tasks_processed = 0
        self.total_workflows_completed = 0
        self.average_task_time = 0.0
        
        # Control flags
        self.is_running = False
        self.max_concurrent_tasks = self.config.get("max_concurrent_tasks", 10)
        
    async def start(self):
        """Start the orchestrator"""
        logger.info("Starting Agent Orchestrator")
        
        # Initialize default agents
        await self._initialize_default_agents()
        
        # Start orchestrator loop
        self.is_running = True
        asyncio.create_task(self._orchestrator_loop())
        
        logger.info(f"Agent Orchestrator started with {len(self.agents)} agents")
    
    async def stop(self):
        """Stop the orchestrator"""
        logger.info("Stopping Agent Orchestrator")
        
        self.is_running = False
        
        # Stop all agents
        for agent in self.agents.values():
            await agent.stop()
        
        logger.info("Agent Orchestrator stopped")
    
    async def _initialize_default_agents(self):
        """Initialize default set of agents"""
        try:
            # Story generation agents
            for i in range(2):
                agent_id = f"story_agent_{i}"
                agent = StoryAgent(agent_id, self.config.get("story_agent", {}))
                await self._register_agent(agent)
            
            # Emotion analysis agents
            for i in range(1):
                agent_id = f"emotion_agent_{i}"
                agent = EmotionAgent(agent_id, self.config.get("emotion_agent", {}))
                await self._register_agent(agent)
            
            # Cultural analysis agents
            for i in range(1):
                agent_id = f"cultural_agent_{i}"
                agent = CulturalAgent(agent_id, self.config.get("cultural_agent", {}))
                await self._register_agent(agent)
            
            logger.info("Default agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing default agents: {str(e)}")
    
    async def _register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        try:
            # Set result callback
            agent.set_result_callback(self._handle_agent_message)
            
            # Start the agent
            await agent.start()
            
            # Register in our tracking
            self.agents[agent.agent_id] = agent
            self.agent_types[agent.agent_type].append(agent.agent_id)
            
            logger.info(f"Registered agent {agent.agent_id} of type {agent.agent_type}")
            
        except Exception as e:
            logger.error(f"Error registering agent {agent.agent_id}: {str(e)}")
    
    async def _orchestrator_loop(self):
        """Main orchestrator loop"""
        while self.is_running:
            try:
                # Process pending tasks
                await self._process_task_queue()
                
                # Process active workflows
                await self._process_workflows()
                
                # Health check agents
                await self._health_check_agents()
                
                # Small delay
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in orchestrator loop: {str(e)}")
                await asyncio.sleep(1.0)
    
    async def _process_task_queue(self):
        """Process tasks from the queue"""
        active_count = len(self.active_tasks)
        
        while active_count < self.max_concurrent_tasks and not self.task_queue.empty():
            try:
                task = await asyncio.wait_for(self.task_queue.get(), timeout=0.1)
                
                # Find suitable agent
                agent = await self._find_suitable_agent(task)
                
                if agent:
                    # Assign task to agent
                    self.active_tasks[task.id] = task
                    asyncio.create_task(self._execute_task(agent, task))
                    active_count += 1
                else:
                    # No suitable agent available, put task back
                    await self.task_queue.put(task)
                    break
                    
            except asyncio.TimeoutError:
                break
            except Exception as e:
                logger.error(f"Error processing task queue: {str(e)}")
    
    async def _find_suitable_agent(self, task: AgentTask) -> Optional[BaseAgent]:
        """Find a suitable agent for the task"""
        # Get agents that can handle this task type
        suitable_agents = []
        
        for agent_id, agent in self.agents.items():
            if (agent.status == AgentStatus.IDLE and 
                agent.can_handle_task(task)):
                suitable_agents.append(agent)
        
        if not suitable_agents:
            return None
        
        # Select agent with least recent activity (load balancing)
        return min(suitable_agents, key=lambda a: a.last_activity)
    
    async def _execute_task(self, agent: BaseAgent, task: AgentTask):
        """Execute a task on an agent"""
        try:
            logger.info(f"Executing task {task.id} on agent {agent.agent_id}")
            
            # Execute task
            result = await agent.process_task(task)
            
            # Store result
            self.completed_tasks[task.id] = result
            
            # Remove from active tasks
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
            
            # Update statistics
            self.total_tasks_processed += 1
            self.average_task_time = (
                (self.average_task_time * (self.total_tasks_processed - 1) + result.execution_time)
                / self.total_tasks_processed
            )
            
            # Notify workflow if this task is part of one
            await self._notify_workflow_task_completion(task.id, result)
            
            logger.info(f"Task {task.id} completed by agent {agent.agent_id}")
            
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {str(e)}")
            
            # Create error result
            error_result = AgentResult(
                task_id=task.id,
                agent_id=agent.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=0.0
            )
            
            self.completed_tasks[task.id] = error_result
            
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
    
    async def _process_workflows(self):
        """Process active workflows"""
        completed_workflows = []
        
        for workflow_id, workflow in self.active_workflows.items():
            try:
                if await self._process_workflow(workflow):
                    completed_workflows.append(workflow_id)
                    
            except Exception as e:
                logger.error(f"Error processing workflow {workflow_id}: {str(e)}")
                workflow.status = "failed"
                completed_workflows.append(workflow_id)
        
        # Remove completed workflows
        for workflow_id in completed_workflows:
            workflow = self.active_workflows.pop(workflow_id)
            self.workflows[workflow_id] = workflow
            
            if workflow.status == "completed":
                self.total_workflows_completed += 1
    
    async def _process_workflow(self, workflow: Workflow) -> bool:
        """Process a single workflow, returns True if completed"""
        if workflow.status != "running":
            return False
        
        # Check if all steps are completed
        if all(step.completed for step in workflow.steps.values()):
            workflow.status = "completed"
            workflow.end_time = time.time()
            logger.info(f"Workflow {workflow.workflow_id} completed")
            return True
        
        # Execute next available steps
        for step_id in workflow.execution_order:
            step = workflow.steps[step_id]
            
            if step.completed:
                continue
            
            # Check if dependencies are met
            if not all(workflow.steps[dep].completed for dep in step.dependencies):
                continue
            
            # Create and submit task for this step
            task_input = self._map_workflow_data_to_task_input(workflow, step)
            
            task = AgentTask(
                id=f"{workflow.workflow_id}_{step_id}_{uuid.uuid4().hex[:8]}",
                task_type=step.task_type,
                input_data=task_input,
                priority=5  # Workflow tasks have higher priority
            )
            
            await self.task_queue.put(task)
            
            # Mark step as submitted (not completed yet)
            step.task_id = task.id
        
        return False
    
    def _map_workflow_data_to_task_input(self, workflow: Workflow, step: WorkflowStep) -> Dict[str, Any]:
        """Map workflow data to task input based on step configuration"""
        task_input = {}
        
        for task_key, workflow_key in step.input_mapping.items():
            if workflow_key in workflow.results:
                task_input[task_key] = workflow.results[workflow_key]
        
        return task_input
    
    async def _notify_workflow_task_completion(self, task_id: str, result: AgentResult):
        """Notify workflows when their tasks complete"""
        for workflow in self.active_workflows.values():
            for step in workflow.steps.values():
                if hasattr(step, 'task_id') and step.task_id == task_id:
                    step.completed = True
                    step.result = result
                    
                    # Store result in workflow results
                    workflow.results[step.step_id] = result.result
                    
                    logger.info(f"Workflow {workflow.workflow_id} step {step.step_id} completed")
                    break
    
    async def _health_check_agents(self):
        """Perform health checks on agents"""
        for agent_id, agent in list(self.agents.items()):
            try:
                # Check if agent is responsive
                if time.time() - agent.last_activity > 300:  # 5 minutes
                    logger.warning(f"Agent {agent_id} appears unresponsive")
                    
                    # Send ping message
                    ping_message = AgentMessage(
                        id=str(uuid.uuid4()),
                        sender_id="orchestrator",
                        receiver_id=agent_id,
                        message_type="ping",
                        content={},
                        timestamp=time.time()
                    )
                    
                    await agent.send_message(ping_message)
                    
            except Exception as e:
                logger.error(f"Error in health check for agent {agent_id}: {str(e)}")
    
    async def _handle_agent_message(self, message: AgentMessage):
        """Handle messages from agents"""
        logger.debug(f"Received message from agent {message.sender_id}: {message.message_type}")
        
        if message.message_type == "pong":
            # Agent responded to ping
            logger.debug(f"Agent {message.sender_id} is responsive")
    
    # Public API methods
    
    async def submit_task(self, task: AgentTask) -> str:
        """Submit a task for execution"""
        await self.task_queue.put(task)
        logger.info(f"Task {task.id} submitted to queue")
        return task.id
    
    async def submit_workflow(self, workflow: Workflow) -> str:
        """Submit a workflow for execution"""
        workflow.status = "running"
        workflow.start_time = time.time()
        self.active_workflows[workflow.workflow_id] = workflow
        
        logger.info(f"Workflow {workflow.workflow_id} submitted")
        return workflow.workflow_id
    
    def get_task_result(self, task_id: str) -> Optional[AgentResult]:
        """Get result of a completed task"""
        return self.completed_tasks.get(task_id)
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow"""
        workflow = (self.active_workflows.get(workflow_id) or 
                   self.workflows.get(workflow_id))
        
        if not workflow:
            return None
        
        return {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "status": workflow.status,
            "steps_completed": sum(1 for step in workflow.steps.values() if step.completed),
            "total_steps": len(workflow.steps),
            "start_time": workflow.start_time,
            "end_time": workflow.end_time,
            "results": workflow.results
        }
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_agents": len(self.agents),
            "agents_by_type": {
                agent_type: len(agent_ids) 
                for agent_type, agent_ids in self.agent_types.items()
            },
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "active_workflows": len(self.active_workflows),
            "completed_workflows": self.total_workflows_completed,
            "total_tasks_processed": self.total_tasks_processed,
            "average_task_time": self.average_task_time,
            "is_running": self.is_running
        }
    
    def get_agent_status(self, agent_id: str = None) -> Dict[str, Any]:
        """Get status of specific agent or all agents"""
        if agent_id:
            agent = self.agents.get(agent_id)
            return agent.get_status() if agent else None
        
        return {
            agent_id: agent.get_status() 
            for agent_id, agent in self.agents.items()
        }