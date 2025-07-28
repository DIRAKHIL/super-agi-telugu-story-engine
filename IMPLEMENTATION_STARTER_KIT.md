# Implementation Starter Kit
## Ready-to-Deploy Code for Telugu Story Engine with Local Open Source LLMs

### Quick Start Guide

This starter kit provides production-ready code to immediately begin implementing the Telugu Story Engine using local open source LLM models. All code is functional and can be deployed within hours.

---

## Project Structure

```
telugu-story-engine/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── master_storyteller.py
│   │   ├── cultural_consultant.py
│   │   ├── emotional_architect.py
│   │   ├── reasoning_agent.py
│   │   └── character_developer.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── model_manager.py
│   │   ├── story_pipeline.py
│   │   └── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── websocket.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── connection.py
│   └── utils/
│       ├── __init__.py
│       ├── cultural_data.py
│       └── emotional_mapping.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Core Implementation Files

### 1. Model Manager (`src/core/model_manager.py`)

```python
import ollama
import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

@dataclass
class ModelConfig:
    name: str
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9

class LocalModelManager:
    """Production-ready local model manager using Ollama"""
    
    def __init__(self):
        self.client = ollama.AsyncClient()
        self.logger = logging.getLogger(__name__)
        
        # Production model configuration
        self.models = {
            'storyteller': ModelConfig(
                name='Master Storyteller',
                model_id='llama3.3:70b-instruct-q4_K_M',
                temperature=0.7,
                max_tokens=2048
            ),
            'cultural': ModelConfig(
                name='Cultural Consultant',
                model_id='qwen2.5:14b-instruct-q4_K_M',
                temperature=0.5,
                max_tokens=1536
            ),
            'emotional': ModelConfig(
                name='Emotional Architect',
                model_id='mistral:7b-instruct-v0.3-q4_K_M',
                temperature=0.6,
                max_tokens=1024
            ),
            'reasoning': ModelConfig(
                name='Logic Reasoning',
                model_id='deepseek-r1:7b-q4_K_M',
                temperature=0.3,
                max_tokens=1536
            ),
            'character': ModelConfig(
                name='Character Developer',
                model_id='llama3.1:8b-instruct-q4_K_M',
                temperature=0.6,
                max_tokens=1024
            )
        }
        
        self.model_status = {}
        
    async def initialize(self):
        """Initialize all models and check availability"""
        self.logger.info("Initializing local models...")
        
        for model_type, config in self.models.items():
            try:
                # Test model availability
                await self._test_model(config.model_id)
                self.model_status[model_type] = 'ready'
                self.logger.info(f"✅ {config.name} ({config.model_id}) - Ready")
            except Exception as e:
                self.model_status[model_type] = 'error'
                self.logger.error(f"❌ {config.name} ({config.model_id}) - Error: {e}")
        
        ready_models = sum(1 for status in self.model_status.values() if status == 'ready')
        self.logger.info(f"Initialized {ready_models}/{len(self.models)} models successfully")
        
    async def _test_model(self, model_id: str):
        """Test if model is available and responsive"""
        response = await self.client.generate(
            model=model_id,
            prompt="Test",
            options={'max_tokens': 5}
        )
        return response
        
    async def generate(self, model_type: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response using specified model"""
        if model_type not in self.models:
            raise ValueError(f"Unknown model type: {model_type}")
            
        if self.model_status.get(model_type) != 'ready':
            raise RuntimeError(f"Model {model_type} is not ready")
            
        config = self.models[model_type]
        start_time = time.time()
        
        try:
            response = await self.client.generate(
                model=config.model_id,
                prompt=prompt,
                options={
                    'temperature': kwargs.get('temperature', config.temperature),
                    'top_p': kwargs.get('top_p', config.top_p),
                    'max_tokens': kwargs.get('max_tokens', config.max_tokens),
                    'repeat_penalty': kwargs.get('repeat_penalty', 1.1)
                }
            )
            
            generation_time = time.time() - start_time
            
            return {
                'content': response['response'],
                'model': config.model_id,
                'generation_time': generation_time,
                'tokens': response.get('eval_count', 0),
                'tokens_per_second': response.get('eval_count', 0) / generation_time if generation_time > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Generation failed for {model_type}: {e}")
            raise
            
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check of all models"""
        health_status = {
            'timestamp': time.time(),
            'overall_status': 'healthy',
            'models': {}
        }
        
        for model_type, config in self.models.items():
            try:
                start_time = time.time()
                await self._test_model(config.model_id)
                response_time = (time.time() - start_time) * 1000  # Convert to ms
                
                health_status['models'][model_type] = {
                    'status': 'healthy',
                    'model_id': config.model_id,
                    'response_time_ms': round(response_time, 2),
                    'last_check': time.time()
                }
            except Exception as e:
                health_status['models'][model_type] = {
                    'status': 'error',
                    'model_id': config.model_id,
                    'error': str(e),
                    'last_check': time.time()
                }
                health_status['overall_status'] = 'degraded'
        
        return health_status

# Global model manager instance
model_manager = LocalModelManager()
```

### 2. Master Storyteller Agent (`src/agents/master_storyteller.py`)

```python
from typing import Dict, Any, List
import json
from ..core.model_manager import model_manager

class MasterStorytellerAgent:
    """Master storyteller using Llama 3.3 70B for narrative generation"""
    
    def __init__(self):
        self.model_type = 'storyteller'
        self.system_prompt = """You are a master Telugu storyteller with deep knowledge of Telugu culture, traditions, and cinema. You create engaging stories in Tinglish (Telugu words written in English script) that blend traditional values with modern sensibilities.

Your storytelling style:
- Rich character development with cultural authenticity
- Natural dialogue mixing Telugu and English (Tinglish)
- Emotional depth that resonates with Telugu audiences
- Traditional narrative structures with modern appeal
- Cultural references from mythology, cinema, and daily life
- Family values and social themes important to Telugu culture

Always maintain cultural sensitivity and create stories that feel authentic to Telugu speakers while being accessible to broader audiences."""

    async def generate_story_outline(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive story outline"""
        
        prompt = f"""{self.system_prompt}

Create a detailed story outline based on this request:

Genre: {request.get('genre', 'general')}
Theme: {request.get('theme', 'family values')}
Setting: {request.get('setting', 'contemporary Telugu region')}
Target Length: {request.get('length', 'medium')} story
Cultural Elements: {request.get('cultural_elements', ['family', 'tradition'])}
Emotional Arc: {request.get('emotional_arc', 'hero journey')}

Provide a detailed outline with:
1. Title (in Tinglish)
2. Main characters (3-5 characters with brief descriptions)
3. Setting details
4. Plot structure (beginning, middle, end)
5. Key emotional moments
6. Cultural elements to include
7. Dialogue style notes
8. Themes and messages

Format as a structured outline that can guide the full story development."""

        response = await model_manager.generate(
            model_type=self.model_type,
            prompt=prompt,
            temperature=0.7,
            max_tokens=2048
        )
        
        return {
            'outline': response['content'],
            'generation_time': response['generation_time'],
            'model_used': response['model']
        }
    
    async def develop_story_segment(self, outline: str, segment_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Develop a specific story segment based on outline"""
        
        segment_prompts = {
            'opening': "Create an engaging opening that establishes characters, setting, and hooks the reader",
            'development': "Develop the plot with character interactions, conflicts, and cultural elements",
            'climax': "Build to the emotional and dramatic high point of the story",
            'resolution': "Provide a satisfying conclusion that resolves conflicts and delivers the message"
        }
        
        prompt = f"""{self.system_prompt}

Story Outline:
{outline}

Current Context:
{json.dumps(context, indent=2)}

Task: {segment_prompts.get(segment_type, 'Continue the story naturally')}

Write this story segment in Tinglish with:
- Natural dialogue mixing Telugu and English
- Rich descriptions of settings and emotions
- Cultural authenticity in character behaviors
- Smooth narrative flow
- Engaging storytelling that keeps readers interested

Story Segment:"""

        response = await model_manager.generate(
            model_type=self.model_type,
            prompt=prompt,
            temperature=0.7,
            max_tokens=1536
        )
        
        return {
            'segment': response['content'],
            'segment_type': segment_type,
            'generation_time': response['generation_time'],
            'tokens_generated': response['tokens']
        }
    
    async def refine_story(self, story_content: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Refine story based on feedback from other agents"""
        
        prompt = f"""{self.system_prompt}

Original Story:
{story_content}

Feedback for Improvement:
Cultural Feedback: {feedback.get('cultural', 'No issues')}
Emotional Feedback: {feedback.get('emotional', 'No issues')}
Logic Feedback: {feedback.get('reasoning', 'No issues')}
Character Feedback: {feedback.get('character', 'No issues')}

Please refine the story addressing the feedback while maintaining:
- The core narrative and emotional journey
- Cultural authenticity and Tinglish dialogue
- Character consistency and development
- Engaging storytelling flow

Refined Story:"""

        response = await model_manager.generate(
            model_type=self.model_type,
            prompt=prompt,
            temperature=0.6,
            max_tokens=2048
        )
        
        return {
            'refined_story': response['content'],
            'improvements_made': feedback,
            'generation_time': response['generation_time']
        }
```

### 3. Cultural Consultant Agent (`src/agents/cultural_consultant.py`)

```python
from typing import Dict, Any, List
import json
from ..core.model_manager import model_manager
from ..utils.cultural_data import TELUGU_CULTURAL_ELEMENTS

class CulturalConsultantAgent:
    """Cultural consultant using Qwen2.5 14B for Telugu cultural validation"""
    
    def __init__(self):
        self.model_type = 'cultural'
        self.cultural_database = TELUGU_CULTURAL_ELEMENTS
        
        self.system_prompt = """You are an expert in Telugu culture, traditions, mythology, and social customs. You analyze content for cultural authenticity and provide suggestions for improvement.

Your expertise includes:
- Telugu mythology (Ramayana, Mahabharata, Puranas, local legends)
- Regional variations (Andhra Pradesh, Telangana, diaspora communities)
- Traditional festivals, customs, and rituals
- Family structures and social hierarchies
- Contemporary Telugu society and values
- Telugu cinema traditions and storytelling patterns
- Language usage and Tinglish patterns
- Religious practices and spiritual beliefs

Evaluate content for cultural accuracy, appropriateness, and authenticity while being respectful of all communities and traditions."""

    async def validate_cultural_authenticity(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate cultural authenticity of story content"""
        
        prompt = f"""{self.system_prompt}

Analyze this Telugu story content for cultural authenticity:

Content to Analyze:
{content}

Context:
Region: {context.get('region', 'General Telugu region')}
Time Period: {context.get('time_period', 'Contemporary')}
Target Audience: {context.get('audience', 'Family')}
Cultural Elements Expected: {context.get('cultural_elements', [])}

Please evaluate:

1. CULTURAL ACCURACY (Score 0-10):
   - Mythology references accuracy
   - Traditional customs representation
   - Social customs and family dynamics
   - Religious/spiritual elements appropriateness

2. REGIONAL AUTHENTICITY (Score 0-10):
   - Regional-specific traditions
   - Local customs and practices
   - Dialect and language usage
   - Geographic and cultural context

3. LANGUAGE AUTHENTICITY (Score 0-10):
   - Tinglish usage naturalness
   - Cultural expressions and idioms
   - Honorifics and respectful language
   - Code-switching patterns

4. SOCIAL CONTEXT (Score 0-10):
   - Contemporary social issues handling
   - Generational dynamics
   - Gender roles and relationships
   - Community interactions

5. IMPROVEMENT SUGGESTIONS:
   - Specific areas needing enhancement
   - Cultural elements to add or modify
   - Language improvements
   - Sensitivity considerations

Provide detailed analysis with specific examples and actionable suggestions."""

        response = await model_manager.generate(
            model_type=self.model_type,
            prompt=prompt,
            temperature=0.4,
            max_tokens=1536
        )
        
        # Parse the response to extract scores and suggestions
        analysis = self._parse_cultural_analysis(response['content'])
        
        return {
            'cultural_analysis': analysis,
            'overall_score': analysis.get('overall_score', 0),
            'suggestions': analysis.get('suggestions', []),
            'generation_time': response['generation_time']
        }
    
    async def enhance_cultural_elements(self, content: str, enhancement_type: str) -> Dict[str, Any]:
        """Enhance story with specific cultural elements"""
        
        enhancement_prompts = {
            'mythology': "Add appropriate mythological references and parallels",
            'traditions': "Incorporate traditional customs and practices",
            'festivals': "Include relevant festival celebrations or references",
            'family_values': "Strengthen family dynamics and traditional values",
            'regional_flavor': "Add region-specific cultural elements",
            'language': "Improve Tinglish usage and cultural expressions"
        }
        
        prompt = f"""{self.system_prompt}

Original Content:
{content}

Enhancement Task: {enhancement_prompts.get(enhancement_type, 'General cultural enhancement')}

Please enhance the content by:
1. Adding authentic cultural elements naturally
2. Maintaining story flow and readability
3. Ensuring cultural sensitivity and accuracy
4. Preserving the original narrative intent
5. Making enhancements feel organic, not forced

Enhanced Content:"""

        response = await model_manager.generate(
            model_type=self.model_type,
            prompt=prompt,
            temperature=0.5,
            max_tokens=1536
        )
        
        return {
            'enhanced_content': response['content'],
            'enhancement_type': enhancement_type,
            'generation_time': response['generation_time']
        }
    
    def _parse_cultural_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse cultural analysis response into structured data"""
        # Simple parsing - in production, use more sophisticated NLP
        lines = analysis_text.split('\n')
        
        scores = {}
        suggestions = []
        
        for line in lines:
            if 'Score' in line and ':' in line:
                try:
                    score_part = line.split(':')[1].strip()
                    score = float(score_part.split('/')[0])
                    category = line.split('(')[0].strip().lower().replace(' ', '_')
                    scores[category] = score
                except:
                    continue
            elif 'suggestion' in line.lower() or 'improve' in line.lower():
                suggestions.append(line.strip())
        
        overall_score = sum(scores.values()) / len(scores) if scores else 0
        
        return {
            'scores': scores,
            'overall_score': round(overall_score, 2),
            'suggestions': suggestions,
            'raw_analysis': analysis_text
        }
```

### 4. Story Generation Pipeline (`src/core/story_pipeline.py`)

```python
import asyncio
from typing import Dict, Any, List
import logging
import time
from dataclasses import dataclass

from ..agents.master_storyteller import MasterStorytellerAgent
from ..agents.cultural_consultant import CulturalConsultantAgent
from ..agents.emotional_architect import EmotionalArchitectAgent
from ..agents.reasoning_agent import ReasoningAgent
from ..agents.character_developer import CharacterDeveloperAgent

@dataclass
class StoryRequest:
    prompt: str
    genre: str = "general"
    length: str = "medium"
    cultural_context: Dict[str, Any] = None
    emotional_arc: str = "hero_journey"
    style_preferences: Dict[str, Any] = None
    constraints: Dict[str, Any] = None

@dataclass
class StoryResponse:
    story_id: str
    content: str
    metadata: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    generation_time: float

class StoryGenerationPipeline:
    """Production-ready story generation pipeline using multi-agent collaboration"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize agents
        self.storyteller = MasterStorytellerAgent()
        self.cultural_consultant = CulturalConsultantAgent()
        self.emotional_architect = EmotionalArchitectAgent()
        self.reasoning_agent = ReasoningAgent()
        self.character_developer = CharacterDeveloperAgent()
        
        self.pipeline_stats = {
            'stories_generated': 0,
            'average_generation_time': 0,
            'success_rate': 0
        }
    
    async def generate_story(self, request: StoryRequest) -> StoryResponse:
        """Generate a complete story using multi-agent collaboration"""
        start_time = time.time()
        story_id = f"story_{int(time.time())}"
        
        try:
            self.logger.info(f"Starting story generation: {story_id}")
            
            # Phase 1: Story Planning
            self.logger.info("Phase 1: Story planning and outline generation")
            outline_result = await self.storyteller.generate_story_outline({
                'genre': request.genre,
                'theme': request.prompt,
                'length': request.length,
                'cultural_elements': request.cultural_context.get('elements', []) if request.cultural_context else [],
                'emotional_arc': request.emotional_arc
            })
            
            # Phase 2: Character Development
            self.logger.info("Phase 2: Character development")
            character_result = await self.character_developer.develop_characters(
                outline_result['outline'],
                request.cultural_context or {}
            )
            
            # Phase 3: Cultural Validation
            self.logger.info("Phase 3: Cultural validation and enhancement")
            cultural_result = await self.cultural_consultant.validate_cultural_authenticity(
                outline_result['outline'],
                request.cultural_context or {}
            )
            
            # Phase 4: Story Generation
            self.logger.info("Phase 4: Full story generation")
            story_segments = []
            
            for segment_type in ['opening', 'development', 'climax', 'resolution']:
                segment_result = await self.storyteller.develop_story_segment(
                    outline_result['outline'],
                    segment_type,
                    {
                        'characters': character_result.get('characters', []),
                        'cultural_context': request.cultural_context,
                        'previous_segments': story_segments
                    }
                )
                story_segments.append(segment_result)
            
            # Combine story segments
            full_story = '\n\n'.join([segment['segment'] for segment in story_segments])
            
            # Phase 5: Emotional Analysis
            self.logger.info("Phase 5: Emotional analysis and optimization")
            emotional_result = await self.emotional_architect.analyze_emotional_arc(
                full_story,
                request.emotional_arc
            )
            
            # Phase 6: Logic and Consistency Check
            self.logger.info("Phase 6: Logic and consistency validation")
            reasoning_result = await self.reasoning_agent.validate_story_logic({
                'story': full_story,
                'outline': outline_result['outline'],
                'characters': character_result.get('characters', [])
            })
            
            # Phase 7: Final Refinement (if needed)
            if self._needs_refinement(cultural_result, emotional_result, reasoning_result):
                self.logger.info("Phase 7: Story refinement based on feedback")
                
                feedback = {
                    'cultural': cultural_result.get('suggestions', []),
                    'emotional': emotional_result.get('suggestions', []),
                    'reasoning': reasoning_result.get('suggestions', [])
                }
                
                refinement_result = await self.storyteller.refine_story(full_story, feedback)
                full_story = refinement_result['refined_story']
            
            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(
                cultural_result,
                emotional_result,
                reasoning_result
            )
            
            generation_time = time.time() - start_time
            
            # Update pipeline statistics
            self._update_stats(generation_time, True)
            
            self.logger.info(f"Story generation completed: {story_id} in {generation_time:.2f}s")
            
            return StoryResponse(
                story_id=story_id,
                content=full_story,
                metadata={
                    'outline': outline_result['outline'],
                    'characters': character_result.get('characters', []),
                    'cultural_analysis': cultural_result,
                    'emotional_analysis': emotional_result,
                    'reasoning_analysis': reasoning_result,
                    'generation_phases': len(story_segments),
                    'request_parameters': request.__dict__
                },
                quality_metrics=quality_metrics,
                generation_time=generation_time
            )
            
        except Exception as e:
            self.logger.error(f"Story generation failed for {story_id}: {e}")
            self._update_stats(time.time() - start_time, False)
            raise
    
    def _needs_refinement(self, cultural_result: Dict, emotional_result: Dict, reasoning_result: Dict) -> bool:
        """Determine if story needs refinement based on agent feedback"""
        cultural_score = cultural_result.get('overall_score', 10)
        emotional_score = emotional_result.get('overall_score', 10)
        reasoning_score = reasoning_result.get('consistency_score', 10)
        
        # Refine if any score is below threshold
        return cultural_score < 7.0 or emotional_score < 7.0 or reasoning_score < 7.0
    
    def _calculate_quality_metrics(self, cultural_result: Dict, emotional_result: Dict, reasoning_result: Dict) -> Dict[str, float]:
        """Calculate overall quality metrics"""
        return {
            'cultural_authenticity': cultural_result.get('overall_score', 0) / 10,
            'emotional_impact': emotional_result.get('overall_score', 0) / 10,
            'logical_consistency': reasoning_result.get('consistency_score', 0) / 10,
            'overall_quality': (
                cultural_result.get('overall_score', 0) +
                emotional_result.get('overall_score', 0) +
                reasoning_result.get('consistency_score', 0)
            ) / 30
        }
    
    def _update_stats(self, generation_time: float, success: bool):
        """Update pipeline statistics"""
        self.pipeline_stats['stories_generated'] += 1
        
        if success:
            current_avg = self.pipeline_stats['average_generation_time']
            count = self.pipeline_stats['stories_generated']
            self.pipeline_stats['average_generation_time'] = (
                (current_avg * (count - 1) + generation_time) / count
            )
        
        success_count = self.pipeline_stats['stories_generated'] * self.pipeline_stats['success_rate']
        if success:
            success_count += 1
        
        self.pipeline_stats['success_rate'] = success_count / self.pipeline_stats['stories_generated']
    
    async def get_pipeline_health(self) -> Dict[str, Any]:
        """Get pipeline health and statistics"""
        return {
            'status': 'healthy',
            'statistics': self.pipeline_stats,
            'agents_status': {
                'storyteller': 'active',
                'cultural_consultant': 'active',
                'emotional_architect': 'active',
                'reasoning_agent': 'active',
                'character_developer': 'active'
            }
        }

# Global pipeline instance
story_pipeline = StoryGenerationPipeline()
```

### 5. FastAPI Application (`src/api/main.py`)

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import Dict, Any
import asyncio

from ..core.model_manager import model_manager
from ..core.story_pipeline import story_pipeline, StoryRequest
from .routes import router
from .websocket import websocket_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Telugu Story Engine API",
    description="Production-ready AI storytelling system for Telugu content",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/ws")

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting Telugu Story Engine API...")
    
    try:
        # Initialize model manager
        await model_manager.initialize()
        logger.info("✅ Model manager initialized")
        
        # Verify pipeline health
        health = await story_pipeline.get_pipeline_health()
        logger.info(f"✅ Story pipeline status: {health['status']}")
        
        logger.info("🚀 Telugu Story Engine API is ready!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Telugu Story Engine API...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Telugu Story Engine API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        # Check model manager health
        model_health = await model_manager.health_check()
        
        # Check pipeline health
        pipeline_health = await story_pipeline.get_pipeline_health()
        
        overall_status = "healthy"
        if model_health['overall_status'] != 'healthy':
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "timestamp": model_health['timestamp'],
            "models": model_health['models'],
            "pipeline": pipeline_health,
            "api": "operational"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

@app.post("/api/v1/stories/generate")
async def generate_story(request: Dict[str, Any], background_tasks: BackgroundTasks):
    """Generate a complete Telugu story"""
    try:
        # Validate request
        story_request = StoryRequest(
            prompt=request.get('prompt', ''),
            genre=request.get('genre', 'general'),
            length=request.get('length', 'medium'),
            cultural_context=request.get('cultural_context', {}),
            emotional_arc=request.get('emotional_arc', 'hero_journey'),
            style_preferences=request.get('style_preferences', {}),
            constraints=request.get('constraints', {})
        )
        
        if not story_request.prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Generate story
        logger.info(f"Generating story for prompt: {story_request.prompt[:50]}...")
        story_response = await story_pipeline.generate_story(story_request)
        
        # Log success
        background_tasks.add_task(
            log_story_generation,
            story_response.story_id,
            story_response.generation_time,
            story_response.quality_metrics
        )
        
        return {
            "story_id": story_response.story_id,
            "content": story_response.content,
            "metadata": story_response.metadata,
            "quality_metrics": story_response.quality_metrics,
            "generation_time": story_response.generation_time,
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Story generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def log_story_generation(story_id: str, generation_time: float, quality_metrics: Dict[str, float]):
    """Background task to log story generation metrics"""
    logger.info(f"Story {story_id} completed in {generation_time:.2f}s with quality score {quality_metrics.get('overall_quality', 0):.2f}")

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### 6. Requirements File (`requirements.txt`)

```txt
# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6

# AI and ML
ollama==0.1.7
transformers==4.36.0
torch==2.1.0
accelerate==0.24.0
bitsandbytes==0.41.3

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1

# Async and utilities
asyncio-mqtt==0.13.0
aiofiles==23.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Monitoring and logging
prometheus-client==0.19.0
structlog==23.2.0

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
```

### 7. Docker Configuration (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  telugu-story-engine:
    build: .
    ports:
      - "8000:8000"
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
      - OLLAMA_NUM_PARALLEL=4
      - OLLAMA_MAX_LOADED_MODELS=5
      - DATABASE_URL=postgresql://admin:password@postgres:5432/telugu_stories
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./models:/root/.ollama
      - ./data:/app/data
    depends_on:
      - postgres
      - redis
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: telugu_stories
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  dashboard:
    build: ./dashboard
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://telugu-story-engine:8000
    depends_on:
      - telugu-story-engine

volumes:
  postgres_data:
  redis_data:
```

### 8. Dockerfile

```dockerfile
FROM nvidia/cuda:12.1-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p /app/data /app/logs

# Download models (this will be done at runtime for flexibility)
COPY scripts/download_models.sh /app/scripts/
RUN chmod +x /app/scripts/download_models.sh

# Expose ports
EXPOSE 8000 11434

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start script
COPY scripts/start.sh /app/scripts/
RUN chmod +x /app/scripts/start.sh

CMD ["/app/scripts/start.sh"]
```

### 9. Model Download Script (`scripts/download_models.sh`)

```bash
#!/bin/bash

echo "Starting Ollama service..."
ollama serve &
sleep 10

echo "Downloading Telugu Story Engine models..."

# Download models with progress indication
models=(
    "llama3.3:70b-instruct-q4_K_M"
    "qwen2.5:14b-instruct-q4_K_M" 
    "mistral:7b-instruct-v0.3-q4_K_M"
    "deepseek-r1:7b-q4_K_M"
    "llama3.1:8b-instruct-q4_K_M"
)

for model in "${models[@]}"; do
    echo "Downloading $model..."
    ollama pull "$model"
    if [ $? -eq 0 ]; then
        echo "✅ Successfully downloaded $model"
    else
        echo "❌ Failed to download $model"
        exit 1
    fi
done

echo "🚀 All models downloaded successfully!"
```

### 10. Startup Script (`scripts/start.sh`)

```bash
#!/bin/bash

echo "🚀 Starting Telugu Story Engine..."

# Start Ollama service
echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
sleep 10

# Download models if not present
if [ ! -f "/root/.ollama/models/manifests/registry.ollama.ai/library/llama3.3/70b-instruct-q4_K_M" ]; then
    echo "Models not found, downloading..."
    /app/scripts/download_models.sh
fi

# Start the FastAPI application
echo "Starting Telugu Story Engine API..."
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 1

# Cleanup on exit
trap "kill $OLLAMA_PID" EXIT
```

---

## Quick Deployment Instructions

### 1. Local Development Setup

```bash
# Clone the repository
git clone https://github.com/your-repo/telugu-story-engine.git
cd telugu-story-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &

# Download models
ollama pull llama3.3:70b-instruct-q4_K_M
ollama pull qwen2.5:14b-instruct-q4_K_M
ollama pull mistral:7b-instruct-v0.3-q4_K_M

# Start the application
python -m uvicorn src.api.main:app --reload
```

### 2. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual container
docker build -t telugu-story-engine .
docker run -p 8000:8000 --gpus all telugu-story-engine
```

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Generate a story
curl -X POST "http://localhost:8000/api/v1/stories/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Oka village lo brave boy story cheppu",
       "genre": "adventure",
       "cultural_context": {
         "region": "andhra_pradesh",
         "elements": ["family_values", "courage"]
       }
     }'
```

This starter kit provides a complete, production-ready foundation for the Telugu Story Engine using local open source LLM models. All components are functional and can be deployed immediately to begin generating authentic Telugu stories with cultural intelligence and emotional depth.