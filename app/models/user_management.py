"""
Pydantic models for user management API.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class CreateUserRequest(BaseModel):
    """Request model for creating a new user."""
    user_id: str = Field(..., min_length=3, max_length=50, description="Unique user identifier")
    display_name: str = Field(..., min_length=1, max_length=100, description="User display name")
    
    @validator('user_id')
    def validate_user_id(cls, v):
        """Validate user ID format."""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('User ID must contain only alphanumeric characters, underscores, and hyphens')
        return v.strip()
    
    @validator('display_name')
    def validate_display_name(cls, v):
        """Validate display name."""
        return v.strip()


class UserInfoResponse(BaseModel):
    """Response model for user information."""
    user_id: str
    display_name: str
    created_at: datetime
    updated_at: datetime
    data_completeness: float = Field(ge=0, le=100, description="Data completeness percentage")


class CreateUserResponse(BaseModel):
    """Response model for user creation."""
    user_info: UserInfoResponse
    digital_twin_created: bool = True
    message: str = "User created successfully"


class ListUsersResponse(BaseModel):
    """Response model for listing users."""
    users: List[UserInfoResponse]
    total_count: int
    message: str = "Users retrieved successfully"


class SelectUserRequest(BaseModel):
    """Request model for selecting an active user."""
    user_id: str = Field(..., min_length=1, description="User ID to select")


class SelectUserResponse(BaseModel):
    """Response model for user selection."""
    selected_user: UserInfoResponse
    digital_twin_loaded: bool = True
    message: str = "User selected successfully"


class DeleteUserResponse(BaseModel):
    """Response model for user deletion."""
    deleted: bool
    user_id: str
    message: str


class UpdateUserDisplayNameRequest(BaseModel):
    """Request model for updating user display name."""
    display_name: str = Field(..., min_length=1, max_length=100, description="New display name")
    
    @validator('display_name')
    def validate_display_name(cls, v):
        """Validate display name."""
        return v.strip()


class UpdateUserDisplayNameResponse(BaseModel):
    """Response model for updating user display name."""
    updated: bool
    user_id: str
    new_display_name: str
    message: str


class UserStatsResponse(BaseModel):
    """Response model for user statistics."""
    total_users: int
    average_completeness: float
    completeness_distribution: Dict[str, int]
    storage_stats: Dict[str, Any]
    message: str = "User statistics retrieved successfully"


class ErrorResponse(BaseModel):
    """Standard error response model."""
    status: str = "error"
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None