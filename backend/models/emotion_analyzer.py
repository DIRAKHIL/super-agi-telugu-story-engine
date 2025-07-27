"""
Emotion Analysis Model for Telugu Film Stories
Real AI-powered emotion detection and sentiment analysis
"""
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
import torch
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    pipeline, AutoConfig
)
from pydantic import BaseModel
import numpy as np
import logging

from .base import BaseAIModel, ModelResponse, TeluguModelMixin
from ..core.config import settings

logger = logging.getLogger(__name__)


class EmotionAnalysisRequest(BaseModel):
    """Request model for emotion analysis"""
    text: str
    analyze_sentiment: bool = True
    analyze_emotions: bool = True
    context: Optional[str] = None


class EmotionResult(BaseModel):
    """Emotion analysis result"""
    emotion: str
    confidence: float
    intensity: float  # 0.0 to 1.0


class SentimentResult(BaseModel):
    """Sentiment analysis result"""
    sentiment: str  # positive, negative, neutral
    confidence: float
    polarity_score: float  # -1.0 to 1.0


class EmotionAnalysisResponse(BaseModel):
    """Complete emotion analysis response"""
    text: str
    emotions: List[EmotionResult]
    sentiment: Optional[SentimentResult] = None
    dominant_emotion: str
    emotional_arc: List[str]  # Sequence of emotions
    cultural_context: Dict[str, Any]


