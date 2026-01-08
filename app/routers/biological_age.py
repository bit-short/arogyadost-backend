from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.biological_age.engine import BiologicalAgeEngine
from app.models.digital_twin import DigitalTwin
from app.storage.digital_twins import digital_twins

router = APIRouter(prefix="/api/biological-age", tags=["biological-age"])

# Initialize the engine
engine = BiologicalAgeEngine()


@router.post("/users/{user_id}/predict")
async def predict_biological_age(user_id: str):
    """Predict biological age for a user's digital twin"""
    if user_id not in digital_twins:
        raise HTTPException(status_code=404, detail="Digital twin not found. Create one first using /api/digital-twin/users/{user_id}/create")
    
    try:
        digital_twin = digital_twins[user_id]
        result = engine.predict_biological_age(digital_twin)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/users/{user_id}/insights")
async def get_age_insights(user_id: str):
    """Get detailed biological age insights and recommendations"""
    if user_id not in digital_twins:
        raise HTTPException(status_code=404, detail="Digital twin not found. Create one first using /api/digital-twin/users/{user_id}/create")
    
    try:
        digital_twin = digital_twins[user_id]
        insights = engine.get_age_insights(digital_twin)
        return insights
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/users/available")
async def get_available_users():
    """Get list of users with digital twins available for biological age prediction"""
    return {
        "users": list(digital_twins.keys()),
        "total": len(digital_twins)
    }


@router.post("/users/all/predict")
async def predict_all_users():
    """Predict biological age for all users with digital twins"""
    if not digital_twins:
        raise HTTPException(status_code=404, detail="No digital twins found. Create some first using /api/digital-twin/")
    
    results = []
    for user_id, digital_twin in digital_twins.items():
        try:
            result = engine.predict_biological_age(digital_twin)
            results.append(result)
        except Exception as e:
            results.append({
                'user_id': user_id,
                'error': str(e)
            })
    
    return {
        "total_users": len(results),
        "results": results
    }


@router.get("/health")
async def health_check():
    """Health check for biological age service"""
    return {
        "status": "healthy",
        "available_digital_twins": len(digital_twins),
        "service": "biological-age-engine"
    }
