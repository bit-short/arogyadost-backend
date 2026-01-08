"""
Persistent storage layer for digital twins with caching.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.models.digital_twin import DigitalTwin
from app.storage.database import DigitalTwinDatabase, UserNotFoundError, UserAlreadyExistsError
from app.config.database import db_config

logger = logging.getLogger(__name__)


class UserInfo:
    """Basic user information."""
    
    def __init__(self, user_id: str, display_name: str, created_at: datetime, updated_at: datetime):
        self.user_id = user_id
        self.display_name = display_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.data_completeness = 0.0  # Will be calculated when needed


class PersistentDigitalTwinStorage:
    """Persistent storage for digital twins with in-memory caching."""
    
    def __init__(self, database: Optional[DigitalTwinDatabase] = None):
        self.database = database or DigitalTwinDatabase(db_config.database_path)
        self._cache: Dict[str, DigitalTwin] = {}
        self._cache_enabled = db_config.enable_cache
        self._max_cache_size = db_config.cache_size
        logger.info(f"Initialized persistent storage with cache {'enabled' if self._cache_enabled else 'disabled'}")
    
    def get_digital_twin(self, user_id: str) -> Optional[DigitalTwin]:
        """Get a digital twin by user ID, using cache if available."""
        if not user_id:
            return None
        
        # Try cache first
        if self._cache_enabled and user_id in self._cache:
            logger.debug(f"Cache hit for user '{user_id}'")
            return self._cache[user_id]
        
        # Load from database
        try:
            digital_twin = self.database.get_digital_twin(user_id)
            if digital_twin and self._cache_enabled:
                self._save_to_cache(user_id, digital_twin)
            return digital_twin
        except Exception as e:
            logger.error(f"Failed to get digital twin for user '{user_id}': {e}")
            return None
    
    def save_digital_twin(self, user_id: str, digital_twin: DigitalTwin) -> None:
        """Save a digital twin to persistent storage and update cache."""
        if not user_id or not digital_twin:
            raise ValueError("User ID and digital twin are required")
        
        try:
            # Update the digital twin's timestamp
            digital_twin.updated_at = datetime.now()
            
            # Save to database
            self.database.save_digital_twin(user_id, digital_twin)
            
            # Update cache
            if self._cache_enabled:
                self._save_to_cache(user_id, digital_twin)
            
            logger.debug(f"Saved digital twin for user '{user_id}'")
            
        except Exception as e:
            logger.error(f"Failed to save digital twin for user '{user_id}': {e}")
            raise
    
    def create_user_digital_twin(self, user_id: str, display_name: str) -> DigitalTwin:
        """Create a new user with an empty digital twin."""
        if not db_config.validate_user_id(user_id):
            raise ValueError(f"Invalid user ID format: '{user_id}'")
        
        if not display_name or not display_name.strip():
            raise ValueError("Display name cannot be empty")
        
        try:
            # Create user in database
            digital_twin = self.database.create_user(user_id, display_name.strip())
            
            # Add to cache
            if self._cache_enabled:
                self._save_to_cache(user_id, digital_twin)
            
            logger.info(f"Created new user '{user_id}' with display name '{display_name}'")
            return digital_twin
            
        except UserAlreadyExistsError:
            raise
        except Exception as e:
            logger.error(f"Failed to create user '{user_id}': {e}")
            raise
    
    def list_all_users(self) -> List[UserInfo]:
        """List all users with their basic information."""
        try:
            users_data = self.database.list_users()
            users = []
            
            for user_data in users_data:
                user_info = UserInfo(
                    user_id=user_data['user_id'],
                    display_name=user_data['display_name'],
                    created_at=datetime.fromisoformat(user_data['created_at']),
                    updated_at=datetime.fromisoformat(user_data['updated_at'])
                )
                
                # Calculate data completeness if digital twin is available
                digital_twin = self.get_digital_twin(user_info.user_id)
                if digital_twin:
                    user_info.data_completeness = digital_twin.get_overall_completeness()
                
                users.append(user_info)
            
            return users
            
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user and their digital twin."""
        if not user_id:
            return False
        
        try:
            # Remove from cache
            if self._cache_enabled and user_id in self._cache:
                del self._cache[user_id]
            
            # Delete from database
            deleted = self.database.delete_user(user_id)
            
            if deleted:
                logger.info(f"Deleted user '{user_id}'")
            
            return deleted
            
        except Exception as e:
            logger.error(f"Failed to delete user '{user_id}': {e}")
            return False
    
    def user_exists(self, user_id: str) -> bool:
        """Check if a user exists."""
        return self.get_digital_twin(user_id) is not None
    
    def _save_to_cache(self, user_id: str, digital_twin: DigitalTwin) -> None:
        """Save digital twin to cache with size management."""
        if not self._cache_enabled:
            return
        
        # Manage cache size (simple LRU-like behavior)
        if len(self._cache) >= self._max_cache_size and user_id not in self._cache:
            # Remove oldest entry (first in dict)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.debug(f"Evicted '{oldest_key}' from cache")
        
        self._cache[user_id] = digital_twin
        logger.debug(f"Cached digital twin for user '{user_id}'")
    
    def clear_cache(self) -> None:
        """Clear the in-memory cache."""
        if self._cache_enabled:
            self._cache.clear()
            logger.info("Cleared digital twin cache")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'enabled': self._cache_enabled,
            'size': len(self._cache),
            'max_size': self._max_cache_size,
            'cached_users': list(self._cache.keys()) if self._cache_enabled else []
        }


# Global instance for the application
persistent_storage = PersistentDigitalTwinStorage()