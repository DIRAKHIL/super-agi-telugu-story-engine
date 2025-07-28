# Comprehensive API Endpoints Documentation
## Telugu Story Engine Production API

### 🎯 API Overview

The Telugu Story Engine API provides comprehensive endpoints for AI-powered story generation, multi-agent collaboration, real-time monitoring, and advanced analytics. Built with FastAPI, it supports both REST and WebSocket protocols for maximum flexibility.

---

## 🏗️ API Architecture

### Technology Stack
```python
# Production API Stack
FastAPI: "0.104+"           # High-performance async API framework
Uvicorn: "0.24+"           # ASGI server with performance optimizations
Pydantic: "2.5+"           # Data validation and serialization
SQLAlchemy: "2.0+"         # Async ORM for database operations
Redis: "5.0+"              # Caching and session management
Celery: "5.3+"             # Distributed task queue
WebSocket: "Socket.IO"     # Real-time bidirectional communication
```

### Base Configuration
```python
from fastapi import FastAPI, WebSocket, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
import asyncio
import redis
from sqlalchemy.ext.asyncio import AsyncSession

# Production FastAPI app
app = FastAPI(
    title="Telugu Story Engine API",
    description="Production AI API for Telugu story generation with multi-agent architecture",
    version="2.0.0",
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redoc",
    openapi_url="/api/v2/openapi.json"
)

# Production middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://telugu-story-engine.com", "https://dashboard.telugu-story-engine.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security
security = HTTPBearer()
```

---

## 📚 Core Story Generation APIs

### 1. Story Generation Endpoints

#### Generate Complete Story
```python
@app.post("/api/v2/stories/generate", response_model=StoryResponse)
async def generate_story(
    request: StoryGenerationRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> StoryResponse:
    """
    Generate a complete Telugu story using multi-agent AI system
    
    Features:
    - Real AI processing (no mocks)
    - Multi-agent collaboration
    - Cultural adaptation
    - Emotion analysis
    - Quality assurance
    """
    
    # Validate request
    if not request.prompt or len(request.prompt.strip()) < 10:
        raise HTTPException(status_code=400, detail="Prompt must be at least 10 characters")
    
    # Initialize multi-agent orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Generate story with real AI processing
    story_result = await orchestrator.generate_story(
        prompt=request.prompt,
        story_type=request.story_type,
        cultural_context=request.cultural_context,
        emotion_focus=request.emotion_focus,
        length=request.length,
        user_preferences=current_user.preferences
    )
    
    # Store in database
    story_record = Story(
        id=generate_uuid(),
        user_id=current_user.id,
        prompt=request.prompt,
        content=story_result.content,
        metadata=story_result.metadata,
        emotions=story_result.emotions,
        cultural_elements=story_result.cultural_elements,
        generation_time=story_result.generation_time,
        quality_score=story_result.quality_score,
        created_at=datetime.utcnow()
    )
    
    session.add(story_record)
    await session.commit()
    
    # Background tasks
    background_tasks.add_task(update_user_analytics, current_user.id, story_result)
    background_tasks.add_task(cache_popular_elements, story_result.cultural_elements)
    
    return StoryResponse(
        story_id=story_record.id,
        content=story_result.content,
        emotions=story_result.emotions,
        cultural_elements=story_result.cultural_elements,
        generation_time=story_result.generation_time,
        quality_score=story_result.quality_score,
        agent_contributions=story_result.agent_contributions,
        metadata=story_result.metadata
    )

# Request/Response Models
class StoryGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=1000, description="Story generation prompt")
    story_type: StoryType = Field(default=StoryType.SHORT_STORY, description="Type of story to generate")
    cultural_context: CulturalContext = Field(default=CulturalContext.MODERN, description="Cultural setting")
    emotion_focus: List[EmotionType] = Field(default=[], description="Primary emotions to emphasize")
    length: int = Field(default=500, ge=100, le=10000, description="Target word count")
    style_preferences: Optional[StylePreferences] = None
    advanced_options: Optional[AdvancedGenerationOptions] = None

class StoryResponse(BaseModel):
    story_id: str
    content: str
    emotions: List[EmotionAnalysis]
    cultural_elements: List[CulturalElement]
    generation_time: float
    quality_score: float
    agent_contributions: Dict[str, AgentContribution]
    metadata: StoryMetadata
    created_at: datetime
```

