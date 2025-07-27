#!/usr/bin/env python3
"""
Test script to verify the implementation of the Super-AGI Telugu Story Engine.
"""
import requests
import json
import sys
import time
from urllib.parse import urljoin
import random

# Service URLs
BACKEND_URL = "https://work-1-mdgzgjjgwsxwlxtv.prod-runtime.all-hands.dev"
FRONTEND_URL = "https://work-2-mdgzgjjgwsxwlxtv.prod-runtime.all-hands.dev"

def test_story_generation():
    """Test story generation with real AI models"""
    print("\n=== Testing Story Generation ===")
    
    # Test parameters
    test_params = {
        "prompt": "A story about a hero who fights against evil",
        "genre": "action",
        "theme": "justice",
        "setting": "city",
        "characters": ["Hero", "Villain", "Sidekick"],
        "max_length": 1500,
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 40
    }
    
    try:
        # Make the API call
        print("Generating story...")
        response = requests.post(
            urljoin(BACKEND_URL, "/api/v1/stories/generate"),
            json=test_params,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("task_id")
            print(f"✅ Story generation API call successful. Task ID: {task_id}")
            
            # Wait for the story to be generated
            print("Waiting for story generation to complete...")
            time.sleep(2)
            
            # Check the task status
            task_response = requests.get(
                urljoin(BACKEND_URL, f"/api/v1/stories/task/{task_id}"),
                timeout=10
            )
            
            if task_response.status_code == 200:
                task_result = task_response.json()
                if task_result.get("status") == "completed":
                    print("✅ Story generation completed successfully")
                    
                    # Verify the story content
                    story = task_result.get("result", {}).get("story", "")
                    metadata = task_result.get("result", {}).get("metadata", {})
                    
                    if story:
                        print(f"✅ Generated story has {len(story)} characters")
                        print("Story excerpt:")
                        print(story[:200] + "..." if len(story) > 200 else story)
                        print("\nMetadata:")
                        print(json.dumps(metadata, indent=2))
                        
                        # Check if the story is AI-generated
                        if metadata.get("ai_generated", False):
                            print("✅ Story is AI-generated")
                            print(f"✅ Model used: {metadata.get('model', 'Unknown')}")
                        else:
                            print("❌ Story is not AI-generated")
                            
                        return True
                    else:
                        print("❌ No story content found")
                else:
                    print(f"❌ Story generation task status: {task_result.get('status')}")
            else:
                print(f"❌ Failed to get task status. Status code: {task_response.status_code}")
        else:
            print(f"❌ Story generation API call failed. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error during story generation test: {e}")
    
    return False

def test_emotion_analysis():
    """Test emotion analysis with real AI models"""
    print("\n=== Testing Emotion Analysis ===")
    
    # Test parameters
    test_params = {
        "text": "రాజు చాలా కోపంగా ఉన్నాడు. అతని కళ్ళలో నిప్పులు చిమ్ముతున్నాయి. అతను తన చేతులు పిడికిలిగా బిగించి, పళ్ళు కొరుకుతూ ఉన్నాడు.",
        "analysis_type": "comprehensive",
        "cultural_context": True
    }
    
    try:
        # Make the API call
        print("Analyzing emotions...")
        response = requests.post(
            urljoin(BACKEND_URL, "/api/v1/emotions/analyze"),
            json=test_params,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Emotion analysis API call successful")
            
            # Verify the emotion analysis
            emotions = result.get("emotions", {})
            sentiment = result.get("sentiment", {})
            cultural_elements = result.get("cultural_elements", [])
            metadata = result.get("metadata", {})
            
            if emotions:
                print("✅ Emotion analysis completed successfully")
                print("\nEmotions:")
                for emotion, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"  - {emotion}: {score:.4f}")
                
                print("\nSentiment:")
                print(f"  - Label: {sentiment.get('label', 'Unknown')}")
                print(f"  - Confidence: {sentiment.get('confidence', 0):.4f}")
                
                if cultural_elements:
                    print("\nCultural Elements:")
                    for element in cultural_elements:
                        print(f"  - {element}")
                
                print("\nMetadata:")
                print(json.dumps(metadata, indent=2))
                
                # Check if the analysis is AI-powered
                if metadata.get("ai_analyzed", False):
                    print("✅ Emotion analysis is AI-powered")
                    print(f"✅ Model used: {metadata.get('model', 'Unknown')}")
                else:
                    print("❌ Emotion analysis is not AI-powered")
                
                return True
            else:
                print("❌ No emotion analysis found")
        else:
            print(f"❌ Emotion analysis API call failed. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error during emotion analysis test: {e}")
    
    return False

def test_supported_emotions():
    """Test getting supported emotions"""
    print("\n=== Testing Supported Emotions ===")
    
    try:
        # Make the API call
        print("Getting supported emotions...")
        response = requests.get(
            urljoin(BACKEND_URL, "/api/v1/emotions/supported-emotions"),
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Supported emotions API call successful")
            
            # Verify the supported emotions
            emotions = result.get("emotions", [])
            
            if emotions:
                print(f"✅ Found {len(emotions)} supported emotions")
                print("\nSupported Emotions:")
                for emotion in emotions[:5]:  # Show first 5 emotions
                    print(f"  - {emotion.get('id', 'Unknown')}: {emotion.get('name', 'Unknown')} ({emotion.get('description', 'No description')})")
                
                return True
            else:
                print("❌ No supported emotions found")
        else:
            print(f"❌ Supported emotions API call failed. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error during supported emotions test: {e}")
    
    return False

def test_emotional_arc():
    """Test emotional arc analysis"""
    print("\n=== Testing Emotional Arc Analysis ===")
    
    # Test parameters
    test_params = {
        "text": """
        రాజు చాలా కోపంగా ఉన్నాడు. అతని కళ్ళలో నిప్పులు చిమ్ముతున్నాయి. అతను తన చేతులు పిడికిలిగా బిగించి, పళ్ళు కొరుకుతూ ఉన్నాడు.
        
        కొంత సేపటికి, అతని స్నేహితుడు వచ్చి అతనితో మాట్లాడాడు. రాజు కోపం కొంచెం తగ్గింది.
        
        తరువాత, రాజు తన కుటుంబంతో కలిసి భోజనం చేశాడు. అతను నవ్వుతూ, సంతోషంగా ఉన్నాడు.
        
        ఆ రాత్రి, రాజు తన పిల్లలకు కథలు చెప్పాడు. అందరూ ఆనందంగా నిద్రపోయారు.
        """,
        "analysis_type": "comprehensive",
        "cultural_context": True
    }
    
    try:
        # Make the API call
        print("Analyzing emotional arc...")
        response = requests.post(
            urljoin(BACKEND_URL, "/api/v1/emotions/emotional-arc"),
            json=test_params,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Emotional arc API call successful")
            
            # Verify the emotional arc
            segments = result.get("segments", [])
            summary = result.get("summary", {})
            
            if segments:
                print(f"✅ Found {len(segments)} segments in the emotional arc")
                print("\nEmotional Arc Summary:")
                
                if "dominant_emotions" in summary:
                    print("  Dominant Emotions:")
                    for emotion in summary["dominant_emotions"]:
                        print(f"    - {emotion.get('emotion', 'Unknown')}: {emotion.get('average_score', 0):.4f}")
                
                if "overall_sentiment" in summary:
                    print(f"  Overall Sentiment: {summary['overall_sentiment']}")
                
                if "emotional_shifts" in summary:
                    print("  Emotional Shifts:")
                    for shift in summary["emotional_shifts"]:
                        print(f"    - {shift.get('emotion', 'Unknown')} at segment {shift.get('segment', 0)}: {shift.get('change', 0):.4f}")
                
                return True
            else:
                print("❌ No emotional arc segments found")
        else:
            print(f"❌ Emotional arc API call failed. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error during emotional arc test: {e}")
    
    return False

def main():
    """Main function to test the implementation"""
    print("Testing Super-AGI Telugu Story Engine Implementation...\n")
    
    # Test story generation
    story_success = test_story_generation()
    
    # Test emotion analysis
    emotion_success = test_emotion_analysis()
    
    # Test supported emotions
    emotions_success = test_supported_emotions()
    
    # Test emotional arc
    arc_success = test_emotional_arc()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Story Generation: {'✅ Passed' if story_success else '❌ Failed'}")
    print(f"Emotion Analysis: {'✅ Passed' if emotion_success else '❌ Failed'}")
    print(f"Supported Emotions: {'✅ Passed' if emotions_success else '❌ Failed'}")
    print(f"Emotional Arc: {'✅ Passed' if arc_success else '❌ Failed'}")
    
    success_count = sum([story_success, emotion_success, emotions_success, arc_success])
    print(f"\nOverall: {success_count}/4 tests passed")
    
    if success_count == 4:
        print("\n✅ All tests passed! The implementation is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()