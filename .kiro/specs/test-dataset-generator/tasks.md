# Implementation Plan: Test Dataset Generator

## Overview

This plan implements a test dataset generator that creates clean, structured health data for AI/ML experimentation. It combines 3 real users from existing OCR data with 10+ synthetically generated users, producing normalized biomarker data in multiple formats (JSON, CSV, pandas DataFrame).

## Tasks

- [ ] 1. Set up project structure and data models
  - Create directory `app/services/dataset_generator/`
  - Define Pydantic models for Demographics, BiomarkerReading, UserProfile, ReferenceRange
  - Define enums for HealthProfileType, ValidationStatus
  - Create constants file with canonical test names and standard units
  - _Requirements: 1.1, 2.1, 2.3, 3.1_

- [ ]* 1.1 Write property test for data model validation
  - **Property 30: Normalized Data Completeness**
  - **Validates: Requirements 8.3**

- [ ] 2. Implement Ground Truth Parser
  - [ ] 2.1 Create GroundTruthParser class with parse_file method
    - Read and parse ground_truth_dataset.json
    - Extract user records from JSON structure
    - _Requirements: 1.1_

  - [ ]* 2.2 Write property test for complete user extraction
    - **Property 1: Complete User Extraction**
    - **Validates: Requirements 1.1**

  - [ ] 2.3 Implement extract_demographics method
    - Parse user identifier format "{age}{gender} {name}"
    - Extract age, gender, name
    - Handle edge cases (missing parts, invalid format)
    - _Requirements: 1.2, 3.1_

  - [ ]* 2.4 Write property test for demographic parsing
    - **Property 2: Demographic Parsing Accuracy**
    - **Validates: Requirements 1.2, 3.1**

  - [ ] 2.5 Implement extract_biomarkers method
    - Extract biomarker arrays from report data
    - Parse filename, text_length, biomarker list
    - _Requirements: 1.3_

  - [ ]* 2.6 Write property test for report field completeness
    - **Property 3: Report Field Completeness**
    - **Validates: Requirements 1.3**

  - [ ] 2.7 Add error handling for malformed input
    - Validate JSON structure
    - Return descriptive error messages
    - _Requirements: 1.4_

  - [ ]* 2.8 Write property test for error handling
    - **Property 4: Malformed Input Error Handling**
    - **Validates: Requirements 1.4**

- [ ] 3. Checkpoint - Ensure parser tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement Biomarker Normalizer
  - [ ] 4.1 Create BiomarkerNormalizer class
    - Implement normalize_test_name with canonical name mapping
    - _Requirements: 2.1_

  - [ ]* 4.2 Write property test for test name canonicalization
    - **Property 5: Test Name Canonicalization**
    - **Validates: Requirements 2.1**

  - [ ] 4.3 Implement normalize_unit method
    - Map units to standard medical units
    - Handle unit conversions if needed (mmol/L to mg/dL)
    - _Requirements: 2.3_

  - [ ]* 4.4 Write property test for unit standardization
    - **Property 7: Unit Standardization**
    - **Validates: Requirements 2.3**

  - [ ] 4.5 Implement parse_reference_range method
    - Parse formats: "< 100", "70-100", "> 5", "5-10"
    - Extract min/max values
    - _Requirements: 2.4_

  - [ ]* 4.6 Write property test for reference range parsing
    - **Property 8: Reference Range Parsing**
    - **Validates: Requirements 2.4**

  - [ ] 4.7 Implement validate_value method
    - Check if value is numeric
    - Validate against plausible ranges for test type
    - Set validation_status (normal, elevated, low, invalid)
    - _Requirements: 2.2, 2.5, 5.2_

  - [ ]* 4.8 Write property test for biomarker value validation
    - **Property 6: Biomarker Value Validation**
    - **Validates: Requirements 2.2, 5.2, 7.3**

  - [ ]* 4.9 Write property test for invalid data flagging
    - **Property 9: Invalid Data Flagging**
    - **Validates: Requirements 2.5**

