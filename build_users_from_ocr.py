#!/usr/bin/env python3
"""
Extract biomarkers from OCR data and create users from real medical reports.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class OCRBiomarkerExtractor:
    """Extract biomarkers from OCR medical reports."""
    
    def __init__(self):
        self.biomarker_patterns = {
            # Basic metabolic panel
            'glucose_fasting': [
                r'FASTING BLOOD SUGAR.*?(\d+\.?\d*)\s*mg/dL',
                r'GLUCOSE.*?(\d+\.?\d*)\s*mg/dL'
            ],
            'hba1c': [
                r'HbA1c.*?(\d+\.?\d*)\s*%',
                r'HPLC.*?(\d+\.?\d*)\s*%'
            ],
            
            # Lipid profile
            'total_cholesterol': [r'TOTAL CHOLESTEROL.*?(\d+)\s*mg/dL'],
            'hdl': [r'HDL CHOLESTEROL.*?(\d+)\s*mg/dL'],
            'ldl': [r'LDL CHOLESTEROL.*?(\d+)\s*mg/dL'],
            'triglycerides': [r'TRIGLYCERIDES.*?(\d+)\s*mg/dL'],
            'vldl': [r'VLDL CHOLESTEROL.*?(\d+\.?\d*)\s*mg/dL'],
            
            # Vitamins
            'vitamin_d': [
                r'25-OH VITAMIN D.*?(\d+\.?\d*)\s*ng/mL',
                r'VITAMIN D.*?(\d+\.?\d*)\s*ng/mL'
            ],
            'vitamin_b12': [r'VITAMIN B-12.*?(\d+)\s*pg/mL'],
            
            # Complete blood count
            'hemoglobin': [r'HEMOGLOBIN.*?(\d+\.?\d*)\s*g/dL'],
            'hematocrit': [r'HEMATOCRIT.*?(\d+\.?\d*)\s*%'],
            'wbc': [r'TOTAL LEUCOCYTES COUNT.*?(\d+\.?\d*)\s*X 10³ / µL'],
            'platelets': [r'PLATELET COUNT.*?(\d+)\s*X 10³ / µL'],
            'rbc': [r'TOTAL RBC.*?(\d+\.?\d*)\s*X 10\^6/µL'],
            
            # Liver function
            'sgot': [r'ASPARTATE AMINOTRANSFERASE.*?(\d+\.?\d*)\s*U/L'],
            'sgpt': [r'ALANINE TRANSAMINASE.*?(\d+\.?\d*)\s*U/L'],
            'bilirubin_total': [r'BILIRUBIN - TOTAL.*?(\d+\.?\d*)\s*mg/dL'],
            'alkaline_phosphatase': [r'ALKALINE PHOSPHATASE.*?(\d+\.?\d*)\s*U/L'],
            
            # Kidney function
            'creatinine': [r'CREATININE - SERUM.*?(\d+\.?\d*)\s*mg/dL'],
            'urea': [r'UREA.*?(\d+\.?\d*)\s*mg/dL'],
            'uric_acid': [r'URIC ACID.*?(\d+\.?\d*)\s*mg/dL'],
            
            # Thyroid
            'tsh': [r'TSH - ULTRASENSITIVE.*?(\d+\.?\d*)\s*µIU/mL'],
            't3': [r'TOTAL TRIIODOTHYRONINE.*?(\d+)\s*ng/dL'],
            't4': [r'TOTAL THYROXINE.*?(\d+\.?\d*)\s*µg/dL'],
            
            # Iron studies
            'iron': [r'IRON.*?(\d+\.?\d*)\s*µg/dL'],
            'tibc': [r'TOTAL IRON BINDING CAPACITY.*?(\d+\.?\d*)\s*µg/dL'],
            'transferrin_saturation': [r'% TRANSFERRIN SATURATION.*?(\d+\.?\d*)\s*%'],
            
            # Hormones
            'testosterone': [r'TESTOSTERONE.*?(\d+\.?\d*)\s*ng/dL'],
            'prolactin': [r'PROLACTIN.*?(\d+\.?\d*)\s*ng/mL'],
            'fsh': [r'FOLLICLE STIMULATING HORMONE.*?(\d+\.?\d*)\s*mIU/mL'],
            'lh': [r'LUTEINISING HORMONE.*?(\d+\.?\d*)\s*mIU/mL'],
            
            # Electrolytes
            'sodium': [r'SODIUM.*?(\d+\.?\d*)\s*mmol/L'],
            'chloride': [r'CHLORIDE.*?(\d+\.?\d*)\s*mmol/L'],
            'calcium': [r'CALCIUM.*?(\d+\.?\d*)\s*mg/dL'],
        }
        
        self.normal_ranges = {
            'glucose_fasting': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
            'hba1c': {'min': 0, 'max': 5.7, 'unit': '%'},
            'total_cholesterol': {'min': 0, 'max': 200, 'unit': 'mg/dL'},
            'hdl': {'min': 40, 'max': 999, 'unit': 'mg/dL'},
            'ldl': {'min': 0, 'max': 100, 'unit': 'mg/dL'},
            'triglycerides': {'min': 0, 'max': 150, 'unit': 'mg/dL'},
            'vitamin_d': {'min': 30, 'max': 999, 'unit': 'ng/mL'},
            'vitamin_b12': {'min': 200, 'max': 900, 'unit': 'pg/mL'},
            'hemoglobin': {'min': 12, 'max': 15.5, 'unit': 'g/dL'},
            'tsh': {'min': 0.54, 'max': 5.30, 'unit': 'µIU/mL'},
            'creatinine': {'min': 0.55, 'max': 1.02, 'unit': 'mg/dL'},
        }
    
    def extract_biomarkers(self, ocr_text: str) -> Dict[str, Any]:
        """Extract biomarkers from OCR text."""
        biomarkers = {}
        
        for biomarker, patterns in self.biomarker_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, ocr_text, re.IGNORECASE)
                if match:
                    try:
                        value = float(match.group(1))
                        normal_range = self.normal_ranges.get(biomarker, {})
                        
                        biomarkers[biomarker] = {
                            'value': value,
                            'unit': normal_range.get('unit', ''),
                            'normal_range': f"{normal_range.get('min', '')}-{normal_range.get('max', '')}" if normal_range else '',
                            'status': self._get_status(value, normal_range)
                        }
                        break  # Use first match
                    except (ValueError, IndexError):
                        continue
        
        return biomarkers
    
    def _get_status(self, value: float, normal_range: Dict) -> str:
        """Determine if biomarker is normal, high, or low."""
        if not normal_range:
            return 'unknown'
        
        min_val = normal_range.get('min', 0)
        max_val = normal_range.get('max', 999999)
        
        if value < min_val:
            return 'low'
        elif value > max_val:
            return 'high'
        else:
            return 'normal'


def extract_user_info_from_filename(filename: str) -> Dict[str, Any]:
    """Extract user info from directory name like user_001_29f."""
    parts = filename.split('_')
    if len(parts) >= 3:
        user_num = parts[1]
        age_gender = parts[2]
        
        # Extract age and gender
        age_match = re.search(r'(\d+)', age_gender)
        gender_match = re.search(r'([fm])', age_gender.lower())
        
        if age_match and gender_match:
            return {
                'user_id': f"ocr_user_{user_num}_{age_gender}",
                'age': int(age_match.group(1)),
                'gender': gender_match.group(1).upper(),
                'user_number': user_num
            }
    
    return None


def create_user_from_ocr(user_dir: Path, extractor: OCRBiomarkerExtractor) -> Optional[Dict[str, Any]]:
    """Create a complete user profile from OCR data."""
    
    # Extract user info from directory name
    user_info = extract_user_info_from_filename(user_dir.name)
    if not user_info:
        return None
    
    # Load OCR profile data
    profile_file = user_dir / "profile.json"
    if not profile_file.exists():
        return None
    
    with open(profile_file, 'r') as f:
        ocr_data = json.load(f)
    
    # Extract biomarkers from OCR text
    biomarkers = {}
    if ocr_data.get('documents'):
        for doc in ocr_data['documents']:
            full_text = doc.get('full_text', '')
            extracted_biomarkers = extractor.extract_biomarkers(full_text)
            biomarkers.update(extracted_biomarkers)
    
    if not biomarkers:
        print(f"⚠️  No biomarkers extracted for {user_info['user_id']}")
        return None
    
    # Create user profile
    user_data = {
        'user_id': user_info['user_id'],
        'demographics': {
            'age': user_info['age'],
            'gender': user_info['gender'],
            'location': {
                'city': 'Bengaluru',  # Default from OCR data
                'country': 'India'
            }
        },
        'health_profile': {
            'height_cm': 165 if user_info['gender'] == 'F' else 175,  # Default values
            'weight_kg': 60 if user_info['gender'] == 'F' else 75,
            'bmi': 22.0,  # Will be calculated
            'blood_type': 'O+',  # Default
            'biological_age': user_info['age'] - 1  # Assume 1 year younger
        },
        'goals': [
            {
                'goal_id': f"{user_info['user_id']}_goal_1",
                'type': 'health_optimization',
                'target': 'Optimize biomarkers based on lab results',
                'start_date': datetime.now().isoformat(),
                'target_date': datetime.now().replace(year=datetime.now().year + 1).isoformat(),
                'status': 'active'
            }
        ],
        'preferences': {
            'units': 'metric',
            'notifications': True,
            'data_sharing': True
        },
        'created_at': datetime.now().isoformat(),
        'last_active': datetime.now().isoformat(),
        'data_source': 'ocr_extracted'
    }
    
    # Calculate BMI
    height_m = user_data['health_profile']['height_cm'] / 100
    weight_kg = user_data['health_profile']['weight_kg']
    user_data['health_profile']['bmi'] = round(weight_kg / (height_m ** 2), 1)
    
    return {
        'profile': user_data,
        'biomarkers': biomarkers,
        'ocr_source': ocr_data.get('processed_at', ''),
        'document_count': len(ocr_data.get('documents', []))
    }


def build_users_from_ocr():
    """Build users from all OCR data."""
    print("🔬 Building Users from OCR Medical Reports")
    print("=" * 50)
    
    extractor = OCRBiomarkerExtractor()
    test_users_dir = Path("test_users")
    
    if not test_users_dir.exists():
        print("❌ test_users directory not found")
        return
    
    users_created = []
    
    # Process each user directory
    for user_dir in test_users_dir.iterdir():
        if user_dir.is_dir() and user_dir.name.startswith('user_'):
            print(f"\n🔍 Processing {user_dir.name}...")
            
            user_data = create_user_from_ocr(user_dir, extractor)
            if user_data:
                user_id = user_data['profile']['user_id']
                biomarker_count = len(user_data['biomarkers'])
                
                print(f"   ✅ Created user: {user_id}")
                print(f"   📊 Extracted {biomarker_count} biomarkers")
                print(f"   📄 From {user_data['document_count']} documents")
                
                # Save to datasets
                save_ocr_user_to_datasets(user_data)
                users_created.append(user_data)
            else:
                print(f"   ❌ Failed to create user from {user_dir.name}")
    
    print("\n" + "=" * 50)
    print(f"🎉 Successfully created {len(users_created)} users from OCR data!")
    
    # Print summary
    for user_data in users_created:
        profile = user_data['profile']
        print(f"   • {profile['user_id']}: {profile['demographics']['age']}{profile['demographics']['gender']} - {len(user_data['biomarkers'])} biomarkers")


def save_ocr_user_to_datasets(user_data: Dict[str, Any]):
    """Save OCR user data to datasets directory."""
    user_id = user_data['profile']['user_id']
    
    # Update users.json
    users_file = Path("datasets/users/users.json")
    users_file.parent.mkdir(parents=True, exist_ok=True)
    
    if users_file.exists():
        with open(users_file, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    # Remove existing user if present
    users = [u for u in users if u['user_id'] != user_id]
    users.append(user_data['profile'])
    
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)
    
    # Save biomarkers
    biomarkers_file = Path(f"datasets/biomarkers/biomarkers_{user_id}.json")
    biomarkers_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(biomarkers_file, 'w') as f:
        json.dump(user_data['biomarkers'], f, indent=2)
    
    # Create basic medical history
    medical_history = {
        'conditions': [],
        'medications': [],
        'supplements': [],
        'family_history': [],
        'notes': f"Data extracted from OCR medical reports on {user_data['ocr_source']}"
    }
    
    medical_file = Path(f"datasets/medical_history/medical_history_{user_id}.json")
    medical_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(medical_file, 'w') as f:
        json.dump(medical_history, f, indent=2)
    
    print(f"   💾 Saved data files for {user_id}")


if __name__ == "__main__":
    build_users_from_ocr()