#### Stream Story Generation (Real-time)
```python
@app.post("/api/v2/stories/generate/stream")
async def stream_story_generation(
    request: StoryGenerationRequest,
    current_user: User = Depends(get_current_user)
) -> StreamingResponse:
    """
    Stream story generation in real-time with progressive updates
    """
    
    async def generate_story_stream():
        orchestrator = MultiAgentOrchestrator()
        
        # Stream story generation updates
        async for update in orchestrator.stream_story_generation(
            prompt=request.prompt,
            story_type=request.story_type,
            cultural_context=request.cultural_context,
            user_id=current_user.id
        ):
            yield f"data: {json.dumps(update.dict())}\n\n"
    
    return StreamingResponse(
        generate_story_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )
```

#### Refine Existing Story
```python
@app.post("/api/v2/stories/{story_id}/refine", response_model=StoryResponse)
async def refine_story(
    story_id: str,
    refinement_request: StoryRefinementRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> StoryResponse:
    """
    Refine existing story with specific improvements
    
    Refinement Types:
    - Emotion enhancement
    - Cultural adaptation
    - Character development
    - Plot improvement
    - Language polishing
    """
    
    # Get original story
    story = await session.get(Story, story_id)
    if not story or story.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Initialize refinement agent
    refinement_agent = StoryRefinementAgent()
    
    # Apply refinements
    refined_story = await refinement_agent.refine(
        original_content=story.content,
        refinement_type=refinement_request.type,
        parameters=refinement_request.parameters,
        target_improvements=refinement_request.improvements
    )
    
    # Update story record
    story.content = refined_story.content
    story.metadata = refined_story.metadata
    story.quality_score = refined_story.quality_score
    story.updated_at = datetime.utcnow()
    
    await session.commit()
    
    return StoryResponse.from_story(story, refined_story)

class StoryRefinementRequest(BaseModel):
    type: RefinementType = Field(..., description="Type of refinement to apply")
    parameters: Dict[str, Any] = Field(default={}, description="Refinement parameters")
    improvements: List[str] = Field(..., description="Specific areas to improve")
    preserve_elements: List[str] = Field(default=[], description="Elements to preserve")
```

### 2. Story Management Endpoints

#### Get Story Details
```python
@app.get("/api/v2/stories/{story_id}", response_model=DetailedStoryResponse)
async def get_story(
    story_id: str,
    include_analytics: bool = Query(False, description="Include detailed analytics"),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> DetailedStoryResponse:
    """Get detailed story information with optional analytics"""
    
    story = await session.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Check permissions
    if story.user_id != current_user.id and not story.is_public:
        raise HTTPException(status_code=403, detail="Access denied")
    
    response_data = DetailedStoryResponse.from_story(story)
    
    if include_analytics:
        analytics = await get_story_analytics(story_id)
        response_data.analytics = analytics
    
    return response_data
```

#### List User Stories
```python
@app.get("/api/v2/stories", response_model=PaginatedStoryResponse)
async def list_stories(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    story_type: Optional[StoryType] = Query(None, description="Filter by story type"),
    cultural_context: Optional[CulturalContext] = Query(None, description="Filter by cultural context"),
    sort_by: SortOption = Query(SortOption.CREATED_DESC, description="Sort option"),
    search: Optional[str] = Query(None, description="Search in story content"),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> PaginatedStoryResponse:
    """List user's stories with filtering and pagination"""
    
    query = select(Story).where(Story.user_id == current_user.id)
    
    # Apply filters
    if story_type:
        query = query.where(Story.story_type == story_type)
    if cultural_context:
        query = query.where(Story.cultural_context == cultural_context)
    if search:
        query = query.where(Story.content.contains(search))
    
    # Apply sorting
    if sort_by == SortOption.CREATED_DESC:
        query = query.order_by(Story.created_at.desc())
    elif sort_by == SortOption.QUALITY_DESC:
        query = query.order_by(Story.quality_score.desc())
    
    # Pagination
    total = await session.scalar(select(func.count()).select_from(query.subquery()))
    stories = await session.execute(
        query.offset((page - 1) * limit).limit(limit)
    )
    
    return PaginatedStoryResponse(
        stories=[StoryListItem.from_story(story) for story in stories.scalars()],
        total=total,
        page=page,
        limit=limit,
        total_pages=math.ceil(total / limit)
    )
```

