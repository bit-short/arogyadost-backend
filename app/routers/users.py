from fastapi import APIRouter, HTTPException
from typing import List

from app.models.user_profile import (
    UserProfile, UserSelectionResponse, UserSelectionRequest, CurrentUserResponse
)
from app.services.user_context import user_context_manager

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/available", response_model=UserSelectionResponse)
async def get_available_users():
    """
    Get list of all available test users including hardcoded default user.
    
    Returns users with demographics, health profiles, goals, and data availability indicators.
    """
    try:
        users = user_context_manager.get_available_users()
        
        return UserSelectionResponse(
            users=users,
            total_count=len(users),
            hardcoded_user_id="hardcoded"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load users: {str(e)}")


@router.post("/select")
async def select_user(request: UserSelectionRequest):
    """
    Select a specific test user or hardcoded default user as active.
    
    All subsequent API calls will use the selected user's data context.
    """
    try:
        selected_user = user_context_manager.select_user(request.user_id)
        
        return {
            "message": f"Successfully selected user: {request.user_id}",
            "selected_user": selected_user,
            "is_hardcoded": selected_user.is_hardcoded
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to select user: {str(e)}")


@router.get("/current", response_model=CurrentUserResponse)
async def get_current_user():
    """
    Get the currently active test user.
    
    Returns the active user's full profile including demographics, health data, and goals.
    """
    try:
        current_user = user_context_manager.get_current_user()
        is_default = user_context_manager.is_hardcoded_user_active()
        
        return CurrentUserResponse(
            active_user=current_user,
            is_default=is_default
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get current user: {str(e)}")


@router.get("/{user_id}", response_model=UserProfile)
async def get_user_by_id(user_id: str):
    """
    Get detailed information about a specific user by ID.
    """
    try:
        user = user_context_manager.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")


@router.get("")
async def list_user_ids():
    """
    Get a simple list of available user IDs for quick reference.
    """
    try:
        users = user_context_manager.get_available_users()
        user_ids = [user.user_id for user in users]
        
        return {
            "user_ids": user_ids,
            "current_user": user_context_manager.active_user_id,
            "total_count": len(user_ids)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list user IDs: {str(e)}")
