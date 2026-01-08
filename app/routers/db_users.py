"""
Database-backed API endpoints for user data.
"""

from fastapi import APIRouter, HTTPException, Request
from app.services.user_db_service import user_db_service
from app.services.digital_twin_db import digital_twin_db
from app.middleware.translation import get_translator, get_language

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
async def get_user_biomarkers(user_id: str, request: Request):
    """Get user biomarkers grouped by category."""
    biomarkers = user_db_service.get_user_biomarkers_by_category(user_id)
    if not biomarkers:
        raise HTTPException(status_code=404, detail=f"No biomarkers found for '{user_id}'")
    
    # Get translation function
    t = get_translator(request)
    
    # Translate biomarker categories and names
    translated_biomarkers = {}
    for category, markers in biomarkers.items():
        translated_category = t(f"health.categories.{category}")
        translated_markers = []
        
        for marker in markers:
            translated_marker = marker.copy()
            # Translate biomarker name if it has a translation key
            if 'name' in marker:
                biomarker_key = marker['name'].lower().replace(' ', '').replace('-', '')
                translated_name = t(f"health.biomarkers.{biomarker_key}")
                if translated_name != f"health.biomarkers.{biomarker_key}":  # Translation found
                    translated_marker['name'] = translated_name
            
            # Translate status
            if 'status' in marker:
                status_key = marker['status'].lower()
                translated_status = t(f"health.status.{status_key}")
                if translated_status != f"health.status.{status_key}":  # Translation found
                    translated_marker['status_label'] = translated_status
            
            translated_markers.append(translated_marker)
        
        translated_biomarkers[translated_category] = translated_markers
    
    total = sum(len(v) for v in biomarkers.values())
    return {
        "user_id": user_id, 
        "biomarkers": translated_biomarkers, 
        "total_count": total,
        "language": get_language(request)
    }


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


@router.get("/users/{user_id}/routines")
async def get_user_routines(user_id: str):
    """Get daily and weekly routines for user (auto-computed)."""
    computed = digital_twin_db.get_computed_data(user_id)
    if not computed:
        # Trigger computation
        digital_twin_db.compute_derived_data(user_id)
        computed = digital_twin_db.get_computed_data(user_id)
    
    return {
        "user_id": user_id,
        "daily_routine": computed.get('daily_routine', []),
        "weekly_routine": computed.get('weekly_routine', [])
    }


@router.get("/users/{user_id}/health-scores")
async def get_user_health_scores(user_id: str):
    """Get computed health scores for user."""
    computed = digital_twin_db.get_computed_data(user_id)
    if not computed or 'health_scores' not in computed:
        digital_twin_db.compute_derived_data(user_id)
        computed = digital_twin_db.get_computed_data(user_id)
    
    return {
        "user_id": user_id,
        "health_scores": computed.get('health_scores', {})
    }


@router.post("/users/{user_id}/recompute")
async def recompute_user_data(user_id: str):
    """Force recomputation of all derived data for user."""
    result = digital_twin_db.compute_derived_data(user_id)
    return {"user_id": user_id, "recomputed": True, "summary": {k: len(v) if isinstance(v, list) else 'computed' for k, v in result.items()}}
