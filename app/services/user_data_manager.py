"""
In-memory user data manager for fast API responses.
Loads all user data (biomarkers, lifestyle, medical history) into memory.
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path


class UserDataManager:
    """Manages all user data in memory for fast API responses."""
    
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.data_dir = Path("datasets")
        self._load_all_users()
    
    def _load_all_users(self):
        """Load all user data into memory."""
        # Load hardcoded user
        self.users["hardcoded"] = self._create_hardcoded_user()
        
        # Load dataset users
        users_file = self.data_dir / "users" / "users.json"
        if users_file.exists():
            with open(users_file, 'r') as f:
                users_data = json.load(f)
                
            for user_data in users_data:
                user_id = user_data["user_id"]
                self.users[user_id] = {
                    "profile": user_data,
                    "biomarkers": self._load_biomarkers(user_id),
                    "lifestyle": self._load_lifestyle(user_id),
                    "medical_history": self._load_medical_history(user_id),
                    "interventions": self._load_interventions(user_id),
                    "ai_interactions": self._load_ai_interactions(user_id)
                }
    
    def _create_hardcoded_user(self) -> Dict[str, Any]:
        """Create hardcoded user data."""
        return {
            "profile": {
                "user_id": "hardcoded",
                "demographics": {
                    "age": 35,
                    "gender": "M",
                    "location": {"city": "Mumbai", "country": "India"}
                },
                "health_profile": {
                    "height_cm": 175,
                    "weight_kg": 75,
                    "bmi": 24.5,
                    "blood_type": "O+",
                    "biological_age": 32.0
                },
                "goals": [{
                    "goal_id": "hardcoded_goal_1",
                    "type": "fitness",
                    "target": "Improve cardiovascular health",
                    "status": "active"
                }],
                "preferences": {
                    "units": "metric",
                    "notifications": True,
                    "data_sharing": True
                },
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            },
            "biomarkers": self._get_hardcoded_biomarkers(),
            "lifestyle": self._get_hardcoded_lifestyle(),
            "medical_history": self._get_hardcoded_medical_history(),
            "interventions": [],
            "ai_interactions": []
        }
    
    def _load_biomarkers(self, user_id: str) -> Dict[str, Any]:
        """Load biomarker data for user."""
        file_path = self.data_dir / "biomarkers" / f"biomarkers_{user_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_lifestyle(self, user_id: str) -> Dict[str, Any]:
        """Load lifestyle data for user."""
        lifestyle_dir = self.data_dir / "lifestyle"
        if lifestyle_dir.exists():
            # Look for any lifestyle file for this user
            for file_path in lifestyle_dir.glob(f"lifestyle_{user_id}_*.json"):
                with open(file_path, 'r') as f:
                    return json.load(f)
        return {}
    
    def _load_medical_history(self, user_id: str) -> Dict[str, Any]:
        """Load medical history for user."""
        file_path = self.data_dir / "medical_history" / f"medical_history_{user_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_interventions(self, user_id: str) -> List[Dict[str, Any]]:
        """Load interventions for user."""
        file_path = self.data_dir / "interventions" / f"interventions_{user_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else [data]
        return []
    
    def _load_ai_interactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Load AI interactions for user."""
        ai_dir = self.data_dir / "ai_interactions"
        interactions = []
        if ai_dir.exists():
            for file_path in ai_dir.glob(f"interactions_{user_id}_*.json"):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    interactions.append(data)
        return interactions
    
    def _get_hardcoded_biomarkers(self) -> Dict[str, Any]:
        """Get hardcoded biomarker data."""
        return {
            "glucose_fasting": {"value": 88, "unit": "mg/dL", "normal_range": "70-100"},
            "hba1c": {"value": 5.4, "unit": "%", "normal_range": "<5.7"},
            "total_cholesterol": {"value": 180, "unit": "mg/dL", "normal_range": "<200"},
            "ldl": {"value": 110, "unit": "mg/dL", "normal_range": "<100"},
            "hdl": {"value": 45, "unit": "mg/dL", "normal_range": ">40"},
            "triglycerides": {"value": 125, "unit": "mg/dL", "normal_range": "<150"},
            "vitamin_d": {"value": 32, "unit": "ng/mL", "normal_range": ">30"},
            "vitamin_b12": {"value": 350, "unit": "pg/mL", "normal_range": "200-900"},
            "crp": {"value": 0.8, "unit": "mg/L", "normal_range": "<1.0"}
        }
    
    def _get_hardcoded_lifestyle(self) -> Dict[str, Any]:
        """Get hardcoded lifestyle data."""
        return {
            "sleep": {
                "average_hours": 7.5,
                "quality_score": 8,
                "bedtime": "22:30",
                "wake_time": "06:00"
            },
            "exercise": {
                "frequency_per_week": 5,
                "primary_activities": ["Running", "Weight Training"],
                "average_duration_minutes": 60
            },
            "nutrition": {
                "diet_type": "Balanced",
                "meals_per_day": 3,
                "water_intake_liters": 3.0,
                "alcohol_drinks_per_week": 2
            },
            "stress": {
                "level": 5,
                "work_hours_per_day": 8,
                "meditation_minutes_per_day": 15
            }
        }
    
    def _get_hardcoded_medical_history(self) -> Dict[str, Any]:
        """Get hardcoded medical history."""
        return {
            "conditions": [],
            "medications": [],
            "supplements": [
                {
                    "name": "Vitamin D3",
                    "dosage": "2000 IU",
                    "frequency": "daily",
                    "purpose": "Maintain optimal levels"
                },
                {
                    "name": "Omega-3",
                    "dosage": "1000 mg",
                    "frequency": "daily",
                    "purpose": "Cardiovascular health"
                }
            ],
            "family_history": [
                {
                    "condition": "Hypertension",
                    "relation": "Father",
                    "age_of_onset": 60
                }
            ]
        }
    
    # Public API methods
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get complete user data."""
        return self.users.get(user_id)
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile only."""
        user = self.users.get(user_id)
        return user["profile"] if user else None
    
    def get_user_biomarkers(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user biomarkers."""
        user = self.users.get(user_id)
        return user["biomarkers"] if user else None
    
    def get_user_lifestyle(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user lifestyle data."""
        user = self.users.get(user_id)
        return user["lifestyle"] if user else None
    
    def get_user_medical_history(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user medical history."""
        user = self.users.get(user_id)
        return user["medical_history"] if user else None
    
    def get_user_interventions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user interventions."""
        user = self.users.get(user_id)
        return user["interventions"] if user else []
    
    def get_user_ai_interactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user AI interactions."""
        user = self.users.get(user_id)
        return user["ai_interactions"] if user else []
    
    def get_all_user_ids(self) -> List[str]:
        """Get all available user IDs."""
        return list(self.users.keys())
    
    def user_exists(self, user_id: str) -> bool:
        """Check if user exists."""
        return user_id in self.users
    
    def get_user_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user summary for listing."""
        user = self.users.get(user_id)
        if not user:
            return None
        
        profile = user["profile"]
        return {
            "user_id": user_id,
            "display_name": f"{profile['demographics']['age']}{profile['demographics']['gender']} - {profile['demographics']['location']['city']}",
            "age": profile["demographics"]["age"],
            "gender": profile["demographics"]["gender"],
            "location": profile["demographics"]["location"]["city"],
            "has_biomarkers": bool(user["biomarkers"]),
            "has_lifestyle": bool(user["lifestyle"]),
            "has_medical_history": bool(user["medical_history"]),
            "data_completeness": self._calculate_completeness(user)
        }
    
    def _calculate_completeness(self, user: Dict[str, Any]) -> float:
        """Calculate data completeness percentage."""
        total_sections = 5
        completed_sections = 1  # Profile always exists
        
        if user["biomarkers"]:
            completed_sections += 1
        if user["lifestyle"]:
            completed_sections += 1
        if user["medical_history"]:
            completed_sections += 1
        if user["interventions"]:
            completed_sections += 1
        
        return (completed_sections / total_sections) * 100


# Global instance
user_data_manager = UserDataManager()
