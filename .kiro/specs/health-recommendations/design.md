# Design Document: Health Recommendations Engine

## Overview

The Health Recommendations Engine analyzes a user's digital twin data to generate personalized blood test recommendations. The system uses a rule-based approach combined with clinical guidelines to identify gaps in testing, monitor existing conditions, and suggest preventive screening based on demographics and risk factors.

The engine processes biomarker history, medical conditions, lifestyle factors, and demographic information to produce prioritized, actionable recommendations with clear rationale and timing guidance.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   API Layer     │
│  (FastAPI)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Recommendation Engine Service  │
│  ┌──────────────────────────┐  │
│  │  Digital Twin Analyzer   │  │
│  └──────────┬───────────────┘  │
│             │                   │
│  ┌──────────▼───────────────┐  │
│  │  Recommendation Builder  │  │
│  │  ┌────────────────────┐  │  │
│  │  │ Rule Evaluators    │  │  │
│  │  │ - Biomarker Rules  │  │  │
│  │  │ - Condition Rules  │  │  │
│  │  │ - Demographic Rules│  │  │
│  │  │ - Temporal Rules   │  │  │
│  │  └────────────────────┘  │  │
│  └──────────┬───────────────┘  │
│             │                   │
│  ┌──────────▼───────────────┐  │
│  │  Priority Scorer         │  │
│  └──────────┬───────────────┘  │
│             │                   │
│  ┌──────────▼───────────────┐  │
│  │  Output Formatter        │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  JSON Response  │
└─────────────────┘
```

### Component Flow

1. **API Layer**: Receives user_id and optional parameters
2. **Digital Twin Analyzer**: Aggregates all user data from multiple sources
3. **Recommendation Builder**: Applies rule evaluators to generate candidate recommendations
4. **Priority Scorer**: Assigns priority levels based on risk factors
5. **Output Formatter**: Structures recommendations into API response format

## Components and Interfaces

### 1. Digital Twin Analyzer

**Purpose**: Aggregate and structure all user health data for analysis

**Input**:
- `user_id`: String identifier for the user
- Data sources: biomarkers, medical_history, lifestyle, user_profile

**Output**: `DigitalTwin` object containing:
```python
{
  "user_id": str,
  "demographics": {
    "age": int,
    "sex": str,
    "location": dict
  },
  "latest_biomarkers": {
    "test_date": datetime,
    "categories": {
      "metabolic": dict,
      "lipid_profile": dict,
      "vitamins": dict,
      "hormones": dict,
      "kidney_function": dict,
      "liver_function": dict,
      "complete_blood_count": dict,
      "minerals": dict,
      "tumor_markers": dict
    }
  },
  "biomarker_history": list[dict],
  "conditions": list[dict],
  "medications": list[dict],
  "supplements": list[dict],
  "family_history": list[dict],
  "lifestyle": {
    "diet_type": str,
    "exercise_frequency": str,
    "smoking": dict,
    "alcohol": dict,
    "sleep_quality": float,
    "stress_level": int
  },
  "goals": list[dict]
}
```

**Key Methods**:
- `load_user_data(user_id: str) -> DigitalTwin`: Loads all data sources
- `get_latest_biomarkers() -> dict`: Returns most recent test results
- `get_biomarker_history(marker: str, months: int) -> list`: Returns historical values
- `get_active_conditions() -> list`: Returns current medical conditions
- `calculate_time_since_test(marker: str) -> timedelta`: Time since last test

### 2. Recommendation Builder

**Purpose**: Generate candidate recommendations using rule evaluators

**Input**: `DigitalTwin` object

**Output**: List of `Recommendation` objects

**Rule Evaluators**:

#### A. Biomarker Rules
Evaluates current biomarker values and generates recommendations:

- **Out-of-Range Follow-up**: When biomarker is outside normal range
  - High priority if significantly abnormal
  - Recommend retest in 1-3 months depending on severity
  
- **Missing Baseline**: When no data exists for important biomarkers
  - Medium priority for comprehensive panels
  - Recommend baseline testing
  
- **Trend Monitoring**: When biomarker shows concerning trend
  - Analyze last 2-3 tests for patterns
  - Recommend monitoring if trending toward abnormal

#### B. Condition Rules
Evaluates medical conditions and generates monitoring recommendations:

- **Active Condition Monitoring**: For each active condition
  - Map condition to required monitoring tests
  - Set frequency based on condition severity
  - Examples:
    - Dyslipidemia → Lipid panel every 3-6 months
    - Vitamin D deficiency → Vitamin D test every 3 months
    - Diabetes → HbA1c every 3 months, fasting glucose monthly

#### C. Demographic Rules
Evaluates age and sex for preventive screening:

- **Age-Based Screening**: Clinical guidelines by age group
  - Women 21-65: Annual Pap smear, mammogram 40+
  - Men 50+: PSA, colonoscopy
  - All adults 40+: Annual lipid panel, diabetes screening
  
- **Sex-Specific Tests**: Hormone panels, reproductive health
  - Women: FSH, LH, estrogen, progesterone
  - Men: Testosterone, PSA
  
- **Family History Risk**: Enhanced screening based on family conditions
  - Diabetes family history → Earlier/more frequent glucose monitoring
  - Cardiovascular family history → Enhanced lipid monitoring

#### D. Temporal Rules
Evaluates timing of last tests:

- **Routine Monitoring Intervals**: Standard retest intervals
  - Annual: Complete metabolic panel, CBC, lipid panel
  - Quarterly: Condition-specific monitoring
  - Monthly: Active management of unstable conditions
  
- **Post-Intervention Testing**: After starting treatment
  - 6-8 weeks after starting supplements
  - 3 months after lifestyle interventions
  - 1 month after medication changes

**Key Methods**:
- `evaluate_biomarker_rules(twin: DigitalTwin) -> list[Recommendation]`
- `evaluate_condition_rules(twin: DigitalTwin) -> list[Recommendation]`
- `evaluate_demographic_rules(twin: DigitalTwin) -> list[Recommendation]`
- `evaluate_temporal_rules(twin: DigitalTwin) -> list[Recommendation]`
- `build_recommendations(twin: DigitalTwin) -> list[Recommendation]`

### 3. Priority Scorer

**Purpose**: Assign priority levels to recommendations based on risk assessment

**Input**: List of `Recommendation` objects

**Output**: List of `Recommendation` objects with priority scores

**Priority Levels**:
- **High**: Critical abnormalities, significant health risks, overdue monitoring
- **Medium**: Moderate abnormalities, preventive screening, baseline establishment
- **Low**: Optimization, routine monitoring, general wellness

**Scoring Factors**:
1. **Severity of Abnormality**: How far from normal range
2. **Clinical Significance**: Impact on health outcomes
3. **Time Sensitivity**: How overdue the test is
4. **Risk Factors**: Presence of multiple risk factors
5. **Condition Severity**: Active conditions requiring monitoring

**Scoring Algorithm**:
```
priority_score = (
  abnormality_severity * 0.3 +
  clinical_significance * 0.25 +
  time_sensitivity * 0.2 +
  risk_factor_count * 0.15 +
  condition_severity * 0.1
)

