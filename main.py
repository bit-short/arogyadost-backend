from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from pathlib import Path

app = FastAPI(title="Aarogyadost API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    ]
}

async def simulate_delay(ms: int = 200):
    await asyncio.sleep(ms / 1000)

@app.get("/")
def read_root():
    return {"message": "Aarogyadost Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

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
    
    # Simple response logic based on keywords
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

# Lab report upload endpoint
@app.post("/api/lab-reports/upload")
async def upload_lab_report(report: dict):
    await simulate_delay(1000)
    return {
        "id": 456,
        "status": "processed",
        "insights": [
            "Biological age 3 years younger - excellent longevity trajectory",
            "VO2 Max in top 25% for age group - maintain cardio fitness", 
            "Vitamin D deficiency detected - critical for immune function and longevity",
            "HDL cholesterol suboptimal - Zone 2 training recommended",
            "Excellent muscle mass and bone density for aging resilience",
            "Low inflammation markers - continue anti-inflammatory lifestyle"
        ],
        "recommendations": mock_data["recommended_actions"][:3],
        "timestamp": "2024-12-22T12:00:00Z"
    }
