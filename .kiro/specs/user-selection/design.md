# Design Document: User Selection Feature

## Overview

The user selection feature provides a mechanism for developers and testers to switch between different test user profiles during development and testing. This includes both dataset-based test users (from `datasets/users/users.json`) and the hardcoded default user (embedded in application code). The feature consists of backend API endpoints for user management and a simple frontend UI for easy user switching.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend UI Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  User Selection Page (HTML/JS)                       │  │
│  │  - Display user cards with profiles                  │  │
│  │  - Handle user selection clicks                      │  │
│  │  - Show active user indicator                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend API Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  User Selection Router (/api/users)                  │  │
│  │  - GET /api/users/available                          │  │
│  │  - POST /api/users/select                            │  │
│  │  - GET /api/users/current                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  User Context Manager                                 │  │
│  │  - Maintain active user state                        │  │
│  │  - Load user data from datasets                      │  │
│  │  - Provide user context to other services            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Sources                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ users.json   │  │ biomarkers/  │  │ Hardcoded Data  │  │
│  │ (datasets/)  │  │ lifestyle/   │  │ (main.py)       │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Session Management

Since this is a development/testing feature, we'll use a simple in-memory session store:

```
┌─────────────────────────────────────┐
│   In-Memory Session Store           │
│                                     │
│   {                                 │
│     "default": "hardcoded",         │
│     "session_123": "test_user_1",   │
│     "session_456": "test_user_3"    │
│   }                                 │
└─────────────────────────────────────┘
```

For MVP, we'll use a global active user (single session). Future enhancement can add proper session management with cookies/tokens.

## Components and Interfaces

### 1. User Selection Router (`app/routers/users.py`)

New FastAPI router handling user selection endpoints.

**Endpoints:**

```python
# GET /api/users/available
# Returns list of all available test users
Response: {
    "users": [
        {
            "user_id": "hardcoded",
            "display_name": "Default (Hardcoded)",
            "is_hardcoded": true,
            "demographics": {...},
            "health_profile": {...},
            "data_availability": {
                "biomarkers": true,
                "medical_history": true,
                "lifestyle": true,
                "ai_interactions": false
            }
        },
        {
            "user_id": "test_user_1_29f",
            "display_name": "Test User 1 (29F)",
            "is_hardcoded": false,
            "demographics": {...},
            "health_profile": {...},
            "data_availability": {...}
        }
    ]
}

# POST /api/users/select
# Selects a user as active
Request: {
    "user_id": "test_user_1_29f"
}
Response: {
    "message": "User selected successfully",
    "user": {...}  # Full user profile
}

# GET /api/users/current
# Returns currently active user
Response: {
    "user_id": "test_user_1_29f",
    "display_name": "Test User 1 (29F)",
    "is_hardcoded": false,
    "demographics": {...},
    "health_profile": {...}
}
```

### 2. User Context Manager (`app/services/user_context.py`)

Service managing active user state and data loading.

**Interface:**

```python
class UserContextManager:
    def __init__(self):
        self.active_user_id: str = "hardcoded"
        self.users_cache: Dict[str, UserProfile] = {}
        self.hardcoded_user: UserProfile = None
    
    def get_available_users(self) -> List[UserProfile]:
        """Load and return all available test users"""
        pass
    
    def select_user(self, user_id: str) -> UserProfile:
        """Set active user and return profile"""
        pass
    
    def get_current_user(self) -> UserProfile:
        """Get currently active user profile"""
        pass
    
    def load_user_data(self, user_id: str) -> UserData:
        """Load complete user data (biomarkers, lifestyle, etc.)"""
        pass
    
    def check_data_availability(self, user_id: str) -> DataAvailability:
        """Check what data files exist for user"""
        pass
```

### 3. User Profile Model (`app/models/user_profile.py`)

Pydantic models for user data structures.

```python
class Demographics(BaseModel):
    age: int
    gender: str
    location: Dict[str, str]

class HealthProfile(BaseModel):
    height_cm: Optional[float]
    weight_kg: Optional[float]
    bmi: Optional[float]
    blood_type: Optional[str]
    biological_age: Optional[int]

class HealthGoal(BaseModel):
    goal_id: str
    type: str
    target: str
    start_date: datetime
    target_date: datetime
    status: str

class DataAvailability(BaseModel):
    biomarkers: bool
    medical_history: bool
    lifestyle: bool
    ai_interactions: bool
    interventions: bool
    completeness_score: float  # 0.0 to 1.0

class UserProfile(BaseModel):
    user_id: str
    display_name: str
    is_hardcoded: bool
    demographics: Demographics
    health_profile: HealthProfile
    goals: List[HealthGoal]
    data_availability: DataAvailability
    preferences: Optional[Dict[str, Any]]
```

### 4. User Selection UI (`static/user-selection.html`)

Simple HTML page with JavaScript for user selection.

**Features:**
- Grid layout displaying user cards
- Each card shows: user ID, age, gender, key health metrics
- Visual indicators for data availability (badges/icons)
- Highlight active user
- Click to select user
- Confirmation message on selection

**Technology:**
- Plain HTML/CSS/JavaScript (no framework needed for MVP)
- Fetch API for backend communication
- Responsive grid layout

## Data Models

### User Data File Structure

```
datasets/
├── users/
│   └── users.json                    # User profiles
├── biomarkers/
│   └── biomarkers_{user_id}.json     # Biomarker data per user
├── lifestyle/
│   └── lifestyle_{user_id}_{date}.json
├── medical_history/
│   └── medical_history_{user_id}.json
├── interventions/
│   └── interventions_{user_id}.json
└── ai_interactions/
    └── interactions_{user_id}_{session}.json
```

