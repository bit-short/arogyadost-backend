from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Any, Dict, List, Optional
from app.models.digital_twin import DigitalTwin, FieldState
from app.storage.digital_twins import digital_twins

router = APIRouter(prefix="/api/digital-twin", tags=["digital-twin"])


@router.post("/users/{user_id}/create")
async def create_digital_twin(user_id: str, metadata: Dict[str, Any] = None):
    """Create a new digital twin for a user"""
    if user_id in digital_twins:
        raise HTTPException(status_code=400, detail="Digital twin already exists for this user")
    
    digital_twins[user_id] = DigitalTwin(user_id=user_id, metadata=metadata or {})
    return {"message": "Digital twin created successfully", "user_id": user_id}


@router.post("/users/{user_id}/data")
async def add_health_data(
    user_id: str,
    domain: str,
    field: str,
    value: Any,
    unit: Optional[str] = None,
    metadata: Dict[str, Any] = None
):
    """Add health data to a user's digital twin"""
    if user_id not in digital_twins:
        # Auto-create digital twin if it doesn't exist
        digital_twins[user_id] = DigitalTwin(user_id=user_id)
    
    digital_twins[user_id].set_value(domain, field, value, unit=unit, metadata=metadata)
    return {"message": "Health data added successfully"}


@router.get("/users/{user_id}/data/{domain}/{field}")
async def get_health_data(user_id: str, domain: str, field: str, latest: bool = True):
    """Get health data from a user's digital twin"""
    if user_id not in digital_twins:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    data = digital_twins[user_id].get_value(domain, field, latest=latest)
    if data is None:
        raise HTTPException(status_code=404, detail="Field not found")
    
    if latest:
        return {
            "value": data.value,
            "unit": data.unit,
            "timestamp": data.timestamp,
            "metadata": data.metadata
        }
    else:
        return [
            {
                "value": dp.value,
                "unit": dp.unit,
                "timestamp": dp.timestamp,
                "metadata": dp.metadata
            }
            for dp in data
        ]


@router.get("/users/{user_id}/domains/{domain}")
async def get_domain_data(user_id: str, domain: str):
    """Get all data from a specific health domain"""
    if user_id not in digital_twins:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    domain_obj = digital_twins[user_id].get_domain(domain)
    if domain_obj is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    result = {}
    for field_name, field in domain_obj.fields.items():
        if field.state == FieldState.POPULATED:
            latest = field.get_latest_value()
            result[field_name] = {
                "value": latest.value,
                "unit": latest.unit,
                "timestamp": latest.timestamp,
                "metadata": latest.metadata
            }
        else:
            result[field_name] = {"state": field.state.value}
    
    return result


@router.get("/users/{user_id}/missing-fields")
async def get_missing_fields(user_id: str):
    """Get all missing fields across domains"""
    if user_id not in digital_twins:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    missing_fields = digital_twins[user_id].get_missing_fields()
    return {"missing_fields": missing_fields}


@router.get("/users/{user_id}/completeness")
async def get_completeness(user_id: str):
    """Get data completeness percentage"""
    if user_id not in digital_twins:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    overall = digital_twins[user_id].get_overall_completeness()
    domain_completeness = {}
    
    for domain_name, domain in digital_twins[user_id].domains.items():
        domain_completeness[domain_name] = domain.get_completeness_percentage()
    
    return {
        "overall_completeness": overall,
        "domain_completeness": domain_completeness
    }


@router.get("/users/{user_id}/profile")
async def get_health_profile(user_id: str):
    """Get complete health profile for AI reasoning"""
    # Check if digital twin exists, if not create it for valid users
    if user_id not in digital_twins:
        from app.services.user_context import user_context_manager
        available_users = [u.user_id for u in user_context_manager.get_available_users()]
        
        if user_id in available_users:
            # Auto-create digital twin for valid users
            digital_twins[user_id] = DigitalTwin(user_id=user_id, metadata={})
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
    twin = digital_twins[user_id]
    profile = {
        "user_id": twin.user_id,
        "created_at": twin.created_at,
        "updated_at": twin.updated_at,
        "metadata": twin.metadata,
        "domains": {}
    }
    
    for domain_name, domain in twin.domains.items():
        domain_data = {}
        for field_name, field in domain.fields.items():
            if field.state == FieldState.POPULATED:
                latest = field.get_latest_value()
                domain_data[field_name] = {
                    "value": latest.value,
                    "unit": latest.unit,
                    "timestamp": latest.timestamp,
                    "metadata": latest.metadata
                }
            else:
                domain_data[field_name] = {"state": field.state.value}
        
        if domain_data:  # Only include domains with data
            profile["domains"][domain_name] = domain_data
    
    return profile
