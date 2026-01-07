# Implementation Plan: API Internationalization

## Overview

This implementation plan breaks down the addition of multi-language support (English, Hindi, Tamil) into discrete, incremental tasks. The approach prioritizes core translation infrastructure first, then applies it to existing endpoints, and finally adds comprehensive testing.

## Tasks

- [ ] 1. Set up translation infrastructure
  - Create directory structure for translations
  - Create translation JSON files for all three locales (en-IN, hi-IN, ta-IN)
  - Implement TranslationService class with loading and lookup methods
  - Add fallback logic for missing keys
  - _Requirements: 1.1, 4.1, 4.2, 4.3_

- [ ]* 1.1 Write property test for translation fallback
  - **Property 8: Translation Fallback Consistency**
  - **Validates: Requirements 4.2**

- [ ]* 1.2 Write property test for locale support
  - **Property 1: Locale Support Completeness**
  - **Validates: Requirements 1.1**

- [ ] 2. Implement language detection middleware
  - Create LanguageMiddleware class
  - Implement Accept-Language header parsing
  - Implement query parameter extraction
  - Add locale precedence logic (query param > header > default)
  - Set up context variable for current locale
  - Add Content-Language response header
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ]* 2.1 Write property test for Accept-Language parsing
  - **Property 4: Accept-Language Header Parsing**
  - **Validates: Requirements 2.1, 2.2**

- [ ]* 2.2 Write property test for query parameter precedence
  - **Property 5: Query Parameter Precedence**
  - **Validates: Requirements 2.5**

- [ ]* 2.3 Write property test for unsupported locale fallback
  - **Property 2: Unsupported Locale Fallback**
  - **Validates: Requirements 1.3, 2.3**

- [ ] 3. Create response formatter
  - Implement ResponseFormatter class
  - Add methods for formatting health categories
  - Add methods for formatting recommendations
  - Add methods for formatting biomarker details
  - Add methods for formatting error messages
  - Implement locale metadata addition
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 6.3_

- [ ]* 3.1 Write property test for response translation completeness
  - **Property 6: Response Translation Completeness**
  - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**

- [ ]* 3.2 Write property test for numeric preservation
  - **Property 7: Numeric and Date Preservation**
  - **Validates: Requirements 3.5**

- [ ]* 3.3 Write property test for medical terminology preservation
  - **Property 3: Medical Terminology Preservation**
  - **Validates: Requirements 1.5**

- [ ] 4. Create translation content files
  - Populate en-IN.json with all English translations
  - Populate hi-IN.json with all Hindi translations
  - Populate ta-IN.json with all Tamil translations
  - Include health categories, statuses, recommendations, biomarkers, errors
  - Ensure consistent key structure across all files
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 4.1 Write property test for translation file key consistency
  - **Property 12: Translation File Key Consistency**
  - **Validates: Requirements 9.3**

- [ ] 5. Integrate middleware into FastAPI application
  - Add LanguageMiddleware to main.py
  - Configure middleware order
  - Test middleware activation
  - Verify context variable propagation
  - _Requirements: 6.1, 6.2_

- [ ]* 5.1 Write unit tests for middleware integration
  - Test middleware with various request patterns
  - Test context variable setting
  - Test response header addition
  - _Requirements: 6.1, 6.2_

- [ ] 6. Apply localization to health endpoints
  - Update /api/health/biomarkers endpoint
  - Update /api/health/recommendations endpoint
  - Update /api/health/metrics endpoint
  - Update /api/health/status endpoint
  - Update /api/biomarkers/{biomarker_id} endpoint
  - Add locale metadata to all responses
  - _Requirements: 3.1, 3.2, 3.3, 6.3_

- [ ]* 6.1 Write integration tests for health endpoints
  - Test each endpoint with all three locales
  - Verify response structure consistency
  - Verify translation correctness
  - _Requirements: 3.1, 3.2, 3.3_

- [ ]* 6.2 Write property test for response structure invariance
  - **Property 11: Response Structure Invariance**
  - **Validates: Requirements 6.5**

- [ ] 7. Apply localization to medical files endpoints
  - Update /api/medical-files/categories endpoint
  - Update /api/medical-files/specialties endpoint
  - Update /api/medical-files endpoints
  - Translate category names and specialty names
  - Preserve file metadata and dates
  - _Requirements: 3.1, 3.5_

- [ ]* 7.1 Write integration tests for medical files endpoints
  - Test with all three locales
  - Verify metadata preservation
  - Verify date preservation
  - _Requirements: 3.1, 3.5_

