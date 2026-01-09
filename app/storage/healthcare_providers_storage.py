"""
Healthcare Providers Storage Layer
Manages storage and retrieval of doctors, labs, and related data
"""

from typing import List, Optional, Dict, Any
from app.models.healthcare_providers import (
    Doctor, Lab, UserProfile, DataSource, ProductImage,
    DoctorsResponse, LabsResponse, UserProfilesResponse, DataSourcesResponse
)
from datetime import datetime
import json
import os


class HealthcareProvidersStorage:
    """Storage layer for healthcare providers data"""
    
    def __init__(self):
        self.data_dir = "datasets/healthcare_providers"
        self._ensure_data_directory()
        self._initialize_default_data()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _initialize_default_data(self):
        """Initialize with default data if files don't exist"""
        if not os.path.exists(f"{self.data_dir}/doctors.json"):
            self._create_default_doctors()
        if not os.path.exists(f"{self.data_dir}/labs.json"):
            self._create_default_labs()
        if not os.path.exists(f"{self.data_dir}/user_profiles.json"):
            self._create_default_profiles()
        if not os.path.exists(f"{self.data_dir}/data_sources.json"):
            self._create_default_data_sources()
        if not os.path.exists(f"{self.data_dir}/product_images.json"):
            self._create_default_product_images()
    
    def _create_default_doctors(self):
        """Create default doctors data"""
        doctors = [
            {
                "id": "dr-001",
                "name": "Dr. Rajesh Sharma",
                "specialty": "Longevity Medicine",
                "rating": 4.9,
                "review_count": 234,
                "distance": "0.8 km",
                "next_available": "Tomorrow, 10:00 AM",
                "image_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=200&h=200&fit=crop&crop=face",
                "is_partner": True,
                "is_sponsored": False,
                "phone": "+91-98765-43210",
                "address": "Apollo Hospital, Sarita Vihar, New Delhi",
                "languages": ["English", "Hindi"],
                "consultation_fee": 1500,
                "experience_years": 15,
                "qualifications": ["MBBS", "MD Internal Medicine", "Fellowship in Longevity Medicine"],
                "available_slots": ["10:00 AM", "2:00 PM", "4:00 PM"]
            },
            {
                "id": "dr-002",
                "name": "Dr. Priya Patel",
                "specialty": "Preventive Cardiology",
                "rating": 4.8,
                "review_count": 189,
                "distance": "1.2 km",
                "next_available": "Wed, 2:30 PM",
                "image_url": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=200&h=200&fit=crop&crop=face",
                "is_partner": True,
                "is_sponsored": True,
                "phone": "+91-98765-43211",
                "address": "Max Hospital, Patparganj, New Delhi",
                "languages": ["English", "Hindi", "Gujarati"],
                "consultation_fee": 1200,
                "experience_years": 12,
                "qualifications": ["MBBS", "MD Cardiology", "DM Interventional Cardiology"],
                "available_slots": ["9:00 AM", "2:30 PM", "5:00 PM"]
            },
            {
                "id": "dr-003",
                "name": "Dr. Amit Kumar",
                "specialty": "Endocrinology & Metabolism",
                "rating": 4.7,
                "review_count": 156,
                "distance": "2.1 km",
                "next_available": "Thu, 9:00 AM",
                "image_url": "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=200&h=200&fit=crop&crop=face",
                "is_partner": False,
                "is_sponsored": False,
                "phone": "+91-98765-43212",
                "address": "AIIMS, Ansari Nagar, New Delhi",
                "languages": ["English", "Hindi"],
                "consultation_fee": 800,
                "experience_years": 18,
                "qualifications": ["MBBS", "MD Medicine", "DM Endocrinology"],
                "available_slots": ["9:00 AM", "11:00 AM", "3:00 PM"]
            },
            {
                "id": "dr-004",
                "name": "Dr. Sunita Reddy",
                "specialty": "Functional Medicine",
                "rating": 4.6,
                "review_count": 98,
                "distance": "3.4 km",
                "next_available": "Fri, 11:00 AM",
                "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=200&h=200&fit=crop&crop=face",
                "is_partner": False,
                "is_sponsored": False,
                "phone": "+91-98765-43213",
                "address": "Fortis Hospital, Vasant Kunj, New Delhi",
                "languages": ["English", "Hindi", "Telugu"],
                "consultation_fee": 1000,
                "experience_years": 10,
                "qualifications": ["MBBS", "MD Medicine", "Certified Functional Medicine Practitioner"],
                "available_slots": ["11:00 AM", "1:00 PM", "4:00 PM"]
            }
        ]
        
        with open(f"{self.data_dir}/doctors.json", "w") as f:
            json.dump(doctors, f, indent=2)
    
    def _create_default_labs(self):
        """Create default labs data"""
        labs = [
            {
                "id": "lab-001",
                "name": "SRL Diagnostics",
                "type": "sponsored",
                "rating": 4.8,
                "review_count": 324,
                "distance": "0.5 km",
                "address": "123 Medical Center Dr, Lajpat Nagar, New Delhi",
                "next_available": "Today, 2:00 PM",
                "specialties": ["Blood Work", "Lipid Panel", "Vitamin Tests", "Hormone Tests"],
                "phone": "+91-11-4567-8901",
                "email": "info@srldiagnostics.com",
                "website": "https://www.srldiagnostics.in",
                "operating_hours": "6:00 AM - 10:00 PM",
                "tests_offered": ["Complete Blood Count", "Lipid Profile", "Vitamin D", "Thyroid Panel", "HbA1c"],
                "home_collection": True,
                "online_reports": True
            },
            {
                "id": "lab-002",
                "name": "Dr. Lal PathLabs",
                "type": "partner",
                "rating": 4.6,
                "review_count": 512,
                "distance": "1.2 km",
                "address": "456 Healthcare Blvd, Karol Bagh, New Delhi",
                "next_available": "Tomorrow, 9:00 AM",
                "specialties": ["Full Panels", "Hormone Tests", "Genetic Testing", "Cardiac Markers"],
                "phone": "+91-11-4567-8902",
                "email": "info@lalpathlabs.com",
                "website": "https://www.lalpathlabs.com",
                "operating_hours": "7:00 AM - 9:00 PM",
                "tests_offered": ["Comprehensive Metabolic Panel", "Cardiac Risk Assessment", "Genetic Screening"],
                "home_collection": True,
                "online_reports": True
            },
            {
                "id": "lab-003",
                "name": "Metropolis Healthcare",
                "type": "partner",
                "rating": 4.7,
                "review_count": 189,
                "distance": "1.8 km",
                "address": "789 Wellness Way, Connaught Place, New Delhi",
                "next_available": "Today, 4:30 PM",
                "specialties": ["Walk-in Available", "Same Day Results", "Specialized Tests"],
                "phone": "+91-11-4567-8903",
                "email": "info@metropolisindia.com",
                "website": "https://www.metropolisindia.com",
                "operating_hours": "24/7",
                "tests_offered": ["Urgent Blood Work", "Emergency Panels", "Specialized Biomarkers"],
                "home_collection": True,
                "online_reports": True
            },
            {
                "id": "lab-004",
                "name": "Thyrocare Technologies",
                "type": "regular",
                "rating": 4.4,
                "review_count": 156,
                "distance": "2.1 km",
                "address": "321 Main Street, Rohini, New Delhi",
                "next_available": "Wed, Dec 11, 10:00 AM",
                "specialties": ["Blood Work", "Urinalysis", "Preventive Health Packages"],
                "phone": "+91-11-4567-8904",
                "email": "info@thyrocare.com",
                "website": "https://www.thyrocare.com",
                "operating_hours": "8:00 AM - 6:00 PM",
                "tests_offered": ["Basic Health Package", "Diabetes Panel", "Kidney Function Tests"],
                "home_collection": False,
                "online_reports": True
            }
        ]
        
        with open(f"{self.data_dir}/labs.json", "w") as f:
            json.dump(labs, f, indent=2)
    
    def _create_default_profiles(self):
        """Create default user profiles"""
        profiles = [
            {
                "id": "profile-001",
                "name": "Main Profile",
                "initial": "M",
                "is_primary": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        with open(f"{self.data_dir}/user_profiles.json", "w") as f:
            json.dump(profiles, f, indent=2)
    
    def _create_default_data_sources(self):
        """Create default data sources"""
        data_sources = [
            {
                "id": "apple-watch",
                "name": "Apple Watch",
                "icon": "Watch",
                "description": "Sleep, Heart Rate, Steps",
                "connected": True,
                "device_type": "wearable",
                "brand": "Apple",
                "model": "Series 9",
                "last_sync": "2024-01-08T10:30:00Z",
                "data_types": ["heart_rate", "steps", "sleep", "workout"]
            },
            {
                "id": "fitbit",
                "name": "Fitbit",
                "icon": "Activity",
                "description": "Activity & Sleep Tracking",
                "connected": False,
                "device_type": "wearable",
                "brand": "Fitbit",
                "model": "Charge 5",
                "last_sync": None,
                "data_types": ["steps", "sleep", "heart_rate", "calories"]
            },
            {
                "id": "bp-monitor",
                "name": "Blood Pressure Monitor",
                "icon": "Heart",
                "description": "Omron, Withings, etc.",
                "connected": False,
                "device_type": "monitor",
                "brand": "Omron",
                "model": "HEM-7120",
                "last_sync": None,
                "data_types": ["blood_pressure", "pulse"]
            },
            {
                "id": "smart-scale",
                "name": "Smart Scale",
                "icon": "Scale",
                "description": "Weight & Body Composition",
                "connected": True,
                "device_type": "scale",
                "brand": "Withings",
                "model": "Body+",
                "last_sync": "2024-01-07T08:00:00Z",
                "data_types": ["weight", "body_fat", "muscle_mass", "bone_mass"]
            },
            {
                "id": "glucose-monitor",
                "name": "Glucose Monitor",
                "icon": "Activity",
                "description": "CGM & Blood Glucose",
                "connected": False,
                "device_type": "monitor",
                "brand": "FreeStyle",
                "model": "Libre 2",
                "last_sync": None,
                "data_types": ["glucose", "trends"]
            }
        ]
        
        with open(f"{self.data_dir}/data_sources.json", "w") as f:
            json.dump(data_sources, f, indent=2)
    
    def _create_default_product_images(self):
        """Create default product images mapping"""
        product_images = [
            {
                "id": "vitamins",
                "name": "Vitamins",
                "category": "supplements",
                "image_path": "/src/assets/products/vitamins.jpg",
                "alt_text": "Daily vitamins and supplements",
                "description": "Essential daily vitamins for optimal health"
            },
            {
                "id": "omega3",
                "name": "Omega-3",
                "category": "supplements",
                "image_path": "/src/assets/products/omega3.jpg",
                "alt_text": "Omega-3 fish oil supplements",
                "description": "High-quality omega-3 fatty acids"
            },
            {
                "id": "walking",
                "name": "Walking",
                "category": "exercise",
                "image_path": "/src/assets/products/walking.jpg",
                "alt_text": "Walking exercise activity",
                "description": "Daily walking for cardiovascular health"
            },
            {
                "id": "probiotic",
                "name": "Probiotic",
                "category": "supplements",
                "image_path": "/src/assets/products/probiotic.jpg",
                "alt_text": "Probiotic supplements for gut health",
                "description": "Beneficial bacteria for digestive wellness"
            },
            {
                "id": "water",
                "name": "Water",
                "category": "hydration",
                "image_path": "/src/assets/products/water.jpg",
                "alt_text": "Daily water intake",
                "description": "Proper hydration for optimal health"
            },
            {
                "id": "meditation",
                "name": "Meditation",
                "category": "wellness",
                "image_path": "/src/assets/products/meditation.jpg",
                "alt_text": "Meditation and mindfulness practice",
                "description": "Daily meditation for mental wellness"
            },
            {
                "id": "moisturizer",
                "name": "Moisturizer",
                "category": "skincare",
                "image_path": "/src/assets/products/moisturizer.jpg",
                "alt_text": "Daily moisturizer for skin health",
                "description": "Skin hydration and protection"
            },
            {
                "id": "spf",
                "name": "SPF Sunscreen",
                "category": "skincare",
                "image_path": "/src/assets/products/spf.jpg",
                "alt_text": "SPF sunscreen protection",
                "description": "Daily sun protection for skin health"
            }
        ]
        
        with open(f"{self.data_dir}/product_images.json", "w") as f:
            json.dump(product_images, f, indent=2)
    
    # Read methods
    def get_doctors(self, specialty: Optional[str] = None, partner_only: bool = False) -> DoctorsResponse:
        """Get list of doctors with optional filtering"""
        with open(f"{self.data_dir}/doctors.json", "r") as f:
            doctors_data = json.load(f)
        
        doctors = [Doctor(**doc) for doc in doctors_data]
        
        # Apply filters
        if specialty:
            doctors = [d for d in doctors if specialty.lower() in d.specialty.lower()]
        if partner_only:
            doctors = [d for d in doctors if d.is_partner or d.is_sponsored]
        
        featured_count = len([d for d in doctors if d.is_partner or d.is_sponsored])
        partner_count = len([d for d in doctors if d.is_partner])
        
        return DoctorsResponse(
            doctors=doctors,
            total_count=len(doctors),
            featured_count=featured_count,
            partner_count=partner_count
        )
    
    def get_labs(self, test_type: Optional[str] = None) -> LabsResponse:
        """Get list of labs with optional filtering"""
        with open(f"{self.data_dir}/labs.json", "r") as f:
            labs_data = json.load(f)
        
        labs = [Lab(**lab) for lab in labs_data]
        
        # Apply filters
        if test_type:
            labs = [l for l in labs if any(test_type.lower() in spec.lower() for spec in l.specialties)]
        
        sponsored_count = len([l for l in labs if l.type == "sponsored"])
        partner_count = len([l for l in labs if l.type == "partner"])
        
        return LabsResponse(
            labs=labs,
            total_count=len(labs),
            sponsored_count=sponsored_count,
            partner_count=partner_count
        )
    
    def get_user_profiles(self) -> UserProfilesResponse:
        """Get user profiles"""
        with open(f"{self.data_dir}/user_profiles.json", "r") as f:
            profiles_data = json.load(f)
        
        profiles = [UserProfile(**profile) for profile in profiles_data]
        active_profile = next((p for p in profiles if p.is_primary), profiles[0] if profiles else None)
        
        return UserProfilesResponse(
            profiles=profiles,
            active_profile_id=active_profile.id if active_profile else ""
        )
    
    def get_data_sources(self) -> DataSourcesResponse:
        """Get data sources"""
        with open(f"{self.data_dir}/data_sources.json", "r") as f:
            sources_data = json.load(f)
        
        data_sources = [DataSource(**source) for source in sources_data]
        connected_count = len([s for s in data_sources if s.connected])
        
        return DataSourcesResponse(
            data_sources=data_sources,
            connected_count=connected_count,
            available_count=len(data_sources)
        )
    
    def get_product_images(self) -> List[ProductImage]:
        """Get product images mapping"""
        with open(f"{self.data_dir}/product_images.json", "r") as f:
            images_data = json.load(f)
        
        return [ProductImage(**img) for img in images_data]
    
    def get_product_image_by_path(self, image_path: str) -> Optional[ProductImage]:
        """Get product image by path"""
        images = self.get_product_images()
        return next((img for img in images if img.image_path == image_path), None)


# Global instance
healthcare_storage = HealthcareProvidersStorage()