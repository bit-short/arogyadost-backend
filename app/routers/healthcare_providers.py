"""
Healthcare Providers Router
API endpoints for doctors, labs, user profiles, and data sources
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.healthcare_providers import (
    DoctorsResponse, LabsResponse, UserProfilesResponse, DataSourcesResponse,
    Doctor, Lab, UserProfile, DataSource, ProductImage
)
from app.storage.healthcare_providers_storage import healthcare_storage

router = APIRouter(prefix="/api/healthcare", tags=["Healthcare Providers"])


@router.get("/doctors", response_model=DoctorsResponse)
async def get_doctors(
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    partner_only: bool = Query(False, description="Show only partner doctors")
):
    """
    Get list of doctors with optional filtering
    
    - **specialty**: Filter doctors by specialty (e.g., "cardiology", "longevity")
    - **partner_only**: If true, only return partner/sponsored doctors
    """
    try:
        return healthcare_storage.get_doctors(specialty=specialty, partner_only=partner_only)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doctors: {str(e)}")


@router.get("/doctors/{doctor_id}", response_model=Doctor)
async def get_doctor_by_id(doctor_id: str):
    """Get specific doctor by ID"""
    try:
        doctors_response = healthcare_storage.get_doctors()
        doctor = next((d for d in doctors_response.doctors if d.id == doctor_id), None)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doctor: {str(e)}")


@router.get("/labs", response_model=LabsResponse)
async def get_labs(
    test_type: Optional[str] = Query(None, description="Filter by test type")
):
    """
    Get list of labs with optional filtering
    
    - **test_type**: Filter labs by test type (e.g., "lipid", "vitamin")
    """
    try:
        return healthcare_storage.get_labs(test_type=test_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch labs: {str(e)}")


@router.get("/labs/{lab_id}", response_model=Lab)
async def get_lab_by_id(lab_id: str):
    """Get specific lab by ID"""
    try:
        labs_response = healthcare_storage.get_labs()
        lab = next((l for l in labs_response.labs if l.id == lab_id), None)
        if not lab:
            raise HTTPException(status_code=404, detail="Lab not found")
        return lab
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lab: {str(e)}")


@router.get("/user-profiles", response_model=UserProfilesResponse)
async def get_user_profiles():
    """Get user profiles for settings"""
    try:
        return healthcare_storage.get_user_profiles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user profiles: {str(e)}")


@router.get("/data-sources", response_model=DataSourcesResponse)
async def get_data_sources():
    """Get available data sources (wearables, devices)"""
    try:
        return healthcare_storage.get_data_sources()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data sources: {str(e)}")


@router.get("/product-images")
async def get_product_images():
    """Get product images mapping"""
    try:
        images = healthcare_storage.get_product_images()
        return {"product_images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product images: {str(e)}")


@router.get("/product-images/by-path")
async def get_product_image_by_path(image_path: str = Query(..., description="Image path to lookup")):
    """Get product image by path"""
    try:
        image = healthcare_storage.get_product_image_by_path(image_path)
        if not image:
            raise HTTPException(status_code=404, detail="Product image not found")
        return image
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product image: {str(e)}")


# Legacy compatibility endpoints (to match existing frontend calls)
@router.get("/doctors-legacy")
async def get_doctors_legacy():
    """Legacy endpoint for doctors (matches existing frontend expectations)"""
    try:
        response = healthcare_storage.get_doctors()
        # Transform to match existing frontend format
        return [
            {
                "id": doc.id,
                "name": doc.name,
                "specialty": doc.specialty,
                "rating": doc.rating,
                "location": doc.address,
                "phone": doc.phone,
                "experience": f"{doc.experience_years} years" if doc.experience_years else "Experienced"
            }
            for doc in response.doctors
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doctors: {str(e)}")


@router.get("/labs-legacy")
async def get_labs_legacy():
    """Legacy endpoint for labs (matches existing frontend expectations)"""
    try:
        response = healthcare_storage.get_labs()
        # Transform to match existing frontend format
        return [
            {
                "id": lab.id,
                "name": lab.name,
                "rating": lab.rating,
                "location": lab.address,
                "tests": lab.specialties
            }
            for lab in response.labs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch labs: {str(e)}")