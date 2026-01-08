import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

from app.models.user_profile import UserProfile, Demographics, HealthProfile, HealthGoal, DataAvailability
from app.storage.persistent_storage import persistent_storage

logger = logging.getLogger(__name__)


class EnhancedUserContextManager:
    """Enhanced user context manager that supports persistent users alongside existing functionality."""
    
    def __init__(self, datasets_dir: str = "datasets"):
        self.datasets_dir = Path(datasets_dir)
        self.active_user_id: str = "hardcoded"  # Default to hardcoded user
        self.users_cache: Dict[str, UserProfile] = {}
        self._load_all_users()
    
    def _load_all_users(self) -> None:
        """Load all available users including hardcoded, dataset, and persistent users."""
        # Load hardcoded user
        self.users_cache["hardcoded"] = self._create_hardcoded_user()
        
        # Load dataset users
        self._load_dataset_users()
        
        # Load persistent users
        self._load_persistent_users()
    
    def _load_dataset_users(self) -> None:
        """Load users from dataset files."""
        users_file = self.datasets_dir / "users" / "users.json"
        if users_file.exists():
            try:
                with open(users_file, 'r') as f:
                    users_data = json.load(f)
                
                for user_data in users_data:
                    user_profile = self._create_user_profile_from_data(user_data)
                    self.users_cache[user_profile.user_id] = user_profile
                    
                logger.info(f"Loaded {len(users_data)} dataset users")
            except Exception as e:
                logger.error(f"Error loading users from dataset: {e}")
    
    def _load_persistent_users(self) -> None:
        """Load users from persistent storage."""
        try:
            persistent_users = persistent_storage.list_all_users()
            for user_info in persistent_users:
                user_profile = self._create_user_profile_from_persistent(user_info)
                self.users_cache[user_profile.user_id] = user_profile
            
            logger.info(f"Loaded {len(persistent_users)} persistent users")
        except Exception as e:
            logger.error(f"Error loading persistent users: {e}")
    
    def _create_user_profile_from_persistent(self, user_info) -> UserProfile:
        """Create user profile from persistent storage user info."""
        # Get digital twin to extract health data
        digital_twin = persistent_storage.get_digital_twin(user_info.user_id)
        
        # Extract demographics from digital twin if available
        demographics = Demographics(age=30, gender="Unknown", location={})
        health_profile = HealthProfile()
        goals = []
        
        if digital_twin:
            # Extract demographics
            demo_domain = digital_twin.get_domain("demographics")
            if demo_domain:
                age_field = demo_domain.fields.get("age")
                gender_field = demo_domain.fields.get("gender")
                location_field = demo_domain.fields.get("location")
                
                demographics = Demographics(
                    age=age_field.get_latest_value().value if age_field and age_field.values else 30,
                    gender=gender_field.get_latest_value().value if gender_field and gender_field.values else "Unknown",
                    location=location_field.get_latest_value().value if location_field and location_field.values else {}
                )
            
            # Extract health profile
            bio_domain = digital_twin.get_domain("biomarkers")
            if bio_domain:
                height_field = bio_domain.fields.get("height_cm")
                weight_field = bio_domain.fields.get("weight_kg")
                bmi_field = bio_domain.fields.get("bmi")
                blood_type_field = bio_domain.fields.get("blood_type")
                
                health_profile = HealthProfile(
                    height_cm=height_field.get_latest_value().value if height_field and height_field.values else None,
                    weight_kg=weight_field.get_latest_value().value if weight_field and weight_field.values else None,
                    bmi=bmi_field.get_latest_value().value if bmi_field and bmi_field.values else None,
                    blood_type=blood_type_field.get_latest_value().value if blood_type_field and blood_type_field.values else None,
                    biological_age=None  # Will be calculated by biological age engine
                )
        
        # Create data availability based on digital twin completeness
        data_availability = DataAvailability(
            biomarkers=digital_twin.get_domain("biomarkers").get_completeness_percentage() > 0 if digital_twin else False,
            medical_history=digital_twin.get_domain("medical_history").get_completeness_percentage() > 0 if digital_twin else False,
            lifestyle=digital_twin.get_domain("lifestyle").get_completeness_percentage() > 0 if digital_twin else False,
            ai_interactions=False,  # Not implemented yet
            interventions=False,    # Not implemented yet
            completeness_score=digital_twin.get_overall_completeness() if digital_twin else 0.0
        )
        
        return UserProfile(
            user_id=user_info.user_id,
            display_name=user_info.display_name,
            is_hardcoded=False,
            demographics=demographics,
            health_profile=health_profile,
            goals=goals,
            data_availability=data_availability,
            created_at=user_info.created_at,
            last_active=user_info.updated_at
        )
    
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
        
        # Medical files are available if medical history exists (we generate them from medical history)
        medical_files_available = medical_history_available
        
        # Calculate completeness score (including medical files)
        total_categories = 6  # Added medical files as a category
        available_categories = sum([
            biomarkers_available,
            medical_history_available,
            lifestyle_available,
            ai_interactions_available,
            interventions_available,
            medical_files_available
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
    
    def get_user_medical_files(self) -> List[dict]:
        """Get medical files for the currently active user."""
        if self.active_user_id == "hardcoded":
            # Return hardcoded mock data
            from main import mock_data
            return mock_data["medical_files"]
        else:
            # For test users, create sample medical files based on their medical history
            medical_history_file = self.datasets_dir / "medical_history" / f"medical_history_{self.active_user_id}.json"
            
            if medical_history_file.exists():
                try:
                    with open(medical_history_file, 'r') as f:
                        medical_history = json.load(f)
                    
                    # Generate sample medical files based on conditions and test results
                    sample_files = []
                    
                    # Add files for each condition (limit to 3 files)
                    for i, condition in enumerate(medical_history.get("conditions", [])[:3]):
                        file_id = f"{self.active_user_id}_cond_{i+1:03d}"
                        
                        # Map condition to appropriate specialty and category
                        specialty_mapping = {
                            "vitamin d deficiency": "Endocrinology",
                            "dyslipidemia": "Cardiology", 
                            "diabetes": "Endocrinology",
                            "hypertension": "Cardiology",
                            "thyroid": "Endocrinology",
                            "anemia": "Hematology"
                        }
                        
                        condition_name_lower = condition['name'].lower()
                        specialty = "Internal Medicine"  # default
                        for key, spec in specialty_mapping.items():
                            if key in condition_name_lower:
                                specialty = spec
                                break
                        
                        # Determine category based on condition type
                        category = "Lab Report" if any(word in condition_name_lower for word in ["deficiency", "level", "diabetes", "lipid"]) else "Diagnostic Test"
                        
                        sample_files.append({
                            "id": file_id,  # Frontend expects 'id', not 'file_id'
                            "filename": f"{condition['name'].replace(' ', '_').lower()}_report.pdf",
                            "upload_date": condition["diagnosed_date"],
                            "file_type": "pdf",
                            "category": category,
                            "specialty": specialty,
                            "hospital": "Apollo Hospital Mumbai",
                            "doctor": "Dr. Sharma",
                            "date": condition["diagnosed_date"][:10],
                            "file_size": "2.3 MB",
                            "summary": f"Lab report showing {condition['name']} - {condition['notes']}",
                            "key_findings": [
                                condition['notes'],
                                f"Severity: {condition['severity']}",
                                f"Status: {condition['status']}"
                            ],
                            "tags": [condition['name'].lower().replace(' ', '_'), condition['severity'], "lab_report"]
                        })
                    
                    # Add a general health checkup file if we have less than 3 files
                    if len(sample_files) < 3:
                        sample_files.append({
                            "id": f"{self.active_user_id}_checkup_001",
                            "filename": "annual_health_checkup_2024.pdf",
                            "upload_date": "2024-07-26T00:00:00Z",
                            "file_type": "pdf",
                            "category": "Health Checkup",
                            "specialty": "General Medicine",
                            "hospital": "Max Healthcare Mumbai",
                            "doctor": "Dr. Patel",
                            "date": "2024-07-26",
                            "file_size": "1.8 MB",
                            "summary": "Comprehensive annual health checkup with blood work and physical examination",
                            "key_findings": [
                                "Overall health status: Good",
                                "Blood pressure: Normal",
                                "BMI: Within normal range"
                            ],
                            "tags": ["annual_checkup", "preventive_care", "general_health"]
                        })
                    
                    # Add biomarker-based lab report if user has biomarkers
                    biomarkers_file = self.datasets_dir / "biomarkers" / f"biomarkers_{self.active_user_id}.json"
                    if biomarkers_file.exists() and len(sample_files) < 4:
                        try:
                            with open(biomarkers_file, 'r') as f:
                                biomarkers_data = json.load(f)
                            
                            # Extract some key biomarkers for the report
                            key_biomarkers = []
                            if "lipid_panel" in biomarkers_data:
                                lipid = biomarkers_data["lipid_panel"]
                                if "total_cholesterol" in lipid:
                                    key_biomarkers.append(f"Total Cholesterol: {lipid['total_cholesterol']['value']} {lipid['total_cholesterol']['unit']}")
                                if "hdl_cholesterol" in lipid:
                                    key_biomarkers.append(f"HDL: {lipid['hdl_cholesterol']['value']} {lipid['hdl_cholesterol']['unit']}")
                                if "triglycerides" in lipid:
                                    key_biomarkers.append(f"Triglycerides: {lipid['triglycerides']['value']} {lipid['triglycerides']['unit']}")
                            
                            if key_biomarkers:
                                sample_files.append({
                                    "id": f"{self.active_user_id}_biomarkers_001",
                                    "filename": "comprehensive_biomarker_panel_2024.pdf",
                                    "upload_date": "2024-07-26T00:00:00Z",
                                    "file_type": "pdf",
                                    "category": "Lab Report",
                                    "specialty": "Pathology",
                                    "hospital": "SRL Diagnostics",
                                    "doctor": "Dr. Kumar",
                                    "date": "2024-07-26",
                                    "file_size": "3.2 MB",
                                    "summary": "Comprehensive biomarker analysis including lipid profile, metabolic markers, and nutritional status",
                                    "key_findings": key_biomarkers[:3],  # Limit to 3 findings
                                    "tags": ["biomarkers", "lipid_profile", "metabolic_health", "lab_report"]
                                })
                        except Exception as e:
                            print(f"Error loading biomarkers for {self.active_user_id}: {e}")
                    
                    return sample_files
                    
                except Exception as e:
                    print(f"Error loading medical history for {self.active_user_id}: {e}")
                    return []
            else:
                # Return empty list if no medical history available
                return []


    
    def create_persistent_user(self, user_id: str, display_name: str) -> UserProfile:
        """Create a new persistent user with digital twin."""
        try:
            # Create user in persistent storage
            digital_twin = persistent_storage.create_user_digital_twin(user_id, display_name)
            
            # Create user profile
            user_profile = UserProfile(
                user_id=user_id,
                display_name=display_name,
                is_hardcoded=False,
                demographics=Demographics(age=30, gender="Unknown", location={}),
                health_profile=HealthProfile(),
                goals=[],
                data_availability=DataAvailability(
                    biomarkers=False,
                    medical_history=False,
                    lifestyle=False,
                    ai_interactions=False,
                    interventions=False,
                    completeness_score=0.0
                ),
                created_at=datetime.now(),
                last_active=datetime.now()
            )
            
            # Add to cache
            self.users_cache[user_id] = user_profile
            
            logger.info(f"Created persistent user '{user_id}' with display name '{display_name}'")
            return user_profile
            
        except Exception as e:
            logger.error(f"Failed to create persistent user '{user_id}': {e}")
            raise
    
    def refresh_persistent_users(self) -> None:
        """Refresh the cache with latest persistent users."""
        try:
            # Remove existing persistent users from cache (keep hardcoded and dataset users)
            persistent_user_ids = []
            for user_id, user_profile in list(self.users_cache.items()):
                if not user_profile.is_hardcoded and not self._is_dataset_user(user_id):
                    persistent_user_ids.append(user_id)
            
            for user_id in persistent_user_ids:
                del self.users_cache[user_id]
            
            # Reload persistent users
            self._load_persistent_users()
            
            logger.info("Refreshed persistent users cache")
        except Exception as e:
            logger.error(f"Failed to refresh persistent users: {e}")
    
    def _is_dataset_user(self, user_id: str) -> bool:
        """Check if a user is from the dataset files."""
        users_file = self.datasets_dir / "users" / "users.json"
        if users_file.exists():
            try:
                with open(users_file, 'r') as f:
                    users_data = json.load(f)
                return any(user_data.get("user_id") == user_id for user_data in users_data)
            except Exception:
                pass
        return False
    
    def is_persistent_user(self, user_id: str) -> bool:
        """Check if a user is a persistent user."""
        if user_id == "hardcoded":
            return False
        if self._is_dataset_user(user_id):
            return False
        return persistent_storage.user_exists(user_id)


# Maintain backward compatibility
class UserContextManager(EnhancedUserContextManager):
    """Backward compatible user context manager."""
    pass


# Global instance for the application
user_context_manager = UserContextManager()
