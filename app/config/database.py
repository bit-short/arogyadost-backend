"""
Database configuration for Digital Brain Integration.
"""

import os
from pathlib import Path
from typing import Optional


class DatabaseConfig:
    """Configuration settings for the digital twin database."""
    
    def __init__(self):
        self.database_path: str = os.getenv("DIGITAL_BRAIN_DB_PATH", "digital_twins.db")
        self.cache_size: int = int(os.getenv("DIGITAL_BRAIN_CACHE_SIZE", "100"))
        self.enable_cache: bool = os.getenv("DIGITAL_BRAIN_ENABLE_CACHE", "true").lower() == "true"
        self.backup_interval_hours: int = int(os.getenv("DIGITAL_BRAIN_BACKUP_INTERVAL", "24"))
        self.max_user_id_length: int = int(os.getenv("DIGITAL_BRAIN_MAX_USER_ID_LENGTH", "50"))
        self.connection_timeout: int = int(os.getenv("DIGITAL_BRAIN_CONNECTION_TIMEOUT", "30"))
    
    @property
    def database_file_path(self) -> Path:
        """Get the full path to the database file."""
        return Path(self.database_path).resolve()
    
    def validate_user_id(self, user_id: str) -> bool:
        """Validate user ID format and constraints."""
        if not user_id or not isinstance(user_id, str):
            return False
        
        # Check length
        if len(user_id) < 3 or len(user_id) > self.max_user_id_length:
            return False
        
        # Check format: alphanumeric and underscore only
        if not user_id.replace('_', '').replace('-', '').isalnum():
            return False
        
        # Prevent SQL injection patterns
        dangerous_patterns = ['--', ';', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE']
        user_id_upper = user_id.upper()
        for pattern in dangerous_patterns:
            if pattern in user_id_upper:
                return False
        
        return True


# Global configuration instance
db_config = DatabaseConfig()