"""
Basic API tests for Aarogyadost Backend
"""

import pytest
import httpx
from main import app

@pytest.fixture
def client():
    """Test client fixture"""
    return httpx.AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test basic health endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    assert "Aarogyadost Backend API" in response.json()["message"]

@pytest.mark.asyncio
async def test_users_available(client):
    """Test users available endpoint"""
    response = await client.get("/api/users/available")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) > 0

@pytest.mark.asyncio
async def test_user_selection(client):
    """Test user selection"""
    # Select a user
    response = await client.post("/api/users/select", json={"user_id": "test_user_1_29f"})
    assert response.status_code == 200
    
    # Check current user
    response = await client.get("/api/users/current")
    assert response.status_code == 200
    assert response.json()["user_id"] == "test_user_1_29f"

@pytest.mark.asyncio
async def test_digital_twin_creation(client):
    """Test digital twin creation"""
    response = await client.post("/api/digital-twin/users/test_user_1_29f/create")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
