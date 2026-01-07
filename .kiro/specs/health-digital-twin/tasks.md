# Implementation Plan: Health Digital Twin

## Overview

This implementation plan breaks down the Health Digital Twin system into discrete coding tasks. The approach follows a bottom-up strategy: first implementing core data structures, then building validation and registry components, followed by serialization and query capabilities, and finally integration with test data.

## Tasks

- [ ] 1. Set up project structure and core data models
  - Create `app/models/digital_twin.py` module
  - Define `FieldState` enum with three states (populated, missing, not_applicable)
  - Implement `HealthDataPoint` class with value, timestamp, unit, and metadata
  - Implement `HealthField` class with state tracking and temporal value storage
  - Implement `HealthDomain` class as container for fields
  - _Requirements: 1.1, 1.3, 2.1, 2.2_

- [ ]* 1.1 Write property test for field state consistency
  - **Property 1: Field State Consistency**
  - **Validates: Requirements 2.1, 2.2**

- [ ] 2. Implement DigitalTwin core class
  - Create main `DigitalTwin` class with user_id and metadata
  - Implement `__init__` to initialize empty twin with metadata
  - Implement `set_value()` method to add data to any domain/field
  - Implement `get_value()` method with latest/historical options
  - Implement `get_domain()` method to retrieve entire domain
  - Implement `get_missing_fields()` method to list missing fields
  - _Requirements: 1.1, 1.2, 8.1, 8.2, 8.3_

- [ ]* 2.1 Write property test for missing field preservation
  - **Property 2: Missing Field Preservation**
  - **Validates: Requirements 2.2, 10.1**

- [ ]* 2.2 Write property test for missing fields list accuracy
  - **Property 9: Missing Fields List Accuracy**
  - **Validates: Requirements 2.4, 9.3**

- [ ] 3. Implement temporal data management
  - Implement `get_time_series()` method with date range filtering
  - Add chronological sorting logic to `HealthField.get_history()`
  - Implement temporal statistics calculation (trend direction, rate of change)
  - Add `get_latest()` method to `HealthField` class
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ]* 3.1 Write property test for temporal ordering
  - **Property 3: Temporal Ordering**
  - **Validates: Requirements 3.1, 3.2**

- [ ]* 3.2 Write property test for query filtering correctness
  - **Property 8: Query Filtering Correctness**
  - **Validates: Requirements 3.4, 9.2**

- [ ]* 3.3 Write property test for latest value retrieval
  - **Property 12: Latest Value Retrieval**
  - **Validates: Requirements 3.3, 8.3**

- [ ] 4. Implement data completeness tracking
  - Implement `calculate_completeness()` method in `HealthDomain`
  - Implement `calculate_completeness()` method in `DigitalTwin` (aggregates domains)
  - Add caching for completeness calculations
  - _Requirements: 2.3, 8.4_

- [ ]* 4.1 Write property test for completeness calculation accuracy
  - **Property 4: Completeness Calculation Accuracy**
  - **Validates: Requirements 2.3**

- [ ] 5. Implement BiomarkerRegistry
  - Create `app/models/biomarker_registry.py` module
  - Define `BiomarkerMetadata` dataclass with all metadata fields
  - Implement `BiomarkerRegistry` class with registration and lookup
  - Implement `get_reference_range()` with age/sex specificity
  - Populate registry with common biomarkers (glucose, cholesterol, HbA1c, blood pressure, etc.)
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 5.1 Write unit tests for biomarker registry
  - Test registration of new biomarkers
  - Test lookup of existing biomarkers
  - Test age-specific reference range selection
  - Test sex-specific reference range selection
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 6. Implement DataValidator
  - Create `app/models/data_validator.py` module
  - Define `ValidationResult` dataclass with is_valid, errors, warnings
  - Implement `DataValidator` class with biomarker registry integration
  - Implement `validate_biomarker()` method with range checking
  - Implement `validate_unit()` method for unit consistency
  - Implement `validate_temporal_consistency()` for timestamp validation
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 6.1 Write property test for biomarker validation
  - **Property 5: Biomarker Validation**
  - **Validates: Requirements 6.1, 6.2**

- [ ]* 6.2 Write property test for unit consistency
  - **Property 6: Unit Consistency**
  - **Validates: Requirements 6.4**

- [ ] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement serialization (to_dict and from_dict)
  - Implement `to_dict()` method in `HealthDataPoint`
  - Implement `to_dict()` method in `HealthField`
  - Implement `to_dict()` method in `HealthDomain`
  - Implement `to_dict()` method in `DigitalTwin`
  - Implement `from_dict()` class method in `DigitalTwin` for deserialization
  - Handle nested structures and type preservation
  - _Requirements: 10.1, 8.5_

- [ ]* 8.1 Write property test for serialization round-trip
  - **Property 7: Serialization Round-Trip**
  - **Validates: Requirements 10.1**

- [ ] 9. Implement ReasoningContextGenerator
  - Create `app/models/reasoning_context.py` module
  - Implement `ReasoningContextGenerator` class
  - Implement `_format_demographics()` method
  - Implement `_format_biomarkers()` with trends and reference ranges
  - Implement `_format_medical_history()` method
  - Implement `_format_completeness_summary()` method
  - Implement `generate()` method that combines all sections
  - Add markdown formatting for readability
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 9.1 Write property test for reasoning context completeness summary
  - **Property 10: Reasoning Context Completeness Summary**
  - **Validates: Requirements 4.2, 10.2**

- [ ]* 9.2 Write unit tests for reasoning context generation
  - Test context generation with complete data
  - Test context generation with missing fields
  - Test context generation with empty domains
  - Test markdown formatting
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 10. Implement query interface methods
  - Implement domain filtering in `get_domain()` method
  - Implement field state filtering in `get_missing_fields()`
  - Add time range filtering to `get_time_series()`
  - Implement query result formatting for consistency
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 10.1 Write property test for domain query isolation
  - **Property 11: Domain Query Isolation**
  - **Validates: Requirements 9.1**

- [ ] 11. Implement test data loading
  - Create `tests/test_data/digital_twins/` directory
  - Create JSON test files for each test profile (healthy, diabetic, cardiovascular, incomplete, athlete, elderly)
  - Implement helper function to load test twins from JSON
  - Add validation during loading
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 11.1 Write unit tests for test data loading
  - Test loading complete profile
  - Test loading partial profile with missing fields
  - Test validation errors on invalid data
  - Test loading multiple profiles
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 12. Implement token estimation and truncation
  - Add `_estimate_tokens()` method to `ReasoningContextGenerator`
  - Implement `_truncate_to_fit()` method with prioritization logic
  - Update `generate()` to support max_tokens parameter
  - Prioritize recent data and populated fields over missing fields
  - _Requirements: 10.4, 10.5_

- [ ]* 12.1 Write unit tests for truncation logic
  - Test truncation with various token limits
  - Test prioritization of recent data
  - Test prioritization of populated fields
  - _Requirements: 10.4, 10.5_

- [ ] 13. Integration and documentation
  - Add docstrings to all public methods
  - Create usage examples in module docstrings
  - Add type hints to all method signatures
  - Create README for the digital twin module
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]* 13.1 Write integration tests
  - Test complete workflow: load data → query → generate reasoning context
  - Test multiple twins with different completeness levels
  - Test validation integration with data loading
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 14. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation follows a bottom-up approach: data structures → validation → serialization → reasoning context
