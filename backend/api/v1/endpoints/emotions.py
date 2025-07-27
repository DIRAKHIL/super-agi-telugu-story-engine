"""
Emotion analysis API endpoints
"""
import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
import logging

# from ....agents.base_agent import AgentTask
# from ....agents.orchestrator import AgentOrchestrator
try:
    from models.emotion_analyzer_simple import telugu_emotion_analyzer
except ImportError:
    from backend.models.emotion_analyzer_simple import telugu_emotion_analyzer

logger = logging.getLogger(__name__)

router = APIRouter()


class EmotionAnalysisRequest(BaseModel):
    """Request model for emotion analysis"""
    text: str = Field(..., description="Text to analyze")
    analyze_sentiment: bool = Field(True, description="Include sentiment analysis")
    analyze_emotions: bool = Field(True, description="Include emotion analysis")
    context: Optional[str] = Field(None, description="Context for analysis")


class EmotionalArcRequest(BaseModel):
    """Request model for emotional arc analysis"""
    story: str = Field(..., description="Complete story text")


class CulturalEmotionMappingRequest(BaseModel):
    """Request model for cultural emotion mapping"""
    emotions: List[Dict[str, Any]] = Field(..., description="Emotions to map")
    context: str = Field("general", description="Cultural context")


class CharacterEmotionProfilingRequest(BaseModel):
    """Request model for character emotion profiling"""
    character_dialogues: Dict[str, List[str]] = Field(..., description="Character dialogues")


class EmotionResponse(BaseModel):
    """Response model for emotion operations"""
    success: bool
    task_id: str
    message: str
    data: Optional[Dict[str, Any]] = None


def get_orchestrator(request: Request) -> AgentOrchestrator:
    """Get orchestrator from app state"""
    if not hasattr(request.app.state, 'orchestrator'):
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    return request.app.state.orchestrator