---

## 🤖 Multi-Agent System APIs

### 3. Agent Management Endpoints

#### Get Agents Status
```python
@app.get("/api/v2/agents/status", response_model=AgentsStatusResponse)
async def get_agents_status(
    include_metrics: bool = Query(True, description="Include performance metrics"),
    current_user: User = Depends(get_current_user)
) -> AgentsStatusResponse:
    """Get real-time status of all AI agents"""
    
    orchestrator = MultiAgentOrchestrator()
    agents_status = await orchestrator.get_all_agents_status()
    
    response_data = AgentsStatusResponse(
        agents=agents_status,
        collaboration_metrics=orchestrator.get_collaboration_metrics(),
        system_health=orchestrator.get_system_health(),
        last_updated=datetime.utcnow()
    )
    
    if include_metrics:
        response_data.performance_metrics = await get_agent_performance_metrics()
    
    return response_data

class AgentsStatusResponse(BaseModel):
    agents: List[AgentStatus]
    collaboration_metrics: CollaborationMetrics
    system_health: SystemHealth
    performance_metrics: Optional[Dict[str, PerformanceMetrics]] = None
    last_updated: datetime

class AgentStatus(BaseModel):
    agent_id: str
    name: str
    type: AgentType
    status: AgentStatusEnum
    current_task: Optional[str]
    performance_score: float
    success_rate: float
    average_response_time: float
    memory_usage: float
    last_activity: datetime
```

#### Agent Collaboration Analytics
```python
@app.get("/api/v2/agents/collaboration", response_model=CollaborationAnalytics)
async def get_collaboration_analytics(
    time_range: TimeRange = Query(TimeRange.LAST_24H, description="Time range for analytics"),
    agent_ids: Optional[List[str]] = Query(None, description="Filter by specific agents"),
    current_user: User = Depends(get_current_user)
) -> CollaborationAnalytics:
    """Get detailed agent collaboration analytics"""
    
    analytics_service = AgentAnalyticsService()
    
    collaboration_data = await analytics_service.get_collaboration_analytics(
        time_range=time_range,
        agent_ids=agent_ids,
        user_id=current_user.id
    )
    
    return CollaborationAnalytics(
        collaboration_patterns=collaboration_data.patterns,
        success_rates=collaboration_data.success_rates,
        communication_flow=collaboration_data.communication_flow,
        performance_trends=collaboration_data.trends,
        bottlenecks=collaboration_data.bottlenecks,
        recommendations=collaboration_data.recommendations
    )
```

### 4. Agent Control Endpoints

#### Configure Agent Behavior
```python
@app.post("/api/v2/agents/{agent_id}/configure", response_model=AgentConfigResponse)
async def configure_agent(
    agent_id: str,
    config: AgentConfiguration,
    current_user: User = Depends(get_current_admin_user)  # Admin only
) -> AgentConfigResponse:
    """Configure agent behavior and parameters"""
    
    orchestrator = MultiAgentOrchestrator()
    agent = await orchestrator.get_agent(agent_id)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Apply configuration
    updated_config = await agent.update_configuration(config)
    
    # Log configuration change
    await log_admin_action(
        user_id=current_user.id,
        action="agent_configuration_update",
        target=agent_id,
        details=config.dict()
    )
    
    return AgentConfigResponse(
        agent_id=agent_id,
        configuration=updated_config,
        status="updated",
        effective_at=datetime.utcnow()
    )

class AgentConfiguration(BaseModel):
    performance_parameters: Dict[str, float]
    collaboration_settings: CollaborationSettings
    resource_limits: ResourceLimits
    quality_thresholds: QualityThresholds
    cultural_adaptation_level: float = Field(ge=0.0, le=1.0)
```

---

## 🎭 Emotion & Cultural Analysis APIs

### 5. Emotion Analysis Endpoints

