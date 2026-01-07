# Requirements Document

## Introduction

This feature creates a structured test dataset with clean, parseable biomarker data for AI/ML experimentation. The system will generate synthetic test users with realistic health profiles and biomarker values, and also incorporate existing OCR-extracted data. The output is clean structured data (no PDFs, no OCR) suitable for training and testing machine learning models across different services.

## Glossary

- **Test_Dataset**: A structured collection of user health data with biomarkers, demographics, and metadata (minimum 10 users)
- **Biomarker**: A measurable health indicator (e.g., HbA1c, cholesterol) with value, unit, and reference range
- **Ground_Truth_Data**: The existing JSON file containing OCR-extracted data from 3 real users
- **Synthetic_User**: A generated test user with realistic demographics and biomarker values
- **User_Profile**: Demographic and health information for a test user (real or synthetic)
- **Normalized_Data**: Data transformed into a consistent format with standardized units and naming
- **ML_Service**: Any AI/ML service that consumes the test dataset (e.g., health insights, recommendations, predictions)
- **Clean_Data**: Structured, parseable data without PDF files or OCR processing

## Requirements

### Requirement 1: Parse Ground Truth Data

**User Story:** As a developer, I want to parse the existing ground truth dataset, so that I can extract user information and biomarker data.

#### Acceptance Criteria

1. WHEN the Ground_Truth_Data file is provided, THE System SHALL parse the JSON structure and extract all user records
2. WHEN parsing user records, THE System SHALL extract user demographics from the user identifier (age, gender, name)
3. WHEN parsing report data, THE System SHALL extract filename, text length, raw text, and biomarker arrays
4. IF the Ground_Truth_Data file is malformed, THEN THE System SHALL return a descriptive error message

### Requirement 2: Normalize Biomarker Data

**User Story:** As a data scientist, I want biomarker data normalized to standard formats, so that I can use consistent data across different ML models.

#### Acceptance Criteria

1. WHEN processing biomarkers, THE System SHALL standardize test names to canonical forms (e.g., "HbA1c", "Total Cholesterol")
2. WHEN biomarker values are present, THE System SHALL validate they are numeric and within plausible ranges
3. WHEN units are present, THE System SHALL normalize them to standard medical units (e.g., "mg/dL", "mmol/L")
4. WHEN reference ranges are present, THE System SHALL parse and structure them as min/max values
5. IF a biomarker has missing or invalid data, THEN THE System SHALL flag it with a validation status

### Requirement 3: Create User Profiles

**User Story:** As a developer, I want structured user profiles with demographics and health data, so that I can test personalized health features.

#### Acceptance Criteria

1. WHEN creating a User_Profile, THE System SHALL extract age, gender, and name from the user identifier
2. WHEN a user has multiple reports, THE System SHALL aggregate all biomarkers across reports
3. WHEN aggregating biomarkers, THE System SHALL include report date and filename as metadata
4. WHEN biomarkers appear in multiple reports, THE System SHALL preserve all instances with timestamps
5. THE System SHALL generate a unique user ID for each User_Profile

### Requirement 4: Export Test Dataset

**User Story:** As a developer, I want to export the test dataset in multiple formats, so that I can use it across different services and tools.

#### Acceptance Criteria

1. THE System SHALL export the Test_Dataset in JSON format with structured user profiles
2. THE System SHALL export the Test_Dataset in CSV format with flattened biomarker data
3. WHERE Python ML services are used, THE System SHALL export the Test_Dataset as a pandas DataFrame pickle file
4. WHEN exporting, THE System SHALL include metadata (export date, version, source file)
5. THE System SHALL create a summary statistics file showing biomarker coverage per user

### Requirement 5: Validate Data Quality

**User Story:** As a data scientist, I want data quality metrics, so that I can assess the reliability of the test dataset.

#### Acceptance Criteria

1. WHEN processing the dataset, THE System SHALL calculate completeness metrics (% of biomarkers with values)
2. WHEN processing biomarkers, THE System SHALL identify outliers based on reference ranges
3. WHEN processing biomarkers, THE System SHALL flag duplicate or conflicting values
4. THE System SHALL generate a data quality report with validation results
5. THE System SHALL provide warnings for users with insufficient data for ML training

### Requirement 6: Support Incremental Updates

**User Story:** As a developer, I want to add new users or reports to the dataset, so that I can expand the test data over time.

#### Acceptance Criteria

1. WHEN new Ground_Truth_Data is provided, THE System SHALL merge it with existing Test_Dataset
2. WHEN merging data, THE System SHALL detect and handle duplicate users
3. WHEN merging data, THE System SHALL detect and handle duplicate reports
4. WHEN conflicts occur, THE System SHALL preserve the most recent data
5. THE System SHALL maintain a changelog of dataset updates

### Requirement 7: Generate Synthetic Test Users

**User Story:** As a developer, I want to generate synthetic test users with realistic health profiles, so that I can have at least 10 users for ML experimentation.

#### Acceptance Criteria

1. THE System SHALL generate at least 10 synthetic test users with unique profiles
2. WHEN generating users, THE System SHALL create realistic demographics (age 18-80, gender distribution, names)
3. WHEN generating biomarkers, THE System SHALL produce values within medically plausible ranges
4. WHEN generating biomarkers, THE System SHALL maintain realistic correlations (e.g., high triglycerides with low HDL)
5. THE System SHALL generate varied health profiles (healthy, pre-diabetic, high cholesterol, etc.)
6. THE System SHALL include common biomarkers (HbA1c, glucose, lipid panel, thyroid, vitamins, CBC)
7. THE System SHALL generate report dates spanning the last 12 months
8. THE System SHALL clearly mark synthetic users to distinguish them from real data

### Requirement 8: Output Clean Structured Data

**User Story:** As a developer, I want clean, parseable data without PDFs or OCR, so that I can directly use it in ML services.

#### Acceptance Criteria

1. THE System SHALL output only structured data files (JSON, CSV, pickle) with no PDF files
2. THE System SHALL NOT include raw OCR text in the output dataset
3. WHEN exporting data, THE System SHALL include only normalized biomarker values, units, and reference ranges
4. THE System SHALL structure data for easy parsing and querying
5. THE System SHALL provide clear schema documentation for all output formats
