"""
Custom Middleware for Telugu Story Engine API
Production-ready middleware for security, logging, and monitoring
"""

import time
import logging
import json
from typing import Dict, Any, Optional
from collections import defaultdict, deque
from datetime import datetime, timedelta

from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis

from ..core.config import get_config

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.clients = defaultdict(deque)
        self.config = get_config()
        
        # Try to use Redis for distributed rate limiting
        try:
            self.redis_client = redis.from_url(self.config.database.redis_url)
            self.use_redis = True
            logger.info("Using Redis for distributed rate limiting")
        except Exception as e:
            logger.warning(f"Redis not available, using in-memory rate limiting: {e}")
            self.use_redis = False
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting"""
        client_ip = self._get_client_ip(request)
        current_time = datetime.now()
        
        if self.use_redis:
            is_allowed = await self._check_rate_limit_redis(client_ip, current_time)
        else:
            is_allowed = self._check_rate_limit_memory(client_ip, current_time)
        
        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute.",
                    "retry_after": 60
                },
                headers={"Retry-After": "60"}
            )
        
        response = await call_next(request)
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    async def _check_rate_limit_redis(self, client_ip: str, current_time: datetime) -> bool:
        """Check rate limit using Redis"""
        try:
            key = f"rate_limit:{client_ip}"
            pipe = self.redis_client.pipeline()
            
            # Remove old entries
            cutoff_time = current_time - timedelta(minutes=1)
            pipe.zremrangebyscore(key, 0, cutoff_time.timestamp())
            
            # Add current request
            pipe.zadd(key, {str(current_time.timestamp()): current_time.timestamp()})
            
            # Count requests in the last minute
            pipe.zcard(key)
            
            # Set expiration
            pipe.expire(key, 120)  # 2 minutes
            
            results = pipe.execute()
            request_count = results[2]
            
            return request_count <= self.requests_per_minute
            
        except Exception as e:
            logger.error(f"Redis rate limiting error: {e}")
            # Fallback to memory-based rate limiting
            return self._check_rate_limit_memory(client_ip, current_time)
    
    def _check_rate_limit_memory(self, client_ip: str, current_time: datetime) -> bool:
        """Check rate limit using in-memory storage"""
        client_requests = self.clients[client_ip]
        
        # Remove old requests (older than 1 minute)
        cutoff_time = current_time - timedelta(minutes=1)
        while client_requests and client_requests[0] < cutoff_time:
            client_requests.popleft()
        
        # Check if limit exceeded
        if len(client_requests) >= self.requests_per_minute:
            return False
        
        # Add current request
        client_requests.append(current_time)
        return True

class LoggingMiddleware(BaseHTTPMiddleware):
    """Request/Response logging middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.config = get_config()
    
    async def dispatch(self, request: Request, call_next):
        """Log requests and responses"""
        start_time = time.time()
        
        # Log request
        request_data = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("User-Agent"),
            "timestamp": datetime.now().isoformat()
        }
        
        # Don't log sensitive data
        if "authorization" in request_data["headers"]:
            request_data["headers"]["authorization"] = "[REDACTED]"
        
        logger.info(f"Request: {json.dumps(request_data)}")
        
        # Process request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            response_data = {
                "status_code": response.status_code,
                "process_time": process_time,
                "response_size": response.headers.get("content-length", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
            
            if response.status_code >= 400:
                logger.warning(f"Response: {json.dumps(response_data)}")
            else:
                logger.info(f"Response: {json.dumps(response_data)}")
            
            # Add timing header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Request failed: {e}, process_time: {process_time}")
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"

class MetricsMiddleware(BaseHTTPMiddleware):
    """Metrics collection middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.metrics = {
            "requests_total": 0,
            "requests_by_method": defaultdict(int),
            "requests_by_status": defaultdict(int),
            "response_times": deque(maxlen=1000),
            "errors_total": 0,
            "active_requests": 0
        }
    
    async def dispatch(self, request: Request, call_next):
        """Collect metrics"""
        self.metrics["requests_total"] += 1
        self.metrics["requests_by_method"][request.method] += 1
        self.metrics["active_requests"] += 1
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Record metrics
            self.metrics["requests_by_status"][response.status_code] += 1
            self.metrics["response_times"].append(process_time)
            
            if response.status_code >= 400:
                self.metrics["errors_total"] += 1
            
            # Add metrics headers
            response.headers["X-Request-Count"] = str(self.metrics["requests_total"])
            response.headers["X-Active-Requests"] = str(self.metrics["active_requests"])
            
            return response
            
        except Exception as e:
            self.metrics["errors_total"] += 1
            raise
        finally:
            self.metrics["active_requests"] -= 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        response_times = list(self.metrics["response_times"])
        
        return {
            "requests_total": self.metrics["requests_total"],
            "requests_by_method": dict(self.metrics["requests_by_method"]),
            "requests_by_status": dict(self.metrics["requests_by_status"]),
            "errors_total": self.metrics["errors_total"],
            "active_requests": self.metrics["active_requests"],
            "response_time_stats": {
                "count": len(response_times),
                "avg": sum(response_times) / len(response_times) if response_times else 0,
                "min": min(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0
            }
        }

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security headers and validation middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.config = get_config()
    
    async def dispatch(self, request: Request, call_next):
        """Apply security measures"""
        # Validate request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse(
                status_code=413,
                content={
                    "error": "payload_too_large",
                    "message": "Request payload too large"
                }
            )
        
        # Check for suspicious patterns
        if self._is_suspicious_request(request):
            logger.warning(f"Suspicious request detected: {request.url}")
            return JSONResponse(
                status_code=400,
                content={
                    "error": "bad_request",
                    "message": "Invalid request"
                }
            )
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
    
    def _is_suspicious_request(self, request: Request) -> bool:
        """Check for suspicious request patterns"""
        # Check for common attack patterns
        suspicious_patterns = [
            "script>", "<iframe", "javascript:", "vbscript:",
            "onload=", "onerror=", "eval(", "alert(",
            "../", "..\\", "/etc/passwd", "/proc/",
            "SELECT * FROM", "DROP TABLE", "UNION SELECT"
        ]
        
        # Check URL
        url_str = str(request.url).lower()
        for pattern in suspicious_patterns:
            if pattern.lower() in url_str:
                return True
        
        # Check headers
        for header_name, header_value in request.headers.items():
            header_value_lower = header_value.lower()
            for pattern in suspicious_patterns:
                if pattern.lower() in header_value_lower:
                    return True
        
        return False

class CacheMiddleware(BaseHTTPMiddleware):
    """Response caching middleware"""
    
    def __init__(self, app, cache_ttl: int = 300):
        super().__init__(app)
        self.cache_ttl = cache_ttl
        self.cache = {}
        self.cache_times = {}
        
        # Try to use Redis for caching
        try:
            config = get_config()
            self.redis_client = redis.from_url(config.database.redis_url)
            self.use_redis = True
            logger.info("Using Redis for response caching")
        except Exception as e:
            logger.warning(f"Redis not available, using in-memory caching: {e}")
            self.use_redis = False
    
    async def dispatch(self, request: Request, call_next):
        """Apply caching"""
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)
        
        # Don't cache certain endpoints
        if any(path in str(request.url) for path in ["/health", "/metrics", "/docs"]):
            return await call_next(request)
        
        cache_key = self._get_cache_key(request)
        
        # Check cache
        cached_response = await self._get_cached_response(cache_key)
        if cached_response:
            logger.info(f"Cache hit for {cache_key}")
            return Response(
                content=cached_response["content"],
                status_code=cached_response["status_code"],
                headers=cached_response["headers"],
                media_type=cached_response["media_type"]
            )
        
        # Process request
        response = await call_next(request)
        
        # Cache successful responses
        if response.status_code == 200:
            await self._cache_response(cache_key, response)
        
        return response
    
    def _get_cache_key(self, request: Request) -> str:
        """Generate cache key for request"""
        return f"cache:{request.method}:{str(request.url)}"
    
    async def _get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached response"""
        if self.use_redis:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                logger.error(f"Redis cache get error: {e}")
        
        # Fallback to memory cache
        if cache_key in self.cache:
            cache_time = self.cache_times.get(cache_key, 0)
            if time.time() - cache_time < self.cache_ttl:
                return self.cache[cache_key]
            else:
                # Remove expired entry
                del self.cache[cache_key]
                del self.cache_times[cache_key]
        
        return None
    
    async def _cache_response(self, cache_key: str, response: Response):
        """Cache response"""
        try:
            # Read response content
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            # Recreate response with the body
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
            
            cache_data = {
                "content": response_body.decode() if response_body else "",
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "media_type": response.media_type
            }
            
            if self.use_redis:
                try:
                    self.redis_client.setex(
                        cache_key,
                        self.cache_ttl,
                        json.dumps(cache_data)
                    )
                except Exception as e:
                    logger.error(f"Redis cache set error: {e}")
            
            # Also store in memory cache as fallback
            self.cache[cache_key] = cache_data
            self.cache_times[cache_key] = time.time()
            
        except Exception as e:
            logger.error(f"Error caching response: {e}")

# Global middleware instances for metrics access
metrics_middleware = None

def get_metrics_middleware() -> Optional[MetricsMiddleware]:
    """Get the global metrics middleware instance"""
    return metrics_middleware

def set_metrics_middleware(middleware: MetricsMiddleware):
    """Set the global metrics middleware instance"""
    global metrics_middleware
    metrics_middleware = middleware