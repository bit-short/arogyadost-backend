from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Demographics(BaseModel):
    age: int
    gender: str
    location: Optional[Dict[str, str]] = None


class HealthProfile(BaseModel):
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    blood_type: Optional[str] = None
    biological_age: Optional[float] = None


class HealthGoal(BaseModel):
    goal_id: str
    type: str
    target: str
    start_date: Optional[datetime] = None
    target_date: Optional[datetime] = None
    status: str = "active"


class DataAvailability(BaseModel):
    biomarkers: bool = False
    medical_history: bool = False
    lifestyle: bool = False
    ai_interactions: bool = False
    interventions: bool = False
    completeness_score: float = 0.0


class UserProfile(BaseModel):
    user_id: str
    display_name: str
    is_hardcoded: bool = False
    demographics: Demographics
    health_profile: Optional[HealthProfile] = None
    goals: List[HealthGoal] = Field(default_factory=list)
    data_availability: DataAvailability
    created_at: Optional[datetime] = None
    last_active: Optional[datetime] = None


class UserSelectionResponse(BaseModel):
    users: List[UserProfile]
    total_count: int
    hardcoded_user_id: str = "hardcoded"


class UserSelectionRequest(BaseModel):
    user_id: str


class CurrentUserResponse(BaseModel):
    active_user: UserProfile
    is_default: bool = False
