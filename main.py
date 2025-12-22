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
        {"id": 1, "title": "Add 30min morning walk", "category": "fitness", "priority": "high", "reason": "Improve HDL cholesterol levels"},
        {"id": 2, "title": "Reduce refined carbs intake", "category": "nutrition", "priority": "high", "reason": "HbA1c trending upward"},
        {"id": 3, "title": "Include omega-3 rich foods", "category": "nutrition", "priority": "medium", "reason": "Support heart health"},
        {"id": 4, "title": "Practice stress management", "category": "lifestyle", "priority": "medium", "reason": "Elevated cortisol levels"},
        {"id": 5, "title": "Improve sleep quality", "category": "lifestyle", "priority": "high", "reason": "Recovery and longevity"}
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
        {"id": "testosterone", "name": "Testosterone", "value": 485, "unit": "ng/dL", "status": "normal", "optimal": "300-1000"}
    ],
    "doctors": [
        {"id": 1, "name": "Dr. Rajesh Sharma", "specialty": "Preventive Medicine", "rating": 4.9, "location": "Delhi", "experience": "15 years"},
        {"id": 2, "name": "Dr. Priya Nair", "specialty": "Endocrinology", "rating": 4.8, "location": "Mumbai", "experience": "12 years"},
        {"id": 3, "name": "Dr. Amit Gupta", "specialty": "Cardiology", "rating": 4.7, "location": "Bangalore", "experience": "18 years"},
        {"id": 4, "name": "Dr. Sunita Reddy", "specialty": "Functional Medicine", "rating": 4.9, "location": "Hyderabad", "experience": "10 years"}
    ],
    "labs": [
        {"id": 1, "name": "SRL Diagnostics", "location": "Multiple locations", "rating": 4.6, "tests": ["Complete Blood Count", "Lipid Profile", "HbA1c"]},
        {"id": 2, "name": "Dr. Lal PathLabs", "location": "Pan India", "rating": 4.5, "tests": ["Comprehensive Metabolic Panel", "Hormone Panel"]},
        {"id": 3, "name": "Metropolis Healthcare", "location": "Major cities", "rating": 4.4, "tests": ["Advanced Cardiac Risk", "Vitamin Panel"]},
        {"id": 4, "name": "Thyrocare", "location": "Home collection", "rating": 4.3, "tests": ["Full Body Checkup", "Thyroid Profile"]}
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
            "Your biological age is 3 years younger than chronological age",
            "Vitamin D deficiency needs immediate attention",
            "HDL cholesterol could be improved with exercise",
            "Excellent inflammation markers indicate good lifestyle choices"
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
            "key_markers": ["HbA1c: 5.8%", "Fasting Glucose: 92 mg/dL", "Insulin: 8.2 μU/mL"],
            "recommendations": ["Reduce refined carbs", "Add post-meal walks", "Consider intermittent fasting"]
        },
        "cardiovascular": {
            "id": "cardiovascular", 
            "name": "Heart Health",
            "current_value": 75,
            "trend": "needs_attention",
            "history": [78, 76, 75],
            "key_markers": ["HDL: 42 mg/dL", "LDL: 128 mg/dL", "BP: 128/82 mmHg"],
            "recommendations": ["Increase cardio exercise", "Add omega-3 supplements", "Monitor blood pressure"]
        },
        "hormonal": {
            "id": "hormonal",
            "name": "Hormonal Balance", 
            "current_value": 88,
            "trend": "good",
            "history": [85, 87, 88],
            "key_markers": ["Testosterone: 485 ng/dL", "Thyroid TSH: 2.1 mIU/L", "Cortisol: 12 μg/dL"],
            "recommendations": ["Maintain sleep schedule", "Manage stress levels", "Regular strength training"]
        },
        "inflammation": {
            "id": "inflammation",
            "name": "Inflammation Markers",
            "current_value": 92,
            "trend": "excellent", 
            "history": [88, 90, 92],
            "key_markers": ["CRP: 0.8 mg/L", "ESR: 8 mm/hr", "IL-6: Low"],
            "recommendations": ["Continue anti-inflammatory diet", "Maintain current exercise routine"]
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
        {"id": 1, "title": "Lab Report Analysis", "last_message": "Your HbA1c levels show pre-diabetic range", "timestamp": "2024-12-22T10:00:00Z"},
        {"id": 2, "title": "Longevity Optimization", "last_message": "Best supplements for Indian diet?", "timestamp": "2024-12-21T15:30:00Z"},
        {"id": 3, "title": "Exercise Planning", "last_message": "30min daily routine suggestions", "timestamp": "2024-12-20T09:15:00Z"}
    ]

@app.post("/api/chat/message")
async def send_chat_message(message: dict):
    await simulate_delay(500)
    user_message = message.get("text", "").lower()
    
    # Simple response logic based on keywords
    if "vitamin d" in user_message:
        response = "Your Vitamin D level at 28 ng/mL is deficient. I recommend 2000 IU daily supplementation and 15-20 minutes of morning sunlight exposure."
    elif "hba1c" in user_message or "diabetes" in user_message:
        response = "Your HbA1c of 5.8% is in the pre-diabetic range. Focus on reducing refined carbs, add post-meal walks, and consider intermittent fasting."
    elif "cholesterol" in user_message:
        response = "Your HDL at 42 mg/dL is low for optimal longevity. Increase cardio exercise, add nuts and olive oil to your diet."
    elif "exercise" in user_message:
        response = "For longevity at 35, combine 150min cardio weekly with 2-3 strength training sessions. Start with 30min morning walks."
    else:
        response = "Based on your recent lab reports, I recommend focusing on vitamin D supplementation, improving HDL cholesterol through exercise, and managing your pre-diabetic HbA1c levels."
    
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
            "HbA1c trending upward - monitor carb intake",
            "Vitamin D deficiency detected - supplement needed", 
            "HDL cholesterol below optimal - increase cardio",
            "Inflammation markers excellent - continue current lifestyle"
        ],
        "recommendations": mock_data["recommended_actions"][:3],
        "timestamp": "2024-12-22T12:00:00Z"
    }