if priority_score >= 0.7: priority = "high"
elif priority_score >= 0.4: priority = "medium"
else: priority = "low"
```

**Key Methods**:
- `calculate_priority_score(rec: Recommendation, twin: DigitalTwin) -> float`
- `assign_priorities(recommendations: list[Recommendation]) -> list[Recommendation]`

### 4. Output Formatter

**Purpose**: Structure recommendations into API response format

**Input**: Prioritized list of `Recommendation` objects

**Output**: Structured JSON response

**Formatting Operations**:
- Group recommendations by category (metabolic, cardiovascular, etc.)
- Sort by priority within each category
- Add educational context
- Format timing as human-readable strings
- Include summary statistics

**Key Methods**:
- `format_recommendations(recommendations: list[Recommendation]) -> dict`
- `group_by_category(recommendations: list[Recommendation]) -> dict`
- `add_educational_context(recommendation: Recommendation) -> Recommendation`

## Data Models

### DigitalTwin
```python
class DigitalTwin(BaseModel):
    user_id: str
    demographics: Demographics
    latest_biomarkers: BiomarkerSnapshot
    biomarker_history: list[BiomarkerSnapshot]
    conditions: list[MedicalCondition]
    medications: list[Medication]
    supplements: list[Supplement]
    family_history: list[FamilyCondition]
    lifestyle: LifestyleFactors
    goals: list[HealthGoal]
