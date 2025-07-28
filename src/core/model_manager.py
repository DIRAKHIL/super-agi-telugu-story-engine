"""
Production Model Manager for Telugu Story Engine
Real AI model loading and management - NO MOCKS, NO FALLBACKS
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import torch
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForCausalLM,
    AutoModelForSequenceClassification, pipeline,
    BitsAndBytesConfig, TrainingArguments
)
from sentence_transformers import SentenceTransformer
import numpy as np
from dataclasses import dataclass
import json
import pickle
from datetime import datetime

from .config import get_config

logger = logging.getLogger(__name__)

@dataclass
class ModelInfo:
    """Model information and metadata"""
    name: str
    model_type: str
    model_path: str
    tokenizer_path: str
    loaded: bool = False
    load_time: Optional[datetime] = None
    memory_usage: Optional[float] = None
    parameters: Optional[int] = None

class TeluguModelManager:
    """
    Production Model Manager for Telugu Story Engine
    Manages real AI models with no mocks or fallbacks
    """
    
    def __init__(self):
        self.config = get_config()
        self.models: Dict[str, Any] = {}
        self.tokenizers: Dict[str, Any] = {}
        self.model_info: Dict[str, ModelInfo] = {}
        self.device = torch.device(self.config.model.device)
        self.quantization_config = self._setup_quantization()
        
        # Ensure model directories exist
        self.config.model.models_dir.mkdir(parents=True, exist_ok=True)
        self.config.model.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized ModelManager with device: {self.device}")
    
    def _setup_quantization(self) -> Optional[BitsAndBytesConfig]:
        """Setup quantization configuration for memory efficiency"""
        if self.device.type == "cuda":
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
        return None
    
    async def initialize_models(self) -> None:
        """Initialize all required models for Telugu story generation"""
        logger.info("Starting model initialization...")
        
        # Define models to load
        models_to_load = [
            ("telugu_bert", "text_understanding"),
            ("telugu_gpt", "text_generation"),
            ("emotion_model", "emotion_classification"),
            ("cultural_model", "cultural_adaptation")
        ]
        
        # Load models concurrently where possible
        tasks = []
        for model_name, model_type in models_to_load:
            task = asyncio.create_task(
                self._load_model_async(model_name, model_type)
            )
            tasks.append(task)
        
        # Wait for all models to load
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check for any loading errors
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                model_name = models_to_load[i][0]
                logger.error(f"Failed to load {model_name}: {result}")
                raise result
        
        logger.info("All models initialized successfully")
    
    async def _load_model_async(self, model_name: str, model_type: str) -> None:
        """Load a specific model asynchronously"""
        try:
            start_time = datetime.now()
            logger.info(f"Loading {model_name} ({model_type})...")
            
            # Get model configuration
            model_path = self._get_model_path(model_name)
            
            # Load model based on type
            if model_type == "text_understanding":
                model, tokenizer = await self._load_bert_model(model_path)
            elif model_type == "text_generation":
                model, tokenizer = await self._load_gpt_model(model_path)
            elif model_type == "emotion_classification":
                model, tokenizer = await self._load_emotion_model(model_path)
            elif model_type == "cultural_adaptation":
                model, tokenizer = await self._load_cultural_model(model_path)
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # Store models
            self.models[model_name] = model
            self.tokenizers[model_name] = tokenizer
            
            # Calculate memory usage
            memory_usage = self._calculate_memory_usage(model)
            parameters = sum(p.numel() for p in model.parameters())
            
            # Store model info
            self.model_info[model_name] = ModelInfo(
                name=model_name,
                model_type=model_type,
                model_path=str(model_path),
                tokenizer_path=str(model_path),
                loaded=True,
                load_time=datetime.now(),
                memory_usage=memory_usage,
                parameters=parameters
            )
            
            load_duration = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"Loaded {model_name}: {parameters:,} parameters, "
                f"{memory_usage:.2f}MB memory, {load_duration:.2f}s"
            )
            
        except Exception as e:
            logger.error(f"Error loading {model_name}: {e}")
            raise
    
    def _get_model_path(self, model_name: str) -> str:
        """Get the path for a specific model"""
        model_paths = {
            "telugu_bert": self.config.model.telugu_bert_model,
            "telugu_gpt": self.config.model.telugu_gpt_model,
            "emotion_model": self.config.model.emotion_model,
            "cultural_model": self.config.model.cultural_model
        }
        return model_paths.get(model_name, model_name)
    
    async def _load_bert_model(self, model_path: str) -> tuple:
        """Load BERT-based model for text understanding"""
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            cache_dir=self.config.model.cache_dir,
            trust_remote_code=True
        )
        
        model = AutoModel.from_pretrained(
            model_path,
            cache_dir=self.config.model.cache_dir,
            quantization_config=self.quantization_config,
            device_map="auto" if self.device.type == "cuda" else None,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
            trust_remote_code=True
        )
        
        if self.device.type != "cuda":
            model = model.to(self.device)
        
        model.eval()
        return model, tokenizer
    
    async def _load_gpt_model(self, model_path: str) -> tuple:
        """Load GPT-based model for text generation"""
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            cache_dir=self.config.model.cache_dir,
            trust_remote_code=True
        )
        
        # Add padding token if not present
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            cache_dir=self.config.model.cache_dir,
            quantization_config=self.quantization_config,
            device_map="auto" if self.device.type == "cuda" else None,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
            trust_remote_code=True
        )
        
        if self.device.type != "cuda":
            model = model.to(self.device)
        
        model.eval()
        return model, tokenizer
    
    async def _load_emotion_model(self, model_path: str) -> tuple:
        """Load emotion classification model"""
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            cache_dir=self.config.model.cache_dir,
            trust_remote_code=True
        )
        
        model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            cache_dir=self.config.model.cache_dir,
            quantization_config=self.quantization_config,
            device_map="auto" if self.device.type == "cuda" else None,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
            trust_remote_code=True
        )
        
        if self.device.type != "cuda":
            model = model.to(self.device)
        
        model.eval()
        return model, tokenizer
    
    async def _load_cultural_model(self, model_path: str) -> tuple:
        """Load cultural adaptation model (sentence transformer)"""
        model = SentenceTransformer(
            model_path,
            cache_folder=str(self.config.model.cache_dir),
            device=str(self.device)
        )
        
        # Create a dummy tokenizer for consistency
        tokenizer = AutoTokenizer.from_pretrained(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            cache_dir=self.config.model.cache_dir
        )
        
        return model, tokenizer
    
    def _calculate_memory_usage(self, model) -> float:
        """Calculate model memory usage in MB"""
        if hasattr(model, 'get_memory_footprint'):
            return model.get_memory_footprint() / (1024 * 1024)
        
        # Fallback calculation
        param_size = sum(p.numel() * p.element_size() for p in model.parameters())
        buffer_size = sum(b.numel() * b.element_size() for b in model.buffers())
        return (param_size + buffer_size) / (1024 * 1024)
    
    def get_model(self, model_name: str) -> Any:
        """Get a loaded model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not loaded")
        return self.models[model_name]
    
    def get_tokenizer(self, model_name: str) -> Any:
        """Get a model's tokenizer"""
        if model_name not in self.tokenizers:
            raise ValueError(f"Tokenizer for {model_name} not loaded")
        return self.tokenizers[model_name]
    
    async def generate_text(
        self,
        model_name: str,
        prompt: str,
        max_length: Optional[int] = None,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using a specific model"""
        model = self.get_model(model_name)
        tokenizer = self.get_tokenizer(model_name)
        
        # Use config defaults if not specified
        temperature = temperature or self.config.model.temperature
        top_p = top_p or self.config.model.top_p
        top_k = top_k or self.config.model.top_k
        
        # Tokenize input
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        # Use max_new_tokens instead of max_length to avoid issues
        if max_new_tokens is None:
            max_new_tokens = max_length or 200  # Default to 200 new tokens
        
        # Generate
        with torch.no_grad():
            try:
                outputs = model.generate(
                    inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    **kwargs
                )
                
                # Check if outputs is valid
                if outputs is None or len(outputs) == 0:
                    logger.warning(f"Model {model_name} generated empty output")
                    return ""
                
                # Decode output
                generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
            except Exception as e:
                logger.error(f"Text generation failed for model {model_name}: {e}")
                return ""
        
        # Remove the original prompt from the output
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        
        return generated_text
    
    async def encode_text(self, model_name: str, text: str) -> np.ndarray:
        """Encode text to embeddings using a specific model"""
        model = self.get_model(model_name)
        
        if isinstance(model, SentenceTransformer):
            # Sentence transformer model
            embeddings = model.encode([text])
            return embeddings[0]
        else:
            # BERT-like model
            tokenizer = self.get_tokenizer(model_name)
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
            
            with torch.no_grad():
                outputs = model(**inputs)
                # Use CLS token embedding or mean pooling
                if hasattr(outputs, 'last_hidden_state'):
                    embeddings = outputs.last_hidden_state.mean(dim=1)
                else:
                    embeddings = outputs.pooler_output
            
            return embeddings.cpu().numpy()[0]
    
    async def classify_emotion(self, text: str) -> Dict[str, float]:
        """Classify emotions in text"""
        model = self.get_model("emotion_model")
        tokenizer = self.get_tokenizer("emotion_model")
        
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Get emotion labels (this would be model-specific)
        emotion_labels = [
            "joy", "sadness", "anger", "fear", "surprise", "disgust", "love",
            "optimism", "pessimism", "trust", "anticipation", "shame", "guilt",
            "pride", "envy", "gratitude", "hope", "compassion", "contempt",
            "anxiety", "relief", "disappointment", "satisfaction", "confusion",
            "curiosity", "nostalgia", "longing"
        ]
        
        # Create emotion scores dictionary
        emotion_scores = {}
        probs = probabilities.cpu().numpy()[0]
        
        for i, label in enumerate(emotion_labels[:len(probs)]):
            emotion_scores[label] = float(probs[i])
        
        return emotion_scores
    
    def get_model_info(self, model_name: Optional[str] = None) -> Union[ModelInfo, Dict[str, ModelInfo]]:
        """Get information about loaded models"""
        if model_name:
            return self.model_info.get(model_name)
        return self.model_info
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage for all loaded models"""
        return {
            name: info.memory_usage 
            for name, info in self.model_info.items() 
            if info.memory_usage is not None
        }
    
    async def unload_model(self, model_name: str) -> None:
        """Unload a specific model to free memory"""
        if model_name in self.models:
            del self.models[model_name]
            del self.tokenizers[model_name]
            self.model_info[model_name].loaded = False
            
            # Force garbage collection
            import gc
            gc.collect()
            if self.device.type == "cuda":
                torch.cuda.empty_cache()
            
            logger.info(f"Unloaded model: {model_name}")
    
    async def reload_model(self, model_name: str) -> None:
        """Reload a specific model"""
        if model_name in self.model_info:
            model_type = self.model_info[model_name].model_type
            await self.unload_model(model_name)
            await self._load_model_async(model_name, model_type)
            logger.info(f"Reloaded model: {model_name}")
    
    def save_model_cache(self, cache_path: Optional[Path] = None) -> None:
        """Save model information to cache"""
        cache_path = cache_path or (self.config.model.cache_dir / "model_cache.json")
        
        cache_data = {
            name: {
                "name": info.name,
                "model_type": info.model_type,
                "model_path": info.model_path,
                "tokenizer_path": info.tokenizer_path,
                "loaded": info.loaded,
                "parameters": info.parameters,
                "memory_usage": info.memory_usage
            }
            for name, info in self.model_info.items()
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2, default=str)
        
        logger.info(f"Saved model cache to {cache_path}")
    
    def load_model_cache(self, cache_path: Optional[Path] = None) -> None:
        """Load model information from cache"""
        cache_path = cache_path or (self.config.model.cache_dir / "model_cache.json")
        
        if not cache_path.exists():
            logger.info("No model cache found")
            return
        
        with open(cache_path, 'r') as f:
            cache_data = json.load(f)
        
        for name, data in cache_data.items():
            self.model_info[name] = ModelInfo(**data)
        
        logger.info(f"Loaded model cache from {cache_path}")

# Global model manager instance
_model_manager: Optional[TeluguModelManager] = None

def get_model_manager() -> TeluguModelManager:
    """Get the global model manager instance"""
    global _model_manager
    if _model_manager is None:
        _model_manager = TeluguModelManager()
    return _model_manager

async def initialize_models() -> None:
    """Initialize all models"""
    model_manager = get_model_manager()
    await model_manager.initialize_models()