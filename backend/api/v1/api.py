"""
API v1 router for Telugu Film Story Generation System
"""
from fastapi import APIRouter

from .endpoints import stories, emotions, cultural, agents, workflows

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(stories.router, prefix="/stories", tags=["stories"])
api_router.include_router(emotions.router, prefix="/emotions", tags=["emotions"])
api_router.include_router(cultural.router, prefix="/cultural", tags=["cultural"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])