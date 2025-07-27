"""
Cultural analysis API endpoints
"""
import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
import logging

from ....agents.base_agent import AgentTask
from ....agents.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter()


class CulturalValidationRequest(BaseModel):
    """Request model for cultural validation"""
    text: str = Field(..., description="Text to validate")
    context: str = Field("general", description="Cultural context")


class TraditionAnalysisRequest(BaseModel):
    """Request model for tradition analysis"""
    text: str = Field(..., description="Text to analyze for traditions")


class FamilyDynamicsRequest(BaseModel):
    """Request model for family dynamics analysis"""
    text: str = Field(..., description="Text to analyze for family dynamics")


class RegionalContextRequest(BaseModel):
    """Request model for regional context analysis"""
    text: str = Field(..., description="Text to analyze for regional context")


class FestivalContextRequest(BaseModel):
    """Request model for festival context analysis"""
    text: str = Field(..., description="Text to analyze for festival context")


class LanguageAuthenticityRequest(BaseModel):
    """Request model for language authenticity check"""
    text: str = Field(..., description="Text to check for language authenticity")


class CulturalResponse(BaseModel):
    """Response model for cultural operations"""
    success: bool
    task_id: str
    message: str
    data: Optional[Dict[str, Any]] = None


def get_orchestrator(request: Request) -> AgentOrchestrator:
    """Get orchestrator from app state"""
    if not hasattr(request.app.state, 'orchestrator'):
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    return request.app.state.orchestrator


