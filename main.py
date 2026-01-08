from fastapi import FastAPI, HTTPException
import json
import asyncio
from pathlib import Path
from cors_config import setup_cors, create_cors_preflight_handler
from app.routers.digital_twin import router as digital_twin_router
from app.routers.biological_age import router as biological_age_router
from app.routers.recommendations import router as recommendations_router

app = FastAPI(title="Aarogyadost API")

# Setup CORS using centralized configuration
setup_cors(app)
create_cors_preflight_handler(app)

# Include routers
app.include_router(digital_twin_router)
app.include_router(biological_age_router)
app.include_router(recommendations_router)

# Mock data - in production, this would come from a database
mock_data = {
    "health_categories": [
        {"id": "metabolic", "name": "Metabolic Health", "status": "good", "score": 82},
        {"id": "cardiovascular", "name": "Heart Health", "status": "attention", "score": 75},
        {"id": "hormonal", "name": "Hormonal Balance", "status": "good", "score": 88},
        {"id": "inflammation", "name": "Inflammation Markers", "status": "excellent", "score": 92},
        {"id": "liver", "name": "Liver Function", "status": "good", "score": 85},
        {"id": "kidney", "name": "Kidney Function", "status": "excellent", "score": 95}
    ],
    "medical_files": [
        # Cardiology Reports
        {
            "id": "card_001",
            "filename": "ECG_Report_2024_03_15.pdf",
            "specialty": "Cardiology",
            "category": "Diagnostic Test",
            "hospital": "Apollo Hospital Delhi",
            "doctor": "Dr. Rajesh Sharma",
            "date": "2024-03-15",
            "file_type": "pdf",
            "file_size": "2.3 MB",
            "summary": "ECG shows normal sinus rhythm, no signs of arrhythmia",
            "key_findings": ["Normal sinus rhythm", "Heart rate: 68 bpm", "No ST elevation"],
            "tags": ["heart", "ecg", "cardiology", "routine"],
            "upload_date": "2024-03-16T10:30:00Z"
        },
        {
            "id": "card_002", 
            "filename": "Echocardiogram_Report_2024_02_28.pdf",
            "specialty": "Cardiology",
            "category": "Imaging",
            "hospital": "Max Hospital Gurgaon",
            "doctor": "Dr. Priya Nair",
            "date": "2024-02-28",
            "file_type": "pdf",
            "file_size": "4.1 MB",
            "summary": "2D Echo shows good left ventricular function, EF 65%",
            "key_findings": ["EF: 65%", "Normal wall motion", "Mild mitral regurgitation"],
            "tags": ["heart", "echo", "imaging", "function"],
            "upload_date": "2024-03-01T14:20:00Z"
        },
        {
            "id": "card_003",
            "filename": "Stress_Test_Report_2024_01_20.pdf", 
            "specialty": "Cardiology",
            "category": "Stress Test",
            "hospital": "Fortis Hospital Mumbai",
            "doctor": "Dr. Amit Gupta",
            "date": "2024-01-20",
            "file_type": "pdf",
            "file_size": "1.8 MB",
            "summary": "TMT negative for inducible ischemia, good exercise tolerance",
            "key_findings": ["Exercise duration: 12 minutes", "Peak HR: 165 bpm", "No chest pain"],
            "tags": ["stress test", "exercise", "ischemia", "fitness"],
            "upload_date": "2024-01-22T09:15:00Z"
        },
        
        # Orthopedic Reports
        {
            "id": "ortho_001",
            "filename": "Knee_MRI_Report_2024_03_10.pdf",
            "specialty": "Orthopedics", 
            "category": "Imaging",
            "hospital": "AIIMS Delhi",
            "doctor": "Dr. Vikram Singh",
            "date": "2024-03-10",
            "file_type": "pdf",
            "file_size": "6.2 MB",
            "summary": "MRI shows mild degenerative changes in medial meniscus",
            "key_findings": ["Grade 1 meniscal tear", "No ACL injury", "Mild joint effusion"],
            "tags": ["knee", "mri", "meniscus", "sports injury"],
            "upload_date": "2024-03-12T16:45:00Z"
        },
        {
            "id": "ortho_002",
            "filename": "Spine_X_Ray_2024_02_15.pdf",
            "specialty": "Orthopedics",
            "category": "X-Ray",
            "hospital": "Manipal Hospital Bangalore",
            "doctor": "Dr. Sunita Reddy",
            "date": "2024-02-15", 
            "file_type": "pdf",
            "file_size": "3.4 MB",
            "summary": "Lumbar spine X-ray shows mild disc space narrowing at L4-L5",
            "key_findings": ["L4-L5 disc narrowing", "No fractures", "Normal alignment"],
            "tags": ["spine", "back pain", "disc", "lumbar"],
            "upload_date": "2024-02-16T11:30:00Z"
        },
        
        # Neurology Reports
        {
            "id": "neuro_001",
            "filename": "Brain_MRI_Report_2024_03_05.pdf",
            "specialty": "Neurology",
            "category": "Imaging", 
            "hospital": "Medanta Hospital Gurgaon",
            "doctor": "Dr. Ravi Kumar",
            "date": "2024-03-05",
            "file_type": "pdf",
            "file_size": "8.1 MB",
            "summary": "Brain MRI shows no acute abnormalities, age-appropriate changes",
            "key_findings": ["No acute lesions", "Normal ventricles", "Mild white matter changes"],
            "tags": ["brain", "mri", "headache", "neurology"],
            "upload_date": "2024-03-07T13:20:00Z"
        },
        {
            "id": "neuro_002",
            "filename": "EEG_Report_2024_01_30.pdf",
            "specialty": "Neurology",
            "category": "Diagnostic Test",
            "hospital": "Kokilaben Hospital Mumbai", 
            "doctor": "Dr. Meera Sharma",
            "date": "2024-01-30",
            "file_type": "pdf",
            "file_size": "2.7 MB",
            "summary": "EEG shows normal background activity, no epileptiform discharges",
            "key_findings": ["Normal alpha rhythm", "No seizure activity", "Good sleep patterns"],
            "tags": ["eeg", "seizure", "brain waves", "sleep"],
            "upload_date": "2024-02-01T10:15:00Z"
        },
        
        # Endocrinology Reports
        {
            "id": "endo_001",
            "filename": "Thyroid_Function_Test_2024_03_20.pdf",
            "specialty": "Endocrinology",
            "category": "Lab Report",
            "hospital": "SRL Diagnostics",
            "doctor": "Dr. Anjali Gupta",
            "date": "2024-03-20",
            "file_type": "pdf", 
            "file_size": "1.2 MB",
            "summary": "Thyroid function tests within normal limits",
            "key_findings": ["TSH: 2.1 mIU/L", "T3: 1.2 ng/mL", "T4: 8.5 μg/dL"],
            "tags": ["thyroid", "hormone", "metabolism", "lab"],
            "upload_date": "2024-03-21T08:45:00Z"
        },
        {
            "id": "endo_002",
            "filename": "HbA1c_Diabetes_Panel_2024_02_25.pdf",
            "specialty": "Endocrinology",
            "category": "Lab Report",
            "hospital": "Dr Lal PathLabs",
            "doctor": "Dr. Suresh Patel",
            "date": "2024-02-25",
            "file_type": "pdf",
            "file_size": "0.9 MB", 
            "summary": "HbA1c slightly elevated, suggests pre-diabetes",
            "key_findings": ["HbA1c: 5.8%", "Fasting glucose: 105 mg/dL", "PPBS: 145 mg/dL"],
            "tags": ["diabetes", "glucose", "hba1c", "prediabetes"],
            "upload_date": "2024-02-26T15:30:00Z"
        },
        
        # Gastroenterology Reports
        {
            "id": "gastro_001",
            "filename": "Colonoscopy_Report_2024_01_15.pdf",
            "specialty": "Gastroenterology",
            "category": "Procedure Report",
            "hospital": "Asian Institute of Gastroenterology",
            "doctor": "Dr. Ramesh Babu",
            "date": "2024-01-15",
            "file_type": "pdf",
            "file_size": "3.8 MB",
            "summary": "Colonoscopy shows normal mucosa, no polyps detected",
            "key_findings": ["Normal colonic mucosa", "No polyps", "Good bowel prep"],
            "tags": ["colonoscopy", "colon", "screening", "polyps"],
            "upload_date": "2024-01-16T12:00:00Z"
        },
        
        # Pulmonology Reports  
        {
            "id": "pulmo_001",
            "filename": "Chest_CT_Report_2024_02_10.pdf",
            "specialty": "Pulmonology",
            "category": "Imaging",
            "hospital": "Chest Research Foundation Pune",
            "doctor": "Dr. Zarir Udwadia",
            "date": "2024-02-10",
            "file_type": "pdf",
            "file_size": "5.6 MB",
            "summary": "HRCT chest shows no active pulmonary disease",
            "key_findings": ["Clear lung fields", "No nodules", "Normal mediastinum"],
            "tags": ["chest", "lungs", "ct scan", "respiratory"],
            "upload_date": "2024-02-12T14:25:00Z"
        },
        {
            "id": "pulmo_002",
            "filename": "Pulmonary_Function_Test_2024_03_01.pdf",
            "specialty": "Pulmonology", 
            "category": "Diagnostic Test",
            "hospital": "Narayana Health Bangalore",
            "doctor": "Dr. Sheetu Singh",
            "date": "2024-03-01",
            "file_type": "pdf",
            "file_size": "2.1 MB",
            "summary": "PFT shows normal lung function, no obstruction",
            "key_findings": ["FEV1: 95% predicted", "FVC: 98% predicted", "Normal flow rates"],
            "tags": ["pft", "lung function", "breathing", "spirometry"],
            "upload_date": "2024-03-03T09:40:00Z"
        }
    ],
    "file_categories": [
        {"id": "lab_reports", "name": "Lab Reports", "count": 15, "icon": "🧪"},
        {"id": "imaging", "name": "Medical Imaging", "count": 8, "icon": "🏥"},
        {"id": "diagnostic_tests", "name": "Diagnostic Tests", "count": 6, "icon": "📊"},
        {"id": "procedure_reports", "name": "Procedure Reports", "count": 4, "icon": "⚕️"},
        {"id": "prescriptions", "name": "Prescriptions", "count": 12, "icon": "💊"},
        {"id": "discharge_summaries", "name": "Discharge Summaries", "count": 3, "icon": "📋"}
    ],
    "specialties": [
        {"id": "cardiology", "name": "Cardiology", "count": 8, "color": "#ef4444"},
        {"id": "orthopedics", "name": "Orthopedics", "count": 6, "color": "#f97316"},
        {"id": "neurology", "name": "Neurology", "count": 4, "color": "#8b5cf6"},
        {"id": "endocrinology", "name": "Endocrinology", "count": 5, "color": "#06b6d4"},
        {"id": "gastroenterology", "name": "Gastroenterology", "count": 3, "color": "#10b981"},
        {"id": "pulmonology", "name": "Pulmonology", "count": 4, "color": "#f59e0b"},
        {"id": "dermatology", "name": "Dermatology", "count": 2, "color": "#ec4899"},
        {"id": "ophthalmology", "name": "Ophthalmology", "count": 2, "color": "#84cc16"}
    ],
    "recommended_actions": [
        {"id": 1, "title": "Start Zone 2 cardio training", "category": "fitness", "priority": "high", "reason": "Improve mitochondrial function and VO2 max for longevity"},
        {"id": 2, "title": "Optimize sleep to 7-8 hours", "category": "lifestyle", "priority": "high", "reason": "Critical for growth hormone release and cellular repair"},
        {"id": 3, "title": "Add resistance training 3x/week", "category": "fitness", "priority": "high", "reason": "Maintain muscle mass and bone density as you age"},
        {"id": 4, "title": "Take Vitamin D3 2000 IU daily", "category": "nutrition", "priority": "high", "reason": "Deficiency linked to increased mortality risk"},
        {"id": 5, "title": "Practice intermittent fasting", "category": "nutrition", "priority": "medium", "reason": "Activate autophagy and improve metabolic flexibility"},
        {"id": 6, "title": "Add omega-3 supplement", "category": "nutrition", "priority": "medium", "reason": "Reduce inflammation and support brain health"},
        {"id": 7, "title": "Monitor HRV daily", "category": "lifestyle", "priority": "medium", "reason": "Track autonomic nervous system health and recovery"},
        {"id": 8, "title": "Cold exposure therapy", "category": "lifestyle", "priority": "low", "reason": "Boost brown fat and improve stress resilience"}
    ],
    "health_metrics": [
        {"id": "hba1c", "name": "HbA1c", "value": 5.8, "unit": "%", "status": "borderline", "optimal": "< 5.7"},
        {"id": "total_cholesterol", "name": "Total Cholesterol", "value": 195, "unit": "mg/dL", "status": "normal", "optimal": "< 200"},
        {"id": "hdl", "name": "HDL Cholesterol", "value": 42, "unit": "mg/dL", "status": "low", "optimal": "> 50"},
        {"id": "ldl", "name": "LDL Cholesterol", "value": 128, "unit": "mg/dL", "status": "normal", "optimal": "< 130"},
        {"id": "triglycerides", "name": "Triglycerides", "value": 145, "unit": "mg/dL", "status": "normal", "optimal": "< 150"},
        {"id": "vitamin_d", "name": "Vitamin D", "value": 28, "unit": "ng/mL", "status": "deficient", "optimal": "> 30"},
        {"id": "vitamin_b12", "name": "Vitamin B12", "value": 320, "unit": "pg/mL", "status": "normal", "optimal": "> 300"},
        {"id": "crp", "name": "C-Reactive Protein", "value": 0.8, "unit": "mg/L", "status": "low", "optimal": "< 1.0"},
        {"id": "testosterone", "name": "Testosterone", "value": 485, "unit": "ng/dL", "status": "normal", "optimal": "300-1000"},
        {"id": "vo2_max", "name": "VO2 Max", "value": 42, "unit": "mL/kg/min", "status": "good", "optimal": "> 40"},
        {"id": "resting_hr", "name": "Resting Heart Rate", "value": 58, "unit": "bpm", "status": "excellent", "optimal": "< 60"},
        {"id": "grip_strength", "name": "Grip Strength", "value": 48, "unit": "kg", "status": "good", "optimal": "> 45"},
        {"id": "body_fat", "name": "Body Fat Percentage", "value": 14.2, "unit": "%", "status": "excellent", "optimal": "10-15%"},
        {"id": "muscle_mass", "name": "Muscle Mass", "value": 72.5, "unit": "kg", "status": "good", "optimal": "> 70"},
        {"id": "bone_density", "name": "Bone Density T-Score", "value": 1.2, "unit": "SD", "status": "excellent", "optimal": "> 1.0"}
    ],
    "doctors": [
        {"id": 1, "name": "Dr. Rajesh Sharma", "specialty": "Longevity Medicine", "rating": 4.9, "location": "Delhi", "experience": "15 years"},
        {"id": 2, "name": "Dr. Priya Nair", "specialty": "Preventive Cardiology", "rating": 4.8, "location": "Mumbai", "experience": "12 years"},
        {"id": 3, "name": "Dr. Amit Gupta", "specialty": "Sports Medicine", "rating": 4.7, "location": "Bangalore", "experience": "18 years"},
        {"id": 4, "name": "Dr. Sunita Reddy", "specialty": "Functional Medicine", "rating": 4.9, "location": "Hyderabad", "experience": "10 years"},
        {"id": 5, "name": "Dr. Vikram Singh", "specialty": "Anti-Aging Medicine", "rating": 4.8, "location": "Gurgaon", "experience": "14 years"}
    ],
    "labs": [
        {"id": 1, "name": "SRL Diagnostics", "location": "Multiple locations", "rating": 4.6, "tests": ["Comprehensive Metabolic Panel", "Longevity Biomarkers", "Advanced Lipid Profile"]},
        {"id": 2, "name": "Dr. Lal PathLabs", "location": "Pan India", "rating": 4.5, "tests": ["Hormone Optimization Panel", "Micronutrient Analysis", "Inflammatory Markers"]},
        {"id": 3, "name": "Metropolis Healthcare", "location": "Major cities", "rating": 4.4, "tests": ["VO2 Max Testing", "Body Composition Analysis", "Genetic Testing"]},
        {"id": 4, "name": "Thyrocare", "location": "Home collection", "rating": 4.3, "tests": ["Full Body Checkup", "Vitamin D3", "Testosterone Panel"]},
        {"id": 5, "name": "Apollo Diagnostics", "location": "Premium centers", "rating": 4.7, "tests": ["Biological Age Assessment", "Telomere Length", "Advanced Cardiac Risk"]}
    ],
    "daily_routine": [
        {
            "step": "Morning Longevity Stack",
            "products": [
                {
                    "name": "Vitamin D3 + K2",
                    "description": "2000 IU with breakfast for bone health",
                    "image": "/src/assets/products/vitamins.jpg"
                },
                {
                    "name": "Omega-3 EPA/DHA",
                    "description": "2g daily for cardiovascular health",
                    "image": "/src/assets/products/omega3.jpg"
                }
            ]
        },
        {
            "step": "Exercise & Movement",
            "products": [
                {
                    "name": "Zone 2 Cardio",
                    "description": "45min at 180-age heart rate",
                    "image": "/src/assets/products/walking.jpg"
                },
                {
                    "name": "Resistance Training",
                    "description": "3x/week for muscle maintenance",
                    "image": "/src/assets/products/walking.jpg"
                }
            ]
        },
        {
            "step": "Supplements",
            "products": [
                {
                    "name": "Magnesium Glycinate",
                    "description": "400mg before bed for sleep quality",
                    "image": "/src/assets/products/vitamins.jpg"
                },
                {
                    "name": "Omega-3 Fish Oil",
                    "description": "Take 2 capsules daily",
                    "image": "/src/assets/products/omega3.jpg"
                },
                {
                    "name": "Probiotic",
                    "description": "Take 1 capsule before bed",
                    "image": "/src/assets/products/probiotic.jpg"
                }
            ]
        },
        {
            "step": "Wellness",
            "products": [
                {
                    "name": "8 Glasses of Water",
                    "description": "Stay hydrated throughout the day",
                    "image": "/src/assets/products/water.jpg"
                },
                {
                    "name": "10-Min Meditation",
                    "description": "Practice mindfulness daily",
                    "image": "/src/assets/products/meditation.jpg"
                }
            ]
        }
    ],
    "weekly_routine": [
        {
            "step": "Exercise",
            "products": [
                {
                    "name": "30-Minute Walk",
                    "description": "2 of 3 completed this week",
                    "image": "/src/assets/products/walking.jpg"
                }
            ]
        }
    ]
}

