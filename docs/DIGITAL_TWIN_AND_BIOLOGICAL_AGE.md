# Digital Twin & Biological Age System

## Overview

The Aarogyadost platform includes a sophisticated digital twin system for storing and managing user health data, coupled with an evidence-based biological age prediction engine. This document describes the architecture, data models, and usage of these systems.

## Digital Twin System

### Concept

A digital twin is a comprehensive, structured representation of a user's health data across multiple domains. It enables:
- Temporal tracking of health metrics
- Data completeness monitoring
- Flexible schema for diverse health data
- Foundation for AI-driven health insights

### Architecture

#### Domain Model

The digital twin is organized into health domains:
- **Demographics**: Age, gender, ethnicity, location
- **Biomarkers**: Lab results, vital signs, metabolic markers
- **Medical History**: Conditions, medications, procedures
- **Lifestyle**: Diet, exercise, sleep, stress
- **Genetics**: Genetic markers and predispositions

#### Data Structure

```python
DigitalTwin
├── user_id: str
├── created_at: datetime
├── updated_at: datetime
├── metadata: Dict[str, Any]
└── domains: Dict[str, HealthDomain]
    └── HealthDomain
        ├── domain_name: str
        └── fields: Dict[str, HealthField]
            └── HealthField
                ├── field_name: str
                ├── field_type: str
                ├── state: FieldState (populated/missing/not_applicable)
                └── values: List[HealthDataPoint]
                    └── HealthDataPoint
                        ├── value: Any
                        ├── timestamp: datetime
                        ├── unit: Optional[str]
                        └── metadata: Dict[str, Any]
```

### API Endpoints

#### Create Digital Twin
```http
POST /api/digital-twin/users/{user_id}/create
Content-Type: application/json

{
  "metadata": {
    "source": "manual_entry",
    "created_by": "user"
  }
}
```

#### Add Health Data
```http
POST /api/digital-twin/users/{user_id}/data
Content-Type: application/json

{
  "domain": "biomarkers",
  "field": "hba1c",
  "value": 5.8,
  "unit": "%",
  "metadata": {
    "lab": "SRL Diagnostics",
    "test_date": "2024-01-15"
  }
}
```

#### Get Specific Data
```http
GET /api/digital-twin/users/{user_id}/data/biomarkers/hba1c?latest=true

Response:
{
  "value": 5.8,
  "unit": "%",
  "timestamp": "2024-01-15T10:30:00Z",
  "metadata": {
    "lab": "SRL Diagnostics",
    "test_date": "2024-01-15"
  }
}
```

#### Get Domain Data
```http
GET /api/digital-twin/users/{user_id}/domains/biomarkers

Response:
{
  "hba1c": {
    "value": 5.8,
    "unit": "%",
    "timestamp": "2024-01-15T10:30:00Z",
    "metadata": {...}
  },
  "total_cholesterol": {
    "value": 195,
    "unit": "mg/dL",
    "timestamp": "2024-01-15T10:30:00Z",
    "metadata": {...}
  }
}
```

#### Get Data Completeness
```http
GET /api/digital-twin/users/{user_id}/completeness

Response:
{
  "overall_completeness": 65.5,
  "domain_completeness": {
    "demographics": 100.0,
    "biomarkers": 75.0,
    "medical_history": 50.0,
    "lifestyle": 60.0,
    "genetics": 20.0
  }
}
```

#### Get Complete Health Profile
```http
GET /api/digital-twin/users/{user_id}/profile

Response:
{
  "user_id": "test_user_1",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "metadata": {...},
  "domains": {
    "demographics": {...},
    "biomarkers": {...},
    "medical_history": {...},
    "lifestyle": {...}
  }
}
```

### Usage Examples

#### Python Client
```python
import httpx

# Create digital twin
response = httpx.post(
    "http://localhost:8000/api/digital-twin/users/user123/create",
    json={"metadata": {"source": "app"}}
)

# Add biomarker data
response = httpx.post(
    "http://localhost:8000/api/digital-twin/users/user123/data",
    json={
        "domain": "biomarkers",
        "field": "hba1c",
        "value": 5.8,
        "unit": "%"
    }
)

# Get completeness
response = httpx.get(
    "http://localhost:8000/api/digital-twin/users/user123/completeness"
)
print(response.json())
```

