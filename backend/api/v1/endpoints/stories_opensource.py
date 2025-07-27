"""
Open Source AI-powered story generation API endpoints
"""
import uuid
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import logging

try:
    from models.story_generator_opensource import telugu_story_generator_opensource, StoryRequest
except ImportError:
    from backend.models.story_generator_opensource import telugu_story_generator_opensource, StoryRequest

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


class StoryResponse(BaseModel):
    """Response model for story generation"""
    success: bool
    task_id: Optional[str] = None
    message: str
    story: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# In-memory task storage
active_tasks = {}
completed_tasks = {}


@router.post("/generate", response_model=StoryResponse)
async def generate_story(request: StoryGenerationRequest, background_tasks: BackgroundTasks):
    """Generate a Telugu story based on the provided parameters using Open Source AI"""
    try:
        task_id = str(uuid.uuid4())
        
        # Create story request
        story_request = StoryRequest(
            prompt=request.prompt,
            genre=request.genre,
            characters=request.characters,
            setting=request.setting,
            theme=request.theme,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k
        )
        
        # Add to active tasks
        active_tasks[task_id] = {
            "status": "processing",
            "request": story_request
        }
        
        # Start background task
        background_tasks.add_task(process_story_generation, task_id, story_request)
        
        logger.info(f"Open Source AI story generation task {task_id} submitted")
        
        return StoryResponse(
            success=True,
            task_id=task_id,
            message="Story generation task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in Open Source AI story generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_story_generation(task_id: str, request: StoryRequest):
    """Background task to process Open Source AI story generation"""
    try:
        # Generate story using Open Source AI
        result = await telugu_story_generator_opensource.generate_story(request)
        
        # Move from active to completed
        if task_id in active_tasks:
            del active_tasks[task_id]
        
        completed_tasks[task_id] = {
            "status": "completed",
            "success": True,
            "result": result,
            "error": None
        }
        
        logger.info(f"Open Source AI story generation task {task_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error processing Open Source AI story generation task {task_id}: {str(e)}")
        
        # Move from active to completed with error
        if task_id in active_tasks:
            del active_tasks[task_id]
        
        completed_tasks[task_id] = {
            "status": "failed",
            "success": False,
            "result": None,
            "error": str(e)
        }


@router.get("/task/{task_id}")
async def get_task_result(task_id: str):
    """Get the result of a story generation task"""
    try:
        # Check if task is still active
        if task_id in active_tasks:
            return {
                "status": "processing",
                "task_id": task_id,
                "message": "Task is still being processed"
            }
        
        # Check if task is completed
        if task_id in completed_tasks:
            result = completed_tasks[task_id]
            return {
                "status": result["status"],
                "task_id": task_id,
                "success": result["success"],
                "result": result["result"],
                "error": result["error"]
            }
        
        # Task not found
        raise HTTPException(status_code=404, detail="Task not found")
        
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
async def get_story_statistics():
    """Get story generation statistics"""
    return {
        "total_stories_generated": len(completed_tasks),
        "active_tasks": len(active_tasks),
        "completed_tasks": len([t for t in completed_tasks.values() if t["success"]]),
        "failed_tasks": len([t for t in completed_tasks.values() if not t["success"]]),
        "success_rate": (
            len([t for t in completed_tasks.values() if t["success"]]) / len(completed_tasks) * 100
            if completed_tasks else 0
        ),
        "ai_powered": True,
        "model": telugu_story_generator_opensource.model_name
    }