async def simulate_delay(ms: int = 200):
    await asyncio.sleep(ms / 1000)

@app.get("/")
def read_root():
    return {"message": "Aarogyadost Backend API", "version": "1.3.0", "focus": "longevity", "deployment_test": "s3_permissions_fixed"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/cors-info")
def cors_info():
    """Debug endpoint to check CORS configuration"""
    from cors_config import get_cors_info
    return get_cors_info()

@app.options("/health")
def health_check_options():
    return {"message": "OK"}

# Add OPTIONS handlers for main API endpoints
@app.options("/api/{path:path}")
def api_options(path: str):
    return {"message": "OK"}

# Health endpoints
@app.get("/api/health/biomarkers")
async def get_biomarkers():
    await simulate_delay(300)
    return mock_data["health_categories"]

@app.get("/api/health/recommendations")
async def get_recommendations():
    await simulate_delay(200)
    return mock_data["recommended_actions"]

@app.get("/api/health/metrics")
async def get_health_metrics():
    await simulate_delay(250)
    return mock_data["health_metrics"]

@app.get("/api/health/status")
async def get_health_status():
    await simulate_delay(300)
    return {
        "overall_score": 84,
        "age": 35,
        "biological_age": 32,
        "longevity_score": 87,
        "categories": mock_data["health_categories"],
        "key_insights": [
            "Your biological age is 3 years younger than chronological age - excellent progress!",
            "VO2 Max of 42 mL/kg/min puts you in top 25% for your age group",
            "Vitamin D deficiency needs immediate attention for optimal longevity",
            "HDL cholesterol could be improved with Zone 2 cardio training",
            "Excellent muscle mass and bone density for long-term health",
            "Low inflammation markers indicate effective lifestyle interventions"
        ],
        "last_updated": "2024-12-22T12:00:00Z"
    }

# Biomarker details
@app.get("/api/biomarkers/{biomarker_id}")
async def get_biomarker_details(biomarker_id: str):
    await simulate_delay(400)
    # Mock detailed biomarker data
    biomarker_details = {
        "metabolic": {
            "id": "metabolic",
            "name": "Metabolic Health",
            "current_value": 82,
            "trend": "stable",
            "history": [78, 80, 82],
            "key_markers": ["HbA1c: 5.8%", "Fasting Glucose: 92 mg/dL", "Insulin: 8.2 μU/mL", "HOMA-IR: 1.9"],
            "recommendations": ["Practice 16:8 intermittent fasting", "Add post-meal walks", "Consider berberine supplementation", "Monitor continuous glucose"]
        },
        "cardiovascular": {
            "id": "cardiovascular", 
            "name": "Heart Health",
            "current_value": 75,
            "trend": "needs_attention",
            "history": [78, 76, 75],
            "key_markers": ["VO2 Max: 42 mL/kg/min", "Resting HR: 58 bpm", "HDL: 42 mg/dL", "BP: 128/82 mmHg"],
            "recommendations": ["Zone 2 cardio 3x/week", "Add omega-3 supplements", "Monitor HRV daily", "Increase NEAT activities"]
        },
        "hormonal": {
            "id": "hormonal",
            "name": "Hormonal Balance", 
            "current_value": 88,
            "trend": "good",
            "history": [85, 87, 88],
            "key_markers": ["Testosterone: 485 ng/dL", "Free T: 12.5 pg/mL", "DHEA-S: 350 μg/dL", "Cortisol: 12 μg/dL"],
            "recommendations": ["Maintain 7-8 hours sleep", "Zinc and magnesium supplementation", "Regular strength training", "Manage stress levels"]
        },
        "inflammation": {
            "id": "inflammation",
            "name": "Inflammation Markers",
            "current_value": 92,
            "trend": "excellent", 
            "history": [88, 90, 92],
            "key_markers": ["CRP: 0.8 mg/L", "ESR: 8 mm/hr", "IL-6: Low", "TNF-α: Normal"],
            "recommendations": ["Continue anti-inflammatory diet", "Maintain current exercise routine", "Consider curcumin supplementation"]
        },
        "liver": {
            "id": "liver",
            "name": "Liver Function",
            "current_value": 85,
            "trend": "good",
            "history": [82, 84, 85],
            "key_markers": ["ALT: 22 U/L", "AST: 24 U/L", "GGT: 18 U/L", "Bilirubin: 0.9 mg/dL"],
            "recommendations": ["Limit alcohol to 2 drinks/week", "Add milk thistle supplement", "Maintain healthy weight"]
        },
        "kidney": {
            "id": "kidney",
            "name": "Kidney Function",
            "current_value": 95,
            "trend": "excellent",
            "history": [93, 94, 95],
            "key_markers": ["Creatinine: 0.9 mg/dL", "eGFR: >90", "BUN: 15 mg/dL", "Microalbumin: Normal"],
            "recommendations": ["Maintain adequate hydration", "Monitor blood pressure", "Continue current lifestyle"]
        }
    }
    
    if biomarker_id not in biomarker_details:
        raise HTTPException(status_code=404, detail="Biomarker not found")
    
    return biomarker_details[biomarker_id]

# Doctors
@app.get("/api/doctors")
async def get_doctors():
    await simulate_delay(300)
    return mock_data["doctors"]

@app.get("/api/doctors/{doctor_id}")
async def get_doctor_details(doctor_id: int):
    await simulate_delay(200)
    doctor = next((d for d in mock_data["doctors"] if d["id"] == doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# Labs
@app.get("/api/labs")
async def get_labs():
    await simulate_delay(250)
    return mock_data["labs"]

@app.get("/api/labs/{lab_id}")
async def get_lab_details(lab_id: int):
    await simulate_delay(200)
    lab = next((l for l in mock_data["labs"] if l["id"] == lab_id), None)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab

# Chat endpoints
@app.get("/api/chat/threads")
async def get_chat_threads():
    await simulate_delay(200)
    return [
        {"id": 1, "title": "Longevity Protocol Review", "last_message": "Your biological age assessment shows excellent progress", "timestamp": "2024-12-22T10:00:00Z"},
        {"id": 2, "title": "VO2 Max Optimization", "last_message": "Zone 2 training plan for improving cardiovascular fitness", "timestamp": "2024-12-21T15:30:00Z"},
        {"id": 3, "title": "Hormone Optimization", "last_message": "Testosterone levels are good, focus on sleep quality", "timestamp": "2024-12-20T09:15:00Z"},
        {"id": 4, "title": "Supplement Stack Review", "last_message": "Vitamin D3, Omega-3, and Magnesium recommendations", "timestamp": "2024-12-19T14:20:00Z"}
    ]

@app.post("/api/chat/message")
async def send_chat_message(message: dict):
    await simulate_delay(500)
    user_message = message.get("text", "").lower()
    file_id = message.get("fileId")  # Optional file context
    
    # Get file context if provided
    file_context = None
    if file_id:
        file_context = next((f for f in mock_data["medical_files"] if f["id"] == file_id), None)
    
    # Enhanced response logic with file context
    if file_context:
        # File-specific responses
        specialty = file_context["specialty"].lower()
        category = file_context["category"].lower()
        
        if "explain" in user_message or "what does" in user_message:
            if specialty == "cardiology":
                response = f"Based on your {file_context['category']} from {file_context['hospital']}, let me explain the key findings: {', '.join(file_context['key_findings'][:2])}. This indicates your cardiovascular health status and any areas that need attention."
            elif specialty == "endocrinology":
                response = f"Your {file_context['category']} shows important metabolic markers. The key findings: {', '.join(file_context['key_findings'][:2])}. These values help assess your hormonal balance and metabolic health for longevity optimization."
            elif specialty == "orthopedics":
                response = f"This {file_context['category']} from {file_context['hospital']} reveals: {', '.join(file_context['key_findings'][:2])}. For longevity, maintaining bone and joint health is crucial for mobility and quality of life as you age."
            else:
                response = f"Your {file_context['category']} from {file_context['date']} shows: {file_context['summary']}. Key findings include: {', '.join(file_context['key_findings'][:2])}. This is important for your overall health assessment."
        
        elif "recommend" in user_message or "what should" in user_message:
            if specialty == "cardiology":
                response = f"Based on your cardiac assessment, I recommend: 1) Zone 2 cardio training 3x/week to improve VO2 max, 2) Omega-3 supplementation (2g EPA/DHA daily), 3) Monitor HRV for recovery tracking, 4) Consider CoQ10 for heart health."
            elif specialty == "endocrinology":
                response = f"For optimal metabolic health based on your results: 1) Implement 16:8 intermittent fasting, 2) Add post-meal walks to improve glucose response, 3) Consider berberine or metformin, 4) Prioritize 7-8 hours of quality sleep for hormone optimization."
            elif specialty == "orthopedics":
                response = f"To support your musculoskeletal health: 1) Resistance training 3x/week to maintain bone density, 2) Adequate protein intake (1.6g/kg body weight), 3) Vitamin D3 + K2 supplementation, 4) Consider collagen peptides for joint health."
            else:
                response = f"Based on your {specialty} report, focus on: 1) Regular monitoring of the identified markers, 2) Lifestyle interventions specific to your condition, 3) Follow-up with your specialist as recommended, 4) Maintain a longevity-focused lifestyle."
        
        elif "concern" in user_message or "worried" in user_message:
            response = f"I understand your concerns about the {file_context['category']} results. The findings '{', '.join(file_context['key_findings'][:1])}' are manageable with proper intervention. Your doctor {file_context['doctor']} at {file_context['hospital']} is the best person to discuss treatment options and next steps."
        
        elif "normal" in user_message or "good" in user_message:
            response = f"Yes, many aspects of your {file_context['category']} appear within normal ranges. The summary states: {file_context['summary']}. This is positive for your longevity goals. Continue your current health optimization strategies and regular monitoring."
        
        else:
            # Default file-specific response
            response = f"I'm analyzing your {file_context['category']} from {file_context['hospital']} dated {file_context['date']}. The report shows: {file_context['summary']}. Key findings include: {', '.join(file_context['key_findings'][:2])}. What specific aspect would you like me to explain or provide recommendations for?"
    
    else:
        # General health responses (existing logic)
        if "vitamin d" in user_message:
            response = "Your Vitamin D level at 28 ng/mL is deficient. For longevity optimization, I recommend 2000-4000 IU daily with K2, plus 15-20 minutes morning sunlight exposure."
        elif "hba1c" in user_message or "diabetes" in user_message:
            response = "Your HbA1c of 5.8% is in the pre-diabetic range. For longevity, implement 16:8 intermittent fasting, post-meal walks, and consider berberine supplementation."
        elif "cholesterol" in user_message or "hdl" in user_message:
            response = "Your HDL at 42 mg/dL needs improvement for cardiovascular longevity. Add Zone 2 cardio 3x/week, omega-3 supplements, and increase NEAT activities."
        elif "exercise" in user_message or "vo2" in user_message:
            response = "Your VO2 Max of 42 mL/kg/min is good but can improve. Focus on Zone 2 cardio (180-age formula) for 45min, 3x/week for longevity benefits."
        elif "testosterone" in user_message or "hormone" in user_message:
            response = "Your testosterone at 485 ng/dL is healthy. Maintain with 7-8 hours sleep, zinc/magnesium supplementation, and regular strength training."
        elif "longevity" in user_message or "aging" in user_message:
            response = "Your biological age is 3 years younger than chronological age! Focus on: Zone 2 cardio, strength training, sleep optimization, and stress management."
        elif "supplement" in user_message:
            response = "Based on your labs, prioritize: Vitamin D3 (2000 IU), Omega-3 (2g EPA/DHA), Magnesium Glycinate (400mg), and consider NMN for longevity."
        else:
            response = "Your longevity profile shows excellent potential. Key focus areas: fix vitamin D deficiency, improve HDL with cardio, maintain muscle mass, and optimize sleep quality."
    
    return {
        "id": 123,
        "message": message.get("text", ""),
        "response": response,
        "timestamp": "2024-12-22T12:00:00Z"
    }

# Medical Files endpoints
@app.get("/api/medical-files/categories")
async def get_file_categories():
    await simulate_delay(150)
    return mock_data["file_categories"]

@app.get("/api/medical-files/specialties")
async def get_specialties():
    await simulate_delay(150)
    return mock_data["specialties"]

@app.get("/api/medical-files/by-specialty/{specialty}")
async def get_files_by_specialty(specialty: str):
    await simulate_delay(250)
    files = [f for f in mock_data["medical_files"] if f["specialty"].lower() == specialty.lower()]
    files = sorted(files, key=lambda x: x["upload_date"], reverse=True)
    return files

@app.get("/api/medical-files/by-category/{category}")
async def get_files_by_category(category: str):
    await simulate_delay(250)
    files = [f for f in mock_data["medical_files"] if f["category"].lower().replace(" ", "_") == category.lower()]
    files = sorted(files, key=lambda x: x["upload_date"], reverse=True)
    return files

@app.get("/api/medical-files")
async def get_medical_files(specialty: str = None, category: str = None, limit: int = 20):
    await simulate_delay(300)
    files = mock_data["medical_files"]
    
    # Filter by specialty if provided
    if specialty:
        files = [f for f in files if f["specialty"].lower() == specialty.lower()]
    
    # Filter by category if provided  
    if category:
        files = [f for f in files if f["category"].lower() == category.lower()]
    
    # Sort by upload date (newest first)
    files = sorted(files, key=lambda x: x["upload_date"], reverse=True)
    
    return files[:limit]

@app.get("/api/medical-files/{file_id}")
async def get_medical_file_details(file_id: str):
    await simulate_delay(200)
    file_detail = next((f for f in mock_data["medical_files"] if f["id"] == file_id), None)
    if not file_detail:
        raise HTTPException(status_code=404, detail="Medical file not found")
    return file_detail

@app.post("/api/medical-files/upload")
async def upload_medical_file(file_data: dict):
    await simulate_delay(1000)
    # Simulate file upload processing
    return {
        "id": f"upload_{len(mock_data['medical_files']) + 1}",
        "status": "uploaded",
        "filename": file_data.get("filename", "unknown.pdf"),
        "message": "File uploaded and processed successfully",
        "processing_status": "completed",
        "extracted_data": {
            "specialty": "Auto-detected from content",
            "key_findings": ["Extracted from OCR/AI analysis"],
            "summary": "AI-generated summary of the medical report"
        },
        "timestamp": "2024-12-22T12:00:00Z"
    }

# Metric details endpoint
@app.get("/api/metrics/{metric_id}")
async def get_metric_details(metric_id: str):
    await simulate_delay(400)
    
    # Mock detailed metric data
    metric_details = {
        "cholesterol": {
            "id": "cholesterol",
            "title": "Cholesterol Panel",
            "subtitle": "Last 12 months trend",
            "status": "attention",
            "metrics": [
                {"name": "Total", "value": "186", "normalRange": "< 200", "color": "#3B82F6"},
                {"name": "LDL", "value": "107", "normalRange": "< 100", "color": "#F97316"},
                {"name": "HDL", "value": "67", "normalRange": "> 40", "color": "#22C55E"},
                {"name": "Triglycerides", "value": "121", "normalRange": "< 150", "color": "#EAB308"},
            ],
            "chartData": [
                {"date": "Jan 20", "total": 190, "ldl": 120, "hdl": 55, "triglycerides": 58},
                {"date": "Jul 20", "total": 195, "ldl": 110, "hdl": 60, "triglycerides": 155},
                {"date": "Jan 21", "total": 200, "ldl": 115, "hdl": 55, "triglycerides": 145},
                {"date": "Jul 21", "total": 220, "ldl": 118, "hdl": 65, "triglycerides": 160},
                {"date": "Jan 22", "total": 185, "ldl": 125, "hdl": 58, "triglycerides": 150},
                {"date": "Jul 22", "total": 210, "ldl": 112, "hdl": 55, "triglycerides": 175},
                {"date": "Jan 23", "total": 205, "ldl": 108, "hdl": 70, "triglycerides": 145},
                {"date": "Jul 23", "total": 210, "ldl": 105, "hdl": 55, "triglycerides": 140},
                {"date": "Jan 24", "total": 200, "ldl": 118, "hdl": 60, "triglycerides": 135},
                {"date": "Jul 24", "total": 215, "ldl": 105, "hdl": 65, "triglycerides": 125},
                {"date": "Jan 25", "total": 220, "ldl": 102, "hdl": 68, "triglycerides": 118},
                {"date": "Jul 25", "total": 186, "ldl": 107, "hdl": 67, "triglycerides": 121},
            ],
            "chartLines": [
                {"key": "total", "name": "Total", "color": "#3B82F6"},
                {"key": "ldl", "name": "LDL", "color": "#F97316"},
                {"key": "hdl", "name": "HDL", "color": "#22C55E"},
                {"key": "triglycerides", "name": "Triglycerides", "color": "#EAB308"},
            ],
        },
        "hba1c": {
            "id": "hba1c",
            "title": "HbA1c",
            "subtitle": "Last 6 months trend",
            "status": "borderline",
            "metrics": [
                {"name": "HbA1c", "value": "5.8", "normalRange": "< 5.7", "color": "#F97316"},
            ],
            "chartData": [
                {"date": "Jun", "hba1c": 5.5},
                {"date": "Jul", "hba1c": 5.6},
                {"date": "Aug", "hba1c": 5.6},
                {"date": "Sep", "hba1c": 5.7},
                {"date": "Oct", "hba1c": 5.7},
                {"date": "Nov", "hba1c": 5.8},
            ],
            "chartLines": [
                {"key": "hba1c", "name": "HbA1c", "color": "#F97316"},
            ],
        },
        "vitamin_d": {
            "id": "vitamin_d",
            "title": "Vitamin D",
            "subtitle": "Last 6 months trend",
            "status": "deficient",
            "metrics": [
                {"name": "Level", "value": "28", "normalRange": "30-100", "color": "#EF4444"},
            ],
            "chartData": [
                {"date": "Jun", "level": 22},
                {"date": "Jul", "level": 24},
                {"date": "Aug", "level": 26},
                {"date": "Sep", "level": 28},
                {"date": "Oct", "level": 29},
                {"date": "Nov", "level": 28},
            ],
            "chartLines": [
                {"key": "level", "name": "Vitamin D", "color": "#EF4444"},
            ],
        }
    }
    
    if metric_id not in metric_details:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    return metric_details[metric_id]

# Action details endpoint
@app.get("/api/actions/{action_id}")
async def get_action_details(action_id: str):
    await simulate_delay(300)
    
    # Mock detailed action data
    action_details = {
        "1": {
            "id": "1",
            "title": "Start Zone 2 cardio training",
            "icon": "Activity",
            "color": "bg-green-500",
            "overview": "Zone 2 cardio training is a low-intensity exercise method that improves mitochondrial function and VO2 max, which are key markers for longevity and metabolic health.",
            "benefits": [
                "Improves mitochondrial function and density",
                "Increases VO2 max and cardiovascular fitness",
                "Enhances fat oxidation and metabolic flexibility",
                "Reduces risk of cardiovascular disease by up to 35%",
                "Supports healthy aging and longevity"
            ],
            "howItHelps": "Your current VO2 max of 42 mL/kg/min is good but can be improved. Zone 2 training specifically targets the aerobic energy system, building more efficient mitochondria and improving your body's ability to use oxygen. This type of training is particularly effective for longevity because it enhances the cellular machinery responsible for energy production.",
            "nextSteps": [
                "Calculate your Zone 2 heart rate (180 minus your age)",
                "Start with 30-minute sessions, 2-3 times per week",
                "Maintain conversational pace throughout the workout",
                "Gradually increase duration to 45-60 minutes",
                "Monitor heart rate to stay in Zone 2 range"
            ],
            "isTodo": True,
            "todoItems": [
                {"label": "Calculate your Zone 2 heart rate range", "checked": False},
                {"label": "Choose your preferred Zone 2 activity (walking, cycling, swimming)", "checked": False},
                {"label": "Schedule 3 weekly Zone 2 sessions in your calendar", "checked": False},
                {"label": "Get a heart rate monitor or fitness tracker", "checked": False},
                {"label": "Complete your first 30-minute Zone 2 session", "checked": False}
            ],
            "personalizedSummary": {
                "improving": [
                    {"label": "Current VO2 Max", "detail": "42 mL/kg/min - good for your age group"},
                    {"label": "Resting Heart Rate", "detail": "58 bpm - excellent cardiovascular fitness indicator"}
                ],
                "declining": [
                    {"label": "Cardiovascular Endurance", "detail": "Could benefit from structured aerobic training"},
                    {"label": "Mitochondrial Efficiency", "detail": "Zone 2 training will optimize cellular energy production"}
                ]
            }
        },
        "2": {
            "id": "2",
            "title": "Optimize sleep to 7-8 hours",
            "icon": "Moon",
            "color": "bg-purple-500",
            "overview": "Quality sleep is critical for growth hormone release, cellular repair, and longevity. Optimizing sleep duration and quality can significantly impact your biological age and overall health.",
            "benefits": [
                "Enhances growth hormone release for cellular repair",
                "Improves cognitive function and memory consolidation",
                "Supports immune system function",
                "Regulates metabolism and weight management",
                "Reduces inflammation and oxidative stress"
            ],
            "howItHelps": "Your current sleep patterns may be impacting your recovery and longevity potential. During deep sleep, your body releases growth hormone, clears metabolic waste from the brain, and repairs cellular damage. Consistent 7-8 hours of quality sleep is one of the most powerful longevity interventions available.",
            "nextSteps": [
                "Set a consistent bedtime and wake time",
                "Create a sleep-conducive environment (cool, dark, quiet)",
                "Establish a relaxing bedtime routine",
                "Limit screen time 1 hour before bed",
                "Track your sleep quality and duration"
            ],
            "isTodo": True,
            "todoItems": [
                {"label": "Set a consistent bedtime (aim for 7-8 hours before wake time)", "checked": False},
                {"label": "Install blackout curtains or use an eye mask", "checked": False},
                {"label": "Remove electronic devices from bedroom", "checked": False},
                {"label": "Create a 30-minute wind-down routine", "checked": False},
                {"label": "Track sleep for one week to establish baseline", "checked": False}
            ]
        },
        "cardiologist": {
            "id": "cardiologist",
            "title": "Cardiologist Visit",
            "icon": "Stethoscope",
            "color": "bg-red-500",
            "overview": "Based on your health data, a visit to a cardiologist is recommended to evaluate your cardiovascular health and address any potential concerns.",
            "benefits": [
                "Comprehensive heart health evaluation",
                "Early detection of cardiovascular issues",
                "Personalized treatment and prevention plan",
                "Peace of mind about your heart health"
            ],
            "howItHelps": "A cardiologist can perform detailed assessments including ECG, stress tests, and echocardiograms to get a complete picture of your heart health. Early intervention is key to preventing serious cardiovascular events.",
            "nextSteps": [],
            "isTodo": True,
            "todoItems": [
                {"label": "Find a cardiologist in your network", "checked": False, "link": "/find-cardiologist"},
                {"label": "Schedule an appointment", "checked": False},
                {"label": "Gather recent health records and test results", "checked": False},
                {"label": "Prepare list of symptoms and questions", "checked": False},
                {"label": "Note family history of heart disease", "checked": False},
                {"label": "List current medications and supplements", "checked": False}
            ],
            "personalizedSummary": {
                "improving": [
                    {"label": "Resting Heart Rate", "detail": "Down 5 bpm over last month"},
                    {"label": "Daily Steps", "detail": "Averaging 6,200 steps (up from 4,800)"}
                ],
                "declining": [
                    {"label": "Blood Pressure", "detail": "Elevated readings (138/88 avg)"},
                    {"label": "Heart Rate Variability", "detail": "Below optimal range for your age"},
                    {"label": "Cholesterol (estimated)", "detail": "LDL trending higher based on lifestyle factors"}
                ]
            },
            "hasReport": True
        }
    }
    
    if action_id not in action_details:
        raise HTTPException(status_code=404, detail="Action not found")
    
    return action_details[action_id]

# Routine endpoints
@app.get("/api/routines/daily")
async def get_daily_routine():
    await simulate_delay(200)
    return mock_data["daily_routine"]

@app.get("/api/routines/weekly")
async def get_weekly_routine():
    await simulate_delay(200)
    return mock_data["weekly_routine"]