## Biological Age Prediction Engine

### Overview

The biological age engine calculates a user's biological age based on biomarkers and lifestyle factors, using evidence-based algorithms from longevity research.

### Calculation Methodology

#### Category Weights
```python
CATEGORY_WEIGHTS = {
    'metabolic': 0.25,      # HbA1c, glucose, insulin
    'cardiovascular': 0.25, # Cholesterol, triglycerides, BP
    'inflammatory': 0.20,   # CRP, inflammatory markers
    'hormonal': 0.15,       # Testosterone, thyroid, cortisol
    'organ_function': 0.15  # Kidney, liver function
}
```

#### Age Adjustments

**Metabolic Age**:
- Fasting glucose > 100 mg/dL: +3 years
- Fasting glucose > 126 mg/dL: +8 years
- HbA1c > 5.7%: +4 years
- HbA1c > 6.5%: +10 years

**Cardiovascular Age**:
- Total cholesterol > 240 mg/dL: +5 years
- Total cholesterol > 200 mg/dL: +2 years
- HDL < 40 mg/dL: +4 years
- HDL > 60 mg/dL: -2 years (protective)
- Triglycerides > 200 mg/dL: +3 years

**Hormonal Age**:
- Testosterone < 300 ng/dL: +3 years
- TSH > 4.0 mIU/L: +2 years

**Organ Function Age**:
- Creatinine > 1.2 mg/dL: +3 years
- ALT > 40 U/L: +2 years

### API Endpoints

#### Predict Biological Age
```http
POST /api/biological-age/users/{user_id}/predict

Response:
{
  "user_id": "test_user_1",
  "chronological_age": 35,
  "biological_age": 32.5,
  "age_delta": -2.5,
  "confidence_score": 85,
  "category_ages": {
    "metabolic": 33.0,
    "cardiovascular": 34.0,
    "inflammatory": 31.0,
    "hormonal": 32.0,
    "organ_function": 30.0
  },
  "interpretation": "Your biological age is 2.5 years younger than your chronological age",
  "confidence_level": "high"
}
```

#### Get Age Insights
```http
POST /api/biological-age/users/{user_id}/insights

Response:
{
  "user_id": "test_user_1",
  "biological_age_summary": {...},
  "key_insights": [
    "Excellent metabolic health - HbA1c in optimal range",
    "Cardiovascular age slightly elevated - focus on HDL improvement",
    "Outstanding organ function - kidney and liver markers optimal"
  ],
  "recommendations": [
    {
      "category": "cardiovascular",
      "priority": "high",
      "action": "Add Zone 2 cardio training 3x/week",
      "expected_impact": "Improve HDL and reduce cardiovascular age by 2-3 years"
    },
    {
      "category": "metabolic",
      "priority": "medium",
      "action": "Maintain current diet and fasting protocol",
      "expected_impact": "Sustain excellent metabolic age"
    }
  ],
  "data_quality": {
    "completeness": 85,
    "missing_markers": ["CRP", "Vitamin D"],
    "recommendation": "Add inflammatory markers for more accurate assessment"
  }
}
```

#### List Available Users
```http
GET /api/biological-age/users/available

Response:
{
  "users": ["test_user_1", "test_user_2", "test_user_3"],
  "total": 3
}
```

#### Predict All Users
```http
POST /api/biological-age/users/all/predict

Response:
{
  "total_users": 3,
  "results": [
    {
      "user_id": "test_user_1",
      "biological_age": 32.5,
      "age_delta": -2.5
    },
    {
      "user_id": "test_user_2",
      "biological_age": 45.2,
      "age_delta": 3.2
    }
  ]
}
```

### Usage Examples

