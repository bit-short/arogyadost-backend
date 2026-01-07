# Design Document: Biological Age Prediction Reasoning Engine

## Overview

The Biological Age Prediction Reasoning Engine implements the PhenoAge algorithm ([Levine et al. 2018](https://doi.org/10.18632/aging.101414)) to calculate biological age from biomarker data. The engine loads test user data from JSON files, processes biomarkers through evidence-based formulas, and returns comprehensive age predictions with contributor analysis.

The MVP focuses on the 6 test users with existing data, providing a foundation for future expansion. The engine is designed as a Python module that can be integrated into the FastAPI backend.

**Key Design Principles:**
- Evidence-based algorithms from peer-reviewed research
- Graceful handling of missing data with confidence scoring
- Clear separation between data loading, calculation, and output formatting
- Extensible architecture for future algorithm additions

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                  Biological Age Engine                       │
│                                                              │
│  ┌────────────────┐  ┌──────────────────┐  ┌─────────────┐ │
│  │  Data Loader   │→ │  Age Calculator  │→ │  Formatter  │ │
│  └────────────────┘  └──────────────────┘  └─────────────┘ │
│         ↓                     ↓                     ↓        │
│  ┌────────────────┐  ┌──────────────────┐  ┌─────────────┐ │
│  │ JSON Files     │  │ PhenoAge Model   │  │ Result Dict │ │
│  │ - users        │  │ - Biomarkers     │  │ - Age       │ │
│  │ - biomarkers   │  │ - Weights        │  │ - Delta     │ │
│  │ - lifestyle    │  │ - Formula        │  │ - Breakdown │ │
│  └────────────────┘  └──────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input**: User ID (e.g., "test_user_1_29f")
2. **Load**: Read user profile, biomarkers, lifestyle from JSON files
3. **Validate**: Check required fields, normalize units
4. **Calculate**: Apply PhenoAge formula to biomarkers
5. **Analyze**: Identify age contributors and compute confidence
6. **Output**: Return structured prediction with metadata

## Components and Interfaces

### 1. Data Loader Module

**Purpose**: Load and validate test user data from JSON files

**Interface**:
```python
class DataLoader:
    def __init__(self, datasets_path: str = "datasets/"):
        """Initialize with path to datasets directory"""
        
    def load_user_profile(self, user_id: str) -> Dict:
        """Load user demographics and health profile"""
        
    def load_biomarkers(self, user_id: str) -> List[Dict]:
        """Load biomarker history for user"""
        
    def load_lifestyle(self, user_id: str) -> Optional[List[Dict]]:
        """Load lifestyle data if available"""
        
    def load_medical_history(self, user_id: str) -> Optional[Dict]:
        """Load medical history if available"""
```

**Responsibilities**:
- Read JSON files from datasets/ directory
- Handle missing files gracefully (return None for optional data)
- Validate JSON structure
- Cache loaded data to avoid repeated file reads

### 2. Biomarker Normalizer Module

**Purpose**: Convert biomarker units to PhenoAge standard units

**Interface**:
```python
class BiomarkerNormalizer:
    @staticmethod
    def normalize_albumin(value: float, unit: str) -> float:
        """Convert albumin to g/L (multiply g/dL by 10)"""
        
    @staticmethod
    def normalize_creatinine(value: float, unit: str) -> float:
        """Convert creatinine to µmol/L (multiply mg/dL by 88.401)"""
        
    @staticmethod
    def normalize_glucose(value: float, unit: str) -> float:
        """Convert glucose to mmol/L (multiply mg/dL by 0.0555)"""
        
    @staticmethod
    def normalize_crp(value: float, unit: str) -> float:
        """Convert CRP to mg/L (multiply mg/dL by 10)"""
```

**Unit Conversions**:
- Albumin: g/dL → g/L (×10)
- Creatinine: mg/dL → µmol/L (×88.401)
- Glucose: mg/dL → mmol/L (×0.0555)
- CRP: mg/dL → mg/L (×10)

### 3. PhenoAge Calculator Module

**Purpose**: Implement the PhenoAge algorithm

**Interface**:
```python
class PhenoAgeCalculator:
    # PhenoAge coefficients from Levine et al. 2018
    COEFFICIENTS = {
        'intercept': -19.9067,
        'albumin': -0.0336,
        'creatinine': 0.0095,
        'glucose': 0.1953,
        'log_crp': 0.0954,
        'lymphocyte_percent': -0.0120,
        'mcv': 0.0268,
        'rdw': 0.3306,
        'alkaline_phosphatase': 0.00188,
        'wbc': 0.0554,
        'chronological_age': 0.0804
    }
    
    def calculate_xb(self, biomarkers: Dict, chronological_age: float) -> float:
        """Calculate weighted sum of biomarkers"""
        
    def calculate_mortality_score(self, xb: float) -> float:
        """Calculate mortality score M from xb"""
        
    def calculate_phenoage(self, mortality_score: float) -> float:
        """Calculate phenotypic age from mortality score"""
        
    def predict(self, biomarkers: Dict, chronological_age: float) -> float:
        """Main prediction function"""
```

**Algorithm** (Content rephrased for compliance with licensing restrictions):

The PhenoAge calculation follows a three-step process:

1. **Weighted Sum (xb)**: Combine biomarker values with their coefficients
2. **Mortality Score (M)**: Transform xb into a mortality probability
3. **Phenotypic Age**: Convert mortality score to biological age estimate

The formula uses 9 biomarkers plus chronological age, each weighted according to their association with mortality risk in the NHANES dataset.

### 4. Age Contributor Analyzer Module

**Purpose**: Identify which factors are aging or de-aging the user

**Interface**:
```python
class AgeContributorAnalyzer:
    def analyze_contributors(
        self, 
        biomarkers: Dict, 
        chronological_age: float,
        biological_age: float
    ) -> Dict:
        """Identify top aging and de-aging factors"""
        
    def calculate_biomarker_impact(
        self, 
        biomarker_name: str, 
        value: float, 
        optimal_range: Tuple[float, float]
    ) -> float:
        """Calculate age impact of single biomarker"""
        
    def categorize_impact(self, impact_years: float) -> str:
        """Categorize as critical (>5y), moderate (2-5y), or minor (<2y)"""
```

**Impact Calculation**:
- Compare each biomarker to optimal ranges for longevity
- Calculate deviation from optimal
- Weight by biomarker coefficient to estimate age impact
- Rank contributors by absolute impact

### 5. Confidence Score Calculator Module

**Purpose**: Assess prediction reliability based on data completeness

**Interface**:
```python
class ConfidenceCalculator:
    def calculate_confidence(
        self,
        biomarkers: Dict,
        lifestyle_data: Optional[Dict],
        data_age_months: int
    ) -> int:
        """Calculate confidence score (0-100)"""
```

**Confidence Rules**:
- Base confidence: 90 (all biomarkers present)
- Missing biomarker category: -10 points each
- Missing lifestyle data: -5 points
- Data age 6-12 months: -10 points
- Data age >12 months: -20 points
- Minimum confidence: 20

### 6. Biological Age Engine (Main Interface)

**Purpose**: Orchestrate all components and provide public API

**Interface**:
```python
class BiologicalAgeEngine:
    def __init__(self, datasets_path: str = "datasets/"):
        """Initialize engine with data loader and calculators"""
        
    def predict_age(self, user_id: str) -> Dict:
        """
        Main prediction function
        
        Returns:
        {
            "user_id": str,
            "chronological_age": float,
            "biological_age": float,
            "age_delta": float,  # negative = younger
            "confidence_score": int,
            "model_version": str,
            "calculation_date": str,
            "biomarkers_used": List[str],
            "contributors": {
                "aging_factors": List[Dict],  # top 5
                "de_aging_factors": List[Dict]  # top 5
            },
            "warnings": List[str]
        }
        """
        
    def predict_batch(self, user_ids: List[str]) -> List[Dict]:
        """Batch prediction for multiple users"""
        
    def predict_with_intervention(
        self, 
        user_id: str, 
        intervention_effects: Dict
    ) -> Dict:
        """Predict age assuming intervention success"""
```

## Data Models

### Input Data Structures

```python
# From datasets/users/users.json
UserProfile = {
    "user_id": str,
    "demographics": {
        "age": int,
        "gender": str,  # "M" or "F"
        "location": {"city": str, "country": str}
    },
    "health_profile": {
        "height_cm": float,
        "weight_kg": float,
        "bmi": float,
        "blood_type": str,
        "biological_age": float  # existing estimate
    }
}

# From datasets/biomarkers/biomarkers_<user_id>.json
BiomarkerData = {
    "user_id": str,
    "test_date": str,  # ISO8601
    "biomarkers": {
        "metabolic": {
            "fasting_glucose": {"value": float, "unit": str, "status": str},
            "hba1c": {"value": float, "unit": str, "status": str}
        },
        "lipid_profile": {...},
        "complete_blood_count": {
            "wbc": {"value": float, "unit": str},
            "lymphocytes": {"value": float, "unit": str},
            "mcv": {"value": float, "unit": str},
            "rdw": {"value": float, "unit": str}
        },
        "liver_function": {
            "alkaline_phosphatase": {"value": float, "unit": str},
            "albumin": {"value": float, "unit": str}
        },
        "kidney_function": {
            "creatinine": {"value": float, "unit": str}
        }
    }
}
```

### Output Data Structure

```python
PredictionResult = {
    "user_id": str,
    "chronological_age": float,
    "biological_age": float,
    "age_delta": float,
    "confidence_score": int,
    "model_version": str,  # "phenoage_v1.0"
    "calculation_date": str,  # ISO8601
    "biomarkers_used": List[str],
    "contributors": {
        "aging_factors": [
            {
                "name": str,
                "value": float,
                "optimal_range": str,
                "impact_years": float,
                "severity": str  # "critical", "moderate", "minor"
            }
        ],
        "de_aging_factors": [...]
    },
    "warnings": List[str]
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Data Loading Completeness
*For any* valid test user ID, loading user data should return either valid structured data or None for optional data, but never crash or return malformed data.
**Validates: Requirements 1.1, 1.2, 1.3, 1.4, 12.5**

### Property 2: Error Handling for Invalid Inputs
*For any* invalid input (missing files, malformed JSON, impossible biomarker values, missing required fields, invalid age), the system should raise a descriptive exception rather than crash or return incorrect results.
**Validates: Requirements 1.5, 10.1, 10.2, 10.3, 10.4, 10.5**

### Property 3: Biomarker Calculation Validity
*For any* set of valid biomarkers, the calculated age contribution should be a finite number within physiologically reasonable bounds (not NaN, not infinite, between 0 and 150 years).
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

### Property 4: Lifestyle Factor Integration
*For any* user with lifestyle data, each lifestyle factor (sleep, activity, nutrition, stress) should produce a numeric impact value, and predictions with lifestyle data should differ from predictions without it.
**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

### Property 5: Output Structure Completeness
*For any* valid prediction, the output should be a dictionary containing all required fields (user_id, chronological_age, biological_age, age_delta, confidence_score, model_version, calculation_date, biomarkers_used, contributors, warnings) with correct types.
**Validates: Requirements 4.1, 4.4, 4.6, 13.3**

### Property 6: Age Delta Consistency
*For any* valid prediction, the age_delta field should equal biological_age minus chronological_age.
**Validates: Requirements 4.2**

### Property 7: Confidence Score Bounds
*For any* valid prediction, the confidence score should be an integer between 20 and 100 (inclusive).
**Validates: Requirements 4.3, 8.6**

### Property 8: Low Confidence Warnings
*For any* prediction with confidence score below 60, the warnings list should be non-empty and describe the data completeness issues.
**Validates: Requirements 4.5**

### Property 9: Contributor List Structure
*For any* valid prediction, both aging_factors and de_aging_factors lists should contain at most 5 items each, sorted by absolute impact magnitude, and each item should have name, value, optimal_range, impact_years, and severity fields.
**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**

### Property 10: Confidence Reduction for Missing Data
*For any* prediction, if biomarker categories are missing, the confidence score should be reduced by 10 points per missing category; if lifestyle data is missing, confidence should be reduced by 5 points.
**Validates: Requirements 2.7, 8.2, 8.3**

### Property 11: Confidence Reduction for Data Age
*For any* prediction where biomarker data is older than 6 months, confidence should be reduced by 10 points; if older than 12 months, reduced by 20 points.
**Validates: Requirements 8.4, 8.5**

### Property 12: Temporal Analysis Completeness
*For any* user with multiple historical biomarker records, the engine should calculate biological age for each time point and return a time series with timestamps, age values, and age velocity.
**Validates: Requirements 6.1, 6.2, 6.4, 6.5**

### Property 13: Intervention Impact Prediction
*For any* user with active interventions, the engine should return a projected biological age, expected age reduction, time horizon, and combined effects when multiple interventions are present.
**Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

### Property 14: Gender and Age-Specific Models
*For any* user, the engine should apply reference ranges and model weights appropriate to their gender (male/female) and age group (under 30, 30-50, over 50).
**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**

### Property 15: Model Version Tagging
*For any* prediction, the model_version field should be present, non-empty, and indicate the algorithm used (e.g., "phenoage_v1.0").
**Validates: Requirements 14.1, 14.2, 14.3**

### Property 16: Explainability Completeness
*For any* prediction, the output should include biomarkers_used list, model_version, and contributors with explanatory information about why each factor impacts aging.
**Validates: Requirements 11.1, 11.2, 11.3, 11.4**

### Property 17: Performance Bounds
*For any* single user prediction, the calculation should complete within 2 seconds; caching should prevent repeated file reads for the same user.
**Validates: Requirements 12.1, 12.3**

### Property 18: API Interface Consistency
*For any* valid user_id string, the predict_age function should accept it as input, load data from JSON files, and return a dictionary; for any error scenario, it should raise an appropriate exception type.
**Validates: Requirements 13.2, 13.5**

## Error Handling

### Error Categories

1. **Data Loading Errors**
   - FileNotFoundError: Required data file missing
   - JSONDecodeError: Malformed JSON in data file
   - KeyError: Required field missing from data structure

2. **Validation Errors**
   - ValueError: Biomarker value outside physiological range
   - ValueError: Chronological age outside [18, 120]
   - ValueError: Required demographics missing

3. **Calculation Errors**
   - RuntimeError: PhenoAge calculation failed (log error, return fallback)
   - ZeroDivisionError: Division by zero in formula (handle gracefully)

### Error Handling Strategy

- **Fail Fast**: Validate inputs before calculation
- **Descriptive Messages**: Include field name and expected format in error messages
- **Graceful Degradation**: Return partial results with warnings when possible
- **Logging**: Log all errors with context for debugging
- **Fallback**: For calculation failures, return chronological age as biological age with confidence=20

### Example Error Messages

```python
# Good error message
raise ValueError(
    f"Glucose value {glucose} mg/dL is outside physiological range [20, 600]. "
    f"Please verify the biomarker data for user {user_id}."
)

# Bad error message
raise ValueError("Invalid glucose")
```

## Testing Strategy

### Dual Testing Approach

The testing strategy combines unit tests for specific examples and edge cases with property-based tests for universal correctness properties. Both approaches are complementary and necessary for comprehensive coverage.

**Unit Tests**:
- Verify specific examples (e.g., test_user_1_29f calculation)
- Test edge cases (missing data, boundary values)
- Test error conditions (invalid inputs, file not found)
- Test integration between components

**Property-Based Tests**:
- Verify universal properties across all inputs
- Use Hypothesis library to generate random test data
- Run minimum 100 iterations per property test
- Each property test references its design document property

### Property-Based Testing Configuration

**Library**: Hypothesis for Python
**Iterations**: Minimum 100 per test
**Tagging Format**: Each test includes a comment:
```python
# Feature: biological-age-engine, Property 1: Data Loading Completeness
```

### Test Organization

```
tests/
├── unit/
│   ├── test_data_loader.py
│   ├── test_biomarker_normalizer.py
│   ├── test_phenoage_calculator.py
│   ├── test_contributor_analyzer.py
│   ├── test_confidence_calculator.py
│   └── test_biological_age_engine.py
├── property/
│   ├── test_properties_data_loading.py
│   ├── test_properties_calculation.py
│   ├── test_properties_output.py
│   └── test_properties_error_handling.py
└── integration/
    └── test_end_to_end.py
```

### Example Property Test

```python
from hypothesis import given, strategies as st
import pytest

# Feature: biological-age-engine, Property 5: Output Structure Completeness
@given(user_id=st.sampled_from([
    "test_user_1_29f", "test_user_2_29m", "test_user_3_31m",
    "test_user_4_31m", "test_user_5_55f", "test_user_6_65m"
]))
def test_output_structure_completeness(user_id):
    """For any valid prediction, output should contain all required fields"""
    engine = BiologicalAgeEngine()
    result = engine.predict_age(user_id)
    
    # Check all required fields present
    required_fields = [
        "user_id", "chronological_age", "biological_age", "age_delta",
        "confidence_score", "model_version", "calculation_date",
        "biomarkers_used", "contributors", "warnings"
    ]
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
    
    # Check types
    assert isinstance(result["chronological_age"], (int, float))
    assert isinstance(result["biological_age"], (int, float))
    assert isinstance(result["confidence_score"], int)
    assert isinstance(result["biomarkers_used"], list)
    assert isinstance(result["contributors"], dict)
```

### Example Unit Test

```python
def test_test_user_1_29f_prediction():
    """Test specific prediction for test_user_1_29f"""
    engine = BiologicalAgeEngine()
    result = engine.predict_age("test_user_1_29f")
    
    # Verify basic structure
    assert result["user_id"] == "test_user_1_29f"
    assert result["chronological_age"] == 29
    
    # Biological age should be reasonable
    assert 20 <= result["biological_age"] <= 40
    
    # Should have high confidence with complete data
    assert result["confidence_score"] >= 70
    
    # Should identify vitamin D and lipid issues as aging factors
    aging_factor_names = [f["name"] for f in result["contributors"]["aging_factors"]]
    assert "vitamin_d" in aging_factor_names or "triglycerides" in aging_factor_names
```

### Test Data Generators

For property-based tests, create generators for:
- Valid biomarker values within physiological ranges
- Invalid biomarker values (negative, extreme, NaN)
- Partial biomarker sets (missing categories)
- User profiles with various ages and genders
- Historical data with multiple time points

### Coverage Goals

- Line coverage: >90%
- Branch coverage: >85%
- Property test iterations: 100+ per property
- All 18 correctness properties tested
- All error conditions tested

## Implementation Notes

### PhenoAge Algorithm Details

The PhenoAge algorithm uses these specific coefficients from [Levine et al. 2018](https://doi.org/10.18632/aging.101414):

```python
PHENOAGE_COEFFICIENTS = {
    'intercept': -19.9067,
    'albumin': -0.0336,        # g/L
    'creatinine': 0.0095,      # µmol/L
    'glucose': 0.1953,         # mmol/L
    'log_crp': 0.0954,         # log(mg/L)
    'lymphocyte_percent': -0.0120,  # %
    'mcv': 0.0268,             # fL
    'rdw': 0.3306,             # %
    'alkaline_phosphatase': 0.00188,  # U/L
    'wbc': 0.0554,             # 10³/µL
    'chronological_age': 0.0804  # years
}
```

### Optimal Ranges for Longevity

Based on longevity research, these are optimal ranges for biological age minimization:

- **Glucose**: 70-85 mg/dL (fasting)
- **HbA1c**: <5.0%
- **CRP**: <0.5 mg/L
- **Albumin**: 4.5-5.0 g/dL
- **Creatinine**: 0.7-1.0 mg/dL (varies by gender)
- **Lymphocyte %**: 25-40%
- **MCV**: 80-90 fL
- **RDW**: <13%
- **Alkaline Phosphatase**: 40-100 U/L
- **WBC**: 4.0-7.0 10³/µL

### Future Enhancements

1. **Additional Algorithms**: Implement GrimAge, DunedinPACE
2. **Machine Learning**: Train custom models on user data
3. **Wearable Integration**: Incorporate HRV, VO2 max, sleep stages
4. **Genetic Data**: Add polygenic risk scores
5. **Real-time Updates**: Stream processing for continuous monitoring
6. **Personalized Interventions**: ML-based intervention recommendations
7. **Cohort Comparisons**: Compare user to similar demographic cohorts

### References

- Levine ME, et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. Aging. [DOI: 10.18632/aging.101414](https://doi.org/10.18632/aging.101414)
- Liu Z, et al. (2018). A new aging measure captures morbidity and mortality risk. PLOS Medicine. [DOI: 10.1371/journal.pmed.1002718](https://doi.org/10.1371/journal.pmed.1002718)
- NHANES (National Health and Nutrition Examination Survey) dataset
- [PhenoAge Calculator Implementation](https://omux.dev/blog/calculating-phenotypic-age-with-python)
