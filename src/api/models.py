"""
Pydantic Models for Telugu Story Engine API
Production-ready data models for real AI system
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

class StoryType(str, Enum):
    """Supported story types"""
    DRAMA = "drama"
    ROMANCE = "romance"
    FAMILY = "family"
    SOCIAL = "social"
    HISTORICAL = "historical"
    MYTHOLOGICAL = "mythological"
    COMEDY = "comedy"
    THRILLER = "thriller"
    ADVENTURE = "adventure"

class CulturalContext(str, Enum):
    """Cultural context options"""
    CONTEMPORARY_TELUGU = "contemporary_telugu"
    TRADITIONAL_TELUGU = "traditional_telugu"
    RURAL_TELUGU = "rural_telugu"
    COASTAL_ANDHRA = "coastal_andhra"
    RAYALASEEMA = "rayalaseema"
    TELANGANA = "telangana"
    DIASPORA = "diaspora"

class EmotionalFocus(str, Enum):
    """Emotional focus options"""
    JOY = "joy"
    SADNESS = "sadness"
    LOVE = "love"
    FAMILY_BONDS = "family_bonds"
    SACRIFICE = "sacrifice"
    TRIUMPH = "triumph"
    NOSTALGIA = "nostalgia"
    HOPE = "hope"
    REDEMPTION = "redemption"
    TRANSFORMATION = "transformation"

class LanguageStyle(str, Enum):
    """Language style options"""
    SIMPLE = "simple"
    LITERARY = "literary"
    CONVERSATIONAL = "conversational"
    FORMAL = "formal"
    POETIC = "poetic"
    REGIONAL_DIALECT = "regional_dialect"

class Character(BaseModel):
    """Character definition"""
    name: str = Field(..., description="Character name in Telugu")
    age: int = Field(..., ge=1, le=100, description="Character age")
    gender: str = Field(..., description="Character gender")
    traits: List[str] = Field(..., description="Character personality traits")
    background: str = Field(..., description="Character background story")
    role: str = Field(default="supporting", description="Character role in story")
    relationships: Dict[str, str] = Field(default_factory=dict, description="Relationships with other characters")

class Setting(BaseModel):
    """Story setting"""
    location: str = Field(..., description="Primary location")
    time_period: str = Field(..., description="Time period")
    social_context: str = Field(..., description="Social context")
    atmosphere: Optional[str] = Field(None, description="Desired atmosphere")
    cultural_elements: List[str] = Field(default_factory=list, description="Specific cultural elements to include")

class StoryGenerationRequest(BaseModel):
    """Request model for story generation"""
    prompt: str = Field(..., min_length=10, max_length=2000, description="Story prompt or theme")
    story_type: StoryType = Field(default=StoryType.DRAMA, description="Type of story")
    length: int = Field(default=2000, ge=500, le=10000, description="Target word count")
    cultural_context: CulturalContext = Field(default=CulturalContext.CONTEMPORARY_TELUGU, description="Cultural context")
    emotional_focus: Optional[EmotionalFocus] = Field(None, description="Primary emotional focus")
    language_style: LanguageStyle = Field(default=LanguageStyle.CONVERSATIONAL, description="Language style")
    
    characters: List[Character] = Field(default_factory=list, description="Character definitions")
    setting: Optional[Setting] = Field(None, description="Story setting")
    
    # Advanced options
    include_dialogue: bool = Field(default=True, description="Include dialogue in story")
    include_cultural_references: bool = Field(default=True, description="Include cultural references")
    target_audience: str = Field(default="general", description="Target audience")
    moral_message: Optional[str] = Field(None, description="Moral or message to convey")
    
    # Agent configuration
    enable_expert_agents: bool = Field(default=True, description="Enable expert domain agents")
    collaboration_rounds: int = Field(default=3, ge=1, le=10, description="Number of collaboration rounds")
    
    @validator('characters')
    def validate_characters(cls, v):
        if len(v) > 10:
            raise ValueError("Maximum 10 characters allowed")
        return v

class StoryMetadata(BaseModel):
    """Story metadata"""
    word_count: int
    character_count: int
    scene_count: int
    dialogue_percentage: float
    cultural_authenticity_score: float
    emotional_coherence_score: float
    quality_score: float
    generation_time: float
    agents_used: List[str]
    collaboration_rounds: int

class StoryResponse(BaseModel):
    """Response model for generated story"""
    id: str = Field(..., description="Unique story ID")
    title: str = Field(..., description="Generated story title")
    content: str = Field(..., description="Story content in Telugu")
    english_summary: Optional[str] = Field(None, description="English summary")
    
    metadata: StoryMetadata = Field(..., description="Story metadata")
    
    # Structure information
    structure_type: str = Field(..., description="Narrative structure used")
    plot_outline: Dict[str, Any] = Field(..., description="Plot outline")
    character_analysis: Dict[str, Any] = Field(..., description="Character analysis")
    cultural_elements: List[str] = Field(..., description="Cultural elements included")
    emotional_arc: Dict[str, Any] = Field(..., description="Emotional arc analysis")
    
    # Generation details
    request_id: str = Field(..., description="Original request ID")
    generated_at: datetime = Field(..., description="Generation timestamp")
    model_versions: Dict[str, str] = Field(..., description="Model versions used")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AgentStatus(BaseModel):
    """Agent status information"""
    agent_id: str
    agent_type: str
    status: str
    current_task: Optional[str] = None
    processing_time: float = 0.0
    confidence: float = 0.0
    memory_usage: float = 0.0
    last_activity: datetime

class SystemStatus(BaseModel):
    """System status information"""
    status: str = Field(..., description="Overall system status")
    uptime: float = Field(..., description="System uptime in seconds")
    active_agents: List[AgentStatus] = Field(..., description="Active agents")
    model_status: Dict[str, str] = Field(..., description="Model loading status")
    memory_usage: Dict[str, float] = Field(..., description="Memory usage by component")
    performance_metrics: Dict[str, float] = Field(..., description="Performance metrics")
    last_updated: datetime = Field(..., description="Last status update")

class StoryAnalysisRequest(BaseModel):
    """Request for story analysis"""
    story_content: str = Field(..., min_length=100, description="Story content to analyze")
    analysis_type: List[str] = Field(..., description="Types of analysis to perform")
    include_suggestions: bool = Field(default=True, description="Include improvement suggestions")

class StoryAnalysisResponse(BaseModel):
    """Response for story analysis"""
    analysis_id: str
    story_length: int
    
    # Analysis results
    structure_analysis: Dict[str, Any]
    character_analysis: Dict[str, Any]
    emotional_analysis: Dict[str, Any]
    cultural_analysis: Dict[str, Any]
    language_analysis: Dict[str, Any]
    
    # Scores
    overall_quality: float
    cultural_authenticity: float
    emotional_coherence: float
    narrative_structure: float
    language_quality: float
    
    # Suggestions
    suggestions: List[Dict[str, str]]
    
    analyzed_at: datetime

class BatchStoryRequest(BaseModel):
    """Request for batch story generation"""
    requests: List[StoryGenerationRequest] = Field(..., max_items=10, description="Batch of story requests")
    priority: str = Field(default="normal", description="Processing priority")
    callback_url: Optional[str] = Field(None, description="Callback URL for completion notification")

class BatchStoryResponse(BaseModel):
    """Response for batch story generation"""
    batch_id: str
    total_requests: int
    completed: int
    failed: int
    in_progress: int
    estimated_completion: Optional[datetime] = None
    results: List[Optional[StoryResponse]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

class ModelInfo(BaseModel):
    """Model information"""
    name: str
    type: str
    version: str
    parameters: int
    memory_usage: float
    loaded: bool
    load_time: Optional[datetime] = None
    performance_metrics: Dict[str, float] = Field(default_factory=dict)

class ConfigurationUpdate(BaseModel):
    """Configuration update request"""
    component: str = Field(..., description="Component to update")
    settings: Dict[str, Any] = Field(..., description="Settings to update")
    restart_required: bool = Field(default=False, description="Whether restart is required")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

class HealthCheck(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, str] = Field(..., description="Component health status")
    uptime: float = Field(..., description="Uptime in seconds")

# WebSocket Models
class WebSocketMessage(BaseModel):
    """WebSocket message model"""
    type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.now)
    client_id: Optional[str] = Field(None, description="Client ID")

class StoryGenerationProgress(BaseModel):
    """Story generation progress update"""
    request_id: str
    stage: str = Field(..., description="Current generation stage")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progress percentage")
    current_agent: Optional[str] = Field(None, description="Currently active agent")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    partial_content: Optional[str] = Field(None, description="Partial story content")

# Dashboard Models
class DashboardMetrics(BaseModel):
    """Dashboard metrics"""
    total_stories_generated: int
    stories_today: int
    average_generation_time: float
    success_rate: float
    active_users: int
    system_load: float
    memory_usage: float
    model_performance: Dict[str, float]
    agent_activity: Dict[str, int]
    cultural_context_distribution: Dict[str, int]
    story_type_distribution: Dict[str, int]
    quality_metrics: Dict[str, float]

class UserPreferences(BaseModel):
    """User preferences"""
    preferred_cultural_context: CulturalContext = CulturalContext.CONTEMPORARY_TELUGU
    preferred_story_types: List[StoryType] = Field(default_factory=list)
    preferred_length: int = Field(default=2000, ge=500, le=10000)
    language_style: LanguageStyle = LanguageStyle.CONVERSATIONAL
    include_cultural_references: bool = True
    enable_expert_agents: bool = True
    notification_preferences: Dict[str, bool] = Field(default_factory=dict)

class UserSession(BaseModel):
    """User session information"""
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    preferences: UserPreferences
    story_history: List[str] = Field(default_factory=list)
    active_requests: List[str] = Field(default_factory=list)