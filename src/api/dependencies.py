"""
FastAPI Dependencies for Telugu Story Engine
Production-ready dependencies for authentication, validation, etc.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import redis

from ..core.config import get_config

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()
config = get_config()

# Redis client for session management
try:
    redis_client = redis.from_url(config.database.redis_url)
except Exception as e:
    logger.warning(f"Redis not available: {e}")
    redis_client = None

class User:
    """User model for authentication"""
    def __init__(self, user_id: str, username: str, preferences: Optional[Dict[str, Any]] = None):
        self.user_id = user_id
        self.username = username
        self.preferences = preferences or {}

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get current authenticated user
    For development, this returns a mock user
    In production, this would validate JWT tokens
    """
    try:
        # For development/demo purposes, return a mock user
        # In production, this would decode and validate the JWT token
        
        token = credentials.credentials
        
        # Mock validation - in production, use proper JWT validation
        if token == "demo-token":
            return User(
                user_id="demo-user",
                username="demo",
                preferences={
                    "preferred_cultural_context": "contemporary_telugu",
                    "preferred_story_types": ["drama", "family"],
                    "preferred_length": 2000
                }
            )
        
        # For actual JWT validation (commented out for demo):
        # try:
        #     payload = jwt.decode(token, config.api.secret_key, algorithms=[config.api.algorithm])
        #     user_id: str = payload.get("sub")
        #     if user_id is None:
        #         raise HTTPException(status_code=401, detail="Invalid token")
        #     return get_user_from_db(user_id)
        # except JWTError:
        #     raise HTTPException(status_code=401, detail="Invalid token")
        
        # For demo, allow any token
        return User(user_id="anonymous", username="anonymous")
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_optional_user(
    request: Request
) -> Optional[User]:
    """
    Get user if authenticated, otherwise return None
    Used for endpoints that work with or without authentication
    """
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.split(" ")[1]
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        return await get_current_user(credentials)
        
    except HTTPException:
        return None
    except Exception as e:
        logger.error(f"Optional authentication error: {e}")
        return None

async def get_db_session():
    """
    Get database session
    For demo purposes, this returns None
    In production, this would return an actual database session
    """
    # In production, this would create and return a database session
    # For now, return None as we're not using a database yet
    return None

def validate_story_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate story generation request
    """
    # Basic validation
    if not request_data.get("prompt"):
        raise HTTPException(
            status_code=400,
            detail="Prompt is required"
        )
    
    if len(request_data["prompt"]) < 10:
        raise HTTPException(
            status_code=400,
            detail="Prompt must be at least 10 characters long"
        )
    
    if len(request_data["prompt"]) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Prompt must be less than 2000 characters"
        )
    
    # Validate length
    length = request_data.get("length", 2000)
    if not isinstance(length, int) or length < 500 or length > 10000:
        raise HTTPException(
            status_code=400,
            detail="Length must be between 500 and 10000 words"
        )
    
    return request_data

def check_rate_limit(request: Request) -> bool:
    """
    Check rate limiting for requests
    """
    if not redis_client:
        # If Redis is not available, allow all requests
        return True
    
    try:
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        # Get current count
        current_count = redis_client.get(key)
        
        if current_count is None:
            # First request from this IP
            redis_client.setex(key, 3600, 1)  # 1 hour expiry
            return True
        
        current_count = int(current_count)
        
        # Check if limit exceeded
        if current_count >= config.api.rate_limit_requests:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Increment counter
        redis_client.incr(key)
        return True
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rate limiting error: {e}")
        # If rate limiting fails, allow the request
        return True

def get_user_session(request: Request) -> Dict[str, Any]:
    """
    Get or create user session
    """
    session_id = request.headers.get("X-Session-ID")
    
    if not session_id:
        # Create new session
        import uuid
        session_id = str(uuid.uuid4())
    
    # In production, this would store/retrieve session data from Redis/database
    # For now, return a basic session
    return {
        "session_id": session_id,
        "created_at": datetime.now(),
        "last_activity": datetime.now(),
        "preferences": {},
        "story_history": []
    }

def validate_admin_access(current_user: User = Depends(get_current_user)) -> User:
    """
    Validate admin access for system management endpoints
    """
    # For demo purposes, allow all authenticated users admin access
    # In production, check user roles/permissions
    
    if current_user.username == "anonymous":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    
    return current_user

def log_request(request: Request):
    """
    Log request for monitoring
    """
    logger.info(f"Request: {request.method} {request.url}")

# Utility functions for JWT token management (for production use)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.api.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.api.secret_key, algorithm=config.api.algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, config.api.secret_key, algorithms=[config.api.algorithm])
        return payload
    except JWTError:
        return None