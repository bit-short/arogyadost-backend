# Implementation Plan: Biological Age Prediction Reasoning Engine

## Overview

This implementation plan breaks down the biological age engine into discrete coding tasks. The approach follows a bottom-up strategy: build core utilities first, then calculators, then the main engine interface. Each task includes property-based tests to validate correctness properties from the design document.

## Tasks

- [ ] 1. Set up project structure and dependencies
  - Create `app/services/biological_age/` directory structure
  - Add Hypothesis to requirements.txt for property-based testing
  - Create `__init__.py` files for Python modules
  - Set up test directory structure under `tests/`
  - _Requirements: 13.1, 13.4_

- [ ] 2. Implement Data Loader module
  - [ ] 2.1 Create DataLoader class with file loading methods
    - Implement `load_user_profile()` to read from datasets/users/users.json
    - Implement `load_biomarkers()` to read from datasets/biomarkers/
    - Implement `load_lifestyle()` to read from datasets/lifestyle/ (optional)
    - Implement `load_medical_history()` to read from datasets/medical_history/ (optional)
    - Add caching to avoid repeated file reads
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 12.3_

  - [ ]* 2.2 Write property test for data loading completeness
    - **Property 1: Data Loading Completeness**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 12.5**

  - [ ]* 2.3 Write unit tests for DataLoader
    - Test loading each of the 6 test users
    - Test handling of missing files
    - Test caching behavior
    - _Requirements: 1.6, 12.5_

- [ ] 3. Implement Biomarker Normalizer module
  - [ ] 3.1 Create BiomarkerNormalizer class with unit conversion methods
    - Implement `normalize_albumin()` (g/dL → g/L)
    - Implement `normalize_creatinine()` (mg/dL → µmol/L)
    - Implement `normalize_glucose()` (mg/dL → mmol/L)
    - Implement `normalize_crp()` (mg/dL → mg/L)
    - Add validation for physiologically possible ranges
    - _Requirements: 1.1, 10.1_

  - [ ]* 3.2 Write property test for unit conversions
    - Test that conversions are reversible (within floating point precision)
    - Test that invalid values raise appropriate errors
    - _Requirements: 10.1_

  - [ ]* 3.3 Write unit tests for specific conversions
    - Test known conversion values
    - Test boundary cases
    - _Requirements: 1.1_

- [ ] 4. Implement PhenoAge Calculator module
  - [ ] 4.1 Create PhenoAgeCalculator class with algorithm implementation
    - Define PHENOAGE_COEFFICIENTS constant with values from design
    - Implement `calculate_xb()` for weighted biomarker sum
    - Implement `calculate_mortality_score()` for M calculation
    - Implement `calculate_phenoage()` for final age calculation
    - Implement `predict()` as main entry point
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [ ]* 4.2 Write property test for biomarker calculation validity
    - **Property 3: Biomarker Calculation Validity**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

  - [ ]* 4.3 Write unit tests for PhenoAge algorithm
    - Test with known biomarker values
    - Test that coefficients match published values
    - Test edge cases (all biomarkers at optimal, all at worst)
    - _Requirements: 2.6_

- [ ] 5. Checkpoint - Ensure core calculation tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement Age Contributor Analyzer module
  - [ ] 6.1 Create AgeContributorAnalyzer class
    - Define optimal ranges for each biomarker
    - Implement `calculate_biomarker_impact()` to quantify age impact
    - Implement `categorize_impact()` for severity classification
    - Implement `analyze_contributors()` to identify top 5 aging/de-aging factors
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 6.2 Write property test for contributor list structure
    - **Property 9: Contributor List Structure**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**

  - [ ]* 6.3 Write unit tests for contributor analysis
    - Test impact calculation for specific biomarkers
    - Test severity categorization
    - Test sorting by impact magnitude
    - _Requirements: 5.3, 5.4_

