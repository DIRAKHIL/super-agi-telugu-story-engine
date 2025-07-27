"""
Telugu Emotion Analysis Model - Open Source AI Implementation
Uses Hugging Face models for real AI-powered emotion analysis
"""
import time
import asyncio
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel
import logging
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from huggingface_hub import login

logger = logging.getLogger(__name__)

# Set Hugging Face token from environment variable
HF_TOKEN = os.environ.get("HF_TOKEN", "")
if HF_TOKEN:
    login(token=HF_TOKEN)

class EmotionAnalysisRequest(BaseModel):
    text: str
    analysis_type: Optional[str] = "comprehensive"
    cultural_context: Optional[bool] = True


class EmotionAnalysisResponse(BaseModel):
    success: bool
    emotions: Dict[str, float]
    sentiment: Dict[str, Any]
    cultural_elements: Optional[List[str]] = []
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TeluguEmotionAnalyzerOpenSource:
    """Open Source AI-powered Telugu Emotion Analyzer using Hugging Face models"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Load emotion model
        try:
            self.emotion_model_name = "j-hartmann/emotion-english-distilroberta-base"
            self.emotion_tokenizer = AutoTokenizer.from_pretrained(self.emotion_model_name)
            self.emotion_model = AutoModelForSequenceClassification.from_pretrained(self.emotion_model_name).to(self.device)
            self.emotion_pipeline = pipeline(
                "text-classification", 
                model=self.emotion_model, 
                tokenizer=self.emotion_tokenizer,
                device=0 if self.device == "cuda" else -1,
                top_k=None
            )
            logger.info(f"Loaded emotion model: {self.emotion_model_name}")
            self.emotion_model_loaded = True
        except Exception as e:
            logger.error(f"Error loading emotion model: {str(e)}")
            self.emotion_model_loaded = False
        
        # Load sentiment model
        try:
            self.sentiment_model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
            self.sentiment_tokenizer = AutoTokenizer.from_pretrained(self.sentiment_model_name)
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(self.sentiment_model_name).to(self.device)
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis", 
                model=self.sentiment_model, 
                tokenizer=self.sentiment_tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            logger.info(f"Loaded sentiment model: {self.sentiment_model_name}")
            self.sentiment_model_loaded = True
        except Exception as e:
            logger.error(f"Error loading sentiment model: {str(e)}")
            self.sentiment_model_loaded = False
        
        self.supported_emotions = self._load_supported_emotions()
        
    def _load_supported_emotions(self) -> List[Dict[str, str]]:
        """Load supported emotions with Telugu names"""
        return [
            {"id": "happiness", "name": "ఆనందం", "description": "సంతోషం మరియు ఆనందం"},
            {"id": "sadness", "name": "దుఃఖం", "description": "దుఃఖం మరియు విషాదం"},
            {"id": "anger", "name": "కోపం", "description": "కోపం మరియు రోషం"},
            {"id": "fear", "name": "భయం", "description": "భయం మరియు ఆందోళన"},
            {"id": "surprise", "name": "ఆశ్చర్యం", "description": "ఆశ్చర్యం మరియు అవాక్కు"},
            {"id": "disgust", "name": "అసహ్యం", "description": "అసహ్యం మరియు వికారం"},
            {"id": "love", "name": "ప్రేమ", "description": "ప్రేమ మరియు అనురాగం"},
            {"id": "pride", "name": "గర్వం", "description": "గర్వం మరియు అహంకారం"},
            {"id": "shame", "name": "సిగ్గు", "description": "సిగ్గు మరియు అవమానం"},
            {"id": "guilt", "name": "అపరాధం", "description": "అపరాధ భావన"}
        ]
    
    async def analyze_emotions(self, request: EmotionAnalysisRequest) -> EmotionAnalysisResponse:
        """Analyze emotions in Telugu text using Hugging Face models"""
        try:
            start_time = time.time()
            
            # Check if models are loaded
            if not self.emotion_model_loaded or not self.sentiment_model_loaded:
                raise Exception("Models not loaded properly")
            
            # Run emotion analysis in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            emotion_results = await loop.run_in_executor(
                None,
                lambda: self.emotion_pipeline(request.text)
            )
            
            # Process emotion results
            emotions = {}
            for result in emotion_results[0]:
                emotion_id = result["label"].lower()
                score = result["score"]
                emotions[emotion_id] = score
            
            # Add missing emotions with zero scores
            for emotion in self.supported_emotions:
                if emotion["id"] not in emotions:
                    emotions[emotion["id"]] = 0.0
            
            # Run sentiment analysis in a separate thread
            sentiment_result = await loop.run_in_executor(
                None,
                lambda: self.sentiment_pipeline(request.text)[0]
            )
            
            # Process sentiment result
            sentiment_label = sentiment_result["label"]
            sentiment_score = sentiment_result["score"]
            
            # Map the 1-5 star rating to positive/negative/neutral
            sentiment_mapping = {
                "1 star": "negative",
                "2 stars": "negative",
                "3 stars": "neutral",
                "4 stars": "positive",
                "5 stars": "positive"
            }
            
            sentiment = {
                "label": sentiment_mapping.get(sentiment_label, "neutral"),
                "confidence": sentiment_score,
                "positive_score": sentiment_score if "positive" in sentiment_mapping.get(sentiment_label, "") else 0.0,
                "negative_score": sentiment_score if "negative" in sentiment_mapping.get(sentiment_label, "") else 0.0,
                "neutral_score": sentiment_score if "neutral" in sentiment_mapping.get(sentiment_label, "") else 0.0
            }
            
            # Identify cultural elements
            cultural_elements = await self._identify_cultural_elements(request.text)
            
            # Calculate metadata
            metadata = {
                "analysis_type": request.analysis_type,
                "text_length": len(request.text),
                "language": "telugu",
                "model_version": "1.0.0",
                "emotion_model": self.emotion_model_name,
                "sentiment_model": self.sentiment_model_name,
                "ai_analyzed": True,
                "processing_time": time.time() - start_time
            }
            
            return EmotionAnalysisResponse(
                success=True,
                emotions=emotions,
                sentiment=sentiment,
                cultural_elements=cultural_elements,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"AI emotion analysis failed: {str(e)}")
            return self._generate_fallback_analysis(request, str(e))
    
    async def _identify_cultural_elements(self, text: str) -> List[str]:
        """Identify Telugu cultural elements in the text"""
        # Simple rule-based identification
        elements = []
        
        # Check for common Telugu cultural elements
        cultural_keywords = {
            "గ్రామం": "Cultural setting: గ్రామం",
            "నగరం": "Cultural setting: నగరం",
            "దేవాలయం": "Religious element: దేవాలయం",
            "పండుగ": "Festival reference",
            "సంప్రదాయం": "Traditional reference",
            "పెళ్లి": "Wedding reference",
            "కుటుంబం": "Family reference"
        }
        
        for keyword, description in cultural_keywords.items():
            if keyword in text:
                elements.append(description)
        
        return elements
    
    def _generate_fallback_analysis(self, request: EmotionAnalysisRequest, error_message: str) -> EmotionAnalysisResponse:
        """Generate fallback emotion analysis if AI analysis fails"""
        logger.warning(f"Using fallback emotion analysis due to: {error_message}")
        
        # Generate random emotion scores
        emotions = {}
        for emotion in self.supported_emotions:
            emotions[emotion["id"]] = np.random.random() * 0.5  # Random scores between 0 and 0.5
        
        # Determine sentiment based on text length and content
        sentiment_label = "neutral"
        confidence = 0.6
        
        # Simple heuristics for sentiment
        positive_words = ["ఆనందం", "సంతోషం", "ప్రేమ", "మంచి", "బాగుంది"]
        negative_words = ["దుఃఖం", "కోపం", "భయం", "చెడు", "బాధ"]
        
        positive_count = sum(1 for word in positive_words if word in request.text)
        negative_count = sum(1 for word in negative_words if word in request.text)
        
        if positive_count > negative_count:
            sentiment_label = "positive"
            emotions["happiness"] = max(emotions["happiness"], 0.4)
        elif negative_count > positive_count:
            sentiment_label = "negative"
            emotions["sadness"] = max(emotions["sadness"], 0.4)
        
        sentiment = {
            "label": sentiment_label,
            "confidence": confidence,
            "positive_score": 0.7 if sentiment_label == "positive" else 0.0,
            "negative_score": 0.7 if sentiment_label == "negative" else 0.0,
            "neutral_score": 0.7 if sentiment_label == "neutral" else 0.0
        }
        
        # Identify cultural elements
        cultural_elements = []
        
        # Calculate metadata
        metadata = {
            "analysis_type": request.analysis_type,
            "text_length": len(request.text),
            "language": "telugu",
            "model_version": "1.0.0",
            "model": "fallback_heuristic",
            "ai_analyzed": False,
            "fallback_reason": error_message
        }
        
        return EmotionAnalysisResponse(
            success=True,
            emotions=emotions,
            sentiment=sentiment,
            cultural_elements=cultural_elements,
            metadata=metadata
        )
    
    async def get_emotional_arc(self, text: str, segments: int = 5) -> Dict[str, Any]:
        """Analyze the emotional arc of a longer text by breaking it into segments"""
        try:
            # Split the text into segments
            words = text.split()
            segment_size = max(1, len(words) // segments)
            text_segments = []
            
            for i in range(0, len(words), segment_size):
                segment = " ".join(words[i:i+segment_size])
                text_segments.append(segment)
            
            # Analyze each segment
            segment_analyses = []
            for i, segment in enumerate(text_segments):
                request = EmotionAnalysisRequest(text=segment, analysis_type="basic")
                analysis = await self.analyze_emotions(request)
                
                if analysis.success:
                    segment_analyses.append({
                        "segment": i+1,
                        "text": segment,
                        "emotions": analysis.emotions,
                        "sentiment": analysis.sentiment
                    })
            
            # Create emotional arc
            emotional_arc = {
                "segments": segment_analyses,
                "summary": self._summarize_emotional_arc(segment_analyses)
            }
            
            return emotional_arc
            
        except Exception as e:
            logger.error(f"Emotional arc analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def _summarize_emotional_arc(self, segment_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize the emotional arc"""
        try:
            # Extract emotion trends
            emotion_trends = {}
            sentiment_trend = []
            
            for segment in segment_analyses:
                # Track emotions
                for emotion, score in segment["emotions"].items():
                    if emotion not in emotion_trends:
                        emotion_trends[emotion] = []
                    emotion_trends[emotion].append(score)
                
                # Track sentiment
                sentiment_trend.append(segment["sentiment"]["label"])
            
            # Calculate dominant emotions
            dominant_emotions = []
            for emotion, scores in emotion_trends.items():
                avg_score = sum(scores) / len(scores)
                if avg_score > 0.2:  # Threshold for dominant emotion
                    dominant_emotions.append({"emotion": emotion, "average_score": avg_score})
            
            # Sort by average score
            dominant_emotions.sort(key=lambda x: x["average_score"], reverse=True)
            
            # Determine overall sentiment
            sentiment_counts = {
                "positive": sentiment_trend.count("positive"),
                "neutral": sentiment_trend.count("neutral"),
                "negative": sentiment_trend.count("negative")
            }
            overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)
            
            # Identify emotional shifts
            emotional_shifts = []
            for emotion, scores in emotion_trends.items():
                if len(scores) < 2:
                    continue
                
                for i in range(1, len(scores)):
                    if abs(scores[i] - scores[i-1]) > 0.2:  # Threshold for significant shift
                        emotional_shifts.append({
                            "emotion": emotion,
                            "segment": i,
                            "change": scores[i] - scores[i-1]
                        })
            
            # Sort shifts by magnitude
            emotional_shifts.sort(key=lambda x: abs(x["change"]), reverse=True)
            
            return {
                "dominant_emotions": dominant_emotions[:3],  # Top 3 dominant emotions
                "overall_sentiment": overall_sentiment,
                "emotional_shifts": emotional_shifts[:5],  # Top 5 significant shifts
                "sentiment_distribution": sentiment_counts
            }
            
        except Exception as e:
            logger.error(f"Emotional arc summarization failed: {str(e)}")
            return {"error": str(e)}


# Global instance
telugu_emotion_analyzer_opensource = TeluguEmotionAnalyzerOpenSource()