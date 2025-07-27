"""
Workflow management API endpoints
"""
import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
import logging

from ....agents.orchestrator import AgentOrchestrator, Workflow, WorkflowStep

logger = logging.getLogger(__name__)

router = APIRouter()


class WorkflowStepRequest(BaseModel):
    """Request model for workflow step"""
    step_id: str = Field(..., description="Step identifier")
    agent_type: str = Field(..., description="Agent type for this step")
    task_type: str = Field(..., description="Task type to execute")
    input_mapping: Dict[str, str] = Field(..., description="Input data mapping")
    dependencies: List[str] = Field([], description="Step dependencies")


class WorkflowCreationRequest(BaseModel):
    """Request model for workflow creation"""
    name: str = Field(..., description="Workflow name")
    steps: List[WorkflowStepRequest] = Field(..., description="Workflow steps")
    initial_data: Dict[str, Any] = Field({}, description="Initial workflow data")


class CompleteStoryWorkflowRequest(BaseModel):
    """Request model for complete story generation workflow"""
    prompt: str = Field(..., description="Story prompt")
    genre: str = Field("drama", description="Story genre")
    characters: List[str] = Field([], description="Character names")
    setting: str = Field("modern", description="Story setting")
    theme: str = Field("family", description="Story theme")
    include_emotion_analysis: bool = Field(True, description="Include emotion analysis")
    include_cultural_validation: bool = Field(True, description="Include cultural validation")


class WorkflowResponse(BaseModel):
    """Response model for workflow operations"""
    success: bool
    workflow_id: str
    message: str
    data: Optional[Dict[str, Any]] = None


def get_orchestrator(request: Request) -> AgentOrchestrator:
    """Get orchestrator from app state"""
    if not hasattr(request.app.state, 'orchestrator'):
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    return request.app.state.orchestrator


