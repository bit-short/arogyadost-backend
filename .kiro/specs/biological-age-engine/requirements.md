# Requirements Document: Biological Age Prediction Reasoning Engine

## Introduction

The Biological Age Prediction Reasoning Engine is a core analytical component that processes digital twin data from test users to estimate biological age. This MVP focuses on the 6 test users with existing biomarker, lifestyle, and medical history data. Unlike chronological age, biological age reflects the true physiological state of the body and serves as a key longevity metric. The engine uses evidence-based algorithms to analyze health biomarkers and provide actionable insights for age optimization.

## Glossary

- **Biological_Age_Engine**: The reasoning system that calculates biological age from digital twin data
- **Digital_Twin**: Comprehensive health data representation including biomarkers, lifestyle, medical history, interventions, and wearables
- **Chronological_Age**: The user's actual age in years
- **Biological_Age**: Estimated physiological age based on health biomarkers and lifestyle factors
- **Age_Delta**: The difference between biological age and chronological age (negative = younger, positive = older)
- **Biomarker**: Measurable health indicator (e.g., HbA1c, cholesterol, vitamin D)
- **Aging_Factor**: A specific biomarker or lifestyle metric that contributes to biological age calculation
- **Confidence_Score**: A measure (0-100) indicating the reliability of the biological age prediction
- **Age_Contributor**: Individual factor with its specific impact on biological age
- **Intervention**: Health action taken by the user (supplements, exercise, diet changes)
- **Prediction_Model**: The algorithm used to calculate biological age from input features

## Requirements

### Requirement 1: Test User Data Loading

**User Story:** As a system, I want to load test user data from JSON files, so that I can perform biological age calculations.

#### Acceptance Criteria

1. WHEN test user data is requested, THE Biological_Age_Engine SHALL load user profiles from datasets/users/users.json
2. WHEN biomarker data is requested, THE Biological_Age_Engine SHALL load from datasets/biomarkers/ directory
3. WHEN lifestyle data is requested, THE Biological_Age_Engine SHALL load from datasets/lifestyle/ directory
4. WHEN medical history data is requested, THE Biological_Age_Engine SHALL load from datasets/medical_history/ directory
5. IF a data file is missing or malformed, THEN THE Biological_Age_Engine SHALL return a descriptive error
6. THE Biological_Age_Engine SHALL support all 6 test users (test_user_1_29f through test_user_6_65m)

### Requirement 2: Biomarker-Based Age Calculation

**User Story:** As a user, I want my biological age calculated from biomarkers, so that I can understand my physiological health status.

#### Acceptance Criteria

1. WHEN metabolic biomarkers are provided, THE Biological_Age_Engine SHALL calculate metabolic age contribution
2. WHEN lipid profile data is provided, THE Biological_Age_Engine SHALL calculate cardiovascular age contribution
3. WHEN inflammatory markers are provided, THE Biological_Age_Engine SHALL calculate inflammation age contribution
4. WHEN hormonal data is provided, THE Biological_Age_Engine SHALL calculate hormonal age contribution
5. WHEN kidney and liver function markers are provided, THE Biological_Age_Engine SHALL calculate organ function age contribution
6. THE Biological_Age_Engine SHALL weight each biomarker category according to evidence-based aging research
7. THE Biological_Age_Engine SHALL handle missing biomarkers by adjusting confidence scores

### Requirement 3: Lifestyle Factor Integration

**User Story:** As a user, I want my lifestyle factors considered in biological age, so that I get a holistic health assessment.

#### Acceptance Criteria

1. WHERE lifestyle data is available, WHEN sleep data is provided, THE Biological_Age_Engine SHALL calculate sleep quality impact on biological age
2. WHERE lifestyle data is available, WHEN physical activity data is provided, THE Biological_Age_Engine SHALL calculate exercise impact on biological age
3. WHERE lifestyle data is available, WHEN nutrition data is provided, THE Biological_Age_Engine SHALL calculate dietary impact on biological age
4. WHERE lifestyle data is available, WHEN stress metrics are provided, THE Biological_Age_Engine SHALL calculate stress impact on biological age
5. WHEN lifestyle data is unavailable, THE Biological_Age_Engine SHALL calculate biological age using biomarkers only and adjust confidence score