- [ ] 7. Implement Confidence Score Calculator module
  - [ ] 7.1 Create ConfidenceCalculator class
    - Implement base confidence calculation (90 for complete data)
    - Implement missing category penalty (-10 per category)
    - Implement missing lifestyle penalty (-5)
    - Implement data age penalties (-10 for >6mo, -20 for >12mo)
    - Implement minimum confidence floor (20)
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

  - [ ]* 7.2 Write property test for confidence score bounds
    - **Property 7: Confidence Score Bounds**
    - **Validates: Requirements 4.3, 8.6**

  - [ ]* 7.3 Write property test for confidence reduction
    - **Property 10: Confidence Reduction for Missing Data**
    - **Property 11: Confidence Reduction for Data Age**
    - **Validates: Requirements 2.7, 8.2, 8.3, 8.4, 8.5**

  - [ ]* 7.4 Write unit tests for confidence calculation
    - Test base confidence with complete data
    - Test each penalty type individually
    - Test minimum confidence floor
    - _Requirements: 8.1, 8.6_

- [ ] 8. Implement main BiologicalAgeEngine class
  - [ ] 8.1 Create BiologicalAgeEngine class with predict_age method
    - Initialize all component modules (DataLoader, Normalizer, Calculator, etc.)
    - Implement `predict_age()` to orchestrate the full prediction pipeline
    - Load user data → normalize biomarkers → calculate age → analyze contributors → calculate confidence
    - Format output as structured dictionary
    - Add model version tagging ("phenoage_v1.0")
    - Add timestamp to results
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.6, 13.1, 13.2, 13.3, 14.1_

  - [ ]* 8.2 Write property test for output structure completeness
    - **Property 5: Output Structure Completeness**
    - **Validates: Requirements 4.1, 4.4, 4.6, 13.3**

  - [ ]* 8.3 Write property test for age delta consistency
    - **Property 6: Age Delta Consistency**
    - **Validates: Requirements 4.2**

  - [ ]* 8.4 Write unit tests for main engine
    - Test prediction for test_user_1_29f
    - Test prediction for all 6 test users
    - Test output structure
    - _Requirements: 1.6, 4.1, 4.2_

- [ ] 9. Implement error handling and validation
  - [ ] 9.1 Add input validation to BiologicalAgeEngine
    - Validate chronological age is between 18 and 120
    - Validate required demographics are present
    - Validate biomarker values are within physiological ranges
    - Add descriptive error messages
    - _Requirements: 10.1, 10.2, 10.3, 10.5_

  - [ ] 9.2 Add error handling for calculation failures
    - Wrap calculations in try-except blocks
    - Log errors with context
    - Return fallback response (chronological age, confidence=20)
    - _Requirements: 10.4_

  - [ ]* 9.3 Write property test for error handling
    - **Property 2: Error Handling for Invalid Inputs**
    - **Validates: Requirements 1.5, 10.1, 10.2, 10.3, 10.4, 10.5**

  - [ ]* 9.4 Write unit tests for validation
    - Test each validation rule
    - Test error message content
    - Test fallback behavior
    - _Requirements: 10.1, 10.2, 10.5_

- [ ] 10. Checkpoint - Ensure all core functionality tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement warnings and explainability
  - [ ] 11.1 Add warning generation for low confidence
    - When confidence < 60, add warnings about missing data
    - Add warnings for old biomarker data
    - Add warnings for missing biomarker categories
    - _Requirements: 4.5_

  - [ ] 11.2 Add explainability fields to output
    - Add biomarkers_used list
    - Add model_version field
    - Add explanatory text for high-impact contributors
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ]* 11.3 Write property test for low confidence warnings
    - **Property 8: Low Confidence Warnings**
    - **Validates: Requirements 4.5**

  - [ ]* 11.4 Write property test for explainability completeness
    - **Property 16: Explainability Completeness**
    - **Validates: Requirements 11.1, 11.2, 11.3, 11.4**

  - [ ]* 11.5 Write unit tests for warnings
    - Test warning generation for various scenarios
    - Test explainability fields are present
    - _Requirements: 4.5, 11.2_

- [ ] 12. Implement batch processing
  - [ ] 12.1 Add predict_batch method to BiologicalAgeEngine
    - Implement `predict_batch()` to process multiple users
    - Reuse cached data across predictions
    - Return list of prediction results
    - _Requirements: 12.2_

  - [ ]* 12.2 Write property test for API interface consistency
    - **Property 18: API Interface Consistency**
    - **Validates: Requirements 13.2, 13.5**

  - [ ]* 12.3 Write unit test for batch processing
    - Test processing all 6 test users
    - Verify performance is within 10 seconds
    - _Requirements: 12.2_

