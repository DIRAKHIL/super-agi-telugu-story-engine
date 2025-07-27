"""
Base AI model interface for the Telugu Film Story Generation System
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class ModelResponse(BaseModel):
    """Standard response format for all AI models"""
    success: bool
    data: Any
    confidence: Optional[float] = None
    processing_time: Optional[float] = None
    model_name: str
    error: Optional[str] = None


class BaseAIModel(ABC):
    """Abstract base class for all AI models"""
    
    def __init__(self, model_name: str, config: Dict[str, Any] = None):
        self.model_name = model_name
        self.config = config or {}
        self.is_loaded = False
        self._model = None
        
    @abstractmethod
    async def load_model(self) -> bool:
        """Load the AI model"""
        pass
    
    @abstractmethod
    async def predict(self, input_data: Any, **kwargs) -> ModelResponse:
        """Make prediction using the model"""
        pass
    
    @abstractmethod
    async def batch_predict(self, input_batch: List[Any], **kwargs) -> List[ModelResponse]:
        """Make batch predictions"""
        pass
    
    async def unload_model(self) -> bool:
        """Unload the model to free memory"""
        try:
            if self._model is not None:
                del self._model
                self._model = None
            self.is_loaded = False
            logger.info(f"Model {self.model_name} unloaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error unloading model {self.model_name}: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "name": self.model_name,
            "loaded": self.is_loaded,
            "config": self.config
        }


class TeluguModelMixin:
    """Mixin for Telugu language specific functionality"""
    
    TELUGU_SCRIPT_RANGE = (0x0C00, 0x0C7F)
    
    def is_telugu_text(self, text: str) -> bool:
        """Check if text contains Telugu characters"""
        for char in text:
            if self.TELUGU_SCRIPT_RANGE[0] <= ord(char) <= self.TELUGU_SCRIPT_RANGE[1]:
                return True
        return False
    
    def preprocess_telugu_text(self, text: str) -> str:
        """Preprocess Telugu text for model input"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Normalize Telugu text (basic normalization)
        text = text.strip()
        
        return text
    
    def postprocess_telugu_text(self, text: str) -> str:
        """Postprocess Telugu text from model output"""
        # Clean up generated text
        text = text.strip()
        
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            text = '.'.join(sentences[:-1]) + '.'
        
        return text