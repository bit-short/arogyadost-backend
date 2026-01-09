"""
User Switching API Models
Pydantic models for user profile management and switching functionality
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    """User preferences and settings"""
    theme: str = Field(default="system", description="UI theme preference")
    language: str = Field(default="en", description="Language preference")
    timezone: str = Field(default="America/New_York", description="User timezone")
    notifications_enabled: bool = Field(default=True, description="Enable notifications")
    incognito_mode: bool = Field(default=False, description="Incognito mode setting")


class UserPermissions(BaseModel):
    """User access permissions"""
    can_view_health_data: bool = Field(default=True, description="Can view health data")
    can_edit_health_data: bool = Field(default=True, description="Can edit health data")
    can_manage_users: bool = Field(default=False, description="Can manage other users")
    can_access_chat: bool = Field(default=True, description="Can access AI chat")


class UserProfileBase(BaseModel):
    """Base user profile information"""
    name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    avatar_url: Optional[str] = Field(None, description="Profile picture URL")
    role: str = Field(..., description="User role (primary_user, family_member, care_team, healthcare_provider)")


class UserProfileCreate(UserProfileBase):
    """Model for creating a new user profile"""
    preferences: Optional[UserPreferences] = Field(default_factory=UserPreferences)
    permissions: Optional[UserPermissions] = Field(default_factory=UserPermissions)


class UserProfileUpdate(BaseModel):
    """Model for updating user profile"""
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class UserProfile(UserProfileBase):
    """Complete user profile with all fields"""
    id: str = Field(..., description="Unique user identifier")
    preferences: UserPreferences
    permissions: UserPermissions
    last_active: Optional[datetime] = Field(None, description="Last activity timestamp")
    created_at: datetime = Field(..., description="Profile creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    status: str = Field(default="active", description="Profile status (active, inactive, suspended)")


class UserProfilesResponse(BaseModel):
    """Response for getting all user profiles"""
    profiles: List[UserProfile]
    total_count: int
    current_user_id: Optional[str] = None


class SessionContext(BaseModel):
    """Session context information"""
    device_id: Optional[str] = None
    app_version: Optional[str] = None
    platform: Optional[str] = None


class UserSwitchRequest(BaseModel):
    """Request to switch active user"""
    user_id: str = Field(..., description="ID of user to switch to")
    session_context: Optional[SessionContext] = None


class UserSwitchResponse(BaseModel):
    """Response after successful user switch"""
    success: bool
    message: str
    active_user: UserProfile
    session_token: str
    expires_at: datetime


class CurrentUserResponse(BaseModel):
    """Response for current active user"""
    id: str
    name: str
    email: str
    role: str
    avatar_url: Optional[str]
    permissions: UserPermissions
    session_started_at: datetime
    last_activity: datetime


class UserDeleteRequest(BaseModel):
    """Request to delete/deactivate user"""
    reason: Optional[str] = None
    transfer_data_to: Optional[str] = None


class UserDeleteResponse(BaseModel):
    """Response after user deletion"""
    success: bool
    message: str
    user_id: str
    status: str
    deactivated_at: datetime


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: Dict[str, Any] = Field(..., description="Error details")


class ErrorDetail(BaseModel):
    """Error detail structure"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime