import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from app.models.user_profile import UserProfile, Demographics, HealthProfile, HealthGoal, DataAvailability


class UserContextManager:
    """Manages user selection and context for testing and development."""
    
    def __init__(self, datasets_dir: str = "datasets"):
        self.datasets_dir = Path(datasets_dir)
        self.active_user_id: str = "hardcoded"  # Default to hardcoded user
        self.users_cache: Dict[str, UserProfile] = {}
        self._load_all_users()
    
    def _load_all_users(self) -> None:
        """Load all available users including hardcoded and dataset users."""
        # Load hardcoded user
        self.users_cache["hardcoded"] = self._create_hardcoded_user()
        
        # Load dataset users
        users_file = self.datasets_dir / "users" / "users.json"
        if users_file.exists():
            try:
                with open(users_file, 'r') as f:
                    users_data = json.load(f)
                
                for user_data in users_data:
                    user_profile = self._create_user_profile_from_data(user_data)
                    self.users_cache[user_profile.user_id] = user_profile
            except Exception as e:
                print(f"Error loading users from dataset: {e}")
    
    def _create_hardcoded_user(self) -> UserProfile:
        """Create user profile for the hardcoded mock data."""
        return UserProfile(
            user_id="hardcoded",
            display_name="Default (Hardcoded)",
            is_hardcoded=True,
            demographics=Demographics(
                age=35,
                gender="M",
                location={"city": "Mumbai", "country": "India"}
            ),
            health_profile=HealthProfile(
                height_cm=175,
                weight_kg=75,
                bmi=24.5,
                blood_type="O+",
                biological_age=32.0
            ),
            goals=[
                HealthGoal(
                    goal_id="hardcoded_goal_1",
                    type="fitness",
                    target="Improve cardiovascular health",
                    status="active"
                )
            ],
            data_availability=DataAvailability(
                biomarkers=True,
                medical_history=True,
                lifestyle=True,
                ai_interactions=False,
                interventions=False,
                completeness_score=85.0
            ),
            created_at=datetime.now(),
            last_active=datetime.now()
        )
    
    def _create_user_profile_from_data(self, user_data: Dict) -> UserProfile:
        """Create user profile from dataset JSON data."""
        user_id = user_data["user_id"]
        
        # Extract demographics
        demographics_data = user_data.get("demographics", {})
        demographics = Demographics(
            age=demographics_data.get("age", 30),
            gender=demographics_data.get("gender", "Unknown"),
            location=demographics_data.get("location", {})
        )
        
        # Extract health profile
        health_data = user_data.get("health_profile", {})
        health_profile = HealthProfile(
            height_cm=health_data.get("height_cm"),
            weight_kg=health_data.get("weight_kg"),
            bmi=health_data.get("bmi"),
            blood_type=health_data.get("blood_type"),
            biological_age=health_data.get("biological_age")
        )
        
        # Extract goals
        goals_data = user_data.get("goals", [])
        goals = []
        for goal_data in goals_data:
            goal = HealthGoal(
                goal_id=goal_data.get("goal_id", ""),
                type=goal_data.get("type", ""),
                target=goal_data.get("target", ""),
                start_date=datetime.fromisoformat(goal_data["start_date"]) if goal_data.get("start_date") else None,
                target_date=datetime.fromisoformat(goal_data["target_date"]) if goal_data.get("target_date") else None,
                status=goal_data.get("status", "active")
            )
            goals.append(goal)
        
        # Check data availability
        data_availability = self._check_data_availability(user_id)
        
        # Create display name
        age = demographics.age
        gender = demographics.gender
        display_name = f"{user_id} ({age}{gender.upper()})"
        
        return UserProfile(
            user_id=user_id,
            display_name=display_name,
            is_hardcoded=False,
            demographics=demographics,
            health_profile=health_profile,
            goals=goals,
            data_availability=data_availability,
            created_at=datetime.fromisoformat(user_data["created_at"]) if user_data.get("created_at") else None,
            last_active=datetime.fromisoformat(user_data["last_active"]) if user_data.get("last_active") else None
        )
    
    def _check_data_availability(self, user_id: str) -> DataAvailability:
        """Check what data files are available for a user."""
        if user_id == "hardcoded":
            return DataAvailability(
                biomarkers=True,
                medical_history=True,
                lifestyle=True,
                ai_interactions=False,
                interventions=False,
                completeness_score=85.0
            )
        
        # Check for dataset files
        biomarkers_file = self.datasets_dir / "biomarkers" / f"biomarkers_{user_id}.json"
        medical_history_file = self.datasets_dir / "medical_history" / f"medical_history_{user_id}.json"
        lifestyle_file = self.datasets_dir / "lifestyle" / f"lifestyle_{user_id}_2024-07.json"
        ai_interactions_file = self.datasets_dir / "ai_interactions" / f"interactions_{user_id}_session_001.json"
        interventions_file = self.datasets_dir / "interventions" / f"interventions_{user_id}.json"
        
        biomarkers_available = biomarkers_file.exists()
        medical_history_available = medical_history_file.exists()
        lifestyle_available = lifestyle_file.exists()
        ai_interactions_available = ai_interactions_file.exists()
        interventions_available = interventions_file.exists()
        
        # Calculate completeness score
        total_categories = 5
        available_categories = sum([
            biomarkers_available,
            medical_history_available,
            lifestyle_available,
            ai_interactions_available,
            interventions_available
        ])
        completeness_score = (available_categories / total_categories) * 100
        
        return DataAvailability(
            biomarkers=biomarkers_available,
            medical_history=medical_history_available,
            lifestyle=lifestyle_available,
            ai_interactions=ai_interactions_available,
            interventions=interventions_available,
            completeness_score=completeness_score
        )
    
    def get_available_users(self) -> List[UserProfile]:
        """Get list of all available users."""
        return list(self.users_cache.values())
    
    def select_user(self, user_id: str) -> UserProfile:
        """Select a user as the active user."""
        if user_id not in self.users_cache:
            available_ids = list(self.users_cache.keys())
            raise ValueError(f"Invalid user_id '{user_id}'. Available users: {available_ids}")
        
        self.active_user_id = user_id
        return self.users_cache[user_id]
    
    def get_current_user(self) -> UserProfile:
        """Get the currently active user."""
        return self.users_cache[self.active_user_id]
    
    def get_user_by_id(self, user_id: str) -> Optional[UserProfile]:
        """Get a specific user by ID."""
        return self.users_cache.get(user_id)
    
    def is_hardcoded_user_active(self) -> bool:
        """Check if the hardcoded user is currently active."""
        return self.active_user_id == "hardcoded"


# Global instance for the application
user_context_manager = UserContextManager()
