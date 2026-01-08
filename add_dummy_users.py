#!/usr/bin/env python3
"""
Helper script to add new dummy users to the system.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def create_dummy_user(
    user_id: str,
    age: int,
    gender: str,
    city: str,
    height_cm: int,
    weight_kg: int,
    blood_type: str,
    goals: list = None
):
    """Create a new dummy user with basic data."""
    
    # Calculate BMI
    bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)
    
    # Create user profile
    user_data = {
        "user_id": user_id,
        "demographics": {
            "age": age,
            "gender": gender,
            "location": {
                "city": city,
                "country": "India"
            }
        },
        "health_profile": {
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "bmi": bmi,
            "blood_type": blood_type,
            "biological_age": age - 2  # Assume 2 years younger biological age
        },
        "goals": goals or [
            {
                "goal_id": f"{user_id}_goal_1",
                "type": "general_health",
                "target": "Optimize overall health markers",
                "start_date": datetime.now().isoformat(),
                "target_date": datetime.now().replace(year=datetime.now().year + 1).isoformat(),
                "status": "active"
            }
        ],
        "preferences": {
            "units": "metric",
            "notifications": True,
            "data_sharing": True
        },
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat()
    }
    
    return user_data


def add_user_to_dataset(user_data):
    """Add user to the users.json file."""
    users_file = Path("datasets/users/users.json")
    
    # Load existing users
    if users_file.exists():
        with open(users_file, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    # Check if user already exists
    for existing_user in users:
        if existing_user["user_id"] == user_data["user_id"]:
            print(f"⚠️  User {user_data['user_id']} already exists. Updating...")
            users.remove(existing_user)
            break
    
    # Add new user
    users.append(user_data)
    
    # Save back to file
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"✅ Added user {user_data['user_id']} to dataset")


def create_basic_biomarkers(user_id: str, age: int, gender: str):
    """Create basic biomarker data for a user."""
    
    # Age and gender-based normal variations
    if gender == "M":
        hdl_base = 42
        hemoglobin_base = 14.5
    else:
        hdl_base = 50
        hemoglobin_base = 13.0
    
    # Age-based variations
    age_factor = 1 + (age - 30) * 0.01  # Slight increase with age
    
    biomarkers = {
        "glucose_fasting": {"value": round(85 + (age - 30) * 0.5), "unit": "mg/dL", "normal_range": "70-100"},
        "hba1c": {"value": round(5.2 + (age - 30) * 0.01, 1), "unit": "%", "normal_range": "<5.7"},
        "total_cholesterol": {"value": round(170 + (age - 30) * 2), "unit": "mg/dL", "normal_range": "<200"},
        "ldl": {"value": round(100 + (age - 30) * 1.5), "unit": "mg/dL", "normal_range": "<100"},
        "hdl": {"value": round(hdl_base * age_factor), "unit": "mg/dL", "normal_range": f">{hdl_base-8}"},
        "triglycerides": {"value": round(120 + (age - 30) * 2), "unit": "mg/dL", "normal_range": "<150"},
        "vitamin_d": {"value": round(25 + (age - 30) * 0.2, 1), "unit": "ng/mL", "normal_range": ">30"},
        "vitamin_b12": {"value": round(300 + (age - 30) * 5), "unit": "pg/mL", "normal_range": "200-900"},
        "crp": {"value": round(0.5 + (age - 30) * 0.02, 1), "unit": "mg/L", "normal_range": "<1.0"},
        "hemoglobin": {"value": round(hemoglobin_base * age_factor, 1), "unit": "g/dL", "normal_range": "12-15.5"}
    }
    
    # Save biomarkers
    biomarkers_file = Path(f"datasets/biomarkers/biomarkers_{user_id}.json")
    biomarkers_file.parent.mkdir(exist_ok=True)
    
    with open(biomarkers_file, 'w') as f:
        json.dump(biomarkers, f, indent=2)
    
    print(f"✅ Created biomarkers for {user_id}")


def create_basic_lifestyle(user_id: str, age: int):
    """Create basic lifestyle data for a user."""
    
    # Age-based lifestyle variations
    sleep_hours = 8.0 - (age - 30) * 0.02  # Slightly less sleep with age
    exercise_freq = max(3, 5 - (age - 30) // 10)  # Less frequent exercise with age
    
    lifestyle = {
        "sleep": {
            "average_hours": round(sleep_hours, 1),
            "quality_score": max(6, 9 - (age - 30) // 10),
            "bedtime": "22:30",
            "wake_time": "06:30"
        },
        "exercise": {
            "frequency_per_week": exercise_freq,
            "primary_activities": ["Walking", "Yoga"] if age > 50 else ["Running", "Gym"],
            "average_duration_minutes": max(30, 60 - (age - 30) // 5)
        },
        "nutrition": {
            "diet_type": "Balanced",
            "meals_per_day": 3,
            "water_intake_liters": 2.5,
            "alcohol_drinks_per_week": max(0, 3 - (age - 30) // 15)
        },
        "stress": {
            "level": min(8, 4 + (age - 30) // 10),
            "work_hours_per_day": max(6, 9 - (age - 60) // 10),
            "meditation_minutes_per_day": (age - 30) // 10
        }
    }
    
    # Save lifestyle
    lifestyle_file = Path(f"datasets/lifestyle/lifestyle_{user_id}_{datetime.now().strftime('%Y-%m')}.json")
    lifestyle_file.parent.mkdir(exist_ok=True)
    
    with open(lifestyle_file, 'w') as f:
        json.dump(lifestyle, f, indent=2)
    
    print(f"✅ Created lifestyle data for {user_id}")


def create_basic_medical_history(user_id: str, age: int):
    """Create basic medical history for a user."""
    
    medical_history = {
        "conditions": [],
        "medications": [],
        "supplements": [
            {
                "supplement_id": f"{user_id}_supp_1",
                "name": "Multivitamin",
                "dosage": "1 tablet",
                "frequency": "daily",
                "start_date": datetime.now().isoformat(),
                "purpose": "General health maintenance"
            }
        ],
        "family_history": [
            {
                "condition": "Hypertension",
                "relation": "Parent",
                "age_of_onset": 55
            }
        ]
    }
    
    # Add age-specific conditions
    if age > 40:
        medical_history["supplements"].append({
            "supplement_id": f"{user_id}_supp_2",
            "name": "Vitamin D3",
            "dosage": "2000 IU",
            "frequency": "daily",
            "start_date": datetime.now().isoformat(),
            "purpose": "Bone health"
        })
    
    # Save medical history
    medical_file = Path(f"datasets/medical_history/medical_history_{user_id}.json")
    medical_file.parent.mkdir(exist_ok=True)
    
    with open(medical_file, 'w') as f:
        json.dump(medical_history, f, indent=2)
    
    print(f"✅ Created medical history for {user_id}")


def add_dummy_user(user_id: str, age: int, gender: str, city: str, height_cm: int, weight_kg: int, blood_type: str):
    """Add a complete dummy user with all data files."""
    
    print(f"🚀 Creating dummy user: {user_id}")
    print("=" * 50)
    
    # Create user profile
    user_data = create_dummy_user(user_id, age, gender, city, height_cm, weight_kg, blood_type)
    add_user_to_dataset(user_data)
    
    # Create supporting data files
    create_basic_biomarkers(user_id, age, gender)
    create_basic_lifestyle(user_id, age)
    create_basic_medical_history(user_id, age)
    
    print("=" * 50)
    print(f"🎉 Successfully created dummy user: {user_id}")
    print(f"   Age: {age}, Gender: {gender}, Location: {city}")
    print(f"   BMI: {user_data['health_profile']['bmi']}")
    print("   ✅ Profile, biomarkers, lifestyle, and medical history created")


if __name__ == "__main__":
    # Example: Add a few dummy users
    print("🧪 Adding sample dummy users...")
    
    # Add diverse test users
    add_dummy_user("test_user_2_35m", 35, "M", "Mumbai", 178, 75, "A+")
    add_dummy_user("test_user_3_42f", 42, "F", "Delhi", 162, 65, "B+")
    add_dummy_user("test_user_4_28m", 28, "M", "Chennai", 175, 70, "O+")
    
    print("\n🎉 All dummy users created successfully!")