- [ ] 5. Implement Synthetic User Generator
  - [ ] 5.1 Create SyntheticUserGenerator class
    - Initialize with seed for reproducibility
    - Define health profile types (healthy, pre-diabetic, high-cholesterol, etc.)
    - _Requirements: 7.1, 7.5_

  - [ ] 5.2 Implement generate_demographics method
    - Generate random age (18-80)
    - Generate random gender (M/F with realistic distribution)
    - Generate random Indian names from predefined lists
    - _Requirements: 7.2_

  - [ ]* 5.3 Write property test for demographic constraints
    - **Property 22: Demographic Constraints**
    - **Validates: Requirements 7.2**

  - [ ] 5.4 Implement generate_health_profile method
    - Assign health profile type to user
    - Define biomarker target ranges for each profile type
    - _Requirements: 7.5_

  - [ ] 5.5 Implement generate_biomarker_value method
    - Generate values within target ranges for profile type
    - Apply realistic correlations (high triglycerides → low HDL)
    - Add random variation within ranges
    - _Requirements: 7.3, 7.4_

  - [ ]* 5.6 Write property test for biomarker correlation maintenance
    - **Property 23: Biomarker Correlation Maintenance**
    - **Validates: Requirements 7.4**

  - [ ] 5.7 Implement generate_users method
    - Generate specified number of users (minimum 10)
    - Ensure diverse health profiles
    - Generate report dates within last 12 months
    - Include common biomarker panel for all users
    - _Requirements: 7.1, 7.6, 7.7_

  - [ ]* 5.8 Write property test for minimum user count
    - **Property 21: Minimum Synthetic User Count**
    - **Validates: Requirements 7.1**

  - [ ]* 5.9 Write property test for health profile diversity
    - **Property 24: Health Profile Diversity**
    - **Validates: Requirements 7.5**

  - [ ]* 5.10 Write property test for common biomarker coverage
    - **Property 25: Common Biomarker Coverage**
    - **Validates: Requirements 7.6**

  - [ ]* 5.11 Write property test for report date constraints
    - **Property 26: Report Date Constraints**
    - **Validates: Requirements 7.7**

- [ ] 6. Checkpoint - Ensure generator tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement User Profile Builder
  - [ ] 7.1 Create UserProfileBuilder class
    - Implement generate_user_id method (USER_001, USER_SYNTH_001)
    - _Requirements: 3.5_

  - [ ]* 7.2 Write property test for user ID uniqueness
    - **Property 13: User ID Uniqueness**
    - **Validates: Requirements 3.5**

  - [ ] 7.3 Implement aggregate_biomarkers method
    - Group biomarkers by test name across multiple reports
    - Preserve all instances with timestamps
    - _Requirements: 3.2, 3.4_

  - [ ]* 7.4 Write property test for multi-report aggregation
    - **Property 10: Multi-Report Aggregation**
    - **Validates: Requirements 3.2**

  - [ ]* 7.5 Write property test for duplicate biomarker preservation
    - **Property 12: Duplicate Biomarker Preservation**
    - **Validates: Requirements 3.4**

  - [ ] 7.6 Implement build_profile method
    - Create UserProfile from raw data or synthetic user
    - Include metadata (source, report_count, biomarker_count)
    - Preserve source metadata (report_date, filename)
    - Mark synthetic users with is_synthetic=true
    - _Requirements: 3.1, 3.3, 7.8_

  - [ ]* 7.7 Write property test for metadata preservation
    - **Property 11: Metadata Preservation**
    - **Validates: Requirements 3.3**

  - [ ]* 7.8 Write property test for synthetic user marking
    - **Property 27: Synthetic User Marking**
    - **Validates: Requirements 7.8**

- [ ] 8. Implement Data Quality Validator
  - [ ] 8.1 Create DataQualityValidator class
    - Implement check_completeness method
    - Calculate biomarker coverage percentage
    - _Requirements: 5.1_

  - [ ]* 8.2 Write property test for completeness metric accuracy
    - **Property 15: Completeness Metric Accuracy**
    - **Validates: Requirements 5.1**

  - [ ] 8.3 Implement detect_outliers method
    - Identify values outside reference ranges
    - Categorize severity (mild, moderate, severe)
    - _Requirements: 5.2_

  - [ ] 8.4 Implement detect_duplicates method
    - Find duplicate users by demographics
    - Find duplicate biomarker readings
    - _Requirements: 5.3_

  - [ ]* 8.5 Write property test for duplicate detection
    - **Property 16: Duplicate Detection**
    - **Validates: Requirements 5.3**

  - [ ] 8.6 Implement validate_dataset method
    - Generate DataQualityReport
    - Include completeness metrics, outlier summary, warnings
    - Warn for users with insufficient data (< 10 biomarkers)
    - _Requirements: 5.4, 5.5_

  - [ ]* 8.7 Write property test for insufficient data warnings
    - **Property 17: Insufficient Data Warnings**
    - **Validates: Requirements 5.5**

