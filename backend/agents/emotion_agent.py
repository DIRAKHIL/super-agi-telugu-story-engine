"""
Emotion Analysis Agent
Specialized agent for emotion and sentiment analysis in Telugu stories
"""
import asyncio
import time
from typing import Dict, List, Any, Optional
import logging

from .base_agent import BaseAgent, AgentTask, AgentResult, AgentStatus
from ..models.emotion_analyzer import TeluguEmotionAnalyzer, EmotionAnalysisRequest

logger = logging.getLogger(__name__)


class EmotionAgent(BaseAgent):
    """Agent specialized in emotion and sentiment analysis"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, "emotion_analyzer", config)
        
        self.emotion_analyzer: Optional[TeluguEmotionAnalyzer] = None
        self.capabilities = [
            "analyze_emotions",
            "analyze_sentiment", 
            "emotional_arc_analysis",
            "cultural_emotion_mapping",
            "character_emotion_profiling"
        ]
        
        # Analysis statistics
        self.texts_analyzed = 0
        self.total_processing_time = 0.0
        self.emotion_distribution = {}
    
    async def initialize(self) -> bool:
        """Initialize the emotion analysis model"""
        try:
            logger.info(f"Initializing emotion analyzer for agent {self.agent_id}")
            
            self.emotion_analyzer = TeluguEmotionAnalyzer(
                config=self.config.get("model_config", {})
            )
            
            # Load the model
            success = await self.emotion_analyzer.load_model()
            
            if success:
                logger.info(f"Emotion agent {self.agent_id} initialized successfully")
                return True
            else:
                logger.error(f"Failed to load emotion analysis model for agent {self.agent_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing emotion agent {self.agent_id}: {str(e)}")
            return False
    
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute emotion analysis task"""
        start_time = time.time()
        
        try:
            if task.task_type == "analyze_emotions":
                return await self._analyze_emotions(task)
            elif task.task_type == "analyze_sentiment":
                return await self._analyze_sentiment(task)
            elif task.task_type == "emotional_arc_analysis":
                return await self._emotional_arc_analysis(task)
            elif task.task_type == "cultural_emotion_mapping":
                return await self._cultural_emotion_mapping(task)
            elif task.task_type == "character_emotion_profiling":
                return await self._character_emotion_profiling(task)
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
    
    async def _analyze_emotions(self, task: AgentTask) -> AgentResult:
        """Analyze emotions in text"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            text = input_data.get("text", "")
            
            if not text:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=False,
                    result=None,
                    error="No text provided for emotion analysis",
                    execution_time=time.time() - start_time
                )
            
            # Create emotion analysis request
            analysis_request = EmotionAnalysisRequest(
                text=text,
                analyze_sentiment=input_data.get("analyze_sentiment", True),
                analyze_emotions=True,
                context=input_data.get("context")
            )
            
            # Perform analysis
            model_response = await self.emotion_analyzer.predict(analysis_request)
            
            if model_response.success:
                # Update statistics
                self.texts_analyzed += 1
                execution_time = time.time() - start_time
                self.total_processing_time += execution_time
                
                # Update emotion distribution
                analysis_data = model_response.data
                for emotion in analysis_data.get("emotions", []):
                    emotion_name = emotion.get("emotion", "unknown")
                    self.emotion_distribution[emotion_name] = (
                        self.emotion_distribution.get(emotion_name, 0) + 1
                    )
                
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=True,
                    result=analysis_data,
                    execution_time=execution_time,
                    metadata={
                        "text_length": len(text),
                        "emotions_detected": len(analysis_data.get("emotions", [])),
                        "dominant_emotion": analysis_data.get("dominant_emotion"),
                        "agent_stats": self.get_analysis_stats()
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
    
    async def _analyze_sentiment(self, task: AgentTask) -> AgentResult:
        """Analyze sentiment only"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            text = input_data.get("text", "")
            
            analysis_request = EmotionAnalysisRequest(
                text=text,
                analyze_sentiment=True,
                analyze_emotions=False,
                context=input_data.get("context")
            )
            
            model_response = await self.emotion_analyzer.predict(analysis_request)
            
            if model_response.success:
                sentiment_data = model_response.data.get("sentiment")
                
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=True,
                    result={
                        "sentiment": sentiment_data,
                        "text": text
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
    
    async def _emotional_arc_analysis(self, task: AgentTask) -> AgentResult:
        """Analyze emotional arc of a complete story"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            story_text = input_data.get("story", "")
            
            if not story_text:
                return AgentResult(
                    task_id=task.id,
                    agent_id=self.agent_id,
                    success=False,
                    result=None,
                    error="No story text provided",
                    execution_time=time.time() - start_time
                )
            
            # Split story into segments for arc analysis
            segments = self._split_story_into_segments(story_text)
            
            emotional_arc = []
            segment_analyses = []
            
            for i, segment in enumerate(segments):
                analysis_request = EmotionAnalysisRequest(
                    text=segment,
                    analyze_sentiment=True,
                    analyze_emotions=True
                )
                
                model_response = await self.emotion_analyzer.predict(analysis_request)
                
                if model_response.success:
                    analysis_data = model_response.data
                    emotional_arc.append(analysis_data.get("dominant_emotion", "neutral"))
                    segment_analyses.append({
                        "segment_index": i,
                        "text": segment[:100] + "..." if len(segment) > 100 else segment,
                        "emotions": analysis_data.get("emotions", []),
                        "sentiment": analysis_data.get("sentiment"),
                        "dominant_emotion": analysis_data.get("dominant_emotion")
                    })
                else:
                    emotional_arc.append("unknown")
                    segment_analyses.append({
                        "segment_index": i,
                        "error": model_response.error
                    })
                
                # Small delay between segments
                await asyncio.sleep(0.1)
            
            # Analyze arc patterns
            arc_analysis = self._analyze_arc_patterns(emotional_arc)
            
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=True,
                result={
                    "emotional_arc": emotional_arc,
                    "segment_analyses": segment_analyses,
                    "arc_analysis": arc_analysis,
                    "total_segments": len(segments)
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
    
    async def _cultural_emotion_mapping(self, task: AgentTask) -> AgentResult:
        """Map emotions to Telugu cultural contexts"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            emotions = input_data.get("emotions", [])
            context = input_data.get("context", "general")
            
            cultural_mappings = {
                "family": {
                    "ఆనందం": ["కుటుంబ సంతోషం", "పిల్లల విజయం", "వివాహ ఆనందం"],
                    "దుఃఖం": ["వియోగం", "కుటుంబ సమస్యలు", "పెద్దల అనారోగ్యం"],
                    "గర్వం": ["కుటుంబ గౌరవం", "సంప్రదాయ పాలన", "పిల్లల సాఫల్యం"],
                    "కోపం": ["అన్యాయం", "కుటుంబ అవమానం", "సంప్రదాయ ఉల్లంఘన"]
                },
                "social": {
                    "ఆనందం": ["సామాజిక గుర్తింపు", "సమాజ సేవ", "మిత్రుల మధ్య"],
                    "దుఃఖం": ["సామాజిక బహిష్కరణ", "అవమానం", "ఒంటరితనం"],
                    "గర్వం": ["సామాజిక స్థానం", "గౌరవం", "నాయకత్వం"],
                    "కోపం": ["అన్యాయం", "అవమానం", "సామాజిక అసమానత"]
                }
            }
            
            mapped_emotions = []
            for emotion in emotions:
                emotion_name = emotion.get("emotion", "")
                cultural_contexts = cultural_mappings.get(context, {}).get(emotion_name, [])
                
                mapped_emotions.append({
                    "emotion": emotion_name,
                    "confidence": emotion.get("confidence", 0.0),
                    "cultural_contexts": cultural_contexts,
                    "cultural_relevance": len(cultural_contexts) > 0
                })
            
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=True,
                result={
                    "mapped_emotions": mapped_emotions,
                    "context": context,
                    "total_emotions": len(emotions),
                    "culturally_relevant": sum(1 for e in mapped_emotions if e["cultural_relevance"])
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
    
    async def _character_emotion_profiling(self, task: AgentTask) -> AgentResult:
        """Create emotional profiles for characters"""
        start_time = time.time()
        
        try:
            input_data = task.input_data
            character_dialogues = input_data.get("character_dialogues", {})
            
            character_profiles = {}
            
            for character_name, dialogues in character_dialogues.items():
                character_emotions = []
                
                for dialogue in dialogues:
                    analysis_request = EmotionAnalysisRequest(
                        text=dialogue,
                        analyze_emotions=True,
                        analyze_sentiment=True
                    )
                    
                    model_response = await self.emotion_analyzer.predict(analysis_request)
                    
                    if model_response.success:
                        analysis_data = model_response.data
                        character_emotions.extend(analysis_data.get("emotions", []))
                    
                    await asyncio.sleep(0.05)
                
                # Aggregate emotions for character
                emotion_counts = {}
                total_confidence = 0
                
                for emotion in character_emotions:
                    emotion_name = emotion.get("emotion", "unknown")
                    confidence = emotion.get("confidence", 0.0)
                    
                    if emotion_name not in emotion_counts:
                        emotion_counts[emotion_name] = {"count": 0, "total_confidence": 0.0}
                    
                    emotion_counts[emotion_name]["count"] += 1
                    emotion_counts[emotion_name]["total_confidence"] += confidence
                    total_confidence += confidence
                
                # Calculate character emotional profile
                character_profile = {
                    "dominant_emotions": [],
                    "emotional_range": len(emotion_counts),
                    "emotional_intensity": total_confidence / len(character_emotions) if character_emotions else 0.0,
                    "dialogue_count": len(dialogues)
                }
                
                # Sort emotions by frequency and confidence
                sorted_emotions = sorted(
                    emotion_counts.items(),
                    key=lambda x: (x[1]["count"], x[1]["total_confidence"]),
                    reverse=True
                )
                
                for emotion_name, stats in sorted_emotions[:5]:  # Top 5 emotions
                    character_profile["dominant_emotions"].append({
                        "emotion": emotion_name,
                        "frequency": stats["count"],
                        "average_confidence": stats["total_confidence"] / stats["count"]
                    })
                
                character_profiles[character_name] = character_profile
            
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                success=True,
                result={
                    "character_profiles": character_profiles,
                    "total_characters": len(character_dialogues)
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
    
    def _split_story_into_segments(self, story: str, segment_size: int = 500) -> List[str]:
        """Split story into segments for arc analysis"""
        words = story.split()
        segments = []
        
        for i in range(0, len(words), segment_size):
            segment = " ".join(words[i:i + segment_size])
            segments.append(segment)
        
        return segments
    
    def _analyze_arc_patterns(self, emotional_arc: List[str]) -> Dict[str, Any]:
        """Analyze patterns in emotional arc"""
        if not emotional_arc:
            return {"pattern": "no_data"}
        
        # Count emotion transitions
        transitions = {}
        for i in range(len(emotional_arc) - 1):
            current = emotional_arc[i]
            next_emotion = emotional_arc[i + 1]
            transition = f"{current} -> {next_emotion}"
            transitions[transition] = transitions.get(transition, 0) + 1
        
        # Identify arc type
        arc_type = "unknown"
        if len(emotional_arc) >= 3:
            start = emotional_arc[0]
            middle = emotional_arc[len(emotional_arc) // 2]
            end = emotional_arc[-1]
            
            if start in ["ఆనందం", "neutral"] and middle in ["దుఃఖం", "కోపం"] and end in ["ఆనందం"]:
                arc_type = "classic_hero_journey"
            elif start in ["ఆనందం"] and end in ["దుఃఖం"]:
                arc_type = "tragedy"
            elif start in ["దుఃఖం"] and end in ["ఆనందం"]:
                arc_type = "redemption"
        
        return {
            "pattern": arc_type,
            "transitions": transitions,
            "arc_length": len(emotional_arc),
            "dominant_emotion": max(set(emotional_arc), key=emotional_arc.count),
            "emotional_variety": len(set(emotional_arc))
        }
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get emotion analysis statistics"""
        return {
            "texts_analyzed": self.texts_analyzed,
            "average_processing_time": (
                self.total_processing_time / self.texts_analyzed 
                if self.texts_analyzed > 0 else 0.0
            ),
            "emotion_distribution": self.emotion_distribution,
            "most_common_emotion": (
                max(self.emotion_distribution.items(), key=lambda x: x[1])[0]
                if self.emotion_distribution else "none"
            )
        }