#### Complete Workflow
```python
import httpx

base_url = "http://localhost:8000"

# 1. Create digital twin
httpx.post(f"{base_url}/api/digital-twin/users/user123/create")

# 2. Add demographic data
httpx.post(
    f"{base_url}/api/digital-twin/users/user123/data",
    json={"domain": "demographics", "field": "age", "value": 35}
)

# 3. Add biomarker data
biomarkers = [
    {"field": "hba1c", "value": 5.8, "unit": "%"},
    {"field": "total_cholesterol", "value": 195, "unit": "mg/dL"},
    {"field": "hdl_cholesterol", "value": 42, "unit": "mg/dL"},
    {"field": "triglycerides", "value": 145, "unit": "mg/dL"},
]

for biomarker in biomarkers:
    httpx.post(
        f"{base_url}/api/digital-twin/users/user123/data",
        json={"domain": "biomarkers", **biomarker}
    )

# 4. Predict biological age
response = httpx.post(
    f"{base_url}/api/biological-age/users/user123/predict"
)
print(f"Biological Age: {response.json()['biological_age']}")

# 5. Get detailed insights
response = httpx.post(
    f"{base_url}/api/biological-age/users/user123/insights"
)
print(response.json()['key_insights'])
```

## Data Requirements

### Minimum Data for Biological Age Prediction

**Required**:
- Age (demographics)
- At least 3 biomarkers from different categories

**Recommended for High Confidence**:
- Metabolic: HbA1c, fasting glucose
- Cardiovascular: Total cholesterol, HDL, triglycerides
- Hormonal: Testosterone, TSH
- Organ function: Creatinine, ALT

### Data Quality Metrics

The system calculates confidence scores based on:
- Number of available biomarkers
- Recency of data points
- Completeness across categories

**Confidence Levels**:
- High (80-100%): 6+ key biomarkers available
- Medium (50-79%): 3-5 key biomarkers available
- Low (<50%): <3 key biomarkers available

## Integration with Recommendation Engine

The biological age engine integrates with the recommendation system to provide:
- Age-specific health recommendations
- Priority scoring based on age delta
- Category-specific interventions
- Temporal tracking of age improvements

## Testing

### Property-Based Testing

The system uses Hypothesis for property-based testing:

```python
from hypothesis import given, strategies as st

@given(
    age=st.integers(min_value=18, max_value=100),
    hba1c=st.floats(min_value=4.0, max_value=15.0)
)
def test_biological_age_bounds(age, hba1c):
    """Biological age should be within reasonable bounds"""
    result = calculate_biological_age(age, {"hba1c": hba1c})
    assert 0 < result < 150
    assert abs(result - age) < 30  # Max 30 year delta
```

### Unit Tests

```bash
# Run all tests
pytest

# Run biological age tests only
pytest tests/unit/biological_age/
pytest tests/property/biological_age/

# Run with coverage
pytest --cov=app/services/biological_age
```

## Performance Considerations

- **In-Memory Storage**: Fast access for MVP, suitable for thousands of users
- **Async Operations**: Non-blocking I/O for better concurrency
- **Caching**: Consider Redis for frequently accessed digital twins
- **Database Migration**: PostgreSQL recommended for production scale

## Security & Privacy

- **Data Isolation**: Each user's digital twin is isolated
- **No PII in Logs**: Health data excluded from application logs
- **HTTPS Only**: All API calls encrypted in production
- **Future**: Add authentication, authorization, and audit logging

## Monitoring & Observability

### Health Check
```http
GET /api/biological-age/health

Response:
{
  "status": "healthy",
  "available_digital_twins": 150,
  "service": "biological-age-engine"
}
```

### Metrics to Monitor
- Digital twin creation rate
- Biological age prediction latency
- Data completeness distribution
- Confidence score distribution
- Error rates by endpoint

## Future Enhancements

1. **Machine Learning**: Train models on larger datasets for more accurate predictions
2. **Genetic Integration**: Incorporate genetic markers (APOE, MTHFR, etc.)
3. **Wearable Data**: Integrate continuous monitoring (HRV, sleep, activity)
4. **Longitudinal Analysis**: Track biological age changes over time
5. **Intervention Tracking**: Measure impact of lifestyle changes on biological age
6. **Population Benchmarking**: Compare against age-matched cohorts