@router.post("/validate", response_model=CulturalResponse)
async def validate_cultural_authenticity(
    request: CulturalValidationRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Validate cultural authenticity of Telugu text"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="cultural_validation",
            input_data={
                "text": request.text,
                "context": request.context
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Cultural validation task {task_id} submitted")
        
        return CulturalResponse(
            success=True,
            task_id=task_id,
            message="Cultural validation task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in cultural validation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-traditions", response_model=CulturalResponse)
async def analyze_traditions(
    request: TraditionAnalysisRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze traditional elements in Telugu text"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="tradition_analysis",
            input_data={
                "text": request.text
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Tradition analysis task {task_id} submitted")
        
        return CulturalResponse(
            success=True,
            task_id=task_id,
            message="Tradition analysis task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in tradition analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-family-dynamics", response_model=CulturalResponse)
async def analyze_family_dynamics(
    request: FamilyDynamicsRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze family dynamics and relationships"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="family_dynamics_analysis",
            input_data={
                "text": request.text
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Family dynamics analysis task {task_id} submitted")
        
        return CulturalResponse(
            success=True,
            task_id=task_id,
            message="Family dynamics analysis task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in family dynamics analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-regional-context", response_model=CulturalResponse)
async def analyze_regional_context(
    request: RegionalContextRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze regional context and dialect usage"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="regional_context_analysis",
            input_data={
                "text": request.text
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Regional context analysis task {task_id} submitted")
        
        return CulturalResponse(
            success=True,
            task_id=task_id,
            message="Regional context analysis task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in regional context analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-festival-context", response_model=CulturalResponse)
async def analyze_festival_context(
    request: FestivalContextRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze festival context and celebrations"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="festival_context_analysis",
            input_data={
                "text": request.text
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Festival context analysis task {task_id} submitted")
        
        return CulturalResponse(
            success=True,
            task_id=task_id,
            message="Festival context analysis task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in festival context analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-language-authenticity", response_model=CulturalResponse)
async def check_language_authenticity(
    request: LanguageAuthenticityRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Check language authenticity and proper usage"""
    try:
        task = AgentTask(
            id=str(uuid.uuid4()),
            task_type="language_authenticity_check",
            input_data={
                "text": request.text
            },
            priority=2
        )
        
        task_id = await orchestrator.submit_task(task)
        
        logger.info(f"Language authenticity check task {task_id} submitted")
        
        return CulturalResponse(
            success=True,
            task_id=task_id,
            message="Language authenticity check task submitted successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in language authenticity check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task/{task_id}")
async def get_cultural_task_result(
    task_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get the result of a cultural analysis task"""
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
        logger.error(f"Error getting cultural task result: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/festivals")
async def get_telugu_festivals():
    """Get list of Telugu festivals and their cultural significance"""
    return {
        "festivals": [
            {
                "name": "దీపావళి",
                "english": "Diwali",
                "type": "major_festival",
                "significance": "Victory of light over darkness",
                "traditions": ["దీపాలు వెలిగించడం", "మిఠాయిలు పంచుకోవడం", "కొత్త బట్టలు"],
                "emotions": ["ఆనందం", "కృతజ్ఞత", "ఐక్యత"]
            },
            {
                "name": "దసరా",
                "english": "Dussehra",
                "type": "major_festival",
                "significance": "Victory of good over evil",
                "traditions": ["గోలు అమర్చడం", "సరస్వతి పూజ", "విజయదశమి"],
                "emotions": ["గర్వం", "భక్తి", "ఆనందం"]
            },
            {
                "name": "ఉగాది",
                "english": "Ugadi",
                "type": "new_year",
                "significance": "Telugu New Year",
                "traditions": ["ఉగాది పచ్చడి", "పంచాంగ శ్రవణం", "కొత్త బట్టలు"],
                "emotions": ["ఆశ", "ఆనందం", "కృతజ్ఞత"]
            },
            {
                "name": "శ్రీరామనవమి",
                "english": "Sri Rama Navami",
                "type": "religious_festival",
                "significance": "Lord Rama's birth",
                "traditions": ["రామ కథ పఠనం", "భజనలు", "ప్రసాదం"],
                "emotions": ["భక్తి", "శాంతి", "ఆనందం"]
            }
        ]
    }


@router.get("/family-relations")
async def get_family_relations():
    """Get Telugu family relations and their cultural significance"""
    return {
        "relations": [
            {
                "telugu": "తల్లి",
                "english": "mother",
                "respect_level": "high",
                "cultural_significance": "Primary caregiver and nurturer"
            },
            {
                "telugu": "తండ్రి",
                "english": "father",
                "respect_level": "high",
                "cultural_significance": "Family head and provider"
            },
            {
                "telugu": "అన్న",
                "english": "elder_brother",
                "respect_level": "high",
                "cultural_significance": "Protector and guide"
            },
            {
                "telugu": "అక్క",
                "english": "elder_sister",
                "respect_level": "high",
                "cultural_significance": "Guide and advisor"
            },
            {
                "telugu": "తమ్మి",
                "english": "younger_brother",
                "respect_level": "medium",
                "cultural_significance": "Companion and friend"
            },
            {
                "telugu": "చెల్లి",
                "english": "younger_sister",
                "respect_level": "medium",
                "cultural_significance": "Beloved and protected"
            },
            {
                "telugu": "అత్త",
                "english": "mother_in_law",
                "respect_level": "very_high",
                "cultural_significance": "Second mother"
            },
            {
                "telugu": "మామ",
                "english": "maternal_uncle",
                "respect_level": "high",
                "cultural_significance": "Mentor and guide"
            }
        ]
    }


@router.get("/cultural-values")
async def get_cultural_values():
    """Get Telugu cultural values and their meanings"""
    return {
        "values": [
            {
                "telugu": "గౌరవం",
                "english": "respect",
                "contexts": ["elders", "teachers", "guests"],
                "expressions": ["నమస్కారం", "పాదాభివందనం", "మర్యాదపూర్వక భాష"]
            },
            {
                "telugu": "ధర్మం",
                "english": "righteousness",
                "contexts": ["moral_duty", "justice", "truth"],
                "expressions": ["న్యాయం", "సత్యం", "కర్తవ్యం"]
            },
            {
                "telugu": "సంస్కృతి",
                "english": "culture",
                "contexts": ["traditions", "customs", "heritage"],
                "expressions": ["సంప్రదాయం", "వారసత్వం", "పరంపర"]
            },
            {
                "telugu": "కుటుంబం",
                "english": "family",
                "contexts": ["joint_family", "family_bonds", "family_honor"],
                "expressions": ["కుటుంబ ఐక్యత", "కుటుంబ గౌరవం", "కుటుంబ బాధ్యత"]
            }
        ]
    }


@router.get("/regional-contexts")
async def get_regional_contexts():
    """Get Telugu regional contexts and characteristics"""
    return {
        "regions": [
            {
                "name": "హైదరాబాద్",
                "english": "Hyderabad",
                "type": "metropolitan",
                "characteristics": ["cosmopolitan", "tech_hub", "nizami_culture"],
                "dialects": ["హైదరాబాదీ తెలుగు", "దక్కనీ"],
                "landmarks": ["చార్మినార్", "గోల్కొండ", "హుస్సేన్ సాగర్"]
            },
            {
                "name": "విజయవాడ",
                "english": "Vijayawada",
                "type": "commercial_city",
                "characteristics": ["business_center", "krishna_river", "cultural_hub"],
                "dialects": ["కోస్తా ఆంధ్ర తెలుగు"],
                "landmarks": ["కనక దుర్గ", "ప్రకాశం బ్యారేజ్", "భవానీ ద్వీపం"]
            },
            {
                "name": "తిరుపతి",
                "english": "Tirupati",
                "type": "pilgrimage_center",
                "characteristics": ["spiritual", "temple_town", "devotional"],
                "dialects": ["రాయలసీమ తెలుగు"],
                "landmarks": ["తిరుమల", "వెంకటేశ్వర స్వామి", "శ్రీవారి కొండ"]
            }
        ]
    }


@router.get("/statistics")
async def get_cultural_statistics(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get cultural analysis statistics"""
    try:
        orchestrator_stats = orchestrator.get_orchestrator_stats()
        
        # Get cultural agent statistics
        cultural_agents = []
        for agent_id, agent in orchestrator.agents.items():
            if agent.agent_type == "cultural_analyzer":
                agent_stats = agent.get_status()
                if hasattr(agent, 'get_analysis_stats'):
                    agent_stats.update(agent.get_analysis_stats())
                cultural_agents.append(agent_stats)
        
        return {
            "orchestrator_stats": orchestrator_stats,
            "cultural_agents": cultural_agents,
            "total_cultural_agents": len(cultural_agents)
        }
        
    except Exception as e:
        logger.error(f"Error getting cultural statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))