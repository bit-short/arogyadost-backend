# Aarogyadost API Documentation

## Base URL
```
Development: http://localhost:8000
Production: TBD
```

## Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Health Endpoints

### Get Health Biomarkers
```
GET /api/health/biomarkers
```

**Response:**
```json
[
  {
    "id": "metabolic",
    "name": "Metabolic Health",
    "status": "good",
    "score": 82
  }
]
```

**Status values:** `excellent`, `good`, `attention`, `critical`

---

### Get Health Recommendations
```
GET /api/health/recommendations
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Add 30min morning walk",
    "category": "fitness",
    "priority": "high",
    "reason": "Improve HDL cholesterol levels"
  }
]
```

**Categories:** `fitness`, `nutrition`, `lifestyle`  
**Priority:** `high`, `medium`, `low`

---

### Get Health Metrics
```
GET /api/health/metrics
```

**Response:**
```json
[
  {
    "id": "hba1c",
    "name": "HbA1c",
    "value": 5.8,
    "unit": "%",
    "status": "borderline",
    "optimal": "< 5.7"
  }
]
```

---

### Get Overall Health Status
```
GET /api/health/status
```

**Response:**
```json
{
  "overall_score": 84,
  "age": 35,
  "biological_age": 32,
  "longevity_score": 87,
  "categories": [...],
  "key_insights": [
    "Your biological age is 3 years younger than chronological age"
  ],
  "last_updated": "2024-12-22T12:00:00Z"
}
```

---

### Get Biomarker Details
```
GET /api/biomarkers/{biomarker_id}
```

**Path Parameters:**
- `biomarker_id`: `metabolic`, `cardiovascular`, `hormonal`, `inflammation`

**Response:**
```json
{
  "id": "metabolic",
  "name": "Metabolic Health",
  "current_value": 82,
  "trend": "stable",
  "history": [78, 80, 82],
  "key_markers": ["HbA1c: 5.8%", "Fasting Glucose: 92 mg/dL"],
  "recommendations": ["Reduce refined carbs", "Add post-meal walks"]
}
```

**Trend values:** `excellent`, `good`, `stable`, `needs_attention`, `declining`

---

## Doctors & Labs

### Get Doctors List
```
GET /api/doctors
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Dr. Rajesh Sharma",
    "specialty": "Preventive Medicine",
    "rating": 4.9,
    "location": "Delhi",
    "experience": "15 years"
  }
]
```

---

### Get Doctor Details
```
GET /api/doctors/{doctor_id}
```

**Path Parameters:**
- `doctor_id`: integer

**Response:** Same as single doctor object above

**Error Response (404):**
```json
{
  "detail": "Doctor not found"
}
```

---

### Get Labs List
```
GET /api/labs
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "SRL Diagnostics",
    "location": "Multiple locations",
    "rating": 4.6,
    "tests": ["Complete Blood Count", "Lipid Profile", "HbA1c"]
  }
]
```

---

### Get Lab Details
```
GET /api/labs/{lab_id}
```

**Path Parameters:**
- `lab_id`: integer

**Response:** Same as single lab object above

---

## Chat & AI Assistant

### Get Chat Threads
```
GET /api/chat/threads
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Lab Report Analysis",
    "last_message": "Your HbA1c levels show pre-diabetic range",
    "timestamp": "2024-12-22T10:00:00Z"
  }
]
```

---

### Send Chat Message
```
POST /api/chat/message
```

**Request Body:**
```json
{
  "text": "What should I do about my vitamin D levels?"
}
```

**Response:**
```json
{
  "id": 123,
  "message": "What should I do about my vitamin D levels?",
  "response": "Your Vitamin D level at 28 ng/mL is deficient. I recommend 2000 IU daily supplementation and 15-20 minutes of morning sunlight exposure.",
  "timestamp": "2024-12-22T12:00:00Z"
}
```

**Smart Keywords:** The AI responds contextually to: `vitamin d`, `hba1c`, `diabetes`, `cholesterol`, `exercise`

---

## Lab Reports

### Upload Lab Report
```
POST /api/lab-reports/upload
```

**Request Body:**
```json
{
  "report_data": "base64_encoded_pdf_or_json",
  "report_date": "2024-12-22",
  "lab_name": "SRL Diagnostics"
}
```

**Response:**
```json
{
  "id": 456,
  "status": "processed",
  "insights": [
    "HbA1c trending upward - monitor carb intake",
    "Vitamin D deficiency detected - supplement needed"
  ],
  "recommendations": [...],
  "timestamp": "2024-12-22T12:00:00Z"
}
```

---

## CORS Configuration

All origins are allowed in development. CORS headers included:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: *`
- `Access-Control-Allow-Headers: *`

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Response Times

All endpoints include simulated delays for realistic behavior:
- Health endpoints: 200-400ms
- Chat endpoints: 500ms
- Lab upload: 1000ms

---

## Notes for Frontend

1. **Base URL**: Use environment variable for base URL
2. **Authentication**: Not implemented yet (coming soon)
3. **Timestamps**: All timestamps in ISO 8601 format (UTC)
4. **IDs**: Biomarker IDs are strings, Doctor/Lab IDs are integers
5. **Status Colors**: 
   - `excellent`: Green
   - `good`: Light Green
   - `attention`: Yellow/Orange
   - `borderline`: Orange
   - `critical`: Red
   - `low`/`deficient`: Red

---

## Example Frontend Integration

```javascript
// Fetch health status
const response = await fetch('http://localhost:8000/api/health/status');
const data = await response.json();
console.log(data.overall_score); // 84

// Send chat message
const chatResponse = await fetch('http://localhost:8000/api/chat/message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Tell me about my vitamin D levels' })
});
const chatData = await chatResponse.json();
console.log(chatData.response);
```

---

## Contact

For API issues or questions, contact the backend team.
