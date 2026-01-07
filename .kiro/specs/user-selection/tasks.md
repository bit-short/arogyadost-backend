# Implementation Plan: User Selection Feature

## Overview

This implementation plan breaks down the user selection feature into incremental coding tasks. The feature enables switching between test users (dataset-based and hardcoded) for development and testing purposes.

## Tasks

- [ ] 1. Create user profile data models
  - Create `app/models/user_profile.py` with Pydantic models
  - Define `Demographics`, `HealthProfile`, `HealthGoal`, `DataAvailability`, and `UserProfile` models
  - Add validation rules for required fields
  - _Requirements: 1.3, 1.4, 1.5, 1.6_

- [ ]* 1.1 Write unit tests for user profile models
  - Test model validation
  - Test field requirements
  - Test data serialization/deserialization
  - _Requirements: 1.3, 1.4, 1.5_

- [ ] 2. Implement user context manager service
  - [ ] 2.1 Create `app/services/user_context.py` with `UserContextManager` class
    - Implement `__init__` with active_user_id and users_cache
    - Add method to load users from `datasets/users/users.json`
    - Add method to create hardcoded user profile from mock data
    - _Requirements: 1.1, 1.2, 2.1, 3.2_

  - [ ] 2.2 Implement user selection logic
    - Add `select_user(user_id)` method with validation
    - Add `get_current_user()` method
    - Add error handling for invalid user IDs
    - _Requirements: 2.1, 2.2, 2.3, 3.1_

  - [ ] 2.3 Implement data availability checking
    - Add `check_data_availability(user_id)` method
    - Check for biomarkers, medical_history, lifestyle, ai_interactions, interventions files
    - Calculate completeness score based on available data
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 2.4 Write property test for user list completeness
    - **Property 1: User List Completeness**
    - **Validates: Requirements 1.1, 1.2**

  - [ ]* 2.5 Write property test for valid user selection
    - **Property 2: Valid User Selection**
    - **Validates: Requirements 2.1, 2.2**

  - [ ]* 2.6 Write property test for invalid user rejection
    - **Property 3: Invalid User Rejection**
    - **Validates: Requirements 2.3**

  - [ ]* 2.7 Write property test for active user persistence
    - **Property 4: Active User Persistence**
    - **Validates: Requirements 2.4, 3.1**

  - [ ]* 2.8 Write property test for data availability accuracy
    - **Property 5: Data Availability Accuracy**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

- [ ] 3. Create user selection API router
  - [ ] 3.1 Create `app/routers/users.py` with FastAPI router
    - Set up router with prefix `/api/users` and tag `["users"]`
    - Initialize UserContextManager instance
    - _Requirements: 1.1_

  - [ ] 3.2 Implement GET /api/users/available endpoint
    - Return list of all available users (hardcoded + dataset users)
    - Include full user profiles with data availability
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

  - [ ] 3.3 Implement POST /api/users/select endpoint
    - Accept user_id in request body
    - Validate and select user
    - Return confirmation with selected user profile
    - Handle errors for invalid user IDs
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ] 3.4 Implement GET /api/users/current endpoint
    - Return currently active user profile
    - Include is_hardcoded indicator
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [ ]* 3.5 Write unit tests for API endpoints
    - Test each endpoint with valid inputs
    - Test error cases
    - Test response formats
    - _Requirements: 1.1, 2.1, 2.3, 3.1_

- [ ] 4. Checkpoint - Test backend API
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Create user selection frontend UI
  - [ ] 5.1 Create `static/user-selection.html` page
    - Create HTML structure with header and user grid container
    - Add CSS for card layout and styling
    - Add visual indicators for active user and data availability
    - _Requirements: 5.1, 5.2, 5.4_

  - [ ] 5.2 Implement JavaScript for user selection
    - Add function to fetch available users from API
    - Add function to render user cards with data
    - Add click handlers for user selection
    - Add function to display selection confirmation
    - Add function to highlight active user
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 5.3 Add navigation and user experience features
    - Add link/button to return to main application
    - Add loading states while fetching data
    - Add error message display for failed requests
    - _Requirements: 5.5_

- [ ] 6. Integrate user context with existing services
  - [ ] 6.1 Update digital twin router to use active user
    - Modify `app/routers/digital_twin.py` to get user_id from UserContextManager
    - Update endpoints to use selected user's data
    - _Requirements: 4.1_

  - [ ] 6.2 Update biological age router to use active user
    - Modify `app/routers/biological_age.py` to get user_id from UserContextManager
    - Ensure calculations use selected user's biomarkers
    - _Requirements: 4.2_

  - [ ] 6.3 Update recommendations router to use active user
    - Modify `app/routers/recommendations.py` to get user_id from UserContextManager
    - Ensure recommendations are generated for selected user
    - _Requirements: 4.3_

  - [ ] 6.4 Update chat router to use active user
    - Modify `app/routers/chat.py` to get user_id from UserContextManager
    - Ensure chat context uses selected user's data
    - _Requirements: 4.4_

  - [ ]* 6.5 Write integration tests for service integration
    - Test user selection affects digital twin data
    - Test user selection affects biological age calculations
    - Test user selection affects recommendations
    - Test user selection affects chat context
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 7. Register user router in main application
  - Update `main.py` to import and include user selection router
  - Ensure router is registered before other routers for proper initialization
  - _Requirements: 1.1_

- [ ] 8. Final checkpoint - End-to-end testing
  - Ensure all tests pass, ask the user if questions arise.
  - Test complete user selection flow from UI to backend
  - Verify user switching works across all endpoints

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Integration tests ensure user selection affects all dependent services correctly