- [ ] 13. Implement gender and age-specific models
  - [ ] 13.1 Add gender and age-specific reference ranges
    - Define male/female-specific optimal ranges
    - Define age-group-specific ranges (under 30, 30-50, over 50)
    - Update AgeContributorAnalyzer to use appropriate ranges
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [ ]* 13.2 Write property test for gender and age-specific models
    - **Property 14: Gender and Age-Specific Models**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**

  - [ ]* 13.3 Write unit tests for model selection
    - Test female user gets female ranges
    - Test male user gets male ranges
    - Test each age group gets appropriate model
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 14. Implement lifestyle factor integration (optional for MVP)
  - [ ] 14.1 Add lifestyle impact calculation
    - Implement sleep quality impact calculation
    - Implement physical activity impact calculation
    - Implement nutrition impact calculation
    - Implement stress impact calculation
    - Integrate lifestyle impacts into biological age calculation
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 14.2 Write property test for lifestyle factor integration
    - **Property 4: Lifestyle Factor Integration**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

  - [ ]* 14.3 Write unit tests for lifestyle impacts
    - Test each lifestyle factor individually
    - Test predictions with and without lifestyle data
    - _Requirements: 3.5_

- [ ] 15. Implement temporal trend analysis (optional for MVP)
  - [ ] 15.1 Add historical analysis methods
    - Implement time series calculation for multiple biomarker records
    - Implement age velocity calculation
    - Implement trend identification (improving/declining biomarkers)
    - _Requirements: 6.1, 6.2, 6.4, 6.5_

  - [ ]* 15.2 Write property test for temporal analysis completeness
    - **Property 12: Temporal Analysis Completeness**
    - **Validates: Requirements 6.1, 6.2, 6.4, 6.5**

  - [ ]* 15.3 Write unit tests for temporal analysis
    - Test with multiple time points
    - Test age velocity calculation
    - Test trend identification
    - _Requirements: 6.2, 6.4_

- [ ] 16. Implement intervention impact prediction (optional for MVP)
  - [ ] 16.1 Add intervention prediction methods
    - Implement `predict_with_intervention()` method
    - Calculate expected age reduction from interventions
    - Calculate projected biological age
    - Calculate time horizon for improvements
    - Handle multiple interventions with combined effects
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ]* 16.2 Write property test for intervention impact prediction
    - **Property 13: Intervention Impact Prediction**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

  - [ ]* 16.3 Write unit tests for intervention predictions
    - Test single intervention impact
    - Test multiple intervention combined effects
    - Test time horizon calculation
    - _Requirements: 9.4, 9.5_

- [ ] 17. Performance optimization and testing
  - [ ] 17.1 Add performance optimizations
    - Verify caching is working correctly
    - Optimize biomarker normalization
    - Optimize contributor analysis
    - _Requirements: 12.1, 12.3_

  - [ ]* 17.2 Write property test for performance bounds
    - **Property 17: Performance Bounds**
    - **Validates: Requirements 12.1, 12.3**

  - [ ]* 17.3 Write performance benchmarks
    - Measure single user prediction time
    - Measure batch processing time
    - Verify caching reduces file reads
    - _Requirements: 12.1, 12.2, 12.3_

- [ ] 18. Final integration and documentation
  - [ ] 18.1 Create integration tests
    - Test end-to-end prediction flow
    - Test all 6 test users
    - Test error scenarios
    - _Requirements: 1.6_

  - [ ] 18.2 Add API documentation
    - Document all public methods with docstrings
    - Add type hints to all functions
    - Create usage examples
    - Document error scenarios
    - _Requirements: 13.4_

  - [ ] 18.3 Add model versioning support
    - Tag predictions with model version
    - Document algorithm and weights
    - Support backward compatibility
    - _Requirements: 14.1, 14.3, 14.4, 14.5_

  - [ ]* 18.4 Write property test for model version tagging
    - **Property 15: Model Version Tagging**
    - **Validates: Requirements 14.1, 14.2, 14.3**

- [ ] 19. Final checkpoint - Ensure all tests pass
  - Run full test suite
  - Verify all 18 correctness properties are tested
  - Verify coverage goals are met (>90% line coverage)
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Tasks 14-16 are marked as optional for MVP but provide valuable functionality
- Core functionality (tasks 1-13) provides a working biological age engine
- The implementation follows a bottom-up approach: utilities → calculators → main engine
