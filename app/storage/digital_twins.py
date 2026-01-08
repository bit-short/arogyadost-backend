from typing import Dict, Optional
from app.models.digital_twin import DigitalTwin
from app.storage.persistent_storage import persistent_storage
import logging

logger = logging.getLogger(__name__)

# Legacy in-memory storage for backward compatibility
_legacy_digital_twins: Dict[str, DigitalTwin] = {}

# Enhanced storage interface that uses persistent storage
class DigitalTwinStorage:
    """Enhanced digital twin storage that uses persistent backend with fallback."""
    
    def __init__(self):
        self._use_persistent = True
        logger.info("Initialized enhanced digital twin storage")
    
    def get(self, user_id: str) -> Optional[DigitalTwin]:
        """Get a digital twin by user ID."""
        if self._use_persistent:
            try:
                return persistent_storage.get_digital_twin(user_id)
            except Exception as e:
                logger.error(f"Persistent storage failed, falling back to in-memory: {e}")
                self._use_persistent = False
        
        # Fallback to in-memory storage
        return _legacy_digital_twins.get(user_id)
    
    def set(self, user_id: str, digital_twin: DigitalTwin) -> None:
        """Save a digital twin."""
        if self._use_persistent:
            try:
                # For new users, create them first
                if not persistent_storage.user_exists(user_id):
                    # Use user_id as display name if not specified
                    display_name = f"User {user_id}"
                    persistent_storage.create_user_digital_twin(user_id, display_name)
                
                persistent_storage.save_digital_twin(user_id, digital_twin)
                return
            except Exception as e:
                logger.error(f"Persistent storage failed, falling back to in-memory: {e}")
                self._use_persistent = False
        
        # Fallback to in-memory storage
        _legacy_digital_twins[user_id] = digital_twin
    
    def delete(self, user_id: str) -> bool:
        """Delete a digital twin."""
        if self._use_persistent:
            try:
                return persistent_storage.delete_user(user_id)
            except Exception as e:
                logger.error(f"Persistent storage failed, falling back to in-memory: {e}")
                self._use_persistent = False
        
        # Fallback to in-memory storage
        if user_id in _legacy_digital_twins:
            del _legacy_digital_twins[user_id]
            return True
        return False
    
    def exists(self, user_id: str) -> bool:
        """Check if a digital twin exists."""
        if self._use_persistent:
            try:
                return persistent_storage.user_exists(user_id)
            except Exception as e:
                logger.error(f"Persistent storage failed, falling back to in-memory: {e}")
                self._use_persistent = False
        
        # Fallback to in-memory storage
        return user_id in _legacy_digital_twins
    
    def list_users(self) -> list:
        """List all users."""
        if self._use_persistent:
            try:
                return persistent_storage.list_all_users()
            except Exception as e:
                logger.error(f"Persistent storage failed, falling back to in-memory: {e}")
                self._use_persistent = False
        
        # Fallback to in-memory storage
        return [{'user_id': user_id, 'display_name': f"User {user_id}"} 
                for user_id in _legacy_digital_twins.keys()]

# Global storage instance
digital_twin_storage = DigitalTwinStorage()

# Maintain backward compatibility with the old interface
digital_twins = _legacy_digital_twins