- [ ] 9. Implement Dataset Merger (for incremental updates)
  - [ ] 9.1 Create DatasetMerger class
    - Implement merge_datasets method
    - Combine user lists from both datasets
    - _Requirements: 6.1_

  - [ ]* 9.2 Write property test for merge completeness
    - **Property 18: Dataset Merge Completeness**
    - **Validates: Requirements 6.1**

  - [ ] 9.3 Implement duplicate detection and resolution
    - Detect duplicate users and reports
    - Preserve most recent data when conflicts occur
    - _Requirements: 6.2, 6.3, 6.4_

  - [ ]* 9.4 Write property test for merge duplicate handling
    - **Property 19: Merge Duplicate Handling**
    - **Validates: Requirements 6.2, 6.3, 6.4**

  - [ ] 9.5 Implement changelog maintenance
    - Log all merge operations with timestamp
    - Record operation details (users added, conflicts resolved)
    - _Requirements: 6.5_

  - [ ]* 9.6 Write property test for changelog maintenance
    - **Property 20: Changelog Maintenance**
    - **Validates: Requirements 6.5**

- [ ] 10. Checkpoint - Ensure validator and merger tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement Dataset Exporter
  - [ ] 11.1 Create DatasetExporter class
    - Implement export_json method
    - Structure output with metadata and user profiles
    - _Requirements: 4.1, 4.4_

  - [ ]* 11.2 Write property test for export metadata completeness
    - **Property 14: Export Metadata Completeness**
    - **Validates: Requirements 4.4**

  - [ ] 11.3 Implement export_csv method
    - Flatten biomarker data (one row per reading)
    - Include all user demographics and biomarker fields
    - _Requirements: 4.2_

  - [ ] 11.4 Implement export_pickle method
    - Convert to pandas DataFrame
    - Save as pickle file
    - _Requirements: 4.3_

  - [ ] 11.5 Implement export_schema method
    - Document JSON structure
    - Document CSV columns
    - Document DataFrame schema
    - _Requirements: 8.5_

  - [ ] 11.6 Implement export_quality_report method
    - Export DataQualityReport as JSON
    - Include summary statistics
    - _Requirements: 4.5, 5.4_

  - [ ] 11.7 Add output file type constraints
    - Ensure only structured data files created (no PDFs)
    - Exclude raw_text fields from output
    - _Requirements: 8.1, 8.2_

  - [ ]* 11.8 Write property test for output file type constraints
    - **Property 28: Output File Type Constraints**
    - **Validates: Requirements 8.1**

  - [ ]* 11.9 Write property test for raw text exclusion
    - **Property 29: Raw Text Exclusion**
    - **Validates: Requirements 8.2**

- [ ] 12. Create main orchestration script
  - [ ] 12.1 Create generate_test_dataset.py script
    - Parse command-line arguments (input file, output dir, user count)
    - Orchestrate all components in sequence
    - Handle errors gracefully
    - _Requirements: All_

  - [ ] 12.2 Add logging and progress reporting
    - Log each processing stage
    - Report progress for synthetic user generation
    - Display summary statistics at end

  - [ ] 12.3 Create output directory structure
    - Create tests/test_data/ml_dataset/
    - Generate all output files
    - Create README.md with dataset documentation

- [ ] 13. Integration testing and validation
  - [ ] 13.1 Test with real ground_truth_dataset.json
    - Verify 3 real users parsed correctly
    - Verify all biomarkers extracted and normalized

  - [ ] 13.2 Test synthetic user generation
    - Generate 10 users with varied profiles
    - Verify biomarker correlations
    - Verify date constraints

  - [ ] 13.3 Test complete pipeline
    - Run end-to-end: parse → normalize → build → validate → export
    - Verify all output files created
    - Verify data quality report accuracy

  - [ ] 13.4 Validate output formats
    - Load and validate JSON structure
    - Load and validate CSV format
    - Load and validate pickle DataFrame

- [ ] 14. Final checkpoint - Complete testing
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation uses Python with Pydantic for data models
- Output directory: `tests/test_data/ml_dataset/`
- Minimum 10 synthetic users + 3 real users = 13+ total users
