from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum


class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestCategory(str, Enum):
    METABOLIC = "metabolic"
    LIPID_PROFILE = "lipid_profile"
    VITAMINS = "vitamins"
    HORMONES = "hormones"
    KIDNEY_FUNCTION = "kidney_function"
    LIVER_FUNCTION = "liver_function"
    COMPLETE_BLOOD_COUNT = "complete_blood_count"
    MINERALS = "minerals"
    TUMOR_MARKERS = "tumor_markers"
    INFLAMMATORY = "inflammatory"
    CARDIOVASCULAR = "cardiovascular"


class BiomarkerValue(BaseModel):
    value: float
    unit: str
    ref_range: str
    status: str  # normal, low, high


class BiomarkerSnapshot(BaseModel):
    test_date: datetime
    lab_name: str
    test_package: str
    categories: Dict[str, Dict[str, BiomarkerValue]]


class Demographics(BaseModel):
    age: int
    sex: str
    location: Optional[Dict[str, Any]] = None


class MedicalCondition(BaseModel):
    condition: str
    status: str  # active, resolved, managed
    diagnosed_date: Optional[datetime] = None
    severity: Optional[str] = None


class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str
    start_date: Optional[datetime] = None


class Supplement(BaseModel):
    name: str
    dosage: str
    frequency: str
    start_date: Optional[datetime] = None


class FamilyCondition(BaseModel):
    condition: str
    relation: str  # parent, sibling, grandparent
    age_of_onset: Optional[int] = None


class LifestyleFactors(BaseModel):
    diet_type: Optional[str] = None
    exercise_frequency: Optional[str] = None
    smoking: Optional[Dict[str, Any]] = None
    alcohol: Optional[Dict[str, Any]] = None
    sleep_quality: Optional[float] = None
    stress_level: Optional[int] = None


class HealthGoal(BaseModel):
    goal: str
    priority: str
    target_date: Optional[datetime] = None


class DigitalTwin(BaseModel):
    user_id: str
    demographics: Demographics
    latest_biomarkers: Optional[BiomarkerSnapshot] = None
    biomarker_history: List[BiomarkerSnapshot] = []
    conditions: List[MedicalCondition] = []
    medications: List[Medication] = []
    supplements: List[Supplement] = []
    family_history: List[FamilyCondition] = []
    lifestyle: Optional[LifestyleFactors] = None
    goals: List[HealthGoal] = []


class Recommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    test_name: str
    test_category: TestCategory
    rationale: str
    priority: PriorityLevel
    priority_score: float = 0.0
    suggested_timing: str
    related_biomarkers: List[str] = []
    related_conditions: List[str] = []
    educational_context: str = ""
    clinical_guideline_reference: Optional[str] = None


class RecommendationSummary(BaseModel):
    total_recommendations: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    categories_covered: List[str]


class RecommendationResponse(BaseModel):
    user_id: str
    generated_at: datetime = Field(default_factory=datetime.now)
    summary: RecommendationSummary
    recommendations: List[Recommendation]
    grouped_by_category: Dict[str, List[Recommendation]]