#### Analyze Text Emotions
```python
@app.post("/api/v2/analysis/emotions", response_model=EmotionAnalysisResponse)
async def analyze_emotions(
    request: EmotionAnalysisRequest,
    current_user: User = Depends(get_current_user)
) -> EmotionAnalysisResponse:
    """Analyze emotions in Telugu text using advanced AI models"""
    
    if not request.text or len(request.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="Text must be at least 5 characters")
    
    # Initialize emotion analyzer
    emotion_analyzer = TeluguEmotionAnalyzer(
        model_version="v2.1",
        cultural_context=request.cultural_context
    )
    
    # Perform emotion analysis
    analysis_result = await emotion_analyzer.analyze(
        text=request.text,
        language=request.language,
        context=request.context
    )
    
    return EmotionAnalysisResponse(
        emotions=analysis_result.emotions,
        dominant_emotion=analysis_result.dominant_emotion,
        confidence_scores=analysis_result.confidence_scores,
        emotional_arc=analysis_result.emotional_arc,
        cultural_nuances=analysis_result.cultural_nuances,
        analysis_metadata=analysis_result.metadata
    )

class EmotionAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=10000)
    language: Language = Field(default=Language.TELUGU)
    cultural_context: Optional[CulturalContext] = None
    context: Optional[str] = Field(None, description="Additional context for analysis")

class EmotionAnalysisResponse(BaseModel):
    emotions: List[EmotionScore]
    dominant_emotion: EmotionScore
    confidence_scores: Dict[str, float]
    emotional_arc: List[EmotionPoint]
    cultural_nuances: List[CulturalNuance]
    analysis_metadata: AnalysisMetadata
```

#### Emotion Trend Analysis
```python
@app.get("/api/v2/analysis/emotions/trends", response_model=EmotionTrendsResponse)
async def get_emotion_trends(
    time_range: TimeRange = Query(TimeRange.LAST_7D),
    story_type: Optional[StoryType] = Query(None),
    cultural_context: Optional[CulturalContext] = Query(None),
    current_user: User = Depends(get_current_user)
) -> EmotionTrendsResponse:
    """Get emotion trends across user's stories"""
    
    analytics_service = EmotionAnalyticsService()
    
    trends = await analytics_service.get_emotion_trends(
        user_id=current_user.id,
        time_range=time_range,
        filters={
            "story_type": story_type,
            "cultural_context": cultural_context
        }
    )
    
    return EmotionTrendsResponse(
        trends=trends.emotion_trends,
        patterns=trends.patterns,
        insights=trends.insights,
        recommendations=trends.recommendations
    )
```

### 6. Cultural Adaptation Endpoints

#### Adapt Cultural Context
```python
@app.post("/api/v2/cultural/adapt", response_model=CulturalAdaptationResponse)
async def adapt_cultural_context(
    request: CulturalAdaptationRequest,
    current_user: User = Depends(get_current_user)
) -> CulturalAdaptationResponse:
    """Adapt content for specific Telugu cultural context"""
    
    # Initialize cultural adaptation agent
    cultural_adapter = CulturalAdaptationAgent()
    
    # Perform adaptation
    adaptation_result = await cultural_adapter.adapt(
        content=request.content,
        source_context=request.source_context,
        target_context=request.target_context,
        adaptation_level=request.adaptation_level,
        preserve_elements=request.preserve_elements
    )
    
    return CulturalAdaptationResponse(
        adapted_content=adaptation_result.content,
        cultural_elements=adaptation_result.cultural_elements,
        adaptation_confidence=adaptation_result.confidence,
        changes_made=adaptation_result.changes,
        cultural_authenticity_score=adaptation_result.authenticity_score,
        recommendations=adaptation_result.recommendations
    )

class CulturalAdaptationRequest(BaseModel):
    content: str = Field(..., min_length=10)
    source_context: CulturalContext
    target_context: CulturalContext
    adaptation_level: float = Field(default=0.7, ge=0.0, le=1.0)
    preserve_elements: List[str] = Field(default=[])

class CulturalAdaptationResponse(BaseModel):
    adapted_content: str
    cultural_elements: List[CulturalElement]
    adaptation_confidence: float
    changes_made: List[AdaptationChange]
    cultural_authenticity_score: float
    recommendations: List[str]
```

---

## 📊 Analytics & Monitoring APIs

### 7. Analytics Endpoints

#### User Analytics Dashboard
```python
@app.get("/api/v2/analytics/dashboard", response_model=UserAnalyticsDashboard)
async def get_user_analytics(
    time_range: TimeRange = Query(TimeRange.LAST_30D),
    current_user: User = Depends(get_current_user)
) -> UserAnalyticsDashboard:
    """Get comprehensive user analytics for dashboard"""
    
    analytics_service = UserAnalyticsService()
    
    dashboard_data = await analytics_service.get_dashboard_analytics(
        user_id=current_user.id,
        time_range=time_range
    )
    
    return UserAnalyticsDashboard(
        story_statistics=dashboard_data.story_stats,
        emotion_analytics=dashboard_data.emotion_analytics,
        cultural_preferences=dashboard_data.cultural_preferences,
        quality_metrics=dashboard_data.quality_metrics,
        usage_patterns=dashboard_data.usage_patterns,
        achievements=dashboard_data.achievements,
        recommendations=dashboard_data.recommendations
    )
```

