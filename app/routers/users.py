from fastapi import APIRouter, HTTPException
from typing import List

from app.models.user_profile import (
    UserProfile, UserSelectionResponse, UserSelectionRequest, CurrentUserResponse
)
from app.services.user_context import user_context_manager
from app.services.user_data_manager import user_data_manager

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


# Fast data access endpoints using in-memory manager
@router.get("/{user_id}/data")
async def get_user_data(user_id: str):
    """
    Get complete user data from in-memory cache for fast response.
    """
    if not user_data_manager.user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    
    user_data = user_data_manager.get_user(user_id)
    return user_data


@router.get("/{user_id}/biomarkers")
async def get_user_biomarkers(user_id: str):
    """
    Get user biomarkers from in-memory cache.
    """
    if not user_data_manager.user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    
    biomarkers = user_data_manager.get_user_biomarkers(user_id)
    return {"user_id": user_id, "biomarkers": biomarkers}


@router.get("/{user_id}/lifestyle")
async def get_user_lifestyle(user_id: str):
    """
    Get user lifestyle data from in-memory cache.
    """
    if not user_data_manager.user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    
    lifestyle = user_data_manager.get_user_lifestyle(user_id)
    return {"user_id": user_id, "lifestyle": lifestyle}


@router.get("/{user_id}/medical-history")
async def get_user_medical_history(user_id: str):
    """
    Get user medical history from in-memory cache.
    """
    if not user_data_manager.user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    
    medical_history = user_data_manager.get_user_medical_history(user_id)
    return {"user_id": user_id, "medical_history": medical_history}


@router.get("/{user_id}/summary")
async def get_user_summary(user_id: str):
    """
    Get user summary with data availability indicators.
    """
    summary = user_data_manager.get_user_summary(user_id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    
    return summary


@router.get("/{user_id}/full")
async def get_user_full_data(user_id: str):
    """
    Get complete user data including biomarkers and missing fields.
    """
    if not user_data_manager.user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    
    user = user_data_manager.get_user(user_id)
    biomarkers = user.get("biomarkers", {})
    
    # Define expected biomarkers
    expected_biomarkers = [
        "glucose_fasting", "hba1c", "total_cholesterol", "hdl", "ldl", "triglycerides",
        "vitamin_d", "vitamin_b12", "hemoglobin", "hematocrit", "wbc", "platelets",
        "tsh", "t3", "t4", "creatinine", "urea", "uric_acid", "iron", "calcium",
        "sodium", "sgot", "sgpt", "bilirubin_total"
    ]
    
    # Find missing biomarkers
    available = list(biomarkers.keys()) if isinstance(biomarkers, dict) else []
    missing = [b for b in expected_biomarkers if b not in available]
    
    return {
        "user_id": user_id,
        "profile": user.get("profile", {}),
        "biomarkers": {
            "available": biomarkers,
            "count": len(available),
            "missing": missing,
            "missing_count": len(missing)
        },
        "lifestyle": user.get("lifestyle", {}),
        "medical_history": user.get("medical_history", {}),
        "data_completeness": {
            "biomarkers_pct": round(len(available) / len(expected_biomarkers) * 100, 1) if expected_biomarkers else 0,
            "has_lifestyle": bool(user.get("lifestyle")),
            "has_medical_history": bool(user.get("medical_history"))
        }
    }
