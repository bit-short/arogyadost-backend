# Implementation Plan: Health Recommendations Engine

## Overview

This implementation plan breaks down the Health Recommendations Engine into discrete coding tasks. The approach follows a bottom-up strategy: first implementing data models and core utilities, then building the rule evaluators, followed by the main engine components, and finally the API integration.

## Tasks

- [ ] 1. Set up project structure and data models
  - Create directory structure: `app/services/recommendations/`
  - Define Pydantic models for DigitalTwin, Recommendation, and response types
  - Create type definitions for biomarker categories and priority levels
  - _Requirements: 1.1, 2.1, 2.2, 2.3, 2.4, 5.1, 5.4_

- [ ]* 1.1 Write property test for data model validation
  - **Property 13: Structured Output Format**
  - **Validates: Requirements 5.1, 5.4**

- [ ] 2. Implement Digital Twin Analyzer
  - [ ] 2.1 Create DigitalTwinAnalyzer class with data loading methods
    - Implement `load_user_data(user_id)` to aggregate data from all sources
    - Implement `get_latest_biomarkers()` to retrieve most recent test results
    - Implement `get_biomarker_history(marker, months)` for historical data
    - Implement `get_active_conditions()` to filter active medical conditions
    - Implement `calculate_time_since_test(marker)` for temporal analysis
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1_

  - [ ]* 2.2 Write property test for complete data loading
    - **Property 1: Complete Digital Twin Analysis**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**

  - [ ]* 2.3 Write property test for graceful handling of missing data
    - **Property 17: Graceful Handling of Missing Data**
    - **Validates: Requirements 6.1**

  - [ ]* 2.4 Write unit tests for Digital Twin Analyzer
    - Test data loading with complete user data
    - Test handling of missing biomarker data
    - Test historical data retrieval
    - Test time calculations
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1_

- [ ] 3. Implement Biomarker Rule Evaluator
  - [ ] 3.1 Create BiomarkerRuleEvaluator class
    - Implement out-of-range follow-up logic
    - Implement missing baseline detection
    - Implement trend monitoring analysis
    - Generate recommendations with rationale and timing
    - _Requirements: 1.5, 2.1, 2.2, 2.4, 2.5, 4.1, 4.2, 4.4_

  - [ ]* 3.2 Write property test for follow-up recommendations
    - **Property 6: Follow-up for Abnormal Values**
    - **Validates: Requirements 2.5**

  - [ ]* 3.3 Write property test for baseline recommendations
    - **Property 2: Non-Empty Recommendations for Incomplete Data**
    - **Validates: Requirements 1.5**

  - [ ]* 3.4 Write property test for temporal recency
    - **Property 10: Temporal Recency Consideration**
    - **Validates: Requirements 4.1, 4.2**

  - [ ]* 3.5 Write property test for abnormal follow-up timing
    - **Property 11: Abnormal Follow-up Timing**
    - **Validates: Requirements 4.4**

  - [ ]* 3.6 Write unit tests for biomarker rules
    - Test out-of-range detection
    - Test missing baseline scenarios
    - Test trend analysis
    - Test timing calculations
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

- [ ] 4. Implement Condition Rule Evaluator
  - [ ] 4.1 Create ConditionRuleEvaluator class
    - Implement condition-to-test mapping logic
    - Implement monitoring frequency determination
    - Generate condition-specific recommendations
    - _Requirements: 2.1, 2.2, 2.4, 3.3, 7.2_

  - [ ]* 4.2 Write property test for chronic condition monitoring
    - **Property 9: Chronic Condition Monitoring Priority**
    - **Validates: Requirements 3.3**

  - [ ]* 4.3 Write property test for condition-specific monitoring
    - **Property 21: Condition-Specific Monitoring**
    - **Validates: Requirements 7.2**

  - [ ]* 4.4 Write unit tests for condition rules
    - Test condition mapping for common conditions
    - Test monitoring frequency logic
    - Test recommendation generation
    - _Requirements: 2.1, 2.2, 3.3, 7.2_

- [ ] 5. Implement Demographic Rule Evaluator
  - [ ] 5.1 Create DemographicRuleEvaluator class
    - Implement age-based screening logic
    - Implement sex-specific test recommendations
    - Implement family history risk assessment
    - _Requirements: 1.4, 2.1, 2.2, 7.1, 7.3_

  - [ ]* 5.2 Write property test for evidence-based test selection
    - **Property 20: Evidence-Based Test Selection**
    - **Validates: Requirements 7.1, 7.3**

  - [ ]* 5.3 Write unit tests for demographic rules
    - Test age-based screening for various age groups
    - Test sex-specific recommendations
    - Test family history impact
    - _Requirements: 1.4, 7.1, 7.3_