```

### Recommendation
```python
class Recommendation(BaseModel):
    recommendation_id: str  # UUID
    test_name: str
    test_category: str  # metabolic, lipid, vitamin, hormone, etc.
    rationale: str
    priority: str  # high, medium, low
    priority_score: float
    suggested_timing: str  # "within 1 week", "within 1 month", etc.
    related_biomarkers: list[str]
    related_conditions: list[str]
    educational_context: str
    clinical_guideline_reference: Optional[str]
```

### BiomarkerSnapshot
```python
class BiomarkerSnapshot(BaseModel):
    test_date: datetime
    lab_name: str
    test_package: str
    categories: dict[str, dict[str, BiomarkerValue]]
```

### BiomarkerValue
```python
class BiomarkerValue(BaseModel):
    value: float
    unit: str
    ref_range: str
    status: str  # normal, low, high
```

### RecommendationResponse
```python
class RecommendationResponse(BaseModel):
    user_id: str
    generated_at: datetime
    summary: RecommendationSummary
    recommendations: list[Recommendation]
    grouped_by_category: dict[str, list[Recommendation]]
```

### RecommendationSummary
```python
class RecommendationSummary(BaseModel):
    total_recommendations: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    categories_covered: list[str]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Complete Digital Twin Analysis
*For any* user with available data, the Digital Twin Analyzer should successfully load and structure all data sources without data loss.

**Validates: Requirements 1.1, 1.2, 1.3, 1.4**

### Property 2: Non-Empty Recommendations for Incomplete Data
*For any* user with missing biomarker data, the Recommendation Engine should generate at least one recommendation for baseline testing.

**Validates: Requirements 1.5**

### Property 3: Rationale Presence
*For any* generated recommendation, the recommendation object should contain a non-empty rationale field explaining why the test is suggested.

**Validates: Requirements 2.2**

### Property 4: Priority Assignment
*For any* generated recommendation, the recommendation should have a valid priority level (high, medium, or low) assigned.

**Validates: Requirements 2.3**

### Property 5: Timing Specification
*For any* generated recommendation, the recommendation should include a suggested timing for when the test should be performed.

**Validates: Requirements 2.4**

### Property 6: Follow-up for Abnormal Values
*For any* biomarker with status "high" or "low", the Recommendation Engine should generate a follow-up recommendation for that biomarker.

**Validates: Requirements 2.5**

### Property 7: Priority Ordering Consistency
*For any* set of recommendations with different priority scores, recommendations with higher priority scores should be assigned higher or equal priority levels compared to those with lower scores.

**Validates: Requirements 3.1**

### Property 8: High Priority for High Risk
*For any* biomarker that is significantly outside normal range (>50% deviation) or indicates high health risk, the related recommendation should be assigned high priority.

**Validates: Requirements 3.2**

### Property 9: Chronic Condition Monitoring Priority
*For any* user with active chronic conditions, the Recommendation Engine should generate high or medium priority recommendations for condition-specific monitoring tests.

**Validates: Requirements 3.3**

### Property 10: Temporal Recency Consideration
*For any* biomarker tested within the last 30 days, the Recommendation Engine should not recommend retesting unless the value was abnormal.

**Validates: Requirements 4.1, 4.2**

### Property 11: Abnormal Follow-up Timing
*For any* biomarker with abnormal results, the recommended follow-up timing should be shorter (more urgent) than the standard monitoring interval for that biomarker.

**Validates: Requirements 4.4**

### Property 12: Baseline Testing for New Users
*For any* user with no biomarker history, the Recommendation Engine should recommend a comprehensive baseline panel.

**Validates: Requirements 4.5**

