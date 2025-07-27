"""
Story generation API endpoints
"""
import uuid
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from pydantic import BaseModel, Field
import logging

# from ....agents.base_agent import AgentTask
# from ....agents.orchestrator import AgentOrchestrator
try:
    from models.story_generator_simple import telugu_story_generator, StoryRequest
except ImportError:
    from backend.models.story_generator_simple import telugu_story_generator, StoryRequest

logger = logging.getLogger(__name__)

router = APIRouter()


class StoryGenerationRequest(BaseModel):
    """Request model for story generation"""
    prompt: str = Field(..., description="Story prompt or theme")
    genre: Optional[str] = Field("drama", description="Story genre")
    characters: Optional[List[str]] = Field([], description="Character names")
    setting: Optional[str] = Field("modern", description="Story setting")
    theme: Optional[str] = Field("family", description="Story theme")
    max_length: Optional[int] = Field(2000, description="Maximum story length")
    temperature: Optional[float] = Field(0.8, description="Generation temperature")
    top_p: Optional[float] = Field(0.9, description="Top-p sampling")
    top_k: Optional[int] = Field(50, description="Top-k sampling")


class StoryEnhancementRequest(BaseModel):
    """Request model for story enhancement"""
    story: str = Field(..., description="Original story text")
    enhancement_type: str = Field("general", description="Type of enhancement")
    genre: Optional[str] = Field("drama", description="Story genre")
    max_length: Optional[int] = Field(1500, description="Maximum enhanced length")


class CharacterDevelopmentRequest(BaseModel):
    """Request model for character development"""
    characters: List[str] = Field(..., description="Character names")
    context: Optional[str] = Field("", description="Story context")


class DialogueCreationRequest(BaseModel):
    """Request model for dialogue creation"""
    scene: str = Field(..., description="Scene description")
    characters: List[str] = Field(..., description="Characters in scene")
    emotion: Optional[str] = Field("neutral", description="Scene emotion")


class NarrativeStructureRequest(BaseModel):
    """Request model for narrative structuring"""
    story: str = Field(..., description="Raw story text")
    structure: str = Field("three_act", description="Narrative structure type")


class StoryResponse(BaseModel):
    """Response model for story operations"""
    success: bool
    task_id: str
    message: str
    data: Optional[Dict[str, Any]] = None


def get_orchestrator(request: Request) -> AgentOrchestrator:
    """Get orchestrator from app state"""
    if not hasattr(request.app.state, 'orchestrator'):
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    return request.app.state.orchestrator


