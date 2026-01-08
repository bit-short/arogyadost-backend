"""
User Switching API
Complete implementation of user profile management and switching functionality
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from app.models.user_switching import (
    UserProfile, UserProfileCreate, UserProfileUpdate, UserProfilesResponse,
    UserSwitchRequest, UserSwitchResponse, CurrentUserResponse,
    UserDeleteRequest, UserDeleteResponse, ErrorResponse
)
from app.data.mock_users import (
    get_all_profiles, get_user_by_id, create_user_profile, update_user_profile,
    delete_user_profile, switch_active_user, get_current_user, get_user_session,
    is_email_taken, CURRENT_ACTIVE_USER
)

router = APIRouter(prefix="/api", tags=["user-switching"])

async def simulate_delay(ms: int = 200):
    """Simulate realistic API delay"""
    await asyncio.sleep(ms / 1000)


# 1. Get All User Profiles
@router.get("/users/profiles", response_model=UserProfilesResponse)
async def get_user_profiles():
    """
    Retrieve all available user profiles for switching
    """
    await simulate_delay(300)
    
    try:
        profiles = get_all_profiles()
        
        return UserProfilesResponse(
            profiles=profiles,
            total_count=len(profiles),
            current_user_id=CURRENT_ACTIVE_USER
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user profiles: {str(e)}"
        )


# 2. Get Specific User Profile
@router.get("/users/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """
    Get detailed information for a specific user profile
    """
    await simulate_delay(250)
    
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": f"User with ID '{user_id}' not found",
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )
    
    return UserProfile(**user)


# 3. Create New User Profile
@router.post("/users/profiles", response_model=UserProfile)
async def create_new_user_profile(profile_data: UserProfileCreate):
    """
    Create a new user profile for switching
    """
    await simulate_delay(400)
    
    try:
        # Check if email is already taken
        if is_email_taken(profile_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": {
                        "code": "EMAIL_ALREADY_EXISTS",
                        "message": "A user with this email address already exists",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        # Create the profile
        new_profile = create_user_profile(profile_data.dict())
        
        return UserProfile(**new_profile)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": f"Invalid user data provided: {str(e)}",
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )


# 4. Switch Active User
@router.post("/users/switch", response_model=UserSwitchResponse)
async def switch_user(switch_request: UserSwitchRequest):
    """
    Switch the active user context for the current session
    """
    await simulate_delay(350)
    
    try:
        result = switch_active_user(switch_request.user_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "USER_NOT_FOUND",
                        "message": f"User with ID '{switch_request.user_id}' not found or inactive",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        user_data = result["user"]
        session_data = result["session"]
        
        return UserSwitchResponse(
            success=True,
            message=f"Successfully switched to user: {user_data['name']}",
            active_user=UserProfile(**user_data),
            session_token=session_data["session_token"],
            expires_at=datetime.fromisoformat(session_data["expires_at"].replace("Z", "+00:00"))
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "SWITCH_FAILED",
                    "message": f"Failed to switch user: {str(e)}",
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )


# 5. Update User Profile
@router.put("/users/{user_id}/profile", response_model=UserProfile)
async def update_user_profile_endpoint(user_id: str, update_data: UserProfileUpdate):
    """
    Update an existing user profile
    """
    await simulate_delay(400)
    
    try:
        # Check if user exists
        existing_user = get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "USER_NOT_FOUND",
                        "message": f"User with ID '{user_id}' not found",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        # Update the profile
        updated_user = update_user_profile(user_id, update_data.dict(exclude_unset=True))
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user profile"
            )
        
        return UserProfile(**updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": f"Invalid update data: {str(e)}",
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )


# 6. Delete User Profile
@router.delete("/users/{user_id}/profile", response_model=UserDeleteResponse)
async def delete_user_profile_endpoint(user_id: str, delete_request: UserDeleteRequest = None):
    """
    Soft delete a user profile (marks as inactive)
    """
    await simulate_delay(300)
    
    try:
        # Check if user exists
        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "USER_NOT_FOUND",
                        "message": f"User with ID '{user_id}' not found",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        # Prevent deleting the current active user
        if user_id == CURRENT_ACTIVE_USER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": {
                        "code": "CANNOT_DELETE_ACTIVE_USER",
                        "message": "Cannot delete the currently active user",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        # Delete the profile
        success = delete_user_profile(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user profile"
            )
        
        return UserDeleteResponse(
            success=True,
            message="User profile successfully deactivated",
            user_id=user_id,
            status="inactive",
            deactivated_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "DELETE_FAILED",
                    "message": f"Failed to delete user: {str(e)}",
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )


# 7. Get Current Active User
@router.get("/users/current", response_model=CurrentUserResponse)
async def get_current_active_user():
    """
    Get the currently active user for the session
    """
    await simulate_delay(200)
    
    try:
        current_user = get_current_user()
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active user found"
            )
        
        session = get_user_session(current_user["id"])
        
        return CurrentUserResponse(
            id=current_user["id"],
            name=current_user["name"],
            email=current_user["email"],
            role=current_user["role"],
            avatar_url=current_user.get("avatar_url"),
            permissions=current_user["permissions"],
            session_started_at=datetime.fromisoformat(session["session_started_at"].replace("Z", "+00:00")) if session else datetime.now(),
            last_activity=datetime.fromisoformat(session["last_activity"].replace("Z", "+00:00")) if session else datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "CURRENT_USER_ERROR",
                    "message": f"Failed to get current user: {str(e)}",
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )


# Health check for user switching API
@router.get("/users/health")
async def user_switching_health_check():
    """Health check for user switching API"""
    await simulate_delay(100)
    
    try:
        profiles = get_all_profiles()
        current_user = get_current_user()
        
        return {
            "status": "healthy",
            "service": "user-switching-api",
            "total_users": len(profiles),
            "active_users": len([u for u in profiles if u["status"] == "active"]),
            "current_user_id": current_user["id"] if current_user else None,
            "timestamp": datetime.now().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "user-switching-api",
            "error": str(e),
            "timestamp": datetime.now().isoformat() + "Z"
        }