#!/usr/bin/env python3
"""
API Test Script for Super-AGI Telugu Story Engine
Tests all API endpoints to verify they are working correctly with real AI models
"""
import requests
import json
import time
import sys
from datetime import datetime

# Base URL for the API
BASE_URL = "https://work-1-mdgzgjjgwsxwlxtv.prod-runtime.all-hands.dev"

# Test results
results = {
    "total_tests": 0,
    "passed_tests": 0,
    "failed_tests": 0,
    "skipped_tests": 0,
    "test_details": []
}

def print_header(message):
    """Print a header message"""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def print_test_result(test_name, passed, response=None, error=None):
    """Print the result of a test"""
    global results
    results["total_tests"] += 1
    
    if passed:
        results["passed_tests"] += 1
        status = "✅ PASSED"
    else:
        results["failed_tests"] += 1
        status = "❌ FAILED"
    
    print(f"{status} - {test_name}")
    
    if error:
        print(f"  Error: {error}")
    
    if response and not passed:
        print(f"  Response: {response}")
    
    # Add to test details
    results["test_details"].append({
        "name": test_name,
        "status": "passed" if passed else "failed",
        "error": error,
        "response": response if not passed else None
    })

def test_root_endpoint():
    """Test the root endpoint"""
    print_header("Testing Root Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        data = response.json()
        
        # Check if the response contains expected fields
        expected_fields = ["message", "description", "version", "status", "features"]
        missing_fields = [field for field in expected_fields if field not in data]
        
        if response.status_code == 200 and not missing_fields:
            print_test_result("Root Endpoint", True)
            print(f"  API Version: {data.get('version')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Features: {', '.join(data.get('features', []))}")
            return True
        else:
            print_test_result("Root Endpoint", False, data, f"Missing fields: {missing_fields}")
            return False
    except Exception as e:
        print_test_result("Root Endpoint", False, None, str(e))
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print_header("Testing Health Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        
        # Check if the response contains expected fields
        expected_fields = ["status", "timestamp", "ai_system", "models_loaded"]
        missing_fields = [field for field in expected_fields if field not in data]
        
        if response.status_code == 200 and not missing_fields:
            print_test_result("Health Endpoint", True)
            print(f"  Status: {data.get('status')}")
            print(f"  AI System: {data.get('ai_system')}")
            print(f"  Models Loaded: {data.get('models_loaded')}")
            return True
        else:
            print_test_result("Health Endpoint", False, data, f"Missing fields: {missing_fields}")
            return False
    except Exception as e:
        print_test_result("Health Endpoint", False, None, str(e))
        return False

def test_story_generation():
    """Test the story generation endpoint"""
    print_header("Testing Story Generation")
    
    try:
        # Request body
        request_data = {
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
        
        # Submit the story generation task
        response = requests.post(
            f"{BASE_URL}/api/v1/stories/generate",
            json=request_data
        )
        data = response.json()
        
        if response.status_code != 200 or not data.get("success"):
            print_test_result("Story Generation Task Submission", False, data)
            return False
        
        print_test_result("Story Generation Task Submission", True)
        print(f"  Task ID: {data.get('task_id')}")
        
        # Wait for the task to complete
        task_id = data.get("task_id")
        max_retries = 10
        retries = 0
        
        while retries < max_retries:
            time.sleep(2)  # Wait for 2 seconds before checking
            
            task_response = requests.get(f"{BASE_URL}/api/v1/stories/task/{task_id}")
            task_data = task_response.json()
            
            if task_data.get("status") == "completed":
                result = task_data.get("result", {})
                
                if result.get("success"):
                    print_test_result("Story Generation Task Completion", True)
                    print(f"  Story Length: {len(result.get('story', ''))}")
                    print(f"  Model Used: {result.get('metadata', {}).get('model')}")
                    print(f"  AI Generated: {result.get('metadata', {}).get('ai_generated')}")
                    
                    # Check if the story is not empty
                    if len(result.get("story", "")) > 100:
                        print_test_result("Story Content Verification", True)
                    else:
                        print_test_result("Story Content Verification", False, result, "Story is too short")
                    
                    return True
                else:
                    print_test_result("Story Generation Task Completion", False, result, result.get("error"))
                    return False
            
            elif task_data.get("status") == "failed":
                print_test_result("Story Generation Task Completion", False, task_data, task_data.get("error"))
                return False
            
            retries += 1
        
        print_test_result("Story Generation Task Completion", False, None, "Task timed out")
        return False
    except Exception as e:
        print_test_result("Story Generation", False, None, str(e))
        return False

def test_emotion_analysis():
    """Test the emotion analysis endpoint"""
    print_header("Testing Emotion Analysis")
    
    try:
        # Request body
        request_data = {
            "text": "రాజు చాలా కోపంగా ఉన్నాడు. అతని కళ్ళలో నిప్పులు చిమ్ముతున్నాయి. అతను తన చేతులు పిడికిలిగా బిగించి, పళ్ళు కొరుకుతూ ఉన్నాడు.",
            "analysis_type": "comprehensive",
            "cultural_context": True
        }
        
        # Submit the emotion analysis request
        response = requests.post(
            f"{BASE_URL}/api/v1/emotions/analyze",
            json=request_data
        )
        data = response.json()
        
        if response.status_code != 200 or not data.get("success"):
            print_test_result("Emotion Analysis", False, data)
            return False
        
        print_test_result("Emotion Analysis", True)
        
        # Check if the response contains emotions and sentiment
        if "emotions" in data and "sentiment" in data:
            print(f"  Top Emotion: {max(data['emotions'].items(), key=lambda x: x[1])[0]}")
            print(f"  Sentiment: {data['sentiment']['label']}")
            print(f"  AI Analyzed: {data.get('metadata', {}).get('ai_analyzed')}")
            print(f"  Emotion Model: {data.get('metadata', {}).get('emotion_model')}")
            
            # Check if the emotions are not all zero
            if any(score > 0 for score in data["emotions"].values()):
                print_test_result("Emotion Content Verification", True)
            else:
                print_test_result("Emotion Content Verification", False, data, "All emotion scores are zero")
            
            return True
        else:
            print_test_result("Emotion Content Verification", False, data, "Missing emotions or sentiment")
            return False
    except Exception as e:
        print_test_result("Emotion Analysis", False, None, str(e))
        return False

def test_emotional_arc():
    """Test the emotional arc endpoint"""
    print_header("Testing Emotional Arc Analysis")
    
    try:
        # Request body
        request_data = {
            "text": "రాజు చాలా కోపంగా ఉన్నాడు. అతని కళ్ళలో నిప్పులు చిమ్ముతున్నాయి. అతను తన చేతులు పిడికిలిగా బిగించి, పళ్ళు కొరుకుతూ ఉన్నాడు. కొంత సేపటికి అతను శాంతించాడు. అతని ముఖంలో చిరునవ్వు కనిపించింది. అతను తన మిత్రుడిని కలిసి సంతోషంగా మాట్లాడాడు. వారు కలిసి ఆనందంగా గడిపారు.",
            "segments": 3
        }
        
        # Submit the emotional arc request
        response = requests.post(
            f"{BASE_URL}/api/v1/emotions/emotional-arc",
            json=request_data
        )
        data = response.json()
        
        if response.status_code != 200:
            print_test_result("Emotional Arc Analysis", False, data)
            return False
        
        print_test_result("Emotional Arc Analysis", True)
        
        # Check if the response contains segments and summary
        if "segments" in data and "summary" in data:
            print(f"  Number of Segments: {len(data['segments'])}")
            print(f"  Overall Sentiment: {data['summary'].get('overall_sentiment')}")
            
            if "dominant_emotions" in data["summary"]:
                dominant_emotions = [e["emotion"] for e in data["summary"]["dominant_emotions"]]
                print(f"  Dominant Emotions: {', '.join(dominant_emotions)}")
            
            # Check if there are segments with emotions
            if all("emotions" in segment for segment in data["segments"]):
                print_test_result("Emotional Arc Content Verification", True)
            else:
                print_test_result("Emotional Arc Content Verification", False, data, "Missing emotions in segments")
            
            return True
        else:
            print_test_result("Emotional Arc Content Verification", False, data, "Missing segments or summary")
            return False
    except Exception as e:
        print_test_result("Emotional Arc Analysis", False, None, str(e))
        return False

def test_supported_emotions():
    """Test the supported emotions endpoint"""
    print_header("Testing Supported Emotions")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/emotions/supported-emotions")
        data = response.json()
        
        if response.status_code != 200 or "emotions" not in data:
            print_test_result("Supported Emotions", False, data)
            return False
        
        print_test_result("Supported Emotions", True)
        print(f"  Number of Emotions: {len(data['emotions'])}")
        print(f"  Emotions: {', '.join([emotion['id'] for emotion in data['emotions']])}")
        return True
    except Exception as e:
        print_test_result("Supported Emotions", False, None, str(e))
        return False

def test_cultural_contexts():
    """Test the cultural contexts endpoint"""
    print_header("Testing Cultural Contexts")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/emotions/cultural-contexts")
        data = response.json()
        
        if response.status_code != 200 or "cultural_contexts" not in data:
            print_test_result("Cultural Contexts", False, data)
            return False
        
        print_test_result("Cultural Contexts", True)
        print(f"  Number of Contexts: {len(data['cultural_contexts'])}")
        print(f"  Contexts: {', '.join([context['id'] for context in data['cultural_contexts']])}")
        return True
    except Exception as e:
        print_test_result("Cultural Contexts", False, None, str(e))
        return False

def test_emotions_statistics():
    """Test the emotions statistics endpoint"""
    print_header("Testing Emotions Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/emotions/statistics")
        data = response.json()
        
        expected_fields = ["supported_emotions", "ai_powered", "emotion_model", "sentiment_model"]
        missing_fields = [field for field in expected_fields if field not in data]
        
        if response.status_code != 200 or missing_fields:
            print_test_result("Emotions Statistics", False, data, f"Missing fields: {missing_fields}")
            return False
        
        print_test_result("Emotions Statistics", True)
        print(f"  Supported Emotions: {data.get('supported_emotions')}")
        print(f"  AI Powered: {data.get('ai_powered')}")
        print(f"  Emotion Model: {data.get('emotion_model')}")
        print(f"  Sentiment Model: {data.get('sentiment_model')}")
        return True
    except Exception as e:
        print_test_result("Emotions Statistics", False, None, str(e))
        return False

def test_story_genres():
    """Test the story genres endpoint"""
    print_header("Testing Story Genres")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stories/genres")
        data = response.json()
        
        if response.status_code != 200 or "genres" not in data:
            print_test_result("Story Genres", False, data)
            return False
        
        print_test_result("Story Genres", True)
        print(f"  Number of Genres: {len(data['genres'])}")
        print(f"  Genres: {', '.join([genre['id'] for genre in data['genres']])}")
        return True
    except Exception as e:
        print_test_result("Story Genres", False, None, str(e))
        return False

def test_story_settings():
    """Test the story settings endpoint"""
    print_header("Testing Story Settings")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stories/settings")
        data = response.json()
        
        if response.status_code != 200 or "settings" not in data:
            print_test_result("Story Settings", False, data)
            return False
        
        print_test_result("Story Settings", True)
        print(f"  Number of Settings: {len(data['settings'])}")
        print(f"  Settings: {', '.join([setting['id'] for setting in data['settings']])}")
        return True
    except Exception as e:
        print_test_result("Story Settings", False, None, str(e))
        return False

def test_story_themes():
    """Test the story themes endpoint"""
    print_header("Testing Story Themes")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stories/themes")
        data = response.json()
        
        if response.status_code != 200 or "themes" not in data:
            print_test_result("Story Themes", False, data)
            return False
        
        print_test_result("Story Themes", True)
        print(f"  Number of Themes: {len(data['themes'])}")
        print(f"  Themes: {', '.join([theme['id'] for theme in data['themes']])}")
        return True
    except Exception as e:
        print_test_result("Story Themes", False, None, str(e))
        return False

def test_story_statistics():
    """Test the story statistics endpoint"""
    print_header("Testing Story Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stories/statistics")
        data = response.json()
        
        expected_fields = ["total_stories_generated", "active_tasks", "completed_tasks", "failed_tasks", "success_rate", "ai_powered", "model"]
        missing_fields = [field for field in expected_fields if field not in data]
        
        if response.status_code != 200 or missing_fields:
            print_test_result("Story Statistics", False, data, f"Missing fields: {missing_fields}")
            return False
        
        print_test_result("Story Statistics", True)
        print(f"  Total Stories Generated: {data.get('total_stories_generated')}")
        print(f"  Success Rate: {data.get('success_rate')}%")
        print(f"  AI Powered: {data.get('ai_powered')}")
        print(f"  Model: {data.get('model')}")
        return True
    except Exception as e:
        print_test_result("Story Statistics", False, None, str(e))
        return False

def test_agents_statistics():
    """Test the agents statistics endpoint"""
    print_header("Testing Agents Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/agents/statistics")
        data = response.json()
        
        expected_fields = ["total_agents", "active_agents", "total_tasks_processed", "active_tasks", "average_task_time", "success_rate"]
        missing_fields = [field for field in expected_fields if field not in data]
        
        if response.status_code != 200 or missing_fields:
            print_test_result("Agents Statistics", False, data, f"Missing fields: {missing_fields}")
            return False
        
        print_test_result("Agents Statistics", True)
        print(f"  Total Agents: {data.get('total_agents')}")
        print(f"  Active Agents: {data.get('active_agents')}")
        print(f"  Success Rate: {data.get('success_rate')}%")
        return True
    except Exception as e:
        print_test_result("Agents Statistics", False, None, str(e))
        return False

def test_agents_status():
    """Test the agents status endpoint"""
    print_header("Testing Agents Status")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/agents/status")
        data = response.json()
        
        expected_fields = ["story_agents", "emotion_agents", "cultural_agents"]
        missing_fields = [field for field in expected_fields if field not in data]
        
        if response.status_code != 200 or missing_fields:
            print_test_result("Agents Status", False, data, f"Missing fields: {missing_fields}")
            return False
        
        print_test_result("Agents Status", True)
        print(f"  Story Agents: {data.get('story_agents', {}).get('count')} ({data.get('story_agents', {}).get('status')})")
        print(f"  Emotion Agents: {data.get('emotion_agents', {}).get('count')} ({data.get('emotion_agents', {}).get('status')})")
        print(f"  Cultural Agents: {data.get('cultural_agents', {}).get('count')} ({data.get('cultural_agents', {}).get('status')})")
        return True
    except Exception as e:
        print_test_result("Agents Status", False, None, str(e))
        return False

def test_cultural_festivals():
    """Test the cultural festivals endpoint"""
    print_header("Testing Cultural Festivals")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/cultural/festivals")
        data = response.json()
        
        if response.status_code != 200 or "festivals" not in data:
            print_test_result("Cultural Festivals", False, data)
            return False
        
        print_test_result("Cultural Festivals", True)
        print(f"  Number of Festivals: {len(data['festivals'])}")
        print(f"  Festivals: {', '.join([festival['name'] for festival in data['festivals']])}")
        return True
    except Exception as e:
        print_test_result("Cultural Festivals", False, None, str(e))
        return False

def test_workflows_active():
    """Test the workflows active endpoint"""
    print_header("Testing Workflows Active")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/workflows/active")
        data = response.json()
        
        expected_fields = ["active_workflows", "total_active"]
        missing_fields = [field for field in expected_fields if field not in data]
        
        if response.status_code != 200 or missing_fields:
            print_test_result("Workflows Active", False, data, f"Missing fields: {missing_fields}")
            return False
        
        print_test_result("Workflows Active", True)
        print(f"  Total Active: {data.get('total_active')}")
        return True
    except Exception as e:
        print_test_result("Workflows Active", False, None, str(e))
        return False

def print_summary():
    """Print a summary of the test results"""
    print_header("Test Summary")
    
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed Tests: {results['passed_tests']}")
    print(f"Failed Tests: {results['failed_tests']}")
    print(f"Skipped Tests: {results['skipped_tests']}")
    
    if results['failed_tests'] > 0:
        print("\nFailed Tests:")
        for test in results['test_details']:
            if test['status'] == 'failed':
                print(f"  - {test['name']}: {test['error']}")
    
    success_rate = (results['passed_tests'] / results['total_tests']) * 100 if results['total_tests'] > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.2f}%")
    
    if success_rate == 100:
        print("\n✅ All tests passed! The API is working correctly with real AI models.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")

def save_results():
    """Save the test results to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"api_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTest results saved to {filename}")

def main():
    """Main function"""
    print_header("API Test for Super-AGI Telugu Story Engine")
    print(f"Testing against: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Basic endpoints
    test_root_endpoint()
    test_health_endpoint()
    
    # Story endpoints
    test_story_generation()
    test_story_genres()
    test_story_settings()
    test_story_themes()
    test_story_statistics()
    
    # Emotion endpoints
    test_emotion_analysis()
    test_emotional_arc()
    test_supported_emotions()
    test_cultural_contexts()
    test_emotions_statistics()
    
    # Agent endpoints
    test_agents_statistics()
    test_agents_status()
    
    # Cultural endpoints
    test_cultural_festivals()
    
    # Workflow endpoints
    test_workflows_active()
    
    # Print summary
    print_summary()
    
    # Save results
    save_results()

if __name__ == "__main__":
    main()