@router.post("/analyze", response_model=EmotionResponse)
async def analyze_emotions(
    request: EmotionAnalysisRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze emotions and sentiment in Telugu text"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="analyze_emotions",
            input_data={
                "text": request.text,
                "analyze_sentiment": request.analyze_sentiment,
                "analyze_emotions": request.analyze_emotions,
                "context": request.context
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Emotion analysis task {task_id} submitted")
        
        return EmotionResponse(
            success=True,
            task_id=task_id,
            message="Emotion analysis task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in emotion analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sentiment", response_model=EmotionResponse)
async def analyze_sentiment(
    request: EmotionAnalysisRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze sentiment only in Telugu text"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="analyze_sentiment",
            input_data={
                "text": request.text,
                "context": request.context
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Sentiment analysis task {task_id} submitted")
        
        return EmotionResponse(
            success=True,
            task_id=task_id,
            message="Sentiment analysis task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/emotional-arc", response_model=EmotionResponse)
async def analyze_emotional_arc(
    request: EmotionalArcRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze emotional arc of a complete story"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="emotional_arc_analysis",
            input_data={
                "story": request.story
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Emotional arc analysis task {task_id} submitted")
        
        return EmotionResponse(
            success=True,
            task_id=task_id,
            message="Emotional arc analysis task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in emotional arc analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cultural-mapping", response_model=EmotionResponse)
async def map_cultural_emotions(
    request: CulturalEmotionMappingRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Map emotions to Telugu cultural contexts"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="cultural_emotion_mapping",
            input_data={
                "emotions": request.emotions,
                "context": request.context
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Cultural emotion mapping task {task_id} submitted")
        
        return EmotionResponse(
            success=True,
            task_id=task_id,
            message="Cultural emotion mapping task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in cultural emotion mapping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/character-profiling", response_model=EmotionResponse)
async def profile_character_emotions(
    request: CharacterEmotionProfilingRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Create emotional profiles for characters"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="character_emotion_profiling",
            input_data={
                "character_dialogues": request.character_dialogues
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Character emotion profiling task {task_id} submitted")
        
        return EmotionResponse(
            success=True,
            task_id=task_id,
            message="Character emotion profiling task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in character emotion profiling: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task/{task_id}")
async def get_emotion_task_result(
    task_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get the result of an emotion analysis task"""
    try:
        result = orchestrator.get_task_result(task_id)
        
        if result is None:
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
        logger.error(f"Error getting emotion task result: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-emotions")
async def get_supported_emotions():
    """Get list of supported emotions in Telugu"""
    return {
        "emotions": [
            {"telugu": "ఆనందం", "english": "joy", "category": "positive"},
            {"telugu": "దుఃఖం", "english": "sadness", "category": "negative"},
            {"telugu": "కోపం", "english": "anger", "category": "negative"},
            {"telugu": "భయం", "english": "fear", "category": "negative"},
            {"telugu": "ఆశ్చర్యం", "english": "surprise", "category": "neutral"},
            {"telugu": "అసహ్యం", "english": "disgust", "category": "negative"},
            {"telugu": "ప్రేమ", "english": "love", "category": "positive"},
            {"telugu": "గర్వం", "english": "pride", "category": "positive"},
            {"telugu": "సిగ్గు", "english": "shame", "category": "negative"},
            {"telugu": "అపరాధభావన", "english": "guilt", "category": "negative"},
            {"telugu": "కృతజ్ఞత", "english": "gratitude", "category": "positive"},
            {"telugu": "ఆశ", "english": "hope", "category": "positive"},
            {"telugu": "నిరాశ", "english": "despair", "category": "negative"},
            {"telugu": "ఉత్సాహం", "english": "excitement", "category": "positive"},
            {"telugu": "శాంతి", "english": "peace", "category": "positive"}
        ]
    }


@router.get("/cultural-contexts")
async def get_cultural_emotion_contexts():
    """Get cultural contexts for emotion analysis"""
    return {
        "contexts": [
            {
                "id": "family",
                "name": "కుటుంబం",
                "description": "Family relationships and dynamics",
                "relevant_emotions": ["ఆనందం", "గర్వం", "దుఃఖం", "కృతజ్ఞత"]
            },
            {
                "id": "social",
                "name": "సామాజిక",
                "description": "Social interactions and community",
                "relevant_emotions": ["గర్వం", "సిగ్గు", "ఆనందం", "కోపం"]
            },
            {
                "id": "traditional",
                "name": "సాంప్రదాయిక",
                "description": "Traditional and cultural values",
                "relevant_emotions": ["గర్వం", "కృతజ్ఞత", "శాంతి", "భక్తి"]
            },
            {
                "id": "modern",
                "name": "ఆధునిక",
                "description": "Modern lifestyle and challenges",
                "relevant_emotions": ["ఉత్సాహం", "ఆశ", "నిరాశ", "గందరగోళం"]
            },
            {
                "id": "romantic",
                "name": "ప్రేమ",
                "description": "Love and romantic relationships",
                "relevant_emotions": ["ప్రేమ", "ఆనందం", "దుఃఖం", "ఆశ"]
            }
        ]
    }


@router.get("/statistics")
async def get_emotion_statistics(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get emotion analysis statistics"""
    try:
        orchestrator_stats = orchestrator.get_orchestrator_stats()
        
        # Get emotion agent statistics
        emotion_agents = []
        for agent_id, agent in orchestrator.agents.items():
            if agent.agent_type == "emotion_analyzer":
                agent_stats = agent.get_status()
                if hasattr(agent, 'get_analysis_stats'):
                    agent_stats.update(agent.get_analysis_stats())
                emotion_agents.append(agent_stats)
        
        return {
            "orchestrator_stats": orchestrator_stats,
            "emotion_agents": emotion_agents,
            "total_emotion_agents": len(emotion_agents)
        }
        
    except Exception as e:
        logger.error(f"Error getting emotion statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))