class TeluguEmotionAnalyzer(BaseAIModel, TeluguModelMixin):
    """Advanced emotion analysis for Telugu text using real AI models"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("telugu_emotion_analyzer", config)
        
        self.emotion_model = None
        self.emotion_tokenizer = None
        self.sentiment_model = None
        self.sentiment_tokenizer = None
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Telugu emotion mappings
        self.emotion_labels = {
            "joy": "ఆనందం",
            "sadness": "దుఃఖం", 
            "anger": "కోపం",
            "fear": "భయం",
            "surprise": "ఆశ్చర్యం",
            "disgust": "అసహ్యం",
            "love": "ప్రేమ",
            "pride": "గర్వం",
            "shame": "సిగ్గు",
            "guilt": "అపరాధభావన"
        }
        
        # Cultural emotion contexts
        self.cultural_emotions = {
            "family_respect": ["గౌరవం", "భక్తి", "కృతజ్ఞత"],
            "social_harmony": ["సామరస్యం", "సహకారం", "ఐక్యత"],
            "traditional_values": ["సంస్కృతి", "సంప్రదాయం", "ధర్మం"],
            "modern_conflicts": ["గందరగోళం", "సంఘర్షణ", "మార్పు"]
        }
    
    async def load_model(self) -> bool:
        """Load emotion and sentiment analysis models"""
        try:
            logger.info("Loading emotion analysis models...")
            
            # Load emotion model
            emotion_model_name = settings.TELUGU_EMOTION_MODEL
            self.emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
            self.emotion_model = AutoModelForSequenceClassification.from_pretrained(
                emotion_model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)
            
            # Load sentiment model
            sentiment_model_name = settings.TELUGU_SENTIMENT_MODEL
            self.sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
                sentiment_model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)
            
            self.is_loaded = True
            logger.info(f"Emotion analysis models loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading emotion analysis models: {str(e)}")
            return False
    
    async def predict(self, input_data: EmotionAnalysisRequest, **kwargs) -> ModelResponse:
        """Analyze emotions and sentiment in Telugu text"""
        start_time = time.time()
        
        try:
            if not self.is_loaded:
                await self.load_model()
            
            text = self.preprocess_telugu_text(input_data.text)
            
            # Analyze emotions
            emotions = []
            if input_data.analyze_emotions:
                emotions = await self._analyze_emotions(text)
            
            # Analyze sentiment
            sentiment = None
            if input_data.analyze_sentiment:
                sentiment = await self._analyze_sentiment(text)
            
            # Determine dominant emotion
            dominant_emotion = emotions[0].emotion if emotions else "neutral"
            
            # Generate emotional arc
            emotional_arc = self._generate_emotional_arc(text, emotions)
            
            # Add cultural context
            cultural_context = self._analyze_cultural_context(text, emotions)
            
            response_data = EmotionAnalysisResponse(
                text=text,
                emotions=emotions,
                sentiment=sentiment,
                dominant_emotion=dominant_emotion,
                emotional_arc=emotional_arc,
                cultural_context=cultural_context
            )
            
            processing_time = time.time() - start_time
            
            return ModelResponse(
                success=True,
                data=response_data.dict(),
                confidence=np.mean([e.confidence for e in emotions]) if emotions else 0.0,
                processing_time=processing_time,
                model_name=self.model_name
            )
            
        except Exception as e:
            logger.error(f"Error analyzing emotions: {str(e)}")
            return ModelResponse(
                success=False,
                data=None,
                model_name=self.model_name,
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    async def batch_predict(self, input_batch: List[EmotionAnalysisRequest], **kwargs) -> List[ModelResponse]:
        """Analyze emotions for multiple texts"""
        results = []
        
        for request in input_batch:
            result = await self.predict(request, **kwargs)
            results.append(result)
            await asyncio.sleep(0.05)  # Small delay
        
        return results
    
    async def _analyze_emotions(self, text: str) -> List[EmotionResult]:
        """Analyze emotions in the text"""
        try:
            # Tokenize input
            inputs = self.emotion_tokenizer(
                text,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            ).to(self.device)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.emotion_model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get emotion labels from model config
            config = AutoConfig.from_pretrained(settings.TELUGU_EMOTION_MODEL)
            labels = config.id2label if hasattr(config, 'id2label') else list(self.emotion_labels.keys())
            
            # Create emotion results
            emotions = []
            for i, (label, score) in enumerate(zip(labels, predictions[0])):
                if score.item() > 0.1:  # Only include emotions with reasonable confidence
                    telugu_emotion = self.emotion_labels.get(label, label)
                    emotions.append(EmotionResult(
                        emotion=telugu_emotion,
                        confidence=float(score.item()),
                        intensity=min(float(score.item()) * 1.2, 1.0)  # Slightly boost intensity
                    ))
            
            # Sort by confidence
            emotions.sort(key=lambda x: x.confidence, reverse=True)
            
            return emotions[:5]  # Return top 5 emotions
            
        except Exception as e:
            logger.error(f"Error in emotion analysis: {str(e)}")
            return []
    
    async def _analyze_sentiment(self, text: str) -> SentimentResult:
        """Analyze sentiment in the text"""
        try:
            # Tokenize input
            inputs = self.sentiment_tokenizer(
                text,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            ).to(self.device)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.sentiment_model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Map to sentiment labels
            sentiment_labels = ["negative", "neutral", "positive"]
            sentiment_scores = predictions[0].cpu().numpy()
            
            # Get dominant sentiment
            dominant_idx = np.argmax(sentiment_scores)
            dominant_sentiment = sentiment_labels[dominant_idx]
            confidence = float(sentiment_scores[dominant_idx])
            
            # Calculate polarity score (-1 to 1)
            polarity_score = float(sentiment_scores[2] - sentiment_scores[0])  # positive - negative
            
            return SentimentResult(
                sentiment=dominant_sentiment,
                confidence=confidence,
                polarity_score=polarity_score
            )
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return SentimentResult(
                sentiment="neutral",
                confidence=0.0,
                polarity_score=0.0
            )
    
    def _generate_emotional_arc(self, text: str, emotions: List[EmotionResult]) -> List[str]:
        """Generate emotional arc for the story"""
        if not emotions:
            return ["neutral"]
        
        # Split text into segments and analyze emotional progression
        sentences = text.split('.')
        arc = []
        
        # Simple emotional arc based on dominant emotions
        if len(emotions) >= 3:
            arc = [emotions[0].emotion, emotions[1].emotion, emotions[2].emotion]
        elif len(emotions) >= 2:
            arc = [emotions[0].emotion, emotions[1].emotion]
        else:
            arc = [emotions[0].emotion]
        
        return arc
    
    def _analyze_cultural_context(self, text: str, emotions: List[EmotionResult]) -> Dict[str, Any]:
        """Analyze cultural context of emotions"""
        context = {
            "cultural_themes": [],
            "family_dynamics": False,
            "traditional_values": False,
            "modern_elements": False,
            "regional_context": None
        }
        
        # Check for cultural keywords
        text_lower = text.lower()
        
        # Family dynamics
        family_keywords = ["కుటుంబం", "తల్లి", "తండ్రి", "అన్న", "అక్క", "తమ్మి", "చెల్లి"]
        if any(keyword in text for keyword in family_keywords):
            context["family_dynamics"] = True
            context["cultural_themes"].append("family_bonds")
        
        # Traditional values
        traditional_keywords = ["సంస్కృతి", "సంప్రదాయం", "పండుగ", "దేవుడు", "ధర్మం"]
        if any(keyword in text for keyword in traditional_keywords):
            context["traditional_values"] = True
            context["cultural_themes"].append("traditional_values")
        
        # Modern elements
        modern_keywords = ["టెక్నాలజీ", "కంప్యూటర్", "మొబైల్", "ఇంటర్నెట్", "సోషల్ మీడియా"]
        if any(keyword in text for keyword in modern_keywords):
            context["modern_elements"] = True
            context["cultural_themes"].append("modernity")
        
        # Regional context (basic detection)
        regions = ["హైదరాబాద్", "విజయవాడ", "విశాఖపట్నం", "తిరుపతి"]
        for region in regions:
            if region in text:
                context["regional_context"] = region
                break
        
        return context
    
    def get_emotion_statistics(self) -> Dict[str, Any]:
        """Get emotion analysis statistics"""
        return {
            "supported_emotions": list(self.emotion_labels.values()),
            "cultural_contexts": list(self.cultural_emotions.keys()),
            "model_info": {
                "emotion_model": settings.TELUGU_EMOTION_MODEL,
                "sentiment_model": settings.TELUGU_SENTIMENT_MODEL,
                "device": str(self.device),
                "is_loaded": self.is_loaded
            }
        }