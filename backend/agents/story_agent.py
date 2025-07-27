"""
Story Generation Agent
Specialized agent for Telugu story generation tasks
"""
import asyncio
import time
from typing import Dict, List, Any, Optional
import logging

from .base_agent import BaseAgent, AgentTask, AgentResult, AgentStatus
from ..models.story_generator import TeluguStoryGenerator, StoryGenerationRequest

logger = logging.getLogger(__name__)


class StoryAgent(BaseAgent):
    """Agent specialized in Telugu story generation"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, "story_generator", config)
        
        self.story_generator: Optional[TeluguStoryGenerator] = None
        self.capabilities = [
            "generate_story",
            "enhance_plot",
            "develop_characters",
            "create_dialogue",
            "structure_narrative"
        ]
        
        # Story generation statistics
        self.stories_generated = 0
        self.total_words_generated = 0
        self.average_generation_time = 0.0
    
    async def initialize(self) -> bool:
        """Initialize the story generation model"""
        try:
            logger.info(f"Initializing story generator for agent {self.agent_id}")
            
            self.story_generator = TeluguStoryGenerator(
                config=self.config.get("model_config", {})
            )
            
            # Load the model
            success = await self.story_generator.load_model()
            
            if success:
                logger.info(f"Story agent {self.agent_id} initialized successfully")
                return True
            else:
                logger.error(f"Failed to load story generation model for agent {self.agent_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing story agent {self.agent_id}: {str(e)}")
            return False
    
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute story generation task"""
        start_time = time.time()
        
        try:
            if task.task_type == "generate_story":
                return await self._generate_story(task)
            elif task.task_type == "enhance_plot":
                return await self._enhance_plot(task)
            elif task.task_type == "develop_characters":
                return await self._develop_characters(task)
            elif task.task_type == "create_dialogue":
                return await self._create_dialogue(task)
            elif task.task_type == "structure_narrative":
                return await self._structure_narrative(task)
            else:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=False,
                    result=None,
                    error=f"Unknown task type: {task.task_type}",
                    execution_time=time.time() - start_time
                )
                
        except Exception as e:
            logger.error(f"Error executing task {task.id} in agent {self.agent_id}: {str(e)}")
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _generate_story(self, task: AgentTask) -> AgentResult:
        """Generate a complete Telugu story"""
        start_time = time.time()
        
        try:
            # Parse input data
            input_data = task.input_data
            
            # Create story generation request
            story_request = StoryGenerationRequest(
                prompt=input_data.get("prompt", ""),
                genre=input_data.get("genre", "drama"),
                characters=input_data.get("characters", []),
                setting=input_data.get("setting", "modern"),
                theme=input_data.get("theme", "family"),
                max_length=input_data.get("max_length", 2000),
                temperature=input_data.get("temperature", 0.8),
                top_p=input_data.get("top_p", 0.9),
                top_k=input_data.get("top_k", 50)
            )
            
            # Generate story
            model_response = await self.story_generator.predict(story_request)
            
            if model_response.success:
                # Update statistics
                self.stories_generated += 1
                story_data = model_response.data
                word_count = story_data["metadata"]["word_count"]
                self.total_words_generated += word_count
                
                execution_time = time.time() - start_time
                self.average_generation_time = (
                    (self.average_generation_time * (self.stories_generated - 1) + execution_time) 
                    / self.stories_generated
                )
                
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=True,
                    result=story_data,
                    execution_time=execution_time,
                    metadata={
                        "word_count": word_count,
                        "genre": story_request.genre,
                        "theme": story_request.theme,
                        "agent_stats": self.get_generation_stats()
                    }
                )
            else:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=False,
                    result=None,
                    error=model_response.error,
                    execution_time=time.time() - start_time
                )
                
        except Exception as e:
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _enhance_plot(self, task: AgentTask) -> AgentResult:
        """Enhance an existing plot"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            existing_plot = input_data.get("plot", "")
            enhancement_type = input_data.get("enhancement_type", "general")
            
            # Create enhancement prompt
            enhancement_prompts = {
                "conflict": "కథలో మరింత సంఘర్షణ మరియు టెన్షన్ జోడించండి:",
                "emotion": "కథలో భావోద్వేగాలను మరింత లోతుగా చేయండి:",
                "character": "పాత్రల అభివృద్ధిని మరింత మెరుగుపరచండి:",
                "cultural": "తెలుగు సాంస్కృతిక అంశాలను మరింత జోడించండి:",
                "general": "కథను మరింత ఆకర్షణీయంగా మరియు పూర్తిగా చేయండి:"
            }
            
            prompt = enhancement_prompts.get(enhancement_type, enhancement_prompts["general"])
            full_prompt = f"{prompt}\n\nమూల కథ: {existing_plot}\n\nమెరుగుపరచిన కథ:"
            
            story_request = StoryGenerationRequest(
                prompt=full_prompt,
                genre=input_data.get("genre", "drama"),
                max_length=input_data.get("max_length", 1500),
                temperature=0.7  # Slightly lower for more focused enhancement
            )
            
            model_response = await self.story_generator.predict(story_request)
            
            if model_response.success:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=True,
                    result={
                        "enhanced_plot": model_response.data["story"],
                        "enhancement_type": enhancement_type,
                        "original_plot": existing_plot,
                        "metadata": model_response.data["metadata"]
                    },
                    execution_time=time.time() - start_time
                )
            else:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=False,
                    result=None,
                    error=model_response.error,
                    execution_time=time.time() - start_time
                )
                
        except Exception as e:
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _develop_characters(self, task: AgentTask) -> AgentResult:
        """Develop character profiles and backgrounds"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            characters = input_data.get("characters", [])
            context = input_data.get("context", "")
            
            character_developments = []
            
            for character in characters:
                prompt = f"""
పాత్ర అభివృద్ధి:
పేరు: {character}
సందర్భం: {context}

ఈ పాత్ర గురించి వివరణాత్మక ప్రొఫైల్ రాయండి:
- వ్యక్తిత్వం
- నేపథ్యం
- లక్ష్యాలు మరియు కోరికలు
- బలాలు మరియు బలహీనతలు
- కుటుంబ నేపథ్యం
- సామాజిక స్థితి

పాత్ర వివరణ:
"""
                
                story_request = StoryGenerationRequest(
                    prompt=prompt,
                    max_length=800,
                    temperature=0.7
                )
                
                model_response = await self.story_generator.predict(story_request)
                
                if model_response.success:
                    character_developments.append({
                        "name": character,
                        "profile": model_response.data["story"],
                        "metadata": model_response.data["metadata"]
                    })
                else:
                    character_developments.append({
                        "name": character,
                        "profile": f"పాత్ర అభివృద్ధిలో లోపం: {model_response.error}",
                        "error": model_response.error
                    })
                
                # Small delay between character generations
                await asyncio.sleep(0.1)
            
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=True,
                result={
                    "character_developments": character_developments,
                    "total_characters": len(characters)
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _create_dialogue(self, task: AgentTask) -> AgentResult:
        """Create dialogue for specific scenes"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            scene_description = input_data.get("scene", "")
            characters = input_data.get("characters", [])
            emotion = input_data.get("emotion", "neutral")
            
            prompt = f"""
దృశ్య వివరణ: {scene_description}
పాత్రలు: {', '.join(characters)}
భావోద్వేగం: {emotion}

ఈ దృశ్యానికి సహజమైన మరియు భావోద్వేగపూర్వకమైన సంభాషణ రాయండి:

సంభాషణ:
"""
            
            story_request = StoryGenerationRequest(
                prompt=prompt,
                max_length=1000,
                temperature=0.8
            )
            
            model_response = await self.story_generator.predict(story_request)
            
            if model_response.success:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=True,
                    result={
                        "dialogue": model_response.data["story"],
                        "scene": scene_description,
                        "characters": characters,
                        "emotion": emotion,
                        "metadata": model_response.data["metadata"]
                    },
                    execution_time=time.time() - start_time
                )
            else:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=False,
                    result=None,
                    error=model_response.error,
                    execution_time=time.time() - start_time
                )
                
        except Exception as e:
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _structure_narrative(self, task: AgentTask) -> AgentResult:
        """Structure narrative with proper story arc"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            raw_story = input_data.get("story", "")
            structure_type = input_data.get("structure", "three_act")
            
            structure_prompts = {
                "three_act": """
ఈ కథను మూడు అంకాల నిర్మాణంలో (Three-Act Structure) క్రమబద్ధీకరించండి:

అంకం 1 - స్థాపన (Setup):
- పాత్రల పరిచయం
- పరిస్థితి స్థాపన
- సమస్య లేదా లక్ష్యం

అంకం 2 - సంఘర్షణ (Confrontation):
- సమస్య తీవ్రీకరణ
- పాత్రల పోరాటం
- క్లైమాక్స్ వైపు నిర్మాణం

అంకం 3 - పరిష్కారం (Resolution):
- క్లైమాక్స్
- సమస్య పరిష్కారం
- ముగింపు

మూల కథ: {raw_story}

నిర్మాణాత్మక కథ:
""",
                "hero_journey": """
ఈ కథను హీరో జర్నీ నిర్మాణంలో క్రమబద్ధీకరించండి:

1. సాధారణ ప్రపంచం
2. సాహసానికి పిలుపు
3. పిలుపును తిరస్కరించడం
4. గురువు కలవడం
5. మొదటి అడుగు
6. పరీక్షలు మరియు మిత్రులు
7. అంతర్గత గుహలోకి ప్రవేశం
8. పరీక్ష
9. బహుమతి
10. తిరుగు ప్రయాణం
11. పునర్జన్మ
12. అమృతంతో తిరుగు రాక

మూల కథ: {raw_story}

హీరో జర్నీ కథ:
"""
            }
            
            prompt = structure_prompts.get(structure_type, structure_prompts["three_act"])
            
            story_request = StoryGenerationRequest(
                prompt=prompt,
                max_length=2500,
                temperature=0.7
            )
            
            model_response = await self.story_generator.predict(story_request)
            
            if model_response.success:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=True,
                    result={
                        "structured_story": model_response.data["story"],
                        "structure_type": structure_type,
                        "original_story": raw_story,
                        "metadata": model_response.data["metadata"]
                    },
                    execution_time=time.time() - start_time
                )
            else:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=False,
                    result=None,
                    error=model_response.error,
                    execution_time=time.time() - start_time
                )
                
        except Exception as e:
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get story generation statistics"""
        return {
            "stories_generated": self.stories_generated,
            "total_words_generated": self.total_words_generated,
            "average_generation_time": self.average_generation_time,
            "average_words_per_story": (
                self.total_words_generated / self.stories_generated 
                if self.stories_generated > 0 else 0
            )
        }