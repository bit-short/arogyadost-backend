#!/usr/bin/env python3
"""
Migrate user data from JSON files to SQLite database.
"""

import json
from pathlib import Path
from datetime import datetime

from app.database import engine, SessionLocal, init_db
from app.models.db_models import User, Biomarker, MedicalHistory, Goal


def parse_datetime(dt_str):
    """Parse datetime string."""
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return None


def get_biomarker_category(name):
    """Map biomarker name to category."""
    categories = {
        'metabolic': ['hba1c', 'glucose_fasting', 'insulin'],
        'lipids': ['total_cholesterol', 'hdl', 'ldl', 'triglycerides', 'vldl'],
        'vitamins': ['vitamin_d', 'vitamin_b12'],
        'thyroid': ['tsh', 't3', 't4'],
        'liver': ['sgot', 'sgpt', 'bilirubin_total', 'alkaline_phosphatase'],
        'kidney': ['creatinine', 'urea', 'uric_acid'],
        'electrolytes': ['sodium', 'chloride', 'calcium', 'potassium'],
        'hormones': ['testosterone', 'prolactin', 'fsh', 'lh'],
        'iron': ['iron', 'tibc', 'transferrin_saturation'],
        'cbc': ['hemoglobin', 'hematocrit', 'wbc', 'platelets', 'rbc']
    }
    for cat, markers in categories.items():
        if name.lower() in markers:
            return cat
    return 'other'


def migrate_users():
    """Migrate all users from JSON to database."""
    print("🚀 Starting database migration...")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Load users from JSON
        users_file = Path("datasets/users/users.json")
        with open(users_file) as f:
            users_data = json.load(f)
        
        for user_data in users_data:
            user_id = user_data['user_id']
            print(f"\n📦 Migrating {user_id}...")
            
            # Check if user exists
            existing = db.query(User).filter(User.id == user_id).first()
            if existing:
                print(f"   ⏭️  User already exists, skipping")
                continue
            
            # Create user
            demographics = user_data.get('demographics', {})
            health_profile = user_data.get('health_profile', {})
            location = demographics.get('location', {})
            
            user = User(
                id=user_id,
                age=demographics.get('age'),
                gender=demographics.get('gender'),
                city=location.get('city'),
                country=location.get('country', 'India'),
                height_cm=health_profile.get('height_cm'),
                weight_kg=health_profile.get('weight_kg'),
                bmi=health_profile.get('bmi'),
                blood_type=health_profile.get('blood_type'),
                biological_age=health_profile.get('biological_age'),
                data_source=user_data.get('data_source', 'manual'),
                created_at=parse_datetime(user_data.get('created_at'))
            )
            db.add(user)
            print(f"   ✅ User created")
            
            # Migrate biomarkers
            bio_file = Path(f"datasets/biomarkers/biomarkers_{user_id}.json")
            if bio_file.exists():
                with open(bio_file) as f:
                    biomarkers_data = json.load(f)
                
                biomarker_count = 0
                
                # Handle different formats
                if isinstance(biomarkers_data, list):
                    # Format: [{biomarkers: {category: {name: {value, unit}}}}]
                    for entry in biomarkers_data:
                        for category, markers in entry.get('biomarkers', {}).items():
                            for name, data in markers.items():
                                if isinstance(data, dict) and 'value' in data:
                                    biomarker = Biomarker(
                                        user_id=user_id,
                                        name=name,
                                        value=data.get('value'),
                                        unit=data.get('unit'),
                                        normal_range=data.get('ref_range') or data.get('normal_range'),
                                        status=data.get('status'),
                                        category=category
                                    )
                                    db.add(biomarker)
                                    biomarker_count += 1
                else:
                    # Format: {name: {value, unit}}
                    for name, data in biomarkers_data.items():
                        if isinstance(data, dict) and 'value' in data:
                            biomarker = Biomarker(
                                user_id=user_id,
                                name=name,
                                value=data.get('value'),
                                unit=data.get('unit'),
                                normal_range=data.get('normal_range'),
                                status=data.get('status'),
                                category=get_biomarker_category(name)
                            )
                            db.add(biomarker)
                            biomarker_count += 1
                
                print(f"   ✅ {biomarker_count} biomarkers added")
            
            # Migrate medical history
            med_file = Path(f"datasets/medical_history/medical_history_{user_id}.json")
            if med_file.exists():
                with open(med_file) as f:
                    med_data = json.load(f)
                
                count = 0
                # Conditions
                for condition in med_data.get('conditions', []):
                    entry = MedicalHistory(
                        user_id=user_id,
                        type='condition',
                        name=condition.get('name'),
                        details=condition,
                        start_date=parse_datetime(condition.get('diagnosed_date'))
                    )
                    db.add(entry)
                    count += 1
                
                # Supplements
                for supp in med_data.get('supplements', []):
                    entry = MedicalHistory(
                        user_id=user_id,
                        type='supplement',
                        name=supp.get('name'),
                        details=supp,
                        start_date=parse_datetime(supp.get('start_date'))
                    )
                    db.add(entry)
                    count += 1
                
                # Family history
                for fam in med_data.get('family_history', []):
                    entry = MedicalHistory(
                        user_id=user_id,
                        type='family_history',
                        name=fam.get('condition'),
                        details=fam
                    )
                    db.add(entry)
                    count += 1
                
                print(f"   ✅ {count} medical history entries added")
            
            # Migrate goals
            for goal_data in user_data.get('goals', []):
                goal = Goal(
                    id=goal_data.get('goal_id'),
                    user_id=user_id,
                    type=goal_data.get('type'),
                    target=goal_data.get('target'),
                    status=goal_data.get('status', 'active'),
                    start_date=parse_datetime(goal_data.get('start_date')),
                    target_date=parse_datetime(goal_data.get('target_date'))
                )
                db.add(goal)
            
            if user_data.get('goals'):
                print(f"   ✅ {len(user_data['goals'])} goals added")
        
        # Commit all changes
        db.commit()
        print("\n✅ Migration completed successfully!")
        
        # Print summary
        user_count = db.query(User).count()
        biomarker_count = db.query(Biomarker).count()
        med_count = db.query(MedicalHistory).count()
        goal_count = db.query(Goal).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   Users: {user_count}")
        print(f"   Biomarkers: {biomarker_count}")
        print(f"   Medical History: {med_count}")
        print(f"   Goals: {goal_count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate_users()
