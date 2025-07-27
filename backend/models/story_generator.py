"""
Telugu Story Generation Model
Real AI-powered story generation using transformer models
"""
import time
import asyncio
from typing import Dict, List, Any, Optional
# import torch
# from transformers import (
#     AutoTokenizer, AutoModelForCausalLM, 
#     pipeline, GenerationConfig
# )
from pydantic import BaseModel
import logging

from .base import BaseAIModel, ModelResponse, TeluguModelMixin
# from ..core.config import settings

logger = logging.getLogger(__name__)


class StoryGenerationRequest(BaseModel):
    """Request model for story generation"""
    prompt: str
    genre: Optional[str] = "drama"
    characters: Optional[List[str]] = []
    setting: Optional[str] = "modern"
    theme: Optional[str] = "family"
    max_length: Optional[int] = 2000
    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 0.9
    top_k: Optional[int] = 50


class TeluguStoryGenerator(BaseAIModel, TeluguModelMixin):
    """Advanced Telugu story generation using real AI models"""
    
    def __init__(self, model_name: str = None, config: Dict[str, Any] = None):
        model_name = model_name or settings.TELUGU_STORY_MODEL
        super().__init__(model_name, config)
        
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Telugu story templates and cultural elements
        self.cultural_elements = {
            "family_values": [
                "కుటుంబ గౌరవం", "తల్లిదండ్రుల ఆశీర్వాదం", "సోదరుల ప్రేమ",
                "పెద్దల మాట", "కుటుంబ సంప్రదాయం"
            ],
            "festivals": [
                "దీపావళి", "దసరా", "ఉగాది", "శ్రీరామనవమి", "కృష్ణాష్టమి",
                "గణేష్ చతుర్థి", "మహాశివరాత్రి"
            ],
            "locations": [
                "హైదరాబాద్", "విజయవాడ", "విశాఖపట్నం", "తిరుపతి", "వరంగల్",
                "గుంటూరు", "నెల్లూరు", "కర్నూలు", "అనంతపురం"
            ],
            "emotions": [
                "ప్రేమ", "కరుణ", "కోపం", "దుఃఖం", "ఆనందం", 
                "గర్వం", "భయం", "ఆశ", "నిరాశ", "ఉత్సాహం"
            ]
        }
    
    async def load_model(self) -> bool:
        """Load the story generation model"""
        try:
            logger.info(f"Loading story generation model: {self.model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                padding_side="left"
            )
            
            # Add pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            
            self.model.to(self.device)
            self.is_loaded = True
            
            logger.info(f"Story generation model loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading story generation model: {str(e)}")
            return False
    
    async def predict(self, input_data: StoryGenerationRequest, **kwargs) -> ModelResponse:
        """Generate a Telugu story based on the request"""
        start_time = time.time()
        
        try:
            if not self.is_loaded:
                await self.load_model()
            
            # Prepare the prompt with cultural context
            enhanced_prompt = self._enhance_prompt(input_data)
            
            # Tokenize input
            inputs = self.tokenizer.encode(
                enhanced_prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True
            ).to(self.device)
            
            # Generation configuration
            generation_config = GenerationConfig(
                max_new_tokens=input_data.max_length or 2000,
                temperature=input_data.temperature or 0.8,
                top_p=input_data.top_p or 0.9,
                top_k=input_data.top_k or 50,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1,
                length_penalty=1.0,
                no_repeat_ngram_size=3
            )
            
            # Generate story
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    generation_config=generation_config,
                    attention_mask=torch.ones_like(inputs)
                )
            
            # Decode generated text
            generated_text = self.tokenizer.decode(
                outputs[0][inputs.shape[1]:],
                skip_special_tokens=True
            )
            
            # Post-process the generated story
            story = self._postprocess_story(generated_text, input_data)
            
            processing_time = time.time() - start_time
            
            return ModelResponse(
                success=True,
                data={
                    "story": story,
                    "metadata": {
                        "genre": input_data.genre,
                        "theme": input_data.theme,
                        "setting": input_data.setting,
                        "characters": input_data.characters,
                        "word_count": len(story.split()),
                        "estimated_reading_time": len(story.split()) // 200  # minutes
                    }
                },
                confidence=0.85,
                processing_time=processing_time,
                model_name=self.model_name
            )
            
        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            return ModelResponse(
                success=False,
                data=None,
                model_name=self.model_name,
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    async def batch_predict(self, input_batch: List[StoryGenerationRequest], **kwargs) -> List[ModelResponse]:
        """Generate multiple stories in batch"""
        results = []
        
        for request in input_batch:
            result = await self.predict(request, **kwargs)
            results.append(result)
            
            # Small delay to prevent overwhelming the system
            await asyncio.sleep(0.1)
        
        return results
    
    def _enhance_prompt(self, request: StoryGenerationRequest) -> str:
        """Enhance the prompt with Telugu cultural context"""
        prompt_parts = []
        
        # Add cultural context based on genre and theme
        if request.genre:
            prompt_parts.append(f"జానర్: {request.genre}")
        
        if request.theme:
            prompt_parts.append(f"థీమ్: {request.theme}")
        
        if request.setting:
            prompt_parts.append(f"నేపథ్యం: {request.setting}")
        
        if request.characters:
            characters_str = ", ".join(request.characters)
            prompt_parts.append(f"పాత్రలు: {characters_str}")
        
        # Add cultural elements
        cultural_context = self._get_cultural_context(request.theme, request.genre)
        if cultural_context:
            prompt_parts.append(f"సాంస్కృతిక సందర్భం: {cultural_context}")
        
        # Combine with original prompt
        enhanced_prompt = "\n".join(prompt_parts) + "\n\n" + request.prompt
        
        # Add story generation instruction
        enhanced_prompt += "\n\nకథ:\n"
        
        return enhanced_prompt
    
    def _get_cultural_context(self, theme: str, genre: str) -> str:
        """Get relevant cultural context for the story"""
        context_elements = []
        
        if theme == "family":
            context_elements.extend(self.cultural_elements["family_values"][:2])
        
        if genre in ["drama", "family"]:
            context_elements.extend(self.cultural_elements["emotions"][:3])
        
        return ", ".join(context_elements)
    
    def _postprocess_story(self, generated_text: str, request: StoryGenerationRequest) -> str:
        """Post-process the generated story"""
        # Clean up the text
        story = self.postprocess_telugu_text(generated_text)
        
        # Ensure minimum length
        if len(story.split()) < settings.MIN_STORY_LENGTH // 5:  # Rough word count
            story += "\n\n[కథ అసంపూర్ణంగా ఉంది. దయచేసి మరింత వివరణాత్మక ప్రాంప్ట్ ఇవ్వండి.]"
        
        # Add story structure if missing
        if not any(marker in story for marker in ["అధ్యాయం", "భాగం", "ప్రారంభం"]):
            story = "కథ ప్రారంభం:\n\n" + story
        
        return story
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get model generation statistics"""
        return {
            "model_name": self.model_name,
            "device": str(self.device),
            "is_loaded": self.is_loaded,
            "cultural_elements_count": sum(len(v) for v in self.cultural_elements.values()),
            "supported_genres": ["drama", "comedy", "action", "romance", "thriller", "family"],
            "supported_themes": ["family", "love", "friendship", "justice", "tradition", "modern"]
        }