- [ ] 6. Implement Temporal Rule Evaluator
  - [ ] 6.1 Create TemporalRuleEvaluator class
    - Implement routine monitoring interval logic
    - Implement post-intervention testing logic
    - Calculate appropriate retest timing
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ]* 6.2 Write property test for baseline testing
    - **Property 12: Baseline Testing for New Users**
    - **Validates: Requirements 4.5**

  - [ ]* 6.3 Write unit tests for temporal rules
    - Test routine interval calculations
    - Test post-intervention timing
    - Test overdue detection
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 7. Implement Recommendation Builder
  - [ ] 7.1 Create RecommendationBuilder class
    - Integrate all rule evaluators
    - Implement `build_recommendations(twin)` method
    - Deduplicate recommendations from multiple rules
    - Merge related recommendations
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ]* 7.2 Write property test for rationale presence
    - **Property 3: Rationale Presence**
    - **Validates: Requirements 2.2**

  - [ ]* 7.3 Write property test for priority assignment
    - **Property 4: Priority Assignment**
    - **Validates: Requirements 2.3**

  - [ ]* 7.4 Write property test for timing specification
    - **Property 5: Timing Specification**
    - **Validates: Requirements 2.4**

  - [ ]* 7.5 Write unit tests for recommendation builder
    - Test integration of multiple rule evaluators
    - Test deduplication logic
    - Test recommendation merging
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 8. Checkpoint - Ensure core recommendation logic works
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement Priority Scorer
  - [ ] 9.1 Create PriorityScorer class
    - Implement priority scoring algorithm
    - Implement `calculate_priority_score(rec, twin)` method
    - Implement `assign_priorities(recommendations)` method
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 9.2 Write property test for priority ordering consistency
    - **Property 7: Priority Ordering Consistency**
    - **Validates: Requirements 3.1**

  - [ ]* 9.3 Write property test for high priority assignment
    - **Property 8: High Priority for High Risk**
    - **Validates: Requirements 3.2**

  - [ ]* 9.4 Write unit tests for priority scorer
    - Test scoring algorithm with various inputs
    - Test priority level assignment
    - Test edge cases (all same priority, etc.)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 10. Implement Output Formatter
  - [ ] 10.1 Create OutputFormatter class
    - Implement `format_recommendations(recommendations)` method
    - Implement `group_by_category(recommendations)` method
    - Implement `add_educational_context(recommendation)` method
    - Generate summary statistics
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 10.2 Write property test for logical grouping
    - **Property 14: Logical Grouping**
    - **Validates: Requirements 5.2**

  - [ ]* 10.3 Write property test for educational context
    - **Property 15: Educational Context Presence**
    - **Validates: Requirements 5.3**

  - [ ]* 10.4 Write property test for empty response
    - **Property 16: Empty Response for No Recommendations**
    - **Validates: Requirements 5.5**

  - [ ]* 10.5 Write unit tests for output formatter
    - Test grouping logic
    - Test summary generation
    - Test educational context addition
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 11. Implement Main Recommendation Engine Service
  - [ ] 11.1 Create RecommendationEngine class
    - Wire together all components
    - Implement main `generate_recommendations(user_id)` method
    - Add error handling and logging
    - _Requirements: All requirements_

  - [ ]* 11.2 Write property test for comprehensive baseline
    - **Property 19: Comprehensive Baseline for Empty Twin**
    - **Validates: Requirements 6.3**

  - [ ]* 11.3 Write property test for longevity biomarkers
    - **Property 22: Longevity Biomarker Inclusion**
    - **Validates: Requirements 7.5**

  - [ ]* 11.4 Write integration tests for full recommendation flow
    - Test with test_user_1_29f data
    - Test with empty user data
    - Test with various user profiles
    - _Requirements: All requirements_

- [ ] 12. Implement Error Handling
  - [ ] 12.1 Add comprehensive error handling
    - Implement input validation
    - Add error response formatting
    - Add logging for all error cases
    - Handle edge cases gracefully
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [ ]* 12.2 Write property test for input validation
    - **Property 18: Input Validation**
    - **Validates: Requirements 6.2, 6.4**

  - [ ]* 12.3 Write unit tests for error handling
    - Test invalid user_id
    - Test malformed data
    - Test missing data sources
    - Test system errors
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 13. Checkpoint - Ensure all components integrated
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Create API endpoint
  - [ ] 14.1 Add FastAPI endpoint for recommendations
    - Create `/api/recommendations/{user_id}` GET endpoint
    - Add request validation
    - Add response serialization
    - Add API documentation
    - _Requirements: 5.1, 5.4_

  - [ ]* 14.2 Write API integration tests
    - Test endpoint with valid user_id
    - Test endpoint with invalid user_id
    - Test response format
    - Test error responses
    - _Requirements: 5.1, 5.4, 6.2, 6.4_

- [ ] 15. Add sample data and documentation
  - [ ] 15.1 Create sample recommendation responses
    - Generate examples for documentation
    - Add to mock data if needed for frontend development
    - _Requirements: 5.1, 5.4_

  - [ ]* 15.2 Write API documentation
    - Document endpoint parameters
    - Document response format
    - Add usage examples
    - _Requirements: 5.1, 5.4_

- [ ] 16. Final checkpoint - End-to-end validation
  - Run full test suite
  - Test with all test users
  - Verify API responses
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties using Hypothesis
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end flows with real data
- The implementation uses Python with FastAPI, matching the existing backend stack
