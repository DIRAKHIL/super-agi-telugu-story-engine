"""
Production API for Telugu Story Engine
Real AI-powered API endpoints - NO MOCKS, NO FALLBACKS
"""

from .main import app
from .routes import router
from .models import *
from .dependencies import *

__all__ = ["app", "router"]