@router.post("/create", response_model=WorkflowResponse)
async def create_workflow(
    request: WorkflowCreationRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Create a custom workflow"""
    try:
        # Convert request steps to WorkflowStep objects
        workflow_steps = []
        for step_req in request.steps:
            step = WorkflowStep(
                step_id=step_req.step_id,
                agent_type=step_req.agent_type,
                task_type=step_req.task_type,
                input_mapping=step_req.input_mapping,
                dependencies=step_req.dependencies
            )
            workflow_steps.append(step)
        
        # Create workflow
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(
            workflow_id=workflow_id,
            name=request.name,
            steps=workflow_steps
        )
        
        # Set initial data
        workflow.results.update(request.initial_data)
        
        # Submit workflow
        submitted_id = await orchestrator.submit_workflow(workflow)
        
        logger.info(f"Custom workflow {submitted_id} created and submitted")
        
        return WorkflowResponse(
            success=True,
            workflow_id=submitted_id,
            message="Custom workflow created and submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete-story", response_model=WorkflowResponse)
async def create_complete_story_workflow(
    request: CompleteStoryWorkflowRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Create a complete story generation workflow with all analysis"""
    try:
        # Define workflow steps
        steps = []
        
        # Step 1: Generate initial story
        steps.append(WorkflowStep(
            step_id="generate_story",
            agent_type="story_generator",
            task_type="generate_story",
            input_mapping={
                "prompt": "prompt",
                "genre": "genre",
                "characters": "characters",
                "setting": "setting",
                "theme": "theme"
            },
            dependencies=[]
        ))
        
        # Step 2: Develop characters (if characters provided)
        if request.characters:
            steps.append(WorkflowStep(
                step_id="develop_characters",
                agent_type="story_generator",
                task_type="develop_characters",
                input_mapping={
                    "characters": "characters",
                    "context": "generate_story"
                },
                dependencies=["generate_story"]
            ))
        
        # Step 3: Emotion analysis (if requested)
        if request.include_emotion_analysis:
            steps.append(WorkflowStep(
                step_id="analyze_emotions",
                agent_type="emotion_analyzer",
                task_type="analyze_emotions",
                input_mapping={
                    "text": "generate_story"
                },
                dependencies=["generate_story"]
            ))
            
            steps.append(WorkflowStep(
                step_id="emotional_arc",
                agent_type="emotion_analyzer",
                task_type="emotional_arc_analysis",
                input_mapping={
                    "story": "generate_story"
                },
                dependencies=["generate_story"]
            ))
        
        # Step 4: Cultural validation (if requested)
        if request.include_cultural_validation:
            steps.append(WorkflowStep(
                step_id="cultural_validation",
                agent_type="cultural_analyzer",
                task_type="cultural_validation",
                input_mapping={
                    "text": "generate_story",
                    "context": "general"
                },
                dependencies=["generate_story"]
            ))
            
            steps.append(WorkflowStep(
                step_id="family_dynamics",
                agent_type="cultural_analyzer",
                task_type="family_dynamics_analysis",
                input_mapping={
                    "text": "generate_story"
                },
                dependencies=["generate_story"]
            ))
        
        # Step 5: Enhance story based on analysis
        enhancement_dependencies = ["generate_story"]
        if request.include_emotion_analysis:
            enhancement_dependencies.append("analyze_emotions")
        if request.include_cultural_validation:
            enhancement_dependencies.append("cultural_validation")
        
        steps.append(WorkflowStep(
            step_id="enhance_story",
            agent_type="story_generator",
            task_type="enhance_plot",
            input_mapping={
                "plot": "generate_story",
                "enhancement_type": "general",
                "genre": "genre"
            },
            dependencies=enhancement_dependencies
        ))
        
        # Create workflow
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(
            workflow_id=workflow_id,
            name=f"Complete Story: {request.prompt[:50]}...",
            steps=steps
        )
        
        # Set initial data
        workflow.results.update({
            "prompt": request.prompt,
            "genre": request.genre,
            "characters": request.characters,
            "setting": request.setting,
            "theme": request.theme
        })
        
        # Submit workflow
        submitted_id = await orchestrator.submit_workflow(workflow)
        
        logger.info(f"Complete story workflow {submitted_id} created and submitted")
        
        return WorkflowResponse(
            success=True,
            workflow_id=submitted_id,
            message="Complete story workflow created and submitted successfully",
            data={
                "steps_count": len(steps),
                "includes_emotion_analysis": request.include_emotion_analysis,
                "includes_cultural_validation": request.include_cultural_validation
            }
        )
        
    except Exception as e:
        logger.error(f"Error creating complete story workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{workflow_id}")
async def get_workflow_status(
    workflow_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get status of a specific workflow"""
    try:
        status = orchestrator.get_workflow_status(workflow_id)
        if status is None:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active")
async def get_active_workflows(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get all active workflows"""
    try:
        active_workflows = []
        for workflow_id, workflow in orchestrator.active_workflows.items():
            status = orchestrator.get_workflow_status(workflow_id)
            if status:
                active_workflows.append(status)
        
        return {
            "active_workflows": active_workflows,
            "total_active": len(active_workflows)
        }
        
    except Exception as e:
        logger.error(f"Error getting active workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/completed")
async def get_completed_workflows(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get all completed workflows"""
    try:
        completed_workflows = []
        for workflow_id, workflow in orchestrator.workflows.items():
            if workflow.status in ["completed", "failed"]:
                status = orchestrator.get_workflow_status(workflow_id)
                if status:
                    completed_workflows.append(status)
        
        return {
            "completed_workflows": completed_workflows,
            "total_completed": len(completed_workflows)
        }
        
    except Exception as e:
        logger.error(f"Error getting completed workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_workflow_templates():
    """Get predefined workflow templates"""
    return {
        "templates": [
            {
                "id": "complete_story",
                "name": "Complete Story Generation",
                "description": "Generate story with full analysis and enhancement",
                "steps": [
                    "Story Generation",
                    "Character Development",
                    "Emotion Analysis",
                    "Cultural Validation",
                    "Story Enhancement"
                ],
                "estimated_time": "5-10 minutes"
            },
            {
                "id": "story_analysis",
                "name": "Story Analysis Only",
                "description": "Analyze existing story for emotions and cultural elements",
                "steps": [
                    "Emotion Analysis",
                    "Emotional Arc Analysis",
                    "Cultural Validation",
                    "Family Dynamics Analysis"
                ],
                "estimated_time": "2-5 minutes"
            },
            {
                "id": "character_focused",
                "name": "Character-Focused Story",
                "description": "Generate story with detailed character development",
                "steps": [
                    "Story Generation",
                    "Character Development",
                    "Character Emotion Profiling",
                    "Dialogue Creation"
                ],
                "estimated_time": "3-7 minutes"
            },
            {
                "id": "cultural_authentic",
                "name": "Culturally Authentic Story",
                "description": "Generate story with strong cultural validation",
                "steps": [
                    "Story Generation",
                    "Cultural Validation",
                    "Tradition Analysis",
                    "Language Authenticity Check",
                    "Story Enhancement"
                ],
                "estimated_time": "4-8 minutes"
            }
        ]
    }


@router.get("/statistics")
async def get_workflow_statistics(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get workflow execution statistics"""
    try:
        orchestrator_stats = orchestrator.get_orchestrator_stats()
        
        # Calculate workflow-specific statistics
        total_workflows = len(orchestrator.workflows) + len(orchestrator.active_workflows)
        completed_workflows = len([w for w in orchestrator.workflows.values() if w.status == "completed"])
        failed_workflows = len([w for w in orchestrator.workflows.values() if w.status == "failed"])
        
        # Calculate average workflow completion time
        completed_workflow_times = []
        for workflow in orchestrator.workflows.values():
            if workflow.status == "completed" and workflow.start_time and workflow.end_time:
                completion_time = workflow.end_time - workflow.start_time
                completed_workflow_times.append(completion_time)
        
        average_completion_time = (
            sum(completed_workflow_times) / len(completed_workflow_times)
            if completed_workflow_times else 0.0
        )
        
        return {
            "orchestrator_stats": orchestrator_stats,
            "workflow_stats": {
                "total_workflows": total_workflows,
                "active_workflows": len(orchestrator.active_workflows),
                "completed_workflows": completed_workflows,
                "failed_workflows": failed_workflows,
                "success_rate": completed_workflows / total_workflows if total_workflows > 0 else 0.0,
                "average_completion_time": average_completion_time
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting workflow statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))