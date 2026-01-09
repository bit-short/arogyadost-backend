"""
Healthcare Providers Models
Defines data models for doctors, labs, and other healthcare providers
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime, time


class Doctor(BaseModel):
    """Doctor/Healthcare Provider model"""
    id: str
    name: str
    specialty: str
    rating: float = Field(ge=0, le=5)
    review_count: int = Field(ge=0)
    distance: str  # e.g., "1.2 mi"
    next_available: str  # e.g., "Tomorrow, 10:00 AM"
    image_url: str
    is_partner: bool = False
    is_sponsored: bool = False
    phone: Optional[str] = None
    address: Optional[str] = None
    languages: List[str] = Field(default_factory=lambda: ["English"])
    consultation_fee: Optional[int] = None  # in INR
    experience_years: Optional[int] = None
    qualifications: List[str] = Field(default_factory=list)
    available_slots: List[str] = Field(default_factory=list)


class Lab(BaseModel):
    """Laboratory/Testing Facility model"""
    id: str
    name: str
    type: Literal["sponsored", "partner", "regular"]
    rating: float = Field(ge=0, le=5)
    review_count: int = Field(ge=0)
    distance: str
    address: str
    next_available: str
    specialties: List[str]
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    operating_hours: Optional[str] = None
    tests_offered: List[str] = Field(default_factory=list)
    home_collection: bool = False
    online_reports: bool = False


class UserProfile(BaseModel):
    """User Profile model for settings"""
    id: str
    name: str
    initial: str
    is_primary: bool = False
    created_at: datetime
    updated_at: datetime


class DataSource(BaseModel):
    """Wearable/Health Device Data Source model"""
    id: str
    name: str
    icon: str  # Icon identifier
    description: str
    connected: bool = False
    device_type: Literal["wearable", "monitor", "scale", "sensor"]
    brand: Optional[str] = None
    model: Optional[str] = None
    last_sync: Optional[datetime] = None
    data_types: List[str] = Field(default_factory=list)  # e.g., ["heart_rate", "steps", "sleep"]


class ProductImage(BaseModel):
    """Product Image mapping model"""
    id: str
    name: str
    category: str
    image_path: str
    alt_text: str
    description: Optional[str] = None


# Response models
class DoctorsResponse(BaseModel):
    """Response model for doctors list"""
    doctors: List[Doctor]
    total_count: int
    featured_count: int
    partner_count: int


class LabsResponse(BaseModel):
    """Response model for labs list"""
    labs: List[Lab]
    total_count: int
    sponsored_count: int
    partner_count: int


class UserProfilesResponse(BaseModel):
    """Response model for user profiles"""
    profiles: List[UserProfile]
    active_profile_id: str


class DataSourcesResponse(BaseModel):
    """Response model for data sources"""
    data_sources: List[DataSource]
    connected_count: int
    available_count: int