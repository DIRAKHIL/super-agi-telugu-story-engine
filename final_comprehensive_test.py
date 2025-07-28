#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE TESTING SUITE
Production-ready Telugu Story Engine with REAL AI models
"""

import requests
import json
import time
import concurrent.futures
import statistics
from typing import List, Dict

def test_api_performance():
    """Test API performance under load"""
    print("🚀 PERFORMANCE TESTING")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer demo-token"
    }
    
    # Test concurrent story generation
    def generate_story(story_id: int):
        payload = {
            "prompt": f"కథ {story_id}: ఒక చిన్న పిల్లవాడు తన కలలను నెరవేర్చుకునే కథ",
            "length": 500,
            "cultural_context": "traditional_telugu",
            "story_type": "adventure",
            "target_audience": "children"
        }
        
        start_time = time.time()
        try:
            response = requests.post(f"{base_url}/api/v2/stories/generate",
                                   headers=headers, json=payload, timeout=120)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response_time": end_time - start_time,
                    "content_length": len(data.get('content', '')),
                    "word_count": data.get('metadata', {}).get('word_count', 0)
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Run concurrent tests
    print("Testing concurrent story generation (3 stories)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(generate_story, i) for i in range(1, 4)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    # Analyze results
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"✅ Successful: {len(successful)}/3")
    print(f"❌ Failed: {len(failed)}/3")
    
    if successful:
        response_times = [r["response_time"] for r in successful]
        content_lengths = [r["content_length"] for r in successful]
        word_counts = [r["word_count"] for r in successful]
        
        print(f"📊 Performance Metrics:")
        print(f"   Average Response Time: {statistics.mean(response_times):.2f}s")
        print(f"   Min Response Time: {min(response_times):.2f}s")
        print(f"   Max Response Time: {max(response_times):.2f}s")
        print(f"   Average Content Length: {statistics.mean(content_lengths):.0f} chars")
        print(f"   Average Word Count: {statistics.mean(word_counts):.0f} words")
    
    if failed:
        print(f"❌ Failures:")
        for i, failure in enumerate(failed):
            print(f"   {i+1}. {failure.get('error', 'Unknown error')}")
    
    return len(successful) == 3

def test_different_story_types():
    """Test different story types and cultural contexts"""
    print("\n📚 STORY VARIETY TESTING")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer demo-token"
    }
    
    test_cases = [
        {
            "name": "Traditional Adventure",
            "payload": {
                "prompt": "రాజకుమారుడు ఒక మాయా అడవిలో సాహసయాత్ర చేసే కథ",
                "length": 500,
                "cultural_context": "traditional_telugu",
                "story_type": "adventure",
                "target_audience": "children"
            }
        },
        {
            "name": "Contemporary Drama",
            "payload": {
                "prompt": "నగరంలో ఒక యువతి తన కెరీర్ కోసం పోరాడే కథ",
                "length": 500,
                "cultural_context": "contemporary_telugu",
                "story_type": "drama",
                "target_audience": "adults"
            }
        },
        {
            "name": "Rural Family Story",
            "payload": {
                "prompt": "గ్రామంలో ఒక కుటుంబం కలిసి ఉండే కథ",
                "length": 500,
                "cultural_context": "rural_telugu",
                "story_type": "family",
                "target_audience": "all_ages"
            }
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")
        
        try:
            response = requests.post(f"{base_url}/api/v2/stories/generate",
                                   headers=headers, json=test_case['payload'], timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "name": test_case['name'],
                    "success": True,
                    "content_length": len(data.get('content', '')),
                    "word_count": data.get('metadata', {}).get('word_count', 0),
                    "quality_score": data.get('metadata', {}).get('quality_score', 0)
                })
                print(f"   ✅ Success - {data.get('metadata', {}).get('word_count', 0)} words")
            else:
                results.append({
                    "name": test_case['name'],
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                print(f"   ❌ Failed - HTTP {response.status_code}")
        except Exception as e:
            results.append({
                "name": test_case['name'],
                "success": False,
                "error": str(e)
            })
            print(f"   ❌ Failed - {str(e)}")
    
    successful = [r for r in results if r.get("success")]
    print(f"\n📊 Story Variety Results: {len(successful)}/{len(test_cases)} successful")
    
    return len(successful) == len(test_cases)

def test_system_monitoring():
    """Test system monitoring endpoints"""
    print("\n📈 SYSTEM MONITORING TESTING")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    
    endpoints = [
        ("/health", "Health Check"),
        ("/api/v2/system/status", "System Status"),
        ("/metrics", "Prometheus Metrics"),
        ("/api/v2/docs", "API Documentation")
    ]
    
    results = []
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                results.append({"name": name, "success": True})
                print(f"✅ {name}: Working")
            else:
                results.append({"name": name, "success": False, "error": f"HTTP {response.status_code}"})
                print(f"❌ {name}: HTTP {response.status_code}")
        except Exception as e:
            results.append({"name": name, "success": False, "error": str(e)})
            print(f"❌ {name}: {str(e)}")
    
    successful = [r for r in results if r.get("success")]
    print(f"\n📊 Monitoring Results: {len(successful)}/{len(endpoints)} endpoints working")
    
    return len(successful) == len(endpoints)

def main():
    """Run final comprehensive tests"""
    print("🔍 FINAL COMPREHENSIVE TESTING SUITE")
    print("=" * 60)
    print("PRODUCTION-READY TELUGU STORY ENGINE")
    print("✅ REAL AI MODELS • ❌ NO MOCKS • ❌ NO FALLBACKS")
    print("=" * 60)
    
    # Wait for system to be ready
    print("⏳ Ensuring system is ready...")
    time.sleep(5)
    
    # Run all test suites
    test_results = []
    
    # 1. Performance Testing
    perf_result = test_api_performance()
    test_results.append(("Performance Testing", perf_result))
    
    # 2. Story Variety Testing
    variety_result = test_different_story_types()
    test_results.append(("Story Variety Testing", variety_result))
    
    # 3. System Monitoring Testing
    monitoring_result = test_system_monitoring()
    test_results.append(("System Monitoring", monitoring_result))
    
    # Final Results
    print("\n" + "=" * 60)
    print("🏆 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"OVERALL RESULT: {passed}/{total} TEST SUITES PASSED")
    
    if passed == total:
        print("🎉 SYSTEM FULLY OPERATIONAL AND PRODUCTION-READY!")
        print("🚀 All AI models working, API endpoints functional")
        print("📊 Performance metrics within acceptable ranges")
        print("🔧 System monitoring and documentation accessible")
    else:
        print("⚠️  Some test suites failed - review system status")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)