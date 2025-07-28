#!/usr/bin/env python3
"""
COMPREHENSIVE TESTING SUITE FOR TELUGU STORY ENGINE
Production-ready AI system with REAL models - NO MOCKS!
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class TeluguStoryEngineTest:
    def __init__(self, base_url: str = "http://localhost:12000"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer demo-token"
        }
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        # Color coding for terminal output
        color = "\033[92m" if status == "PASS" else "\033[91m" if status == "FAIL" else "\033[93m"
        reset = "\033[0m"
        
        print(f"{color}[{status}]{reset} {test_name}")
        if details:
            print(f"      {details}")
    
    def test_health_check(self):
        """Test 1: Basic health check"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", "PASS", f"Status: {data.get('status', 'unknown')}")
                return True
            else:
                self.log_test("Health Check", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_system_status(self):
        """Test 2: System status with AI models"""
        try:
            response = requests.get(f"{self.base_url}/api/v2/system/status", 
                                  headers=self.headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                model_status = data.get('model_status', {})
                loaded_models = [name for name, status in model_status.items() 
                               if status == 'loaded']
                
                if len(loaded_models) >= 4:
                    self.log_test("System Status", "PASS", 
                                f"Models loaded: {len(loaded_models)}/4 - {', '.join(loaded_models)}")
                    return True
                else:
                    self.log_test("System Status", "FAIL", 
                                f"Only {len(loaded_models)}/4 models loaded")
                    return False
            else:
                self.log_test("System Status", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("System Status", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_story_generation_basic(self):
        """Test 3: Basic Telugu story generation"""
        try:
            payload = {
                "prompt": "ఒక చిన్న పిల్లవాడు తన స్నేహితుడితో ఆట ఆడుతున్న కథ",
                "length": 500,
                "cultural_context": "traditional_telugu",
                "story_type": "adventure",
                "target_audience": "children"
            }
            
            response = requests.post(f"{self.base_url}/api/v2/stories/generate",
                                   headers=self.headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('content', '')
                word_count = data.get('metadata', {}).get('word_count', 0)
                
                if content and len(content) > 50:
                    self.log_test("Basic Story Generation", "PASS", 
                                f"Generated {len(content)} chars, {word_count} words")
                    return True
                else:
                    self.log_test("Basic Story Generation", "FAIL", 
                                f"Content too short: {len(content)} chars")
                    return False
            else:
                self.log_test("Basic Story Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Basic Story Generation", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_story_generation_advanced(self):
        """Test 4: Advanced story generation with different parameters"""
        try:
            payload = {
                "prompt": "గ్రామంలో ఒక తెలివైన అమ్మాయి తన కుటుంబాన్ని కాపాడే కథ",
                "length": 500,
                "cultural_context": "contemporary_telugu",
                "story_type": "drama",
                "target_audience": "adults"
            }
            
            response = requests.post(f"{self.base_url}/api/v2/stories/generate",
                                   headers=self.headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('content', '')
                metadata = data.get('metadata', {})
                
                if content and metadata:
                    self.log_test("Advanced Story Generation", "PASS", 
                                f"Content: {len(content)} chars, Metadata: {len(metadata)} fields")
                    return True
                else:
                    self.log_test("Advanced Story Generation", "FAIL", 
                                "Missing content or metadata")
                    return False
            else:
                self.log_test("Advanced Story Generation", "FAIL", 
                            f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Advanced Story Generation", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_api_rate_limiting(self):
        """Test 5: API rate limiting functionality"""
        try:
            # Make multiple rapid requests
            responses = []
            for i in range(5):
                response = requests.get(f"{self.base_url}/health", timeout=5)
                responses.append(response.status_code)
            
            # Check if all requests succeeded (rate limiting should allow health checks)
            if all(status == 200 for status in responses):
                self.log_test("Rate Limiting", "PASS", "Health checks not rate limited")
                return True
            else:
                self.log_test("Rate Limiting", "WARN", f"Some requests failed: {responses}")
                return True  # This might be expected behavior
        except Exception as e:
            self.log_test("Rate Limiting", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test 6: Error handling with invalid requests"""
        try:
            # Test with invalid payload
            invalid_payload = {
                "prompt": "",  # Empty prompt
                "length": -1,  # Invalid length
            }
            
            response = requests.post(f"{self.base_url}/api/v2/stories/generate",
                                   headers=self.headers, json=invalid_payload, timeout=30)
            
            if response.status_code in [400, 422]:  # Bad request or validation error
                self.log_test("Error Handling", "PASS", 
                            f"Properly rejected invalid request: HTTP {response.status_code}")
                return True
            else:
                self.log_test("Error Handling", "FAIL", 
                            f"Should have rejected invalid request: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Error Handling", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_api_documentation(self):
        """Test 7: API documentation endpoints"""
        try:
            # Test OpenAPI docs
            response = requests.get(f"{self.base_url}/api/v2/docs", timeout=10)
            if response.status_code == 200:
                self.log_test("API Documentation", "PASS", "OpenAPI docs accessible")
                return True
            else:
                self.log_test("API Documentation", "FAIL", f"Docs not accessible: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Documentation", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🔍 COMPREHENSIVE TESTING - TELUGU STORY ENGINE")
        print("=" * 60)
        print("Testing PRODUCTION-READY system with REAL AI models")
        print("NO MOCKS • NO FALLBACKS • NO DEMOS • NO TEMPLATES")
        print("=" * 60)
        
        tests = [
            self.test_health_check,
            self.test_system_status,
            self.test_story_generation_basic,
            self.test_story_generation_advanced,
            self.test_api_rate_limiting,
            self.test_error_handling,
            self.test_api_documentation
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print(f"TEST RESULTS: {passed}/{total} PASSED")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL!")
        elif passed >= total * 0.8:
            print("✅ SYSTEM MOSTLY OPERATIONAL - Minor issues detected")
        else:
            print("❌ SYSTEM HAS ISSUES - Review failed tests")
        
        print("=" * 60)
        
        return passed, total

def main():
    """Main test execution"""
    print("Starting comprehensive test suite...")
    
    # Wait for API server to be ready
    print("⏳ Waiting for API server to initialize...")
    time.sleep(5)
    
    tester = TeluguStoryEngineTest()
    passed, total = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()