#### System Performance Metrics
```python
@app.get("/api/v2/analytics/system/performance", response_model=SystemPerformanceMetrics)
async def get_system_performance(
    time_range: TimeRange = Query(TimeRange.LAST_1H),
    metric_types: List[MetricType] = Query(default=[]),
    current_user: User = Depends(get_current_admin_user)  # Admin only
) -> SystemPerformanceMetrics:
    """Get detailed system performance metrics"""
    
    metrics_service = SystemMetricsService()
    
    performance_data = await metrics_service.get_performance_metrics(
        time_range=time_range,
        metric_types=metric_types or [MetricType.ALL]
    )
    
    return SystemPerformanceMetrics(
        ai_model_metrics=performance_data.ai_metrics,
        infrastructure_metrics=performance_data.infrastructure_metrics,
        api_performance=performance_data.api_performance,
        database_metrics=performance_data.database_metrics,
        cache_metrics=performance_data.cache_metrics,
        alerts=performance_data.active_alerts
    )
```

### 8. Real-time Monitoring WebSocket APIs

#### WebSocket Connection for Real-time Updates
```python
@app.websocket("/api/v2/ws/monitoring")
async def websocket_monitoring(
    websocket: WebSocket,
    token: str = Query(..., description="Authentication token")
):
    """WebSocket endpoint for real-time monitoring updates"""
    
    # Authenticate user
    try:
        user = await authenticate_websocket_token(token)
        await websocket.accept()
    except AuthenticationError:
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    # Subscribe to monitoring channels
    monitoring_service = RealTimeMonitoringService()
    subscription = await monitoring_service.subscribe_user(user.id)
    
    try:
        while True:
            # Send real-time updates
            update = await subscription.get_next_update()
            await websocket.send_json({
                "type": update.type,
                "data": update.data,
                "timestamp": update.timestamp.isoformat()
            })
            
            # Handle incoming messages
            try:
                message = await asyncio.wait_for(websocket.receive_json(), timeout=0.1)
                await handle_websocket_message(user, message, subscription)
            except asyncio.TimeoutError:
                continue
                
    except WebSocketDisconnect:
        await monitoring_service.unsubscribe_user(user.id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user.id}: {e}")
        await websocket.close(code=1011, reason="Internal error")
```

#### Story Generation Progress WebSocket
```python
@app.websocket("/api/v2/ws/stories/generate")
async def websocket_story_generation(
    websocket: WebSocket,
    token: str = Query(..., description="Authentication token")
):
    """WebSocket for real-time story generation progress"""
    
    user = await authenticate_websocket_token(token)
    await websocket.accept()
    
    try:
        while True:
            # Receive generation request
            request_data = await websocket.receive_json()
            
            # Validate request
            try:
                generation_request = StoryGenerationRequest(**request_data)
            except ValidationError as e:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid request",
                    "details": e.errors()
                })
                continue
            
            # Start story generation with progress updates
            orchestrator = MultiAgentOrchestrator()
            
            async for progress_update in orchestrator.stream_story_generation(
                prompt=generation_request.prompt,
                story_type=generation_request.story_type,
                cultural_context=generation_request.cultural_context,
                user_id=user.id
            ):
                await websocket.send_json({
                    "type": "generation_progress",
                    "data": progress_update.dict(),
                    "timestamp": datetime.utcnow().isoformat()
                })
                
    except WebSocketDisconnect:
        logger.info(f"Story generation WebSocket disconnected for user {user.id}")
    except Exception as e:
        logger.error(f"Story generation WebSocket error: {e}")
        await websocket.close(code=1011, reason="Generation error")
```

---

## 🔐 Authentication & User Management APIs

### 9. Authentication Endpoints