### Property 13: Structured Output Format
*For any* recommendation response, the output should contain all required fields: user_id, generated_at, summary, recommendations, and grouped_by_category.

**Validates: Requirements 5.1, 5.4**

### Property 14: Logical Grouping
*For any* set of recommendations, recommendations in the same category group should all have the same test_category value.

**Validates: Requirements 5.2**

### Property 15: Educational Context Presence
*For any* recommendation, the educational_context field should contain information explaining the clinical significance of the test.

**Validates: Requirements 5.3**

### Property 16: Empty Response for No Recommendations
*For any* user with complete recent testing and no abnormalities, if no recommendations are needed, the response should contain an empty recommendations list with an appropriate summary message.

**Validates: Requirements 5.5**

### Property 17: Graceful Handling of Missing Data
*For any* user with partially missing data fields, the Recommendation Engine should generate recommendations based on available data without raising errors.

**Validates: Requirements 6.1**

### Property 18: Input Validation
*For any* invalid user_id or malformed input data, the system should return a structured error response rather than crashing.

**Validates: Requirements 6.2, 6.4**

### Property 19: Comprehensive Baseline for Empty Twin
*For any* user with no existing digital twin data, the Recommendation Engine should recommend a comprehensive baseline panel covering all major biomarker categories.

**Validates: Requirements 6.3**

### Property 20: Evidence-Based Test Selection
*For any* demographic group (age/sex combination), the recommended preventive screening tests should align with established clinical guidelines for that demographic.

**Validates: Requirements 7.1, 7.3**

### Property 21: Condition-Specific Monitoring
*For any* active medical condition, the recommended monitoring tests should be appropriate for that specific condition based on clinical protocols.

**Validates: Requirements 7.2**

### Property 22: Longevity Biomarker Inclusion
*For any* user with longevity optimization goals, the recommendations should include biomarkers relevant to healthspan and lifespan (e.g., inflammatory markers, metabolic health, hormonal balance).

**Validates: Requirements 7.5**

## Error Handling

### Input Validation Errors
- **Invalid user_id**: Return 404 with message "User not found"
- **Malformed data**: Return 400 with specific validation error details
- **Missing required fields**: Return 400 with list of missing fields

### Data Processing Errors
- **Data source unavailable**: Log warning, proceed with available data
- **Parsing errors**: Log error, skip malformed records, continue processing
- **Calculation errors**: Log error, exclude affected recommendation, continue

### Business Logic Errors
- **No data available**: Return success with baseline recommendations
- **Conflicting rules**: Apply priority-based rule resolution
- **Invalid biomarker values**: Flag for review, exclude from calculations

### System Errors
- **Database connection failure**: Return 503 with retry guidance
- **Timeout**: Return 504 with partial results if available
- **Unexpected exceptions**: Log full stack trace, return 500 with generic message

## Testing Strategy

### Unit Tests
- Test each rule evaluator independently with mock digital twin data
- Test priority scoring algorithm with various input combinations
- Test output formatting with different recommendation sets
- Test edge cases: empty data, single biomarker, all normal values
- Test error handling: invalid inputs, missing data, malformed values

### Property-Based Tests
- Generate random digital twin data and verify all properties hold
- Test with various combinations of biomarker statuses
- Test with different demographic profiles
- Test with varying data completeness levels
- Minimum 100 iterations per property test
- Each test tagged with: **Feature: health-recommendations, Property {N}: {property_text}**

### Integration Tests
- Test full recommendation flow from API request to response
- Test with real sample data from test users
- Test data loading from all sources
- Test recommendation generation for various user profiles
- Verify response format matches API specification

### Test Data Strategy
- Use existing test user data (test_user_1_29f, etc.)
- Create synthetic edge case scenarios
- Generate property test data with Hypothesis
- Mock external dependencies (database, file system)

### Property Test Implementation
- Use Hypothesis library for property-based testing
- Create custom strategies for generating valid digital twin data
- Implement generators for biomarker values, conditions, demographics
- Configure tests to run 100+ iterations
- Tag each test with corresponding design property number
