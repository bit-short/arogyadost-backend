# Aarogyadost API Documentation v2.0

## Base URLs
```
Local Development: http://localhost:8000
Development: https://api-dev.arogyadost.in
Production: https://api.arogyadost.in
```

## Interactive Documentation
- **Swagger UI (Local)**: http://localhost:8000/docs
- **Swagger UI (Dev)**: https://api-dev.arogyadost.in/docs
- **ReDoc (Local)**: http://localhost:8000/redoc
- **ReDoc (Dev)**: https://api-dev.arogyadost.in/redoc

---

## 🧬 Digital Twin API

### Create Digital Twin
```http
POST /api/digital-twin/users/{user_id}/create
```

**Response:**
```json
{
  "user_id": "user_123",
  "status": "created",
  "timestamp": "2024-01-08T03:30:00Z"
}
```

### Add Health Data
```http
POST /api/digital-twin/users/{user_id}/data
```

**Request Body:**
```json
{
  "domain": "biomarkers",
  "field": "cholesterol",
  "value": 220,
  "unit": "mg/dL",
  "test_date": "2024-01-08T00:00:00Z"
}
```

### Get User Profile
```http
GET /api/digital-twin/users/{user_id}/profile
```

**Response:**
```json
{
  "user_id": "user_123",
  "demographics": {
    "age": 29,
    "sex": "female"
  },
  "latest_biomarkers": {
    "cholesterol": {
      "value": 220,
      "unit": "mg/dL",
      "status": "high",
      "test_date": "2024-01-08T00:00:00Z"
    }
  },
  "conditions": ["Dyslipidemia"],
  "completeness": 75.5
}
```

---

## 🧠 Biological Age API

### Predict Biological Age
```http
POST /api/biological-age/users/{user_id}/predict
```

**Response:**
```json
{
  "user_id": "user_123",
  "chronological_age": 29,
  "biological_age": 27.3,
  "age_difference": -1.7,
  "confidence_score": 0.85,
  "category_ages": {
    "metabolic_age": 26.5,
    "cardiovascular_age": 28.1,
    "inflammatory_age": 27.8
  },
  "insights": [
    "Your biological age is 1.7 years younger than your chronological age",
    "Excellent metabolic health contributing to younger biological age"
  ]
}
```

---

## 💊 Health Recommendations API

### Get Personalized Recommendations
```http
GET /api/recommendations/{user_id}
```

**Response:**
```json
{
  "user_id": "user_123",
  "generated_at": "2024-01-08T03:30:00Z",
  "summary": {
    "total_recommendations": 6,
    "high_priority_count": 2,
    "medium_priority_count": 4,
    "low_priority_count": 0,
    "categories_covered": ["lipid_profile", "vitamins", "metabolic"]
  },
  "recommendations": [
    {
      "recommendation_id": "rec_001",
      "test_name": "Lipid Profile Retest",
      "test_category": "lipid_profile",
      "rationale": "Cholesterol is high (220 mg/dL) - follow-up needed",
      "priority": "high",
      "priority_score": 0.85,
      "suggested_timing": "within 1 month",
      "related_biomarkers": ["cholesterol", "ldl", "hdl"],
      "educational_context": "Regular lipid monitoring helps assess cardiovascular risk and treatment effectiveness"
    }
  ],
  "grouped_by_category": {
    "lipid_profile": [...],
    "vitamins": [...],
    "metabolic": [...]
  }
}
```

---

## 💬 Health Chat Assistant API

### Create Chat Session
```http
POST /api/chat/sessions?user_id={user_id}&title=Health Discussion
```

### Send Message with Streaming
```http
POST /api/chat/sessions/{session_id}/messages?user_id={user_id}
```

**Request Body:**
```json
{
  "message": "What should I know about my cholesterol levels?",
  "include_research": false
}
```

**Response (Server-Sent Events):**
```
data: {"type": "session_info", "data": {"session_id": "session_abc123"}}
data: {"type": "thinking", "data": "Analyzing your health data..."}
data: {"type": "token", "data": "Based "}
data: {"type": "token", "data": "on "}
data: {"type": "complete", "data": "Based on your recent test results..."}
data: {"type": "stream_end"}
```

### Send Simple Message (Non-Streaming)
```http
POST /api/chat/message?user_id={user_id}
```

**Request Body:**
```json
{
  "message": "Hello, I want to discuss my health",
  "session_id": "session_abc123"
}
```

**Response:**
```json
{
  "session_id": "session_abc123",
  "message": "Hello! I'm your health chat assistant. I have access to your health profile and can see you're managing Dyslipidemia. How can I help you with your health today?",
  "timestamp": "2024-01-08T03:30:00Z"
}
```

---

## ⚙️ Admin API

### Get LLM Configuration
```http
GET /api/admin/llm/config
```

### Update LLM Configuration
```http
PUT /api/admin/llm/config
```

**Request Body:**
```json
{
  "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
  "temperature": 0.5,
  "max_tokens": 1500
}
```

### List Available Models
```http
GET /api/admin/llm/models
```

### Test LLM Connection
```http
POST /api/admin/llm/test?test_prompt=Hello, how are you?
```

---

## 🚀 Getting Started

### 1. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Create a Digital Twin
```bash
# Local
curl -X POST "http://localhost:8000/api/digital-twin/users/user_123/create"

# Dev Environment
curl -X POST "https://api-dev.arogyadost.in/api/digital-twin/users/user_123/create"
```

### 3. Add Health Data
```bash
# Local
curl -X POST "http://localhost:8000/api/digital-twin/users/user_123/data" \
  -H "Content-Type: application/json" \
  -d '{"domain": "biomarkers", "field": "cholesterol", "value": 220, "unit": "mg/dL"}'

# Dev Environment  
curl -X POST "https://api-dev.arogyadost.in/api/digital-twin/users/user_123/data" \
  -H "Content-Type: application/json" \
  -d '{"domain": "biomarkers", "field": "cholesterol", "value": 220, "unit": "mg/dL"}'
```

### 4. Get Recommendations
```bash
# Local
curl "http://localhost:8000/api/recommendations/user_123"

# Dev Environment
curl "https://api-dev.arogyadost.in/api/recommendations/user_123"
```

### 5. Start Chat Session
```bash
# Local
curl -X POST "http://localhost:8000/api/chat/sessions?user_id=user_123&title=Health Chat"

# Dev Environment
curl -X POST "https://api-dev.arogyadost.in/api/chat/sessions?user_id=user_123&title=Health Chat"
```

---

## 💰 AWS Bedrock Costs

### Model Pricing (per 1K tokens)
- **Titan Text Lite**: $0.0003 input / $0.0004 output (~$0.81/month for 100 conversations/day)
- **Titan Text Express**: $0.0008 input / $0.0016 output
- **Claude 3 Haiku**: $0.00025 input / $0.00125 output

---

## 🧪 Test Users Available

- **user_001_29f** - 29F with comprehensive medical data
- **user_003_31m** - 31M with OCR medical data
- **user_004_31m** - 31M with OCR medical data
- **user_007_27f** - 27F with basic health package
- **user_009_26f** - 26F with women's health panel
- **user_011_34f** - 34F with comprehensive health package

---

**Last Updated:** January 8, 2024 | **API Version:** 2.0 | **Status:** ✅ Complete
