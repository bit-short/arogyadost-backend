import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

from app.models.user_profile import UserProfile, Demographics, HealthProfile, HealthGoal, DataAvailability

logger = logging.getLogger(__name__)


class EnhancedUserContextManager:
    """Enhanced user context manager that supports database users alongside existing functionality."""
    
    def __init__(self, datasets_dir: str = "datasets"):
        self.datasets_dir = Path(datasets_dir)
        self.active_user_id: str = "hardcoded"  # Default to hardcoded user
        self.users_cache: Dict[str, UserProfile] = {}
        self._load_all_users()
    
    def _load_all_users(self) -> None:
        """Load all available users including hardcoded, dataset, and database users."""
        # Load hardcoded user
        self.users_cache["hardcoded"] = self._create_hardcoded_user()
        
        # Load dataset users
        self._load_dataset_users()
        
        # Load database users
        self._load_database_users()
    
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
    
    def _load_database_users(self) -> None:
        """Load users from unified database."""
        try:
            from app.services.user_db_service import user_db_service
            db_users = user_db_service.get_all_users()
            
            for user_data in db_users:
                user_profile = self._create_user_profile_from_database(user_data)
                self.users_cache[user_profile.user_id] = user_profile
            
            logger.info(f"Loaded {len(db_users)} database users")
        except Exception as e:
            logger.error(f"Error loading database users: {e}")
    
    def _create_user_profile_from_database(self, user_data: Dict) -> UserProfile:
        """Create user profile from database user data."""
        user_id = user_data["user_id"]
        
        # Extract demographics
        demographics = Demographics(
            age=user_data.get("age", 30),
            gender=user_data.get("gender", "Unknown"),
            location={"city": user_data.get("city"), "country": user_data.get("country", "India")}
        )
        
        # Extract health profile
        health_profile = HealthProfile(
            height_cm=user_data.get("height_cm"),
            weight_kg=user_data.get("weight_kg"),
            bmi=user_data.get("bmi"),
            blood_type=user_data.get("blood_type"),
            biological_age=user_data.get("biological_age")
        )
        
        # Get additional data to determine availability
        try:
            from app.services.user_db_service import user_db_service
            biomarkers = user_db_service.get_user_biomarkers(user_id)
            medical_history = user_db_service.get_user_medical_history(user_id)
            goals = user_db_service.get_user_goals(user_id)
            
            # Convert goals to HealthGoal objects
            health_goals = []
            for goal_data in goals:
                health_goal = HealthGoal(
                    goal_id=goal_data.get("goal_id", ""),
                    type=goal_data.get("type", ""),
                    target=goal_data.get("target", ""),
                    status=goal_data.get("status", "active")
                )
                health_goals.append(health_goal)
            
            # Calculate data availability
            data_availability = DataAvailability(
                biomarkers=len(biomarkers) > 0,
                medical_history=any(len(v) > 0 for v in medical_history.values()),
                lifestyle=False,  # Not implemented in database yet
                ai_interactions=False,  # Not implemented yet
                interventions=False,    # Not implemented yet
                completeness_score=self._calculate_db_completeness(biomarkers, medical_history, goals)
            )
            
        except Exception as e:
            logger.error(f"Error loading additional data for user {user_id}: {e}")
            health_goals = []
            data_availability = DataAvailability(
                biomarkers=False,
                medical_history=False,
                lifestyle=False,
                ai_interactions=False,
                interventions=False,
                completeness_score=0.0
            )
        
        return UserProfile(
            user_id=user_id,
            display_name=f"{user_id} ({user_data.get('data_source', 'database')})",
            is_hardcoded=False,
            demographics=demographics,
            health_profile=health_profile,
            goals=health_goals,
            data_availability=data_availability,
            created_at=datetime.now(),  # Database doesn't store created_at yet
            last_active=datetime.now()
        )
    
    def _calculate_db_completeness(self, biomarkers: List, medical_history: Dict, goals: List) -> float:
        """Calculate completeness score for database users."""
        total_categories = 5  # biomarkers, medical_history, goals, demographics, health_profile
        available_categories = 0
        
        if len(biomarkers) > 0:
            available_categories += 1
        if any(len(v) > 0 for v in medical_history.values()):
            available_categories += 1
        if len(goals) > 0:
            available_categories += 1
        
        # Demographics and health_profile are always available from database
        available_categories += 2
        
        return (available_categories / total_categories) * 100
    
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
                start_date=datetime.fromisoformat(goal_data["start_date"].replace('Z', '+00:00')) if goal_data.get("start_date") else None,
                target_date=datetime.fromisoformat(goal_data["target_date"].replace('Z', '+00:00')) if goal_data.get("target_date") else None,
                status=goal_data.get("status", "active")
            )
            goals.append(goal)
        
        # Check data availability
        data_availability = self._check_data_availability(user_id)
        
        # Use user_id as display name
        display_name = user_id
        
        return UserProfile(
            user_id=user_id,
            display_name=display_name,
            is_hardcoded=False,
            demographics=demographics,
            health_profile=health_profile,
            goals=goals,
            data_availability=data_availability,
            created_at=datetime.fromisoformat(user_data["created_at"].replace('Z', '+00:00')) if user_data.get("created_at") else None,
            last_active=datetime.fromisoformat(user_data["last_active"].replace('Z', '+00:00')) if user_data.get("last_active") else None
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
        
        # Check for dataset files - support multiple naming patterns
        biomarkers_file = self.datasets_dir / "biomarkers" / f"biomarkers_{user_id}.json"
        medical_history_file = self.datasets_dir / "medical_history" / f"medical_history_{user_id}.json"
        interventions_file = self.datasets_dir / "interventions" / f"interventions_{user_id}.json"
        
        # Check lifestyle files with any date pattern
        lifestyle_dir = self.datasets_dir / "lifestyle"
        lifestyle_available = False
        if lifestyle_dir.exists():
            lifestyle_available = any(lifestyle_dir.glob(f"lifestyle_{user_id}_*.json"))
        
        # Check AI interactions with any session pattern
        ai_dir = self.datasets_dir / "ai_interactions"
        ai_interactions_available = False
        if ai_dir.exists():
            ai_interactions_available = any(ai_dir.glob(f"interactions_{user_id}_*.json"))
        
        biomarkers_available = biomarkers_file.exists()
        medical_history_available = medical_history_file.exists()
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
            # For database users, generate sample medical files based on their medical history
            try:
                from app.services.user_db_service import user_db_service
                medical_history = user_db_service.get_user_medical_history(self.active_user_id)
                
                if not medical_history or not any(len(v) > 0 for v in medical_history.values()):
                    # Try dataset files as fallback
                    return self._get_dataset_medical_files()
                
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
                        "id": file_id,
                        "filename": f"{condition['name'].replace(' ', '_').lower()}_report.pdf",
                        "upload_date": condition.get("start_date", "2024-07-26T00:00:00Z"),
                        "file_type": "pdf",
                        "category": category,
                        "specialty": specialty,
                        "hospital": "Apollo Hospital Mumbai",
                        "doctor": "Dr. Sharma",
                        "date": condition.get("start_date", "2024-07-26")[:10] if condition.get("start_date") else "2024-07-26",
                        "file_size": "2.3 MB",
                        "summary": f"Medical report for {condition['name']} - {condition.get('details', 'No additional details')}",
                        "key_findings": [
                            condition.get('details', 'No details available'),
                            f"Type: {condition.get('type', 'condition')}",
                            "Status: Active"
                        ],
                        "tags": [condition['name'].lower().replace(' ', '_'), "medical_condition", "lab_report"]
                    })
                
                # Add biomarker-based lab report if user has biomarkers
                biomarkers = user_db_service.get_user_biomarkers(self.active_user_id)
                if biomarkers and len(sample_files) < 4:
                    # Extract some key biomarkers for the report
                    key_biomarkers = []
                    for biomarker in biomarkers[:3]:  # Limit to 3 biomarkers
                        key_biomarkers.append(f"{biomarker['name']}: {biomarker['value']} {biomarker.get('unit', '')}")
                    
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
                            "summary": "Comprehensive biomarker analysis including metabolic markers and nutritional status",
                            "key_findings": key_biomarkers,
                            "tags": ["biomarkers", "metabolic_health", "lab_report"]
                        })
                
                # Add a general health checkup file if we have less than 2 files
                if len(sample_files) < 2:
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
                
                return sample_files
                
            except Exception as e:
                logger.error(f"Error loading medical files for database user {self.active_user_id}: {e}")
                # Fallback to dataset files
                return self._get_dataset_medical_files()
    
    def _get_dataset_medical_files(self) -> List[dict]:
        """Get medical files from dataset files (fallback method)."""
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
                        logger.error(f"Error loading biomarkers for {self.active_user_id}: {e}")
                
                return sample_files
                
            except Exception as e:
                logger.error(f"Error loading medical history for {self.active_user_id}: {e}")
                return []
        else:
            # Return empty list if no medical history available
            return []


    
    def create_persistent_user(self, user_id: str, display_name: str) -> UserProfile:
        """Create a new database user."""
        try:
            from app.services.user_db_service import user_db_service
            from app.database import SessionLocal
            from app.models.db_models import User
            
            # Create user in database
            db = SessionLocal()
            try:
                new_user = User(
                    id=user_id,
                    age=30,  # Default values
                    gender="Unknown",
                    city="Unknown",
                    country="India",
                    data_source="manual"
                )
                db.add(new_user)
                db.commit()
                
                # Create user profile
                user_profile = UserProfile(
                    user_id=user_id,
                    display_name=display_name,
                    is_hardcoded=False,
                    demographics=Demographics(age=30, gender="Unknown", location={"city": "Unknown", "country": "India"}),
                    health_profile=HealthProfile(),
                    goals=[],
                    data_availability=DataAvailability(
                        biomarkers=False,
                        medical_history=False,
                        lifestyle=False,
                        ai_interactions=False,
                        interventions=False,
                        completeness_score=40.0  # Demographics and health_profile available
                    ),
                    created_at=datetime.now(),
                    last_active=datetime.now()
                )
                
                # Add to cache
                self.users_cache[user_id] = user_profile
                
                logger.info(f"Created database user '{user_id}' with display name '{display_name}'")
                return user_profile
                
            finally:
                db.close()
            
        except Exception as e:
            logger.error(f"Failed to create database user '{user_id}': {e}")
            raise
    
    def refresh_persistent_users(self) -> None:
        """Refresh the cache with latest database users."""
        try:
            # Remove existing database users from cache (keep hardcoded and dataset users)
            db_user_ids = []
            for user_id, user_profile in list(self.users_cache.items()):
                if not user_profile.is_hardcoded and not self._is_dataset_user(user_id):
                    db_user_ids.append(user_id)
            
            for user_id in db_user_ids:
                del self.users_cache[user_id]
            
            # Reload database users
            self._load_database_users()
            
            logger.info("Refreshed database users cache")
        except Exception as e:
            logger.error(f"Failed to refresh database users: {e}")
    
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
        """Check if a user is a database user."""
        if user_id == "hardcoded":
            return False
        if self._is_dataset_user(user_id):
            return False
        
        try:
            from app.services.user_db_service import user_db_service
            user = user_db_service.get_user(user_id)
            return user is not None
        except Exception:
            return False


# Maintain backward compatibility
class UserContextManager(EnhancedUserContextManager):
    """Backward compatible user context manager."""
    pass


# Global instance for the application
user_context_manager = UserContextManager()
