# Requirements Document

## Introduction

This feature enables developers and testers to select and switch between different test users in the Aarogyadost application. This is essential for testing various user scenarios, health profiles, and data configurations without manually modifying code or database entries.

## Glossary

- **Test_User**: A pre-configured user profile with associated health data (biomarkers, medical history, lifestyle data) used for testing and development
- **Hardcoded_User**: The default user profile with mock data embedded directly in the application code (main.py), used as the fallback when no test user is selected
- **User_Selector**: The interface component that displays available test users and allows selection
- **Active_User**: The currently selected test user whose data is being displayed and used in the application
- **User_Session**: The context that maintains the selected user's identity across API requests
- **Digital_Twin**: The comprehensive health data model for a user including biomarkers, conditions, lifestyle, and medical history

## Requirements

### Requirement 1: List Available Test Users

**User Story:** As a developer, I want to see all available test users including the hardcoded default user, so that I can choose which user profile to test with.

#### Acceptance Criteria

1. WHEN the user selection endpoint is called, THE System SHALL return a list of all available test users
2. THE System SHALL include a special "default" or "hardcoded" user entry representing the mock data embedded in the application
3. THE System SHALL include user demographics (age, gender, location) for each test user
4. THE System SHALL include health profile summary (BMI, biological age, blood type) for each test user
5. THE System SHALL include active health goals for each test user
6. THE System SHALL indicate which test users have comprehensive data (biomarkers, medical history, lifestyle data)
7. THE System SHALL clearly label the hardcoded user as "Default (Hardcoded)" or similar to distinguish it from dataset users

### Requirement 2: Select Active Test User

**User Story:** As a developer, I want to select a specific test user or the hardcoded default user, so that all subsequent API calls use that user's data.

#### Acceptance Criteria

1. WHEN a valid user_id is provided, THE System SHALL set that user as the active user
2. WHEN the special "default" or "hardcoded" user_id is provided, THE System SHALL use the hardcoded mock data
3. WHEN an invalid user_id is provided, THE System SHALL return an error with available user IDs
4. WHEN a user is selected, THE System SHALL return confirmation with the selected user's profile
5. THE System SHALL persist the selected user across multiple API requests within the same session

### Requirement 3: Retrieve Current Active User

**User Story:** As a developer, I want to know which test user is currently active, so that I can verify the correct user context.

#### Acceptance Criteria

1. WHEN the current user endpoint is called, THE System SHALL return the active user's profile
2. WHEN no user has been selected, THE System SHALL return the default hardcoded user
3. WHEN the hardcoded user is active, THE System SHALL clearly indicate this in the response
4. THE System SHALL include the user's full profile including demographics, health profile, and goals

### Requirement 4: User Data Integration

**User Story:** As a developer, I want all existing endpoints to use the selected test user's data, so that I can test different user scenarios seamlessly.

#### Acceptance Criteria

1. WHEN a user is selected, THE Digital_Twin endpoints SHALL return that user's health data
2. WHEN a user is selected, THE Biological_Age endpoint SHALL calculate using that user's biomarkers
3. WHEN a user is selected, THE Recommendations endpoint SHALL generate recommendations for that user
4. WHEN a user is selected, THE Chat endpoint SHALL use that user's context for responses

### Requirement 5: User Selection UI Page

**User Story:** As a developer, I want a simple web page to select users, so that I don't need to use API tools or command line.

#### Acceptance Criteria

1. WHEN the user selection page is accessed, THE System SHALL display a grid or list of available test users
2. WHEN displaying users, THE System SHALL show user ID, age, gender, and key health metrics
3. WHEN a user card is clicked, THE System SHALL select that user and provide visual confirmation
4. WHEN a user is selected, THE System SHALL highlight the active user in the interface
5. THE System SHALL provide a link or button to return to the main application with the selected user

### Requirement 6: Data Availability Indicators

**User Story:** As a developer, I want to see what data is available for each test user, so that I can choose users with the right data for my testing needs.

#### Acceptance Criteria

1. WHEN displaying test users, THE System SHALL indicate if biomarker data is available
2. WHEN displaying test users, THE System SHALL indicate if medical history data is available
3. WHEN displaying test users, THE System SHALL indicate if lifestyle data is available
4. WHEN displaying test users, THE System SHALL indicate if AI interaction history is available
5. WHEN displaying test users, THE System SHALL show the data completeness percentage or score
