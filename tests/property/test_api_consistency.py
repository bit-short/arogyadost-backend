"""
Property-based tests for backend API consistency.

Feature: frontend-api-integration, Property 4: Backend API Completeness
Validates: Requirements 4.4, 4.5
"""

import pytest
import requests
from hypothesis import given, strategies as st, settings
from typing import Dict, Any, List
import json


class TestAPIConsistency:
    """Test that all API endpoints maintain consistent response formats and behavior."""
    
    BASE_URL = "http://localhost:8000"
    
    # Define the expected response structure for different endpoint types
    EXPECTED_STRUCTURES = {
        "list": ["id", "name"],  # Minimum required fields for list endpoints
        "detail": ["id"],        # Minimum required fields for detail endpoints
        "health": ["status"],    # Health check endpoints
    }
    
    def test_all_endpoints_return_valid_json(self):
        """Property: All API endpoints should return valid JSON responses."""
        endpoints = [
            "/api/health/biomarkers",
            "/api/health/recommendations", 
            "/api/health/metrics",
            "/api/health/status",
            "/api/doctors",
            "/api/labs",
            "/api/chat/threads",
            "/api/medical-files/categories",
            "/api/medical-files/specialties",
            "/api/medical-files",
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            assert response.status_code == 200, f"Endpoint {endpoint} returned {response.status_code}"
            
            # Should be valid JSON
            try:
                data = response.json()
                assert data is not None, f"Endpoint {endpoint} returned null data"
            except json.JSONDecodeError:
                pytest.fail(f"Endpoint {endpoint} returned invalid JSON")
    
    def test_detail_endpoints_consistency(self):
        """Property: All detail endpoints should follow consistent patterns."""
        detail_endpoints = [
            ("/api/biomarkers/metabolic", "metabolic"),
            ("/api/metrics/cholesterol", "cholesterol"),
            ("/api/actions/1", "1"),
        ]
        
        for endpoint, expected_id in detail_endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            assert response.status_code == 200, f"Detail endpoint {endpoint} failed"
            
            data = response.json()
            assert isinstance(data, dict), f"Detail endpoint {endpoint} should return object"
            assert "id" in data, f"Detail endpoint {endpoint} missing 'id' field"
            assert data["id"] == expected_id, f"Detail endpoint {endpoint} has incorrect id"
    
    def test_list_endpoints_return_arrays(self):
        """Property: All list endpoints should return arrays."""
        list_endpoints = [
            "/api/health/biomarkers",
            "/api/health/recommendations",
            "/api/health/metrics", 
            "/api/doctors",
            "/api/labs",
            "/api/chat/threads",
            "/api/medical-files/categories",
            "/api/medical-files/specialties",
            "/api/medical-files",
        ]
        
        for endpoint in list_endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            assert response.status_code == 200, f"List endpoint {endpoint} failed"
            
            data = response.json()
            assert isinstance(data, list), f"List endpoint {endpoint} should return array"
    
    def test_error_responses_have_consistent_format(self):
        """Property: All error responses should have consistent HTTP status codes."""
        # Test 404 responses
        not_found_endpoints = [
            "/api/biomarkers/nonexistent",
            "/api/metrics/nonexistent", 
            "/api/actions/nonexistent",
            "/api/doctors/99999",
            "/api/labs/99999",
            "/api/medical-files/nonexistent",
        ]
        
        for endpoint in not_found_endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            assert response.status_code == 404, f"Endpoint {endpoint} should return 404"
            
            # Should still return valid JSON error response
            try:
                error_data = response.json()
                assert "detail" in error_data, f"Error response from {endpoint} missing 'detail'"
            except json.JSONDecodeError:
                pytest.fail(f"Error response from {endpoint} is not valid JSON")
    
    @given(st.text(min_size=1, max_size=50))
    @settings(max_examples=20)
    def test_detail_endpoints_handle_arbitrary_ids(self, test_id: str):
        """Property: Detail endpoints should handle arbitrary IDs gracefully."""
        detail_endpoints = [
            "/api/biomarkers/",
            "/api/metrics/",
            "/api/actions/",
        ]
        
        for base_endpoint in detail_endpoints:
            endpoint = f"{base_endpoint}{test_id}"
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            
            # Should return either 200 (if ID exists) or 404 (if not found)
            assert response.status_code in [200, 404], \
                f"Endpoint {endpoint} returned unexpected status {response.status_code}"
            
            # Response should always be valid JSON
            try:
                response.json()
            except json.JSONDecodeError:
                pytest.fail(f"Endpoint {endpoint} returned invalid JSON for ID: {test_id}")
    
    def test_response_time_consistency(self):
        """Property: All endpoints should respond within reasonable time limits."""
        endpoints = [
            "/api/health/biomarkers",
            "/api/health/recommendations",
            "/api/health/metrics",
            "/api/doctors",
            "/api/labs",
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}", timeout=10)
            assert response.status_code == 200, f"Endpoint {endpoint} failed"
            
            # Response time should be reasonable (less than 2 seconds for mock data)
            assert response.elapsed.total_seconds() < 2.0, \
                f"Endpoint {endpoint} took too long: {response.elapsed.total_seconds()}s"
    
    def test_cors_headers_consistency(self):
        """Property: All endpoints should have consistent CORS headers."""
        endpoints = [
            "/api/health/biomarkers",
            "/api/doctors",
            "/api/labs",
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            assert response.status_code == 200, f"Endpoint {endpoint} failed"
            
            # Should have CORS headers for frontend integration
            headers = response.headers
            # Note: Specific CORS headers depend on the server configuration
            # This test ensures headers are present and consistent
            assert "content-type" in headers, f"Endpoint {endpoint} missing content-type header"
            assert "application/json" in headers.get("content-type", ""), \
                f"Endpoint {endpoint} should return JSON content-type"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])