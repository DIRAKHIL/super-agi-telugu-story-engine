"""
System tests for the API server.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.server import create_app
from src.utils.config.config_manager import ConfigManager


class TestAPIServer:
    """System tests for the API server."""
    
    @pytest.fixture
    def config(self):
        """Load test configuration."""
        config_manager = ConfigManager()
        return config_manager.load_config("test")
    
    @pytest.fixture
    def client(self, config):
        """Create a test client for the API server."""
        app = create_app(config)
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_story_generation_api(self, client):
        """Test the story generation API endpoint."""
        request_data = {
            "parameters": {
                "length": 1000,
                "genre": "drama",
                "emotional_arc": "family_restoration",
                "characters": [
                    {
                        "name": "రాజు",
                        "age": 30,
                        "traits": ["brave", "loyal", "impulsive"],
                        "background": "Born in coastal village, left to city for work"
                    },
                    {
                        "name": "లక్ష్మి",
                        "age": 28,
                        "traits": ["intelligent", "determined", "compassionate"],
                        "background": "Teacher from rural background"
                    }
                ],
                "setting": {
                    "location": "Coastal Andhra Pradesh",
                    "time_period": "Contemporary",
                    "social_context": "Rural fishing community"
                },
                "theme": "Family reconciliation after long separation",
                "language_style": "Simple and direct with regional dialect"
            }
        }
        
        # Set API key header for production-ready system
        headers = {"X-API-Key": "test-api-key"}
        
        response = client.post("/api/v1/stories", json=request_data, headers=headers)
        
        # In production-ready system, we expect a 202 Accepted response for async processing
        assert response.status_code in [200, 202]
        
        response_data = response.json()
        
        # For 202 responses, we expect a task ID
        if response.status_code == 202:
            assert "task_id" in response_data
            # We would then poll the task status endpoint, but we'll skip that for the test
        else:
            # For 200 responses, we expect the complete story
            assert "id" in response_data
            assert "title" in response_data
            assert "content" in response_data
            assert "metadata" in response_data
    
    def test_invalid_request(self, client):
        """Test API response to invalid requests."""
        # Missing required parameters
        invalid_request = {
            "parameters": {
                "genre": "drama",
                "theme": "Test theme"
                # Missing other required parameters
            }
        }
        
        response = client.post("/api/v1/stories", json=invalid_request)
        assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors
        
        # Invalid parameter values
        invalid_length_request = {
            "parameters": {
                "length": 50,  # Too short
                "genre": "drama",
                "characters": [{"name": "Test", "age": 30, "traits": ["brave"]}],
                "setting": {"location": "Test", "time_period": "Contemporary"},
                "theme": "Test theme"
            }
        }
        
        response = client.post("/api/v1/stories", json=invalid_length_request)
        assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors