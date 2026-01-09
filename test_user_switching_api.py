#!/usr/bin/env python3
"""
Simple test script for User Switching API
Run this to verify all endpoints are working correctly
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

async def test_user_switching_api():
    """Test all user switching API endpoints"""
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing User Switching API")
        print("=" * 50)
        
        # Test 1: Get all user profiles
        print("\n1️⃣ Testing GET /users/profiles")
        response = await client.get(f"{BASE_URL}/users/profiles")
        assert response.status_code == 200
        profiles_data = response.json()
        print(f"✅ Found {profiles_data['total_count']} user profiles")
        
        # Test 2: Get current user
        print("\n2️⃣ Testing GET /users/current")
        response = await client.get(f"{BASE_URL}/users/current")
        assert response.status_code == 200
        current_user = response.json()
        print(f"✅ Current user: {current_user['name']} ({current_user['id']})")
        
        # Test 3: Get specific user profile
        print("\n3️⃣ Testing GET /users/{user_id}/profile")
        user_id = "user_456"
        response = await client.get(f"{BASE_URL}/users/{user_id}/profile")
        assert response.status_code == 200
        user_profile = response.json()
        print(f"✅ Retrieved profile for: {user_profile['name']}")
        
        # Test 4: Switch user
        print("\n4️⃣ Testing POST /users/switch")
        switch_data = {
            "user_id": user_id,
            "session_context": {
                "device_id": "test_device",
                "platform": "web"
            }
        }
        response = await client.post(f"{BASE_URL}/users/switch", json=switch_data)
        assert response.status_code == 200
        switch_result = response.json()
        print(f"✅ Switched to user: {switch_result['active_user']['name']}")
        
        # Test 5: Create new user profile
        print("\n5️⃣ Testing POST /users/profiles")
        new_user_data = {
            "name": "API Test User",
            "email": f"test.{datetime.now().timestamp()}@example.com",
            "phone": "+1-555-TEST",
            "role": "family_member"
        }
        response = await client.post(f"{BASE_URL}/users/profiles", json=new_user_data)
        assert response.status_code == 200
        new_user = response.json()
        print(f"✅ Created new user: {new_user['name']} ({new_user['id']})")
        
        # Test 6: Update user profile
        print("\n6️⃣ Testing PUT /users/{user_id}/profile")
        update_data = {
            "name": "Updated API Test User",
            "preferences": {
                "theme": "dark"
            }
        }
        response = await client.put(f"{BASE_URL}/users/{new_user['id']}/profile", json=update_data)
        assert response.status_code == 200
        updated_user = response.json()
        print(f"✅ Updated user: {updated_user['name']}")
        
        # Test 7: Health check
        print("\n7️⃣ Testing GET /users/health")
        response = await client.get(f"{BASE_URL}/users/health")
        assert response.status_code == 200
        health_data = response.json()
        print(f"✅ API Health: {health_data['status']} - {health_data['total_users']} users")
        
        # Test 8: Error handling - non-existent user
        print("\n8️⃣ Testing error handling")
        response = await client.get(f"{BASE_URL}/users/user_999/profile")
        assert response.status_code == 404
        error_data = response.json()
        print(f"✅ Error handling works: {error_data['detail']['error']['code']}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! User Switching API is working correctly.")
        print("\n📋 API Summary:")
        print(f"   • Total Users: {health_data['total_users']}")
        print(f"   • Active Users: {health_data['active_users']}")
        print(f"   • Current User: {health_data['current_user_id']}")
        print(f"   • Service Status: {health_data['status']}")

if __name__ == "__main__":
    print("🚀 Starting User Switching API Tests...")
    print("Make sure the server is running: uvicorn main:app --reload")
    print()
    
    try:
        asyncio.run(test_user_switching_api())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the server is running on http://localhost:8000")