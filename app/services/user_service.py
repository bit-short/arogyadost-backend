"""
User management service for Digital Brain Integration.
"""

import logging
from typing import List, Optional
from datetime import datetime

from app.storage.persistent_storage import persistent_storage, UserInfo
from app.storage.database import UserAlreadyExistsError, UserNotFoundError
from app.config.database import db_config

logger = logging.getLogger(__name__)


class UserService:
    """Service for managing users and their digital twins."""
    
    def __init__(self):
        self.storage = persistent_storage
        logger.info("Initialized user service")
    
    def create_user(self, user_id: str, display_name: str) -> UserInfo:
        """Create a new user with digital twin."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        
        if not display_name or not display_name.strip():
            raise ValueError("Display name cannot be empty")
        
        # Validate user ID format
        if not db_config.validate_user_id(user_id):
            raise ValueError(f"Invalid user ID format: '{user_id}'. Must be 3-{db_config.max_user_id_length} characters, alphanumeric and underscore only")
        
        try:
            # Create user with digital twin
            digital_twin = self.storage.create_user_digital_twin(user_id.strip(), display_name.strip())
            
            # Return user info
            user_info = UserInfo(
                user_id=user_id.strip(),
                display_name=display_name.strip(),
                created_at=digital_twin.created_at,
                updated_at=digital_twin.updated_at
            )
            user_info.data_completeness = digital_twin.get_overall_completeness()
            
            logger.info(f"Created user '{user_id}' successfully")
            return user_info
            
        except UserAlreadyExistsError:
            logger.warning(f"Attempted to create existing user '{user_id}'")
            raise ValueError(f"User '{user_id}' already exists")
        except Exception as e:
            logger.error(f"Failed to create user '{user_id}': {e}")
            raise RuntimeError(f"Failed to create user: {str(e)}")
    
    def get_user_info(self, user_id: str) -> Optional[UserInfo]:
        """Get user information by ID."""
        if not user_id:
            return None
        
        try:
            digital_twin = self.storage.get_digital_twin(user_id)
            if not digital_twin:
                return None
            
            # Get user info from database
            users = self.storage.list_all_users()
            for user_info in users:
                if user_info.user_id == user_id:
                    user_info.data_completeness = digital_twin.get_overall_completeness()
                    return user_info
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user info for '{user_id}': {e}")
            return None
    
    def list_users(self) -> List[UserInfo]:
        """List all users with their information."""
        try:
            users = self.storage.list_all_users()
            logger.debug(f"Listed {len(users)} users")
            return users
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user and their digital twin."""
        if not user_id:
            return False
        
        try:
            deleted = self.storage.delete_user(user_id)
            if deleted:
                logger.info(f"Deleted user '{user_id}' successfully")
            else:
                logger.warning(f"User '{user_id}' not found for deletion")
            return deleted
        except Exception as e:
            logger.error(f"Failed to delete user '{user_id}': {e}")
            return False
    
    def user_exists(self, user_id: str) -> bool:
        """Check if a user exists."""
        if not user_id:
            return False
        
        try:
            return self.storage.user_exists(user_id)
        except Exception as e:
            logger.error(f"Failed to check if user '{user_id}' exists: {e}")
            return False
    
    def update_user_display_name(self, user_id: str, new_display_name: str) -> bool:
        """Update a user's display name."""
        if not user_id or not new_display_name or not new_display_name.strip():
            return False
        
        try:
            # Get the digital twin
            digital_twin = self.storage.get_digital_twin(user_id)
            if not digital_twin:
                return False
            
            # Update metadata with new display name
            digital_twin.metadata['display_name'] = new_display_name.strip()
            
            # Save the updated digital twin
            self.storage.save_digital_twin(user_id, digital_twin)
            
            logger.info(f"Updated display name for user '{user_id}' to '{new_display_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update display name for user '{user_id}': {e}")
            return False
    
    def get_user_stats(self) -> dict:
        """Get statistics about users."""
        try:
            users = self.list_users()
            total_users = len(users)
            
            # Calculate completeness statistics
            completeness_scores = [user.data_completeness for user in users]
            avg_completeness = sum(completeness_scores) / total_users if total_users > 0 else 0
            
            # Count users by completeness ranges
            high_completeness = sum(1 for score in completeness_scores if score >= 75)
            medium_completeness = sum(1 for score in completeness_scores if 25 <= score < 75)
            low_completeness = sum(1 for score in completeness_scores if score < 25)
            
            return {
                'total_users': total_users,
                'average_completeness': round(avg_completeness, 2),
                'completeness_distribution': {
                    'high': high_completeness,
                    'medium': medium_completeness,
                    'low': low_completeness
                },
                'storage_stats': self.storage.get_cache_stats()
            }
        except Exception as e:
            logger.error(f"Failed to get user stats: {e}")
            return {
                'total_users': 0,
                'average_completeness': 0,
                'completeness_distribution': {'high': 0, 'medium': 0, 'low': 0},
                'storage_stats': {}
            }


# Global service instance
user_service = UserService()