#### User Registration
```python
@app.post("/api/v2/auth/register", response_model=AuthResponse)
async def register_user(
    request: UserRegistrationRequest,
    session: AsyncSession = Depends(get_db_session)
) -> AuthResponse:
    """Register new user account"""
    
    # Validate email uniqueness
    existing_user = await session.scalar(
        select(User).where(User.email == request.email)
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user account
    password_hash = hash_password(request.password)
    
    new_user = User(
        id=generate_uuid(),
        email=request.email,
        username=request.username,
        password_hash=password_hash,
        preferences=UserPreferences(),
        created_at=datetime.utcnow()
    )
    
    session.add(new_user)
    await session.commit()
    
    # Generate tokens
    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600,
        user=UserProfile.from_user(new_user)
    )

class UserRegistrationRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    preferences: Optional[UserPreferences] = None
```

#### User Login
```python
@app.post("/api/v2/auth/login", response_model=AuthResponse)
async def login_user(
    request: UserLoginRequest,
    session: AsyncSession = Depends(get_db_session)
) -> AuthResponse:
    """Authenticate user and return tokens"""
    
    # Find user
    user = await session.scalar(
        select(User).where(User.email == request.email)
    )
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    user.last_login = datetime.utcnow()
    await session.commit()
    
    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600,
        user=UserProfile.from_user(user)
    )
```

### 10. User Profile Management

#### Get User Profile
```python
@app.get("/api/v2/users/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserProfile:
    """Get current user's profile information"""
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        preferences=current_user.preferences,
        statistics=await get_user_statistics(current_user.id),
        achievements=await get_user_achievements(current_user.id),
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )
```

#### Update User Preferences
```python
@app.put("/api/v2/users/preferences", response_model=UserPreferences)
async def update_user_preferences(
    preferences: UserPreferences,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> UserPreferences:
    """Update user preferences"""
    
    current_user.preferences = preferences
    current_user.updated_at = datetime.utcnow()
    
    await session.commit()
    
    return preferences

class UserPreferences(BaseModel):
    preferred_story_types: List[StoryType] = []
    cultural_contexts: List[CulturalContext] = []
    emotion_preferences: List[EmotionType] = []
    language_preference: Language = Language.TELUGU
    quality_threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    notification_settings: NotificationSettings = NotificationSettings()
```

---

## 📈 Advanced Features APIs

### 11. Collaborative Storytelling

#### Create Collaborative Session
```python
@app.post("/api/v2/collaboration/sessions", response_model=CollaborativeSessionResponse)
async def create_collaborative_session(
    request: CreateCollaborativeSessionRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> CollaborativeSessionResponse:
    """Create a new collaborative storytelling session"""
    
    # Create session
    collab_session = CollaborativeSession(
        id=generate_uuid(),
        creator_id=current_user.id,
        title=request.title,
        description=request.description,
        max_participants=request.max_participants,
        settings=request.settings,
        status=SessionStatus.WAITING_FOR_PARTICIPANTS,
        created_at=datetime.utcnow()
    )
    
    session.add(collab_session)
    await session.commit()
    
    # Initialize collaborative engine
    collab_engine = CollaborativeStoryEngine()
    await collab_engine.initialize_session(collab_session.id)
    
    return CollaborativeSessionResponse(
        session_id=collab_session.id,
        title=collab_session.title,
        creator=UserProfile.from_user(current_user),
        settings=collab_session.settings,
        status=collab_session.status,
        join_code=generate_join_code(collab_session.id)
    )
```

#### Join Collaborative Session
```python
@app.post("/api/v2/collaboration/sessions/{session_id}/join", response_model=JoinSessionResponse)
async def join_collaborative_session(
    session_id: str,
    join_code: Optional[str] = None,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> JoinSessionResponse:
    """Join an existing collaborative session"""
    
    # Validate session and join code
    collab_session = await session.get(CollaborativeSession, session_id)
    if not collab_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if collab_session.settings.requires_join_code and not verify_join_code(session_id, join_code):
        raise HTTPException(status_code=403, detail="Invalid join code")
    
    # Add participant
    participant = SessionParticipant(
        session_id=session_id,
        user_id=current_user.id,
        role=ParticipantRole.CONTRIBUTOR,
        joined_at=datetime.utcnow()
    )
    
    session.add(participant)
    await session.commit()
    
    # Notify other participants
    collab_engine = CollaborativeStoryEngine()
    await collab_engine.notify_participant_joined(session_id, current_user.id)
    
    return JoinSessionResponse(
        session_id=session_id,
        participant_id=participant.id,
        role=participant.role,
        websocket_url=f"/api/v2/ws/collaboration/{session_id}"
    )
```

