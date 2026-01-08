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


# Global instance for the application
user_context_manager = UserContextManager()
