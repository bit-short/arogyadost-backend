# User Switching API

Complete implementation of user profile management and switching functionality for the Aarogyadost healthcare platform.

## Overview

The User Switching API allows users to manage multiple profiles within the same application instance. This is useful for:
- Family members sharing the same device
- Healthcare providers managing multiple patients  
- Care team members accessing different user profiles

## Features

✅ **Complete API Implementation**
- Get all user profiles
- Get specific user profile details
- Create new user profiles
- Update existing profiles
- Switch active user context
- Delete/deactivate profiles
- Current user information
- Health check endpoint

✅ **Comprehensive Mock Data**
- 5 pre-configured user profiles
- Different user roles (primary_user, family_member, healthcare_provider, care_team)
- Realistic user preferences and permissions
- Session management with tokens

✅ **Error Handling**
- Proper HTTP status codes
- Structured error responses
- Input validation
- Edge case handling

## API Endpoints

### Base URL
```
http://localhost:8000/api
```

### 1. Get All User Profiles
```http
GET /users/profiles
```

**Response:**
```json
{
  "profiles": [...],
  "total_count": 5,
  "current_user_id": "user_123"
}
```

### 2. Get Specific User Profile
```http
GET /users/{user_id}/profile
```

### 3. Create New User Profile
```http
POST /users/profiles
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@email.com",
  "phone": "+1-555-0123",
  "role": "family_member"
}
```

### 4. Switch Active User
```http
POST /users/switch
Content-Type: application/json

{
  "user_id": "user_456",
  "session_context": {
    "device_id": "device_123",
    "platform": "web"
  }
}
```

### 5. Update User Profile
```http
PUT /users/{user_id}/profile
Content-Type: application/json

{
  "name": "Updated Name",
  "preferences": {
    "theme": "dark",
    "notifications_enabled": false
  }
}
```

### 6. Delete User Profile
```http
DELETE /users/{user_id}/profile
Content-Type: application/json

{
  "reason": "User requested deletion"
}
```

### 7. Get Current Active User
```http
GET /users/current
```

### 8. Health Check
```http
GET /users/health
```

## User Roles & Permissions

### Primary User
- Full access to all features
- Can manage other users
- Can edit all health data

### Family Member
- Can view and edit own health data
- Limited user management
- Full chat access

### Healthcare Provider
- Professional access with audit logging
- Can manage multiple users
- Full health data access

### Care Team
- Can view multiple users
- Limited editing permissions
- Read-only access to most data

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
uvicorn main:app --reload
```

### 3. Test the API
```bash
# Run the test script
python test_user_switching_api.py

# Or test manually
curl http://localhost:8000/api/users/profiles
```

### 4. View API Documentation
Open your browser to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Mock Data

The API includes 5 pre-configured users:

1. **Dr. Sarah Johnson** (user_123) - Primary User
2. **Michael Chen** (user_456) - Family Member  
3. **Alex Thompson** (user_789) - Family Member
4. **Dr. Emily Rodriguez** (user_101) - Healthcare Provider
5. **James Wilson** (user_202) - Care Team

Each user has:
- Complete profile information
- Role-based permissions
- User preferences (theme, language, notifications)
- Realistic avatar URLs from Unsplash
- Activity timestamps

## File Structure

```
app/
├── models/
│   └── user_switching.py      # Pydantic models
├── routers/
│   └── user_switching.py      # API endpoints
├── data/
│   └── mock_users.py          # Mock data and utilities
└── ...

test_user_switching_api.py     # Test script
USER_SWITCHING_API.md          # This documentation
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": {
    "error": {
      "code": "USER_NOT_FOUND",
      "message": "User with ID 'user_999' not found",
      "timestamp": "2024-01-08T10:00:00Z"
    }
  }
}
```

Common error codes:
- `USER_NOT_FOUND` (404)
- `EMAIL_ALREADY_EXISTS` (409)
- `INVALID_REQUEST` (400)
- `INSUFFICIENT_PERMISSIONS` (403)
- `UNAUTHORIZED` (401)

## Session Management

- Each user switch generates a new session token
- Session tokens expire after 24 hours
- Include session token in Authorization header: `Bearer {token}`
- Session context tracks device and platform information

## Rate Limiting (Future)

Planned rate limits:
- User switching: 10 requests per minute per IP
- Profile creation: 5 requests per hour per IP  
- Profile updates: 20 requests per minute per user

## Frontend Integration

The API is designed to work with the existing frontend `SettingsSheet.tsx` component. Key integration points:

1. Replace `mockProfiles` with API calls to `/users/profiles`
2. Implement user switching via `/users/switch`
3. Add profile management (create/update/delete)
4. Handle authentication tokens and permissions
5. Update UI to show current active user

## Testing

Run the comprehensive test suite:

```bash
# Start the server
uvicorn main:app --reload

# In another terminal, run tests
python test_user_switching_api.py
```

The test script verifies:
- All endpoint functionality
- Error handling
- Data validation
- Session management
- CRUD operations

## Next Steps

1. **Database Integration**: Replace mock data with PostgreSQL
2. **Authentication**: Add JWT token validation
3. **Rate Limiting**: Implement request throttling
4. **Audit Logging**: Track user switches and profile changes
5. **Real-time Updates**: WebSocket notifications for profile changes
6. **Data Migration**: Tools for importing existing user data

## Support

For questions or issues:
1. Check the API documentation at `/docs`
2. Run the test script to verify functionality
3. Review error responses for debugging
4. Check server logs for detailed error information

---

**Status**: ✅ Complete and Ready for Use  
**Last Updated**: January 8, 2026  
**API Version**: 2.0.0