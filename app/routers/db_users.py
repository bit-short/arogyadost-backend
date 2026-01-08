"""
Database-backed API endpoints for user data.
"""

from fastapi import APIRouter, HTTPException
from app.services.user_db_service import user_db_service

router = APIRouter(prefix="/api/db", tags=["database"])


@router.get("/users")
async def get_all_users():
    """Get all users from database."""
    users = user_db_service.get_all_users()
    return {"users": users, "count": len(users)}


@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user profile from database."""
    user = user_db_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return user


@router.get("/users/{user_id}/biomarkers")
async def get_user_biomarkers(user_id: str):
    """Get user biomarkers grouped by category."""
    biomarkers = user_db_service.get_user_biomarkers_by_category(user_id)
    if not biomarkers:
        raise HTTPException(status_code=404, detail=f"No biomarkers found for '{user_id}'")
    
    total = sum(len(v) for v in biomarkers.values())
    return {"user_id": user_id, "biomarkers": biomarkers, "total_count": total}


@router.get("/users/{user_id}/medical-history")
async def get_user_medical_history(user_id: str):
    """Get user medical history."""
    history = user_db_service.get_user_medical_history(user_id)
    return {"user_id": user_id, "medical_history": history}


@router.get("/users/{user_id}/full")
async def get_user_full_data(user_id: str):
    """Get complete user data from database."""
    data = user_db_service.get_user_full_data(user_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return data
