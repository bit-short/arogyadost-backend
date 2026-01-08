"""
Mock data for user switching API
Comprehensive hardcoded data for development and testing
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

# Generate session tokens (mock JWT-like tokens)
def generate_session_token(user_id: str) -> str:
    """Generate a mock session token"""
    return f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.{user_id}.mock_signature_{uuid.uuid4().hex[:16]}"

# Mock user profiles with comprehensive data
MOCK_USER_PROFILES = [
    {
        "id": "user_123",
        "name": "Dr. Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "+1-555-0123",
        "avatar_url": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
        "role": "primary_user",
        "preferences": {
            "theme": "system",
            "language": "en",
            "timezone": "America/New_York",
            "notifications_enabled": True,
            "incognito_mode": False
        },
        "permissions": {
            "can_view_health_data": True,
            "can_edit_health_data": True,
            "can_manage_users": True,
            "can_access_chat": True
        },
        "last_active": "2024-01-08T10:30:00Z",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-08T09:00:00Z",
        "status": "active"
    },
    {
        "id": "user_456",
        "name": "Michael Chen",
        "email": "michael.chen@email.com",
        "phone": "+1-555-0456",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
        "role": "family_member",
        "preferences": {
            "theme": "dark",
            "language": "en",
            "timezone": "America/Los_Angeles",
            "notifications_enabled": True,
            "incognito_mode": False
        },
        "permissions": {
            "can_view_health_data": True,
            "can_edit_health_data": True,
            "can_manage_users": False,
            "can_access_chat": True
        },
        "last_active": "2024-01-08T08:15:00Z",
        "created_at": "2024-01-02T00:00:00Z",
        "updated_at": "2024-01-07T14:30:00Z",
        "status": "active"
    },
    {
        "id": "user_789",
        "name": "Alex Thompson",
        "email": "alex.thompson@email.com",
        "phone": "+1-555-0789",
        "avatar_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
        "role": "family_member",
        "preferences": {
            "theme": "light",
            "language": "en",
            "timezone": "America/Chicago",
            "notifications_enabled": False,
            "incognito_mode": True
        },
        "permissions": {
            "can_view_health_data": True,
            "can_edit_health_data": False,
            "can_manage_users": False,
            "can_access_chat": True
        },
        "last_active": "2024-01-07T16:45:00Z",
        "created_at": "2024-01-03T00:00:00Z",
        "updated_at": "2024-01-06T11:20:00Z",
        "status": "active"
    },
    {
        "id": "user_101",
        "name": "Dr. Emily Rodriguez",
        "email": "emily.rodriguez@healthcenter.com",
        "phone": "+1-555-0101",
        "avatar_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&h=150&fit=crop&crop=face",
        "role": "healthcare_provider",
        "preferences": {
            "theme": "system",
            "language": "en",
            "timezone": "America/New_York",
            "notifications_enabled": True,
            "incognito_mode": False
        },
        "permissions": {
            "can_view_health_data": True,
            "can_edit_health_data": True,
            "can_manage_users": True,
            "can_access_chat": True
        },
        "last_active": "2024-01-08T07:30:00Z",
        "created_at": "2024-01-04T00:00:00Z",
        "updated_at": "2024-01-08T07:30:00Z",
        "status": "active"
    },
    {
        "id": "user_202",
        "name": "James Wilson",
        "email": "james.wilson@email.com",
        "phone": "+1-555-0202",
        "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
        "role": "care_team",
        "preferences": {
            "theme": "dark",
            "language": "en",
            "timezone": "America/Denver",
            "notifications_enabled": True,
            "incognito_mode": False
        },
        "permissions": {
            "can_view_health_data": True,
            "can_edit_health_data": False,
            "can_manage_users": False,
            "can_access_chat": True
        },
        "last_active": "2024-01-06T12:00:00Z",
        "created_at": "2024-01-05T00:00:00Z",
        "updated_at": "2024-01-06T12:00:00Z",
        "status": "active"
    }
]

# Current active user (session state)
CURRENT_ACTIVE_USER = "user_123"

# Session data
MOCK_SESSIONS = {
    "user_123": {
        "session_token": generate_session_token("user_123"),
        "session_started_at": "2024-01-08T10:00:00Z",
        "last_activity": "2024-01-08T10:30:00Z",
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat() + "Z"
    }
}

def get_user_by_id(user_id: str) -> Dict[str, Any] | None:
    """Get user profile by ID"""
    return next((user for user in MOCK_USER_PROFILES if user["id"] == user_id), None)

def get_all_profiles() -> List[Dict[str, Any]]:
    """Get all user profiles"""
    return MOCK_USER_PROFILES.copy()

def create_user_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new user profile"""
    new_user_id = f"user_{len(MOCK_USER_PROFILES) + 1000}"
    
    new_profile = {
        "id": new_user_id,
        "name": profile_data["name"],
        "email": profile_data["email"],
        "phone": profile_data.get("phone", ""),
        "avatar_url": profile_data.get("avatar_url", f"https://api.dicebear.com/7.x/avataaars/svg?seed={new_user_id}"),
        "role": profile_data["role"],
        "preferences": profile_data.get("preferences", {
            "theme": "system",
            "language": "en",
            "timezone": "America/New_York",
            "notifications_enabled": True,
            "incognito_mode": False
        }),
        "permissions": profile_data.get("permissions", {
            "can_view_health_data": True,
            "can_edit_health_data": True if profile_data["role"] in ["primary_user", "healthcare_provider"] else False,
            "can_manage_users": True if profile_data["role"] in ["primary_user", "healthcare_provider"] else False,
            "can_access_chat": True
        }),
        "last_active": None,
        "created_at": datetime.now().isoformat() + "Z",
        "updated_at": datetime.now().isoformat() + "Z",
        "status": "active"
    }
    
    MOCK_USER_PROFILES.append(new_profile)
    return new_profile