### Requirement 4: Biological Age Prediction Output

**User Story:** As a user, I want to receive my biological age prediction, so that I can track my health optimization progress.

#### Acceptance Criteria

1. THE Biological_Age_Engine SHALL return a biological age value as a decimal number
2. THE Biological_Age_Engine SHALL return an age delta comparing biological age to chronological age
3. THE Biological_Age_Engine SHALL return a confidence score indicating prediction reliability
4. THE Biological_Age_Engine SHALL return a breakdown of age contributors by category
5. WHEN confidence score is below 60, THE Biological_Age_Engine SHALL include warnings about data completeness
6. THE Biological_Age_Engine SHALL return results in a structured JSON format

### Requirement 5: Age Contributor Analysis

**User Story:** As a user, I want to understand which factors are aging me, so that I can prioritize interventions.

#### Acceptance Criteria

1. THE Biological_Age_Engine SHALL identify the top 5 factors increasing biological age
2. THE Biological_Age_Engine SHALL identify the top 5 factors decreasing biological age
3. WHEN a biomarker is out of optimal range, THE Biological_Age_Engine SHALL quantify its age impact in years
4. THE Biological_Age_Engine SHALL categorize contributors as critical, moderate, or minor based on impact magnitude
5. THE Biological_Age_Engine SHALL provide reference ranges for optimal aging for each contributor

### Requirement 6: Temporal Trend Analysis

**User Story:** As a user, I want to track biological age changes over time, so that I can measure intervention effectiveness.

#### Acceptance Criteria

1. WHERE multiple historical data points exist, WHEN historical biomarker data is available, THE Biological_Age_Engine SHALL calculate biological age for each time point
2. WHERE historical calculations exist, THE Biological_Age_Engine SHALL compute age velocity (rate of aging)
3. WHERE intervention data exists, WHEN interventions are recorded, THE Biological_Age_Engine SHALL correlate intervention timing with age changes
4. THE Biological_Age_Engine SHALL identify improving and declining biomarker trends
5. THE Biological_Age_Engine SHALL return a time series of biological age values with timestamps

### Requirement 7: Gender and Age-Specific Calculations

**User Story:** As a system, I want to use gender and age-specific models, so that predictions are accurate for diverse users.

#### Acceptance Criteria

1. WHEN user gender is female, THE Biological_Age_Engine SHALL apply female-specific biomarker reference ranges
2. WHEN user gender is male, THE Biological_Age_Engine SHALL apply male-specific biomarker reference ranges
3. WHEN user is under 30, THE Biological_Age_Engine SHALL apply young adult aging models
4. WHEN user is 30-50, THE Biological_Age_Engine SHALL apply middle-age aging models
5. WHEN user is over 50, THE Biological_Age_Engine SHALL apply senior aging models
6. THE Biological_Age_Engine SHALL adjust hormonal factor weights based on age and gender

### Requirement 8: Confidence Score Calculation

**User Story:** As a user, I want to know how reliable my biological age prediction is, so that I can trust the results.

#### Acceptance Criteria

1. WHEN all biomarker categories have data, THE Biological_Age_Engine SHALL set base confidence to 90
2. WHEN a biomarker category is missing, THE Biological_Age_Engine SHALL reduce confidence by 10 points per category
3. WHEN lifestyle data is missing, THE Biological_Age_Engine SHALL reduce confidence by 5 points
4. WHEN biomarker data is older than 6 months, THE Biological_Age_Engine SHALL reduce confidence by 10 points
5. WHEN biomarker data is older than 12 months, THE Biological_Age_Engine SHALL reduce confidence by 20 points
6. THE Biological_Age_Engine SHALL never return a confidence score below 20

