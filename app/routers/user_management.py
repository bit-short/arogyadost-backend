"""
User management API router for Digital Brain Integration.
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.user_management import (
    CreateUserRequest, CreateUserResponse, UserInfoResponse,
    ListUsersResponse, SelectUserRequest, SelectUserResponse,
    DeleteUserResponse, UpdateUserDisplayNameRequest, UpdateUserDisplayNameResponse,
    UserStatsResponse, ErrorResponse
)
from app.services.user_service import user_service
from app.services.user_context import user_context_manager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["User Management"])


@router.post("/", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest):
    """Create a new user with digital twin."""
    try:
        # Check if user already exists
        if user_service.user_exists(request.user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User '{request.user_id}' already exists"
            )
        
        # Create user
        user_info = user_service.create_user(request.user_id, request.display_name)
        
        # Refresh user context manager to include new user
        user_context_manager.refresh_persistent_users()
        
        # Convert to response model
        user_info_response = UserInfoResponse(
            user_id=user_info.user_id,
            display_name=user_info.display_name,
            created_at=user_info.created_at,
            updated_at=user_info.updated_at,
            data_completeness=user_info.data_completeness
        )
        
        logger.info(f"Created user '{request.user_id}' via API")
        return CreateUserResponse(
            user_info=user_info_response,
            digital_twin_created=True,
            message=f"User '{request.user_id}' created successfully"
        )
        
    except ValueError as e:
        logger.warning(f"Invalid user creation request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create user '{request.user_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/", response_model=ListUsersResponse)
async def list_users():
    """List all users with their basic information."""
    try:
        # Get users from service
        users = user_service.list_users()
        
        # Convert to response models
        user_responses = []
        for user_info in users:
            user_responses.append(UserInfoResponse(
                user_id=user_info.user_id,
                display_name=user_info.display_name,
                created_at=user_info.created_at,
                updated_at=user_info.updated_at,
                data_completeness=user_info.data_completeness
            ))
        
        logger.debug(f"Listed {len(users)} users via API")
        return ListUsersResponse(
            users=user_responses,
            total_count=len(users),
            message=f"Retrieved {len(users)} users successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to list users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.put("/select", response_model=SelectUserResponse)
async def select_user(request: SelectUserRequest):
    """Select/switch the active user."""
    try:
        # Check if user exists (including hardcoded and dataset users)
        user_profile = user_context_manager.get_user_by_id(request.user_id)
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{request.user_id}' not found"
            )
        
        # Select the user
        selected_profile = user_context_manager.select_user(request.user_id)
        
        # Convert to response model
        user_info_response = UserInfoResponse(
            user_id=selected_profile.user_id,
            display_name=selected_profile.display_name,
            created_at=selected_profile.created_at or selected_profile.last_active,
            updated_at=selected_profile.last_active or selected_profile.created_at,
            data_completeness=selected_profile.data_availability.completeness_score
        )
        
        logger.info(f"Selected user '{request.user_id}' via API")
        return SelectUserResponse(
            selected_user=user_info_response,
            digital_twin_loaded=True,
            message=f"User '{request.user_id}' selected successfully"
        )
        
    except ValueError as e:
        logger.warning(f"Invalid user selection: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to select user '{request.user_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to select user"
        )


@router.get("/{user_id}", response_model=UserInfoResponse)
async def get_user(user_id: str):
    """Get user information by ID."""
    try:
        user_info = user_service.get_user_info(user_id)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{user_id}' not found"
            )
        
        user_response = UserInfoResponse(
            user_id=user_info.user_id,
            display_name=user_info.display_name,
            created_at=user_info.created_at,
            updated_at=user_info.updated_at,
            data_completeness=user_info.data_completeness
        )
        
        logger.debug(f"Retrieved user '{user_id}' via API")
        return user_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user '{user_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: str):
    """Delete a user and their digital twin."""
    try:
        # Check if user exists
        if not user_service.user_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{user_id}' not found"
            )
        
        # Don't allow deletion of hardcoded user
        if user_id == "hardcoded":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete hardcoded user"
            )
        
        # Delete user
        deleted = user_service.delete_user(user_id)
        
        if deleted:
            # Refresh user context manager
            user_context_manager.refresh_persistent_users()
            
            # If the deleted user was active, switch to hardcoded user
            if user_context_manager.active_user_id == user_id:
                user_context_manager.select_user("hardcoded")
            
            logger.info(f"Deleted user '{user_id}' via API")
            return DeleteUserResponse(
                deleted=True,
                user_id=user_id,
                message=f"User '{user_id}' deleted successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete user '{user_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.put("/{user_id}/display-name", response_model=UpdateUserDisplayNameResponse)
async def update_user_display_name(user_id: str, request: UpdateUserDisplayNameRequest):
    """Update a user's display name."""
    try:
        # Check if user exists
        if not user_service.user_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{user_id}' not found"
            )
        
        # Update display name
        updated = user_service.update_user_display_name(user_id, request.display_name)
        
        if updated:
            # Refresh user context manager
            user_context_manager.refresh_persistent_users()
            
            logger.info(f"Updated display name for user '{user_id}' via API")
            return UpdateUserDisplayNameResponse(
                updated=True,
                user_id=user_id,
                new_display_name=request.display_name,
                message=f"Display name updated successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update display name"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update display name for user '{user_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update display name"
        )


@router.get("/stats/overview", response_model=UserStatsResponse)
async def get_user_stats():
    """Get user statistics and overview."""
    try:
        stats = user_service.get_user_stats()
        
        return UserStatsResponse(
            total_users=stats['total_users'],
            average_completeness=stats['average_completeness'],
            completeness_distribution=stats['completeness_distribution'],
            storage_stats=stats['storage_stats'],
            message="User statistics retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get user stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user statistics"
        )


# Health check endpoint for user management
@router.get("/health", include_in_schema=False)
async def user_management_health():
    """Health check for user management service."""
    try:
        # Test basic functionality
        users_count = len(user_service.list_users())
        
        return {
            "status": "healthy",
            "service": "user_management",
            "users_count": users_count,
            "timestamp": "2025-01-08T10:30:00Z"
        }
    except Exception as e:
        logger.error(f"User management health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "user_management",
                "error": str(e),
                "timestamp": "2025-01-08T10:30:00Z"
            }
        )