### Hardcoded User Representation

The hardcoded user will be synthesized from the mock data in `main.py`:

```python
HARDCODED_USER = {
    "user_id": "hardcoded",
    "display_name": "Default (Hardcoded)",
    "is_hardcoded": True,
    "demographics": {
        "age": 29,
        "gender": "F",
        "location": {"city": "Unknown", "country": "Unknown"}
    },
    "health_profile": {
        # Extracted from mock_data in main.py
    },
    "data_availability": {
        "biomarkers": True,
        "medical_history": True,
        "lifestyle": True,
        "ai_interactions": False,
        "interventions": False,
        "completeness_score": 0.6
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: User List Completeness

*For any* call to get available users, the returned list should contain the hardcoded user plus all users from `datasets/users/users.json`, with no duplicates.

**Validates: Requirements 1.1, 1.2**

### Property 2: Valid User Selection

*For any* user_id in the available users list, selecting that user should succeed and set it as the active user.

**Validates: Requirements 2.1, 2.2**

### Property 3: Invalid User Rejection

*For any* user_id not in the available users list, attempting to select that user should return an error with the list of valid user IDs.

**Validates: Requirements 2.3**

### Property 4: Active User Persistence

*For any* selected user, subsequent calls to get current user should return that same user until a different user is selected.

**Validates: Requirements 2.4, 3.1**

### Property 5: Data Availability Accuracy

*For any* test user, the data_availability indicators should accurately reflect the existence of corresponding data files in the datasets directory.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

### Property 6: Hardcoded User Identification

*For any* response containing the hardcoded user, the `is_hardcoded` field should be `true` and the `user_id` should be "hardcoded".

**Validates: Requirements 1.7, 2.2, 3.3**

### Property 7: User Profile Completeness

*For any* user in the available users list, the user profile should contain all required fields: user_id, display_name, demographics, health_profile, and data_availability.

**Validates: Requirements 1.3, 1.4, 1.5**

## Error Handling

### Error Scenarios

1. **Invalid User ID**: Return 400 with list of valid user IDs
2. **Missing User Data File**: Log warning, return user with partial data
3. **Corrupted JSON**: Return 500 with error details
4. **File System Access Error**: Return 500 with generic error message

### Error Response Format

```python
{
    "error": "Invalid user_id",
    "message": "User 'invalid_user' not found",
    "valid_user_ids": ["hardcoded", "test_user_1_29f", ...],
    "status_code": 400
}
```

## Testing Strategy

### Unit Tests

**Test Coverage:**
- User context manager initialization
- Loading users from JSON file
- Creating hardcoded user profile
- Selecting valid/invalid users
- Checking data file availability
- Error handling for missing files

**Example Tests:**
```python
def test_load_users_from_json():
    """Test loading users from datasets/users/users.json"""
    
def test_hardcoded_user_creation():
    """Test creating hardcoded user profile from mock data"""
    
def test_select_valid_user():
    """Test selecting a valid user sets it as active"""
    
def test_select_invalid_user_raises_error():
    """Test selecting invalid user returns error"""
    
def test_data_availability_check():
    """Test checking which data files exist for a user"""
```

### Property-Based Tests

**Property Test Configuration:**
- Minimum 100 iterations per test
- Use Hypothesis for generating test data

**Test Cases:**

```python
@given(user_id=st.sampled_from(get_all_user_ids()))
def test_property_valid_user_selection(user_id):
    """
    Property 2: Valid User Selection
    For any user_id in available users, selection should succeed
    
    Feature: user-selection, Property 2
    Validates: Requirements 2.1, 2.2
    """
    
@given(user_id=st.text().filter(lambda x: x not in get_all_user_ids()))
def test_property_invalid_user_rejection(user_id):
    """
    Property 3: Invalid User Rejection
    For any user_id not in available users, selection should fail
    
    Feature: user-selection, Property 3
    Validates: Requirements 2.3
    """

@given(user_id=st.sampled_from(get_all_user_ids()))
def test_property_data_availability_accuracy(user_id):
    """
    Property 5: Data Availability Accuracy
    For any user, data_availability should match actual file existence
    
    Feature: user-selection, Property 5
    Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5
    """
```

### Integration Tests

- Test user selection affects digital twin endpoints
- Test user selection affects biological age calculations
- Test user selection affects recommendations
- Test frontend UI interaction with backend API

### Manual Testing Checklist

- [ ] User selection page displays all users correctly
- [ ] Clicking a user card selects that user
- [ ] Active user is visually highlighted
- [ ] Data availability badges show correctly
- [ ] Selecting hardcoded user works
- [ ] Switching between users updates all endpoints
- [ ] Error messages display for invalid selections

## Implementation Notes

### Phase 1: Backend API (Core Functionality)
1. Create user context manager service
2. Create user profile models
3. Implement user selection router
4. Add unit tests

### Phase 2: Data Integration
1. Load users from datasets/users/users.json
2. Create hardcoded user profile
3. Implement data availability checking
4. Add property-based tests

### Phase 3: Frontend UI
1. Create HTML page with user cards
2. Implement JavaScript for API calls
3. Add styling and visual indicators
4. Test user selection flow

### Phase 4: Integration
1. Update existing endpoints to use active user
2. Test end-to-end user switching
3. Add integration tests

## Future Enhancements

- Session-based user selection (multiple concurrent users)
- User search and filtering
- Bulk user data loading
- User comparison view
- Export user data
- User creation wizard for new test users
