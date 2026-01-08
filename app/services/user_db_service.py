"""
Database service for querying user health data.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.db_models import User, Biomarker, MedicalHistory, Goal


class UserDBService:
    """Service for database operations on user data."""
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        users = self.db.query(User).all()
        return [self._user_to_dict(u) for u in users]
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        user = self.db.query(User).filter(User.id == user_id).first()
        return self._user_to_dict(user) if user else None
    
    def get_user_biomarkers(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all biomarkers for a user."""
        biomarkers = self.db.query(Biomarker).filter(Biomarker.user_id == user_id).all()
        return [self._biomarker_to_dict(b) for b in biomarkers]
    
    def get_user_biomarkers_by_category(self, user_id: str) -> Dict[str, List[Dict]]:
        """Get biomarkers grouped by category."""
        biomarkers = self.db.query(Biomarker).filter(Biomarker.user_id == user_id).all()
        result = {}
        for b in biomarkers:
            cat = b.category or 'other'
            if cat not in result:
                result[cat] = []
            result[cat].append(self._biomarker_to_dict(b))
        return result
    
    def get_user_medical_history(self, user_id: str) -> Dict[str, List[Dict]]:
        """Get medical history grouped by type."""
        entries = self.db.query(MedicalHistory).filter(MedicalHistory.user_id == user_id).all()
        result = {'conditions': [], 'supplements': [], 'medications': [], 'family_history': []}
        for e in entries:
            if e.type in result:
                result[e.type].append(self._medical_to_dict(e))
        return result
    
    def get_user_goals(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user goals."""
        goals = self.db.query(Goal).filter(Goal.user_id == user_id).all()
        return [self._goal_to_dict(g) for g in goals]
    
    def get_user_full_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get complete user data."""
        user = self.get_user(user_id)
        if not user:
            return None
        
        return {
            'profile': user,
            'biomarkers': self.get_user_biomarkers_by_category(user_id),
            'medical_history': self.get_user_medical_history(user_id),
            'goals': self.get_user_goals(user_id)
        }
    
    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        return {
            'user_id': user.id,
            'age': user.age,
            'gender': user.gender,
            'city': user.city,
            'country': user.country,
            'height_cm': user.height_cm,
            'weight_kg': user.weight_kg,
            'bmi': user.bmi,
            'blood_type': user.blood_type,
            'biological_age': user.biological_age,
            'data_source': user.data_source
        }
    
    def _biomarker_to_dict(self, b: Biomarker) -> Dict[str, Any]:
        return {
            'name': b.name,
            'value': b.value,
            'unit': b.unit,
            'normal_range': b.normal_range,
            'status': b.status,
            'category': b.category
        }
    
    def _medical_to_dict(self, m: MedicalHistory) -> Dict[str, Any]:
        return {
            'name': m.name,
            'type': m.type,
            'details': m.details,
            'start_date': m.start_date.isoformat() if m.start_date else None
        }
    
    def _goal_to_dict(self, g: Goal) -> Dict[str, Any]:
        return {
            'goal_id': g.id,
            'type': g.type,
            'target': g.target,
            'status': g.status
        }
    
    def close(self):
        self.db.close()


# Global instance
user_db_service = UserDBService()