def update_user_profile(user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update user profile"""
    user = get_user_by_id(user_id)
    if not user:
        return None
    
    # Update fields
    for key, value in update_data.items():
        if key in user and value is not None:
            if key == "preferences" and isinstance(value, dict):
                user["preferences"].update(value)
            else:
                user[key] = value
    
    user["updated_at"] = datetime.now().isoformat() + "Z"
    return user

def delete_user_profile(user_id: str) -> bool:
    """Soft delete user profile"""
    user = get_user_by_id(user_id)
    if not user:
        return False
    
    user["status"] = "inactive"
    user["updated_at"] = datetime.now().isoformat() + "Z"
    return True

def switch_active_user(user_id: str) -> Dict[str, Any] | None:
    """Switch the active user and create session"""
    global CURRENT_ACTIVE_USER
    
    user = get_user_by_id(user_id)
    if not user or user["status"] != "active":
        return None
    
    # Update current active user
    CURRENT_ACTIVE_USER = user_id
    
    # Update user's last active time
    user["last_active"] = datetime.now().isoformat() + "Z"
    
    # Create/update session
    session_token = generate_session_token(user_id)
    expires_at = datetime.now() + timedelta(hours=24)
    
    MOCK_SESSIONS[user_id] = {
        "session_token": session_token,
        "session_started_at": datetime.now().isoformat() + "Z",
        "last_activity": datetime.now().isoformat() + "Z",
        "expires_at": expires_at.isoformat() + "Z"
    }
    
    return {
        "user": user,
        "session": MOCK_SESSIONS[user_id]
    }

def get_current_user() -> Dict[str, Any] | None:
    """Get current active user"""
    return get_user_by_id(CURRENT_ACTIVE_USER)

def get_user_session(user_id: str) -> Dict[str, Any] | None:
    """Get user session data"""
    return MOCK_SESSIONS.get(user_id)

# Email validation helper
def is_email_taken(email: str, exclude_user_id: str = None) -> bool:
    """Check if email is already taken by another user"""
    for user in MOCK_USER_PROFILES:
        if user["email"] == email and user["id"] != exclude_user_id:
            return True
    return False