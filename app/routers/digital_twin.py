from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Any, Dict, List, Optional
from app.models.digital_twin import DigitalTwin, FieldState
from app.storage.digital_twins import digital_twin_storage
from app.services.digital_twin_db import digital_twin_db

router = APIRouter(prefix="/api/digital-twin", tags=["digital-twin"])


@router.get("/users/{user_id}/from-db")
async def get_digital_twin_from_db(user_id: str):
    """Get digital twin populated from database."""
    twin = digital_twin_db.get_or_create_digital_twin(user_id)
    if not twin:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found in database")
    
    return {
        "user_id": user_id,
        "domains": {domain: len(fields) for domain, fields in twin.domains.items()},
        "completeness": twin.get_overall_completeness(),
        "data": {
            domain: {
                field: {
                    "value": state.value,
                    "unit": state.unit,
                    "timestamp": state.timestamp.isoformat() if state.timestamp else None
                }
                for field, state in fields.items()
            }
            for domain, fields in twin.domains.items()
        }
    }


@router.get("/users/{user_id}/summary")
async def get_digital_twin_summary(user_id: str):
    """Get digital twin summary from database."""
    summary = digital_twin_db.get_digital_twin_summary(user_id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return summary


@router.get("/db/users")
async def list_db_digital_twins():
    """List all users with digital twin data from database."""
    return digital_twin_db.list_available_twins()


@router.post("/users/{user_id}/create")
async def create_digital_twin(user_id: str, metadata: Dict[str, Any] = None):
    """Create a new digital twin for a user"""
    if digital_twin_storage.exists(user_id):
        raise HTTPException(status_code=400, detail="Digital twin already exists for this user")
    
    digital_twin = DigitalTwin(user_id=user_id, metadata=metadata or {})
    digital_twin_storage.set(user_id, digital_twin)
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
    digital_twin = digital_twin_storage.get(user_id)
    if not digital_twin:
        # Auto-create digital twin if it doesn't exist
        digital_twin = DigitalTwin(user_id=user_id)
    
    digital_twin.set_value(domain, field, value, unit=unit, metadata=metadata)
    digital_twin_storage.set(user_id, digital_twin)
    return {"message": "Health data added successfully"}


@router.get("/users/{user_id}/data/{domain}/{field}")
async def get_health_data(user_id: str, domain: str, field: str, latest: bool = True):
    """Get health data from a user's digital twin"""
    digital_twin = digital_twin_storage.get(user_id)
    if not digital_twin:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    data = digital_twin.get_value(domain, field, latest=latest)
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
    digital_twin = digital_twin_storage.get(user_id)
    if not digital_twin:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    domain_obj = digital_twin.get_domain(domain)
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
    digital_twin = digital_twin_storage.get(user_id)
    if not digital_twin:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    missing_fields = digital_twin.get_missing_fields()
    return {"missing_fields": missing_fields}


@router.get("/users/{user_id}/completeness")
async def get_completeness(user_id: str):
    """Get data completeness percentage"""
    digital_twin = digital_twin_storage.get(user_id)
    if not digital_twin:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    overall = digital_twin.get_overall_completeness()
    domain_completeness = {}
    
    for domain_name, domain in digital_twin.domains.items():
        domain_completeness[domain_name] = domain.get_completeness_percentage()
    
    return {
        "overall_completeness": overall,
        "domain_completeness": domain_completeness
    }


@router.get("/users/{user_id}/profile")
async def get_health_profile(user_id: str):
    """Get complete health profile for AI reasoning"""
    # Check if digital twin exists, if not create it for valid users
    digital_twin = digital_twin_storage.get(user_id)
    if not digital_twin:
        from app.services.user_context import user_context_manager
        available_users = [u.user_id for u in user_context_manager.get_available_users()]
        
        if user_id in available_users:
            # Auto-create digital twin for valid users
            digital_twin = DigitalTwin(user_id=user_id, metadata={})
            digital_twin_storage.set(user_id, digital_twin)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
    profile = {
        "user_id": digital_twin.user_id,
        "created_at": digital_twin.created_at,
        "updated_at": digital_twin.updated_at,
        "metadata": digital_twin.metadata,
        "domains": {}
    }
    
    for domain_name, domain in digital_twin.domains.items():
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
