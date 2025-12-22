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
        {"id": "cardiovascular", "name": "Cardiovascular", "status": "good", "score": 85},
        {"id": "metabolic", "name": "Metabolic", "status": "attention", "score": 72},
        {"id": "inflammation", "name": "Inflammation", "status": "good", "score": 88}
    ],
    "recommended_actions": [
        {"id": 1, "title": "Increase cardio exercise", "category": "fitness", "priority": "high"},
        {"id": 2, "title": "Reduce sugar intake", "category": "nutrition", "priority": "medium"}
    ],
    "health_metrics": [
        {"id": "cholesterol", "name": "Cholesterol", "value": 180, "unit": "mg/dL", "status": "normal"},
        {"id": "glucose", "name": "Blood Glucose", "value": 95, "unit": "mg/dL", "status": "normal"}
    ],
    "doctors": [
        {"id": 1, "name": "Dr. Smith", "specialty": "Cardiology", "rating": 4.8},
        {"id": 2, "name": "Dr. Johnson", "specialty": "Endocrinology", "rating": 4.9}
    ],
    "labs": [
        {"id": 1, "name": "Quest Diagnostics", "location": "Downtown", "rating": 4.5},
        {"id": 2, "name": "LabCorp", "location": "Uptown", "rating": 4.3}
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
        "overall_score": 82,
        "categories": mock_data["health_categories"],
        "last_updated": "2024-12-22T12:00:00Z"
    }

# Biomarker details
@app.get("/api/biomarkers/{biomarker_id}")
async def get_biomarker_details(biomarker_id: str):
    await simulate_delay(400)
    # Mock detailed biomarker data
    biomarker_details = {
        "cardiovascular": {
            "id": "cardiovascular",
            "name": "Cardiovascular Health",
            "current_value": 85,
            "trend": "improving",
            "history": [80, 82, 85],
            "recommendations": ["Increase cardio", "Monitor blood pressure"]
        },
        "metabolic": {
            "id": "metabolic", 
            "name": "Metabolic Health",
            "current_value": 72,
            "trend": "stable",
            "history": [70, 71, 72],
            "recommendations": ["Reduce sugar intake", "Increase fiber"]
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
        {"id": 1, "title": "Health Questions", "last_message": "How to improve sleep?", "timestamp": "2024-12-22T10:00:00Z"},
        {"id": 2, "title": "Nutrition Advice", "last_message": "Best foods for heart health", "timestamp": "2024-12-21T15:30:00Z"}
    ]

@app.post("/api/chat/message")
async def send_chat_message(message: dict):
    await simulate_delay(500)
    return {
        "id": 123,
        "message": message.get("text", ""),
        "response": "Thank you for your question. I'll help you with that.",
        "timestamp": "2024-12-22T12:00:00Z"
    }
