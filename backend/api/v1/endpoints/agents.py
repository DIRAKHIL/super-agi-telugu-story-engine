"""
Agent management API endpoints
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import logging

from ....agents.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter()


def get_orchestrator(request: Request) -> AgentOrchestrator:
    """Get orchestrator from app state"""
    if not hasattr(request.app.state, 'orchestrator'):
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    return request.app.state.orchestrator


@router.get("/status")
async def get_all_agents_status(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get status of all agents"""
    try:
        return orchestrator.get_agent_status()
    except Exception as e:
        logger.error(f"Error getting agents status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{agent_id}")
async def get_agent_status(
    agent_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get status of a specific agent"""
    try:
        status = orchestrator.get_agent_status(agent_id)
        if status is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
async def get_agent_types(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get available agent types and their capabilities"""
    try:
        agent_types_info = {}
        
        for agent_id, agent in orchestrator.agents.items():
            agent_type = agent.agent_type
            if agent_type not in agent_types_info:
                agent_types_info[agent_type] = {
                    "type": agent_type,
                    "capabilities": agent.capabilities,
                    "agents": [],
                    "total_agents": 0
                }
            
            agent_types_info[agent_type]["agents"].append({
                "agent_id": agent_id,
                "status": agent.status.value,
                "last_activity": agent.last_activity
            })
            agent_types_info[agent_type]["total_agents"] += 1
        
        return {
            "agent_types": list(agent_types_info.values()),
            "total_types": len(agent_types_info)
        }
        
    except Exception as e:
        logger.error(f"Error getting agent types: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities")
async def get_all_capabilities(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get all available capabilities across agents"""
    try:
        all_capabilities = set()
        capabilities_by_type = {}
        
        for agent_id, agent in orchestrator.agents.items():
            agent_type = agent.agent_type
            
            if agent_type not in capabilities_by_type:
                capabilities_by_type[agent_type] = set()
            
            for capability in agent.capabilities:
                all_capabilities.add(capability)
                capabilities_by_type[agent_type].add(capability)
        
        # Convert sets to lists for JSON serialization
        capabilities_by_type = {
            agent_type: list(capabilities) 
            for agent_type, capabilities in capabilities_by_type.items()
        }
        
        return {
            "all_capabilities": list(all_capabilities),
            "capabilities_by_type": capabilities_by_type,
            "total_capabilities": len(all_capabilities)
        }
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_agent_statistics(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get comprehensive agent statistics"""
    try:
        orchestrator_stats = orchestrator.get_orchestrator_stats()
        
        # Get detailed agent statistics
        agent_details = []
        for agent_id, agent in orchestrator.agents.items():
            agent_info = agent.get_status()
            
            # Add type-specific statistics if available
            if hasattr(agent, 'get_generation_stats'):
                agent_info['generation_stats'] = agent.get_generation_stats()
            elif hasattr(agent, 'get_analysis_stats'):
                agent_info['analysis_stats'] = agent.get_analysis_stats()
            
            agent_details.append(agent_info)
        
        return {
            "orchestrator_stats": orchestrator_stats,
            "agent_details": agent_details,
            "summary": {
                "total_agents": len(agent_details),
                "active_agents": len([a for a in agent_details if a["status"] == "idle"]),
                "working_agents": len([a for a in agent_details if a["status"] == "working"]),
                "failed_agents": len([a for a in agent_details if a["status"] == "failed"])
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting agent statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def check_agents_health(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Check health of all agents"""
    try:
        import time
        current_time = time.time()
        
        health_report = {
            "overall_health": "healthy",
            "agents": [],
            "issues": []
        }
        
        for agent_id, agent in orchestrator.agents.items():
            agent_health = {
                "agent_id": agent_id,
                "agent_type": agent.agent_type,
                "status": agent.status.value,
                "last_activity": agent.last_activity,
                "time_since_activity": current_time - agent.last_activity,
                "health": "healthy"
            }
            
            # Check for potential issues
            if current_time - agent.last_activity > 300:  # 5 minutes
                agent_health["health"] = "unresponsive"
                health_report["issues"].append(f"Agent {agent_id} appears unresponsive")
            
            if agent.status.value == "failed":
                agent_health["health"] = "failed"
                health_report["issues"].append(f"Agent {agent_id} is in failed state")
            
            health_report["agents"].append(agent_health)
        
        # Determine overall health
        if health_report["issues"]:
            health_report["overall_health"] = "degraded" if len(health_report["issues"]) < len(orchestrator.agents) / 2 else "unhealthy"
        
        return health_report
        
    except Exception as e:
        logger.error(f"Error checking agents health: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
async def get_agent_performance(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """Get agent performance metrics"""
    try:
        performance_data = {
            "orchestrator_performance": {
                "total_tasks_processed": orchestrator.total_tasks_processed,
                "average_task_time": orchestrator.average_task_time,
                "active_tasks": len(orchestrator.active_tasks),
                "completed_tasks": len(orchestrator.completed_tasks)
            },
            "agent_performance": []
        }
        
        for agent_id, agent in orchestrator.agents.items():
            agent_perf = {
                "agent_id": agent_id,
                "agent_type": agent.agent_type,
                "uptime": agent.last_activity - agent.created_at,
                "status": agent.status.value
            }
            
            # Add type-specific performance metrics
            if hasattr(agent, 'get_generation_stats'):
                stats = agent.get_generation_stats()
                agent_perf.update({
                    "stories_generated": stats.get("stories_generated", 0),
                    "average_generation_time": stats.get("average_generation_time", 0.0),
                    "total_words_generated": stats.get("total_words_generated", 0)
                })
            elif hasattr(agent, 'get_analysis_stats'):
                stats = agent.get_analysis_stats()
                agent_perf.update({
                    "texts_analyzed": stats.get("texts_analyzed", 0),
                    "average_processing_time": stats.get("average_processing_time", 0.0),
                    "elements_found": stats.get("cultural_elements_found", 0)
                })
            
            performance_data["agent_performance"].append(agent_perf)
        
        return performance_data
        
    except Exception as e:
        logger.error(f"Error getting agent performance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))