- [ ] 8. Apply localization to chat endpoints
  - Update /api/chat/message endpoint responses
  - Translate AI response content where appropriate
  - Preserve timestamps and IDs
  - Add locale-aware response generation
  - _Requirements: 3.1, 3.5_

- [ ]* 8.1 Write integration tests for chat endpoints
  - Test message responses in all locales
  - Verify timestamp preservation
  - _Requirements: 3.1, 3.5_

- [ ] 9. Apply localization to doctor and lab endpoints
  - Update /api/doctors endpoint
  - Update /api/labs endpoint
  - Translate specialty names
  - Preserve ratings and contact information
  - _Requirements: 3.1, 3.5_

- [ ]* 9.1 Write integration tests for doctor and lab endpoints
  - Test with all three locales
  - Verify data preservation
  - _Requirements: 3.1, 3.5_

- [ ] 10. Add backward compatibility support
  - Verify existing endpoints work without language specification
  - Ensure default English responses
  - Add deprecation warnings to response headers (if needed)
  - Document migration path
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 10.1 Write property test for backward compatibility
  - **Property 9: Backward Compatibility**
  - **Validates: Requirements 5.2**

- [ ]* 10.2 Write unit tests for deprecation headers
  - Test header presence
  - Test header content
  - _Requirements: 5.3_

- [ ] 11. Apply localization to Digital Twin endpoints
  - Update /api/digital-twin endpoints
  - Translate domain names and field descriptions
  - Preserve data values and timestamps
  - Add locale metadata
  - _Requirements: 3.1, 3.5, 6.3_

- [ ]* 11.1 Write integration tests for Digital Twin endpoints
  - Test with all three locales
  - Verify data preservation
  - Verify structure consistency
  - _Requirements: 3.1, 3.5_

- [ ] 12. Apply localization to Biological Age endpoints
  - Update /api/biological-age endpoints
  - Translate insights and recommendations
  - Preserve numeric age calculations
  - Add locale metadata
  - _Requirements: 3.1, 3.5, 6.3_

- [ ]* 12.1 Write integration tests for Biological Age endpoints
  - Test with all three locales
  - Verify calculation preservation
  - Verify insight translation
  - _Requirements: 3.1, 3.5_

- [ ] 13. Apply localization to Recommendations endpoints
  - Update /api/recommendations endpoints
  - Translate recommendation text and summaries
  - Preserve priority scores and metadata
  - Add locale metadata
  - _Requirements: 3.2, 3.5, 6.3_

- [ ]* 13.1 Write integration tests for Recommendations endpoints
  - Test with all three locales
  - Verify recommendation translation
  - Verify metadata preservation
  - _Requirements: 3.2, 3.5_

- [ ] 14. Add error message localization
  - Create error message translations
  - Update HTTPException handling
  - Translate validation errors
  - Ensure error codes remain consistent
  - _Requirements: 3.4, 7.5_

- [ ]* 14.1 Write property test for error message translation
  - Test error messages in all locales
  - Verify error codes preserved
  - _Requirements: 3.4_

- [ ] 15. Add locale metadata to all responses
  - Implement helper function to add locale field
  - Apply to all endpoint responses
  - Verify locale field presence
  - _Requirements: 6.3_

- [ ]* 15.1 Write property test for locale metadata inclusion
  - **Property 10: Locale Metadata Inclusion**
  - **Validates: Requirements 6.3**

- [ ] 16. Performance optimization
  - Verify translations are cached in memory
  - Measure translation lookup performance
  - Optimize hot paths if needed
  - Add performance monitoring
  - _Requirements: 8.1, 8.3_

- [ ]* 16.1 Write unit tests for caching behavior
  - Test translation loading
  - Verify no reloading on requests
  - _Requirements: 8.1, 8.3_

- [ ] 17. Add comprehensive logging
  - Log missing translation keys
  - Log unsupported locale requests
  - Log translation file loading
  - Add development mode warnings
  - _Requirements: 4.5_

- [ ]* 17.1 Write unit tests for logging behavior
  - Test missing key warnings
  - Test locale fallback logging
  - _Requirements: 4.5_

- [ ] 18. Update API documentation
  - Document Accept-Language header usage
  - Document lang query parameter
  - Provide examples for each locale
  - Document translation coverage
  - Document migration guide
  - _Requirements: 10.1, 10.2, 10.4, 10.5_

- [ ] 19. Final integration testing
  - Run full test suite with all locales
  - Verify all endpoints work correctly
  - Test edge cases and error conditions
  - Verify backward compatibility
  - _Requirements: All_

- [ ] 20. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Integration tests verify end-to-end functionality
- The implementation follows an incremental approach: infrastructure → application → testing
- Backward compatibility is maintained throughout
