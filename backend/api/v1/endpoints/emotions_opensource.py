"""
Open Source AI-powered emotion analysis API endpoints
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging

try:
    from models.emotion_analyzer_opensource import telugu_emotion_analyzer_opensource, EmotionAnalysisRequest
except ImportError:
    from backend.models.emotion_analyzer_opensource import telugu_emotion_analyzer_opensource, EmotionAnalysisRequest

logger = logging.getLogger(__name__)

router = APIRouter()


class EmotionRequest(BaseModel):
    """Request model for emotion analysis"""
    text: str = Field(..., description="Text to analyze")
    analysis_type: Optional[str] = Field("comprehensive", description="Type of analysis")
    cultural_context: Optional[bool] = Field(True, description="Include cultural context")


class EmotionResponse(BaseModel):
    """Response model for emotion analysis"""
    success: bool
    emotions: Dict[str, float]
    sentiment: Dict[str, Any]
    cultural_elements: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


@router.post("/analyze", response_model=EmotionResponse)
async def analyze_emotions(request: EmotionRequest):
    """Analyze emotions in Telugu text using Open Source AI"""
    try:
        # Create analysis request
        analysis_request = EmotionAnalysisRequest(
            text=request.text,
            analysis_type=request.analysis_type,
            cultural_context=request.cultural_context
        )
        
        # Analyze emotions using Open Source AI
        result = await telugu_emotion_analyzer_opensource.analyze_emotions(analysis_request)
        
        logger.info(f"Open Source emotion analysis completed for text length: {len(request.text)}")
        
        return EmotionResponse(
            success=result.success,
            emotions=result.emotions,
            sentiment=result.sentiment,
            cultural_elements=result.cultural_elements,
            metadata=result.metadata
        )
        
    except Exception as e:
        logger.error(f"Error in Open Source emotion analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-emotions")
async def get_supported_emotions():
    """Get list of supported emotions"""
    return {
        "emotions": telugu_emotion_analyzer_opensource.supported_emotions
    }


@router.get("/cultural-contexts")
async def get_cultural_contexts():
    """Get list of Telugu cultural contexts for emotion analysis"""
    return {
        "cultural_contexts": [
            {"id": "family", "name": "కుటుంబం", "description": "Family relationships and dynamics"},
            {"id": "festival", "name": "పండుగలు", "description": "Telugu festivals and celebrations"},
            {"id": "tradition", "name": "సంప్రదాయాలు", "description": "Traditional customs and practices"},
            {"id": "rural", "name": "గ్రామీణ", "description": "Rural life and village settings"},
            {"id": "urban", "name": "నగర", "description": "Urban life and city settings"},
            {"id": "religious", "name": "మతపరమైన", "description": "Religious contexts and references"}
        ]
    }


@router.post("/emotional-arc")
async def analyze_emotional_arc(request: EmotionRequest):
    """Analyze the emotional arc of a longer text"""
    try:
        # Analyze emotional arc
        result = await telugu_emotion_analyzer_opensource.get_emotional_arc(request.text)
        
        logger.info(f"Emotional arc analysis completed for text length: {len(request.text)}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in emotional arc analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_emotion_statistics():
    """Get emotion analysis statistics"""
    return {
        "supported_emotions": len(telugu_emotion_analyzer_opensource.supported_emotions),
        "ai_powered": True,
        "emotion_model": telugu_emotion_analyzer_opensource.emotion_model_name if hasattr(telugu_emotion_analyzer_opensource, "emotion_model_name") else "Unknown",
        "sentiment_model": telugu_emotion_analyzer_opensource.sentiment_model_name if hasattr(telugu_emotion_analyzer_opensource, "sentiment_model_name") else "Unknown"
    }