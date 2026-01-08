from fastapi import APIRouter, HTTPException
from app.services.recommendations.engine import RecommendationEngine
from app.services.recommendations.models import RecommendationResponse

router = APIRouter(prefix="/api", tags=["recommendations"])

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()


@router.get("/recommendations/{user_id}", response_model=RecommendationResponse)
async def get_recommendations(user_id: str):
    """
    Generate personalized health recommendations for a user.
    
    This endpoint analyzes the user's digital twin data including:
    - Biomarker history and current values
    - Medical conditions and medications
    - Demographics and family history
    - Lifestyle factors and health goals
    
    Returns prioritized recommendations for blood tests and health monitoring.
    """
    try:
        if not user_id or user_id.strip() == "":
            raise HTTPException(status_code=400, detail="User ID is required")
        
        # Generate recommendations
        response = recommendation_engine.generate_recommendations(user_id)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/recommendations/{user_id}/summary")
async def get_recommendations_summary(user_id: str):
    """
    Get a summary of recommendations for a user without full details.
    """
    try:
        if not user_id or user_id.strip() == "":
            raise HTTPException(status_code=400, detail="User ID is required")
        
        response = recommendation_engine.generate_recommendations(user_id)
        
        return {
            "user_id": response.user_id,
            "generated_at": response.generated_at,
            "summary": response.summary
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate recommendations summary: {str(e)}"
        )
