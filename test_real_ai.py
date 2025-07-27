#!/usr/bin/env python3
"""
Test script to verify that the real AI models are working.
"""
import os
import sys
import time
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def test_story_generation_model():
    """Test the story generation model"""
    print("\n=== Testing Story Generation Model ===")
    
    try:
        # Load the model and tokenizer
        print("Loading model and tokenizer...")
        model_name = "facebook/mbart-large-50"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        print(f"✅ Successfully loaded model: {model_name}")
        
        # Generate text
        print("Generating text...")
        input_text = "A story about a hero who fights against evil"
        
        # Set the source language
        tokenizer.src_lang = "en_XX"
        
        # Encode the input
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate
        outputs = model.generate(
            inputs.input_ids,
            max_length=150,
            num_beams=4,
            early_stopping=True,
            forced_bos_token_id=tokenizer.lang_code_to_id["te_IN"]  # Force Telugu output
        )
        
        # Decode
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print(f"✅ Successfully generated text:")
        print(f"Input: {input_text}")
        print(f"Output: {generated_text}")
        
        return True
    except Exception as e:
        print(f"❌ Error during story generation model test: {e}")
        return False

def test_emotion_analysis_model():
    """Test the emotion analysis model"""
    print("\n=== Testing Emotion Analysis Model ===")
    
    try:
        # Load the model and tokenizer
        print("Loading emotion model...")
        model_name = "j-hartmann/emotion-english-distilroberta-base"
        
        # Create a pipeline
        classifier = pipeline("text-classification", model=model_name, top_k=None)
        
        print(f"✅ Successfully loaded model: {model_name}")
        
        # Analyze text
        print("Analyzing text...")
        text = "I am feeling very happy today!"
        result = classifier(text)
        
        print(f"✅ Successfully analyzed text:")
        print(f"Input: {text}")
        print(f"Output: {result}")
        
        # Load sentiment model
        print("\nLoading sentiment model...")
        sentiment_model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        sentiment_classifier = pipeline("sentiment-analysis", model=sentiment_model_name)
        
        print(f"✅ Successfully loaded model: {sentiment_model_name}")
        
        # Analyze sentiment
        print("Analyzing sentiment...")
        sentiment_result = sentiment_classifier(text)
        
        print(f"✅ Successfully analyzed sentiment:")
        print(f"Input: {text}")
        print(f"Output: {sentiment_result}")
        
        return True
    except Exception as e:
        print(f"❌ Error during emotion analysis model test: {e}")
        return False

def main():
    """Main function"""
    print("Testing Real AI Models...\n")
    
    # Check if CUDA is available
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    if cuda_available:
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    
    # Test story generation model
    story_success = test_story_generation_model()
    
    # Test emotion analysis model
    emotion_success = test_emotion_analysis_model()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Story Generation Model: {'✅ Passed' if story_success else '❌ Failed'}")
    print(f"Emotion Analysis Model: {'✅ Passed' if emotion_success else '❌ Failed'}")
    
    success_count = sum([story_success, emotion_success])
    print(f"\nOverall: {success_count}/2 tests passed")
    
    if success_count == 2:
        print("\n✅ All tests passed! The real AI models are working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()