### Requirement 9: Intervention Impact Prediction

**User Story:** As a user, I want to see predicted biological age improvements from interventions, so that I can make informed health decisions.

#### Acceptance Criteria

1. WHERE intervention data exists, WHEN a user has active interventions, THE Biological_Age_Engine SHALL estimate expected age reduction
2. WHEN an intervention targets a specific biomarker, THE Biological_Age_Engine SHALL calculate potential age impact
3. THE Biological_Age_Engine SHALL provide a projected biological age assuming intervention success
4. THE Biological_Age_Engine SHALL indicate the time horizon for expected improvements
5. WHEN multiple interventions are active, THE Biological_Age_Engine SHALL calculate combined effects

### Requirement 10: Error Handling and Validation

**User Story:** As a system, I want robust error handling, so that invalid data doesn't cause system failures.

#### Acceptance Criteria

1. WHEN biomarker values are outside physiologically possible ranges, THE Biological_Age_Engine SHALL reject the input
2. WHEN required user demographics are missing, THE Biological_Age_Engine SHALL return a validation error
3. WHEN data format is invalid, THE Biological_Age_Engine SHALL return a descriptive error message
4. IF calculation fails, THEN THE Biological_Age_Engine SHALL log the error and return a safe fallback response
5. THE Biological_Age_Engine SHALL validate that chronological age is between 18 and 120 years

### Requirement 11: Explainability and Transparency

**User Story:** As a user, I want to understand how my biological age was calculated, so that I can trust and act on the results.

#### Acceptance Criteria

1. THE Biological_Age_Engine SHALL provide a human-readable explanation of the calculation methodology
2. THE Biological_Age_Engine SHALL list all biomarkers used in the calculation with their individual contributions
3. THE Biological_Age_Engine SHALL indicate which research models or algorithms were applied
4. WHEN a biomarker has high impact, THE Biological_Age_Engine SHALL explain why it matters for aging
5. THE Biological_Age_Engine SHALL provide actionable recommendations for improving biological age

### Requirement 12: Performance and Scalability

**User Story:** As a system, I want fast biological age calculations, so that users receive real-time results.

#### Acceptance Criteria

1. WHEN a single user's data is processed, THE Biological_Age_Engine SHALL complete calculation within 2 seconds
2. WHEN processing all 6 test users, THE Biological_Age_Engine SHALL complete within 10 seconds
3. THE Biological_Age_Engine SHALL cache loaded JSON data to avoid repeated file reads
4. WHEN processing historical data, THE Biological_Age_Engine SHALL optimize for time-series calculations
5. THE Biological_Age_Engine SHALL handle missing data files gracefully without crashing

### Requirement 13: API Integration

**User Story:** As a developer, I want a clean API interface, so that I can integrate biological age predictions into the application.

#### Acceptance Criteria

1. THE Biological_Age_Engine SHALL expose a Python function interface for age prediction
2. THE Biological_Age_Engine SHALL accept user_id as input and load data from JSON files
3. THE Biological_Age_Engine SHALL return predictions as Python dictionaries with consistent schema
4. THE Biological_Age_Engine SHALL provide clear function signatures with type hints
5. THE Biological_Age_Engine SHALL raise appropriate exceptions for error scenarios

### Requirement 14: Model Versioning and Updates

**User Story:** As a system administrator, I want to version prediction models, so that I can track and improve accuracy over time.

#### Acceptance Criteria

1. THE Biological_Age_Engine SHALL tag each prediction with the model version used
2. THE Biological_Age_Engine SHALL log model version in prediction output
3. THE Biological_Age_Engine SHALL allow comparison of predictions across model versions
4. THE Biological_Age_Engine SHALL document the algorithm and weights used in each version
5. WHEN model updates occur, THE Biological_Age_Engine SHALL maintain backward compatibility