### 12. Multi-Modal Story Generation

#### Generate Multi-Modal Story
```python
@app.post("/api/v2/stories/multimodal/generate", response_model=MultiModalStoryResponse)
async def generate_multimodal_story(
    request: MultiModalGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> MultiModalStoryResponse:
    """Generate story with text, audio, and visual elements"""
    
    # Initialize multi-modal generator
    multimodal_generator = MultiModalStoryGenerator()
    
    # Generate multimedia story
    multimedia_story = await multimodal_generator.generate_multimedia_story(
        prompt=request.prompt,
        modalities=request.modalities,
        style_preferences=request.style_preferences,
        cultural_context=request.cultural_context
    )
    
    # Store multimedia elements
    background_tasks.add_task(
        store_multimedia_elements,
        multimedia_story.multimedia_elements,
        current_user.id
    )
    
    return MultiModalStoryResponse(
        story_id=multimedia_story.id,
        text_content=multimedia_story.story.content,
        audio_url=multimedia_story.multimedia_elements.get("audio", {}).get("url"),
        images=multimedia_story.multimedia_elements.get("images", []),
        video_url=multimedia_story.multimedia_elements.get("video", {}).get("url"),
        generation_metadata=multimedia_story.metadata
    )

class MultiModalGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10)
    modalities: List[Modality] = Field(..., description="Requested output modalities")
    style_preferences: MultiModalStylePreferences
    cultural_context: CulturalContext = CulturalContext.MODERN
    quality_settings: QualitySettings = QualitySettings()

class MultiModalStoryResponse(BaseModel):
    story_id: str
    text_content: str
    audio_url: Optional[str] = None
    images: List[GeneratedImage] = []
    video_url: Optional[str] = None
    generation_metadata: MultiModalMetadata
```

---

## 🔧 API Configuration & Utilities

### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply rate limits to endpoints
@app.post("/api/v2/stories/generate")
@limiter.limit("10/minute")  # 10 requests per minute
async def generate_story_with_limit(request: Request, ...):
    # Implementation
    pass
```

### Error Handling
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class APIError(Exception):
    def __init__(self, status_code: int, message: str, details: Optional[Dict] = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url)
            }
        }
    )
```

### API Versioning
```python
# Version-specific routers
v1_router = APIRouter(prefix="/api/v1", tags=["v1"])
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

# Include routers
app.include_router(v1_router)
app.include_router(v2_router)

# Version deprecation warnings
@v1_router.middleware("http")
async def add_deprecation_warning(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-API-Deprecation"] = "v1 is deprecated, please use v2"
    response.headers["X-API-Sunset"] = "2025-12-31"
    return response
```

---

## 📊 API Performance & Monitoring

### Performance Metrics
```yaml
Target Performance:
  Response Time (95th percentile): < 100ms
  Throughput: 1000+ requests/second
  Availability: 99.9%
  Error Rate: < 0.1%

Monitoring:
  - Request/response times
  - Error rates and types
  - Resource utilization
  - Database query performance
  - Cache hit rates
  - WebSocket connection health
```

### Health Checks
```python
@app.get("/health", include_in_schema=False)
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/health/detailed", include_in_schema=False)
async def detailed_health_check():
    """Detailed health check with dependency status"""
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "dependencies": {}
    }
    
    # Check database
    try:
        async with get_db_session() as session:
            await session.execute(text("SELECT 1"))
        health_status["dependencies"]["database"] = "healthy"
    except Exception as e:
        health_status["dependencies"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Redis
    try:
        redis_client = get_redis_client()
        await redis_client.ping()
        health_status["dependencies"]["redis"] = "healthy"
    except Exception as e:
        health_status["dependencies"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check AI models
    try:
        orchestrator = MultiAgentOrchestrator()
        model_status = await orchestrator.health_check()
        health_status["dependencies"]["ai_models"] = model_status
    except Exception as e:
        health_status["dependencies"]["ai_models"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status
```

---

**This comprehensive API documentation provides complete endpoints for a production-ready Telugu Story Engine with real AI capabilities, advanced features, and robust monitoring. All endpoints are designed for real-world deployment with proper authentication, validation, error handling, and performance optimization.**