@router.post("/generate", response_model=StoryResponse)
async def generate_story(
    request: StoryGenerationRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Generate a Telugu story based on the provided prompt and parameters"""
    try:
        # Create task for story generation
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="generate_story",
            input_data={
                "prompt": request.prompt,
                "genre": request.genre,
                "characters": request.characters,
                "setting": request.setting,
                "theme": request.theme,
                "max_length": request.max_length,
                "temperature": request.temperature,
                "top_p": request.top_p,
                "top_k": request.top_k
            },
            priority=3
        )
        
        # Submit task to orchestrator
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Story generation task {task_id} submitted")
        
        return StoryResponse(
            success=True,
            task_id=task_id,
            message="Story generation task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in story generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enhance", response_model=StoryResponse)
async def enhance_story(
    request: StoryEnhancementRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Enhance an existing story with additional elements"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="enhance_plot",
            input_data={
                "plot": request.story,
                "enhancement_type": request.enhancement_type,
                "genre": request.genre,
                "max_length": request.max_length
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Story enhancement task {task_id} submitted")
        
        return StoryResponse(
            success=True,
            task_id=task_id,
            message="Story enhancement task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in story enhancement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/develop-characters", response_model=StoryResponse)
async def develop_characters(
    request: CharacterDevelopmentRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Develop detailed character profiles and backgrounds"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="develop_characters",
            input_data={
                "characters": request.characters,
                "context": request.context
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Character development task {task_id} submitted")
        
        return StoryResponse(
            success=True,
            task_id=task_id,
            message="Character development task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in character development: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-dialogue", response_model=StoryResponse)
async def create_dialogue(
    request: DialogueCreationRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Create dialogue for specific scenes"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="create_dialogue",
            input_data={
                "scene": request.scene,
                "characters": request.characters,
                "emotion": request.emotion
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Dialogue creation task {task_id} submitted")
        
        return StoryResponse(
            success=True,
            task_id=task_id,
            message="Dialogue creation task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in dialogue creation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/structure-narrative", response_model=StoryResponse)
async def structure_narrative(
    request: NarrativeStructureRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Structure narrative with proper story arc"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="structure_narrative",
            input_data={
                "story": request.story,
                "structure": request.structure
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Narrative structuring task {task_id} submitted")
        
        return StoryResponse(
            success=True,
            task_id=task_id,
            message="Narrative structuring task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in narrative structuring: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task/{task_id}")
async def get_task_result(
    task_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get the result of a story generation task"""
    try:
        result = orchestrator.get_task_result(task_id)
        
        if result is None:
            # Check if task is still active
            orchestrator_stats = orchestrator.get_orchestrator_stats()
            if task_id in orchestrator.active_tasks:
                return {
                    "status": "processing",
                    "task_id": task_id,
                    "message": "Task is still being processed"
                }
            else:
                raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "status": "completed" if result.success else "failed",
            "task_id": task_id,
            "success": result.success,
            "result": result.result,
            "error": result.error,
            "execution_time": result.execution_time,
            "agent_id": result.agent_id,
            "metadata": result.metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task result: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genres")
async def get_supported_genres():
    """Get list of supported story genres"""
    return {
        "genres": [
            {"id": "drama", "name": "డ్రామా", "description": "భావోద్వేగ కథలు"},
            {"id": "comedy", "name": "కామెడీ", "description": "హాస్య కథలు"},
            {"id": "action", "name": "యాక్షన్", "description": "సాహస కథలు"},
            {"id": "romance", "name": "రొమాన్స్", "description": "ప్రేమ కథలు"},
            {"id": "thriller", "name": "థ్రిల్లర్", "description": "ఉత్కంఠ కథలు"},
            {"id": "family", "name": "కుటుంబ", "description": "కుటుంబ కథలు"},
            {"id": "social", "name": "సామాజిక", "description": "సామాజిక కథలు"},
            {"id": "historical", "name": "చారిత్రక", "description": "చారిత్రక కథలు"}
        ]
    }


@router.get("/themes")
async def get_supported_themes():
    """Get list of supported story themes"""
    return {
        "themes": [
            {"id": "family", "name": "కుటుంబం", "description": "కుటుంబ బంధాలు మరియు విలువలు"},
            {"id": "love", "name": "ప్రేమ", "description": "ప్రేమ మరియు రొమాన్స్"},
            {"id": "friendship", "name": "స్నేహం", "description": "స్నేహ బంధాలు"},
            {"id": "justice", "name": "న్యాయం", "description": "న్యాయం మరియు ధర్మం"},
            {"id": "tradition", "name": "సంప్రదాయం", "description": "సాంప్రదాయిక విలువలు"},
            {"id": "modern", "name": "ఆధునిక", "description": "ఆధునిక జీవన శైలి"},
            {"id": "sacrifice", "name": "త్యాగం", "description": "త్యాగం మరియు సేవ"},
            {"id": "success", "name": "విజయం", "description": "విజయం మరియు సాఫల్యం"}
        ]
    }


@router.get("/settings")
async def get_supported_settings():
    """Get list of supported story settings"""
    return {
        "settings": [
            {"id": "village", "name": "గ్రామం", "description": "గ్రామీణ నేపథ్యం"},
            {"id": "city", "name": "నగరం", "description": "పట్టణ నేపథ్యం"},
            {"id": "modern", "name": "ఆధునిక", "description": "ఆధునిక నేపథ్యం"},
            {"id": "traditional", "name": "సాంప్రదాయిక", "description": "సాంప్రదాయిక నేపథ్యం"},
            {"id": "historical", "name": "చారిత్రక", "description": "చారిత్రక నేపథ్యం"},
            {"id": "contemporary", "name": "సమకాలీన", "description": "సమకాలీన నేపథ్యం"}
        ]
    }


@router.get("/statistics")
async def get_story_statistics(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get story generation statistics"""
    try:
        orchestrator_stats = orchestrator.get_orchestrator_stats()
        
        # Get story agent statistics
        story_agents = []
        for agent_id, agent in orchestrator.agents.items():
            if agent.agent_type == "story_generator":
                agent_stats = agent.get_status()
                if hasattr(agent, 'get_generation_stats'):
                    agent_stats.update(agent.get_generation_stats())
                story_agents.append(agent_stats)
        
        return {
            "orchestrator_stats": orchestrator_stats,
            "story_agents": story_agents,
            "total_story_agents": len(story_agents)
        }
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))