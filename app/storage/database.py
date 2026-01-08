"""
Database layer for Digital Brain Integration.
Provides SQLite-based persistent storage for digital twin data.
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

from app.models.digital_twin import DigitalTwin

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base exception for database operations."""
    pass


class UserNotFoundError(DatabaseError):
    """Raised when a user is not found in the database."""
    pass


class UserAlreadyExistsError(DatabaseError):
    """Raised when trying to create a user that already exists."""
    pass


class DigitalTwinSerializationError(DatabaseError):
    """Raised when digital twin serialization/deserialization fails."""
    pass


class DigitalTwinDatabase:
    """SQLite database manager for digital twin data."""
    
    def __init__(self, db_path: str = "digital_twins.db"):
        self.db_path = Path(db_path)
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS digital_twins (
                        user_id TEXT PRIMARY KEY,
                        display_name TEXT NOT NULL,
                        digital_twin_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create index for better query performance
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_digital_twins_updated_at 
                    ON digital_twins(updated_at)
                """)
                
                conn.commit()
                logger.info(f"Database initialized at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseError(f"Database initialization failed: {e}")
    
    @contextmanager
    def _get_connection(self):
        """Get a database connection with proper error handling."""
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database operation failed: {e}")
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()
    
    def create_user(self, user_id: str, display_name: str) -> DigitalTwin:
        """Create a new user with an empty digital twin."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        
        if not display_name or not display_name.strip():
            raise ValueError("Display name cannot be empty")
        
        # Create empty digital twin
        digital_twin = DigitalTwin(user_id=user_id)
        
        try:
            digital_twin_json = self._serialize_digital_twin(digital_twin)
            
            with self._get_connection() as conn:
                # Check if user already exists
                cursor = conn.execute(
                    "SELECT user_id FROM digital_twins WHERE user_id = ?",
                    (user_id,)
                )
                if cursor.fetchone():
                    raise UserAlreadyExistsError(f"User '{user_id}' already exists")
                
                # Insert new user
                conn.execute("""
                    INSERT INTO digital_twins (user_id, display_name, digital_twin_data)
                    VALUES (?, ?, ?)
                """, (user_id, display_name, digital_twin_json))
                
                conn.commit()
                logger.info(f"Created user '{user_id}' with display name '{display_name}'")
                return digital_twin
                
        except sqlite3.IntegrityError:
            raise UserAlreadyExistsError(f"User '{user_id}' already exists")
        except Exception as e:
            logger.error(f"Failed to create user '{user_id}': {e}")
            raise DatabaseError(f"Failed to create user: {e}")
    
    def get_digital_twin(self, user_id: str) -> Optional[DigitalTwin]:
        """Retrieve a digital twin by user ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT digital_twin_data FROM digital_twins WHERE user_id = ?",
                    (user_id,)
                )
                row = cursor.fetchone()
                
                if not row:
                    return None
                
                return self._deserialize_digital_twin(row['digital_twin_data'])
                
        except Exception as e:
            logger.error(f"Failed to get digital twin for user '{user_id}': {e}")
            raise DatabaseError(f"Failed to retrieve digital twin: {e}")
    
    def save_digital_twin(self, user_id: str, digital_twin: DigitalTwin) -> None:
        """Save a digital twin to the database."""
        try:
            digital_twin_json = self._serialize_digital_twin(digital_twin)
            
            with self._get_connection() as conn:
                # Check if user exists
                cursor = conn.execute(
                    "SELECT user_id FROM digital_twins WHERE user_id = ?",
                    (user_id,)
                )
                if not cursor.fetchone():
                    raise UserNotFoundError(f"User '{user_id}' not found")
                
                # Update digital twin data and timestamp
                conn.execute("""
                    UPDATE digital_twins 
                    SET digital_twin_data = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (digital_twin_json, user_id))
                
                conn.commit()
                logger.debug(f"Saved digital twin for user '{user_id}'")
                
        except UserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to save digital twin for user '{user_id}': {e}")
            raise DatabaseError(f"Failed to save digital twin: {e}")
    
    def list_users(self) -> List[Dict[str, Any]]:
        """List all users with their basic information."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT user_id, display_name, created_at, updated_at
                    FROM digital_twins
                    ORDER BY created_at DESC
                """)
                
                users = []
                for row in cursor.fetchall():
                    users.append({
                        'user_id': row['user_id'],
                        'display_name': row['display_name'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    })
                
                return users
                
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            raise DatabaseError(f"Failed to list users: {e}")
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user and their digital twin."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM digital_twins WHERE user_id = ?",
                    (user_id,)
                )
                
                deleted = cursor.rowcount > 0
                conn.commit()
                
                if deleted:
                    logger.info(f"Deleted user '{user_id}'")
                else:
                    logger.warning(f"User '{user_id}' not found for deletion")
                
                return deleted
                
        except Exception as e:
            logger.error(f"Failed to delete user '{user_id}': {e}")
            raise DatabaseError(f"Failed to delete user: {e}")
    
    def _serialize_digital_twin(self, digital_twin: DigitalTwin) -> str:
        """Serialize a digital twin to JSON string."""
        try:
            # Convert digital twin to dictionary
            data = {
                'user_id': digital_twin.user_id,
                'created_at': digital_twin.created_at.isoformat(),
                'updated_at': digital_twin.updated_at.isoformat(),
                'metadata': digital_twin.metadata,
                'domains': {}
            }
            
            # Serialize each domain
            for domain_name, domain in digital_twin.domains.items():
                domain_data = {
                    'domain_name': domain.domain_name,
                    'fields': {}
                }
                
                # Serialize each field in the domain
                for field_name, field in domain.fields.items():
                    field_data = {
                        'field_name': field.field_name,
                        'field_type': field.field_type,
                        'state': field.state.value,
                        'values': []
                    }
                    
                    # Serialize each data point
                    for data_point in field.values:
                        point_data = {
                            'value': data_point.value,
                            'timestamp': data_point.timestamp.isoformat(),
                            'unit': data_point.unit,
                            'metadata': data_point.metadata
                        }
                        field_data['values'].append(point_data)
                    
                    domain_data['fields'][field_name] = field_data
                
                data['domains'][domain_name] = domain_data
            
            return json.dumps(data, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Failed to serialize digital twin: {e}")
            raise DigitalTwinSerializationError(f"Serialization failed: {e}")
    
    def _deserialize_digital_twin(self, json_data: str) -> DigitalTwin:
        """Deserialize a digital twin from JSON string."""
        try:
            data = json.loads(json_data)
            
            # Create digital twin with metadata
            digital_twin = DigitalTwin(
                user_id=data['user_id'],
                metadata=data.get('metadata', {})
            )
            
            # Set timestamps
            digital_twin.created_at = datetime.fromisoformat(data['created_at'])
            digital_twin.updated_at = datetime.fromisoformat(data['updated_at'])
            
            # Deserialize domains
            for domain_name, domain_data in data.get('domains', {}).items():
                # Import here to avoid circular imports
                from app.models.digital_twin import HealthDomain, HealthField, HealthDataPoint, FieldState
                
                domain = HealthDomain(domain_name=domain_data['domain_name'])
                
                # Deserialize fields
                for field_name, field_data in domain_data.get('fields', {}).items():
                    field = HealthField(
                        field_name=field_data['field_name'],
                        field_type=field_data['field_type'],
                        state=FieldState(field_data['state'])
                    )
                    
                    # Deserialize data points
                    for point_data in field_data.get('values', []):
                        data_point = HealthDataPoint(
                            value=point_data['value'],
                            timestamp=datetime.fromisoformat(point_data['timestamp']),
                            unit=point_data.get('unit'),
                            metadata=point_data.get('metadata', {})
                        )
                        field.values.append(data_point)
                    
                    domain.fields[field_name] = field
                
                digital_twin.domains[domain_name] = domain
            
            return digital_twin
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON data: {e}")
            raise DigitalTwinSerializationError(f"Invalid JSON: {e}")
        except KeyError as e:
            logger.error(f"Missing required field in JSON: {e}")
            raise DigitalTwinSerializationError(f"Missing field: {e}")
        except Exception as e:
            logger.error(f"Failed to deserialize digital twin: {e}")
            raise DigitalTwinSerializationError(f"Deserialization failed: {e}")