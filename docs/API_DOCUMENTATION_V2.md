# Aarogyadost API Documentation v2.0

## Base URLs
```
Development: http://localhost:8000
Production: https://api.arogyadost.in
```

## Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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

### Get Data Completeness
```http
GET /api/digital-twin/users/{user_id}/completeness
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

### Get Age Insights
```http
POST /api/biological-age/users/{user_id}/insights
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

### Get Recommendations Summary
```http
GET /api/recommendations/{user_id}/summary
```

---

## 💬 Health Chat Assistant API

### Create Chat Session
```http
POST /api/chat/sessions?user_id={user_id}&title=Health Discussion
```

**Response:**
```json
{
  "session_id": "session_abc123",
  "user_id": "user_123",
  "title": "Health Discussion",
  "created_at": "2024-01-08T03:30:00Z",
  "message_count": 0
}
```

### List Chat Sessions
```http
GET /api/chat/sessions?user_id={user_id}&limit=50
```

**Response:**
```json
[
  {
    "session_id": "session_abc123",
    "title": "Health Discussion",
    "last_message_preview": "What can you tell me about my cholesterol...",
    "last_activity": "2024-01-08T03:30:00Z",
    "message_count": 5
  }
]
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

data: {"type": "token", "data": "your "}

data: {"type": "complete", "data": "Based on your recent test results, your cholesterol level is 220 mg/dL, which is high..."}

data: {"type": "stream_end"}
```

### Get Session Messages
```http
GET /api/chat/sessions/{session_id}/messages?user_id={user_id}&limit=50&offset=0
```

### Delete Chat Session
```http
DELETE /api/chat/sessions/{session_id}?user_id={user_id}
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

**Response:**
```json
{
  "provider": "aws_bedrock",
  "model_id": "amazon.titan-text-lite-v1",
  "region": "us-east-1",
  "max_tokens": 1000,
  "temperature": 0.7
}
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

**Response:**
```json
{
  "cheap_models": [
    {
      "model_id": "amazon.titan-text-lite-v1",
      "name": "Amazon Titan Text Lite",
      "cost": "Very Low",
      "description": "Lightweight model for basic text generation"
    }
  ],
  "premium_models": [
    {
      "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
      "name": "Claude 3 Haiku",
      "cost": "Medium",
      "description": "Fast, accurate responses"
    }
  ]
}
```

### Test LLM Connection
```http
POST /api/admin/llm/test?test_prompt=Hello, how are you?
```

---

## 📊 Legacy Health Endpoints (Mock Data)

### Get Health Categories
```http
GET /api/health/biomarkers
```

### Get Health Recommendations
```http
GET /api/health/recommendations
```

### Get Health Metrics
```http
GET /api/health/metrics
```

### Get Health Status
```http
GET /api/health/status
```

### Get Biomarker Details
```http
GET /api/biomarkers/{id}
```

---

## 👨‍⚕️ Doctors & Labs (Mock Data)

### Get Doctors
```http
GET /api/doctors
```

### Get Doctor Details
```http
GET /api/doctors/{id}
```

### Get Labs
```http
GET /api/labs
```

### Get Lab Details
```http
GET /api/labs/{id}
```

---

## 📁 Medical Files (Mock Data)

### Get File Categories
```http
GET /api/medical-files/categories
```

### Get Medical Specialties
```http
GET /api/medical-files/specialties
```

### Get Files by Specialty
```http
GET /api/medical-files/by-specialty/{specialty}
```

### Get Files by Category
```http
GET /api/medical-files/by-category/{category}
```

### Get All Files
```http
GET /api/medical-files?specialty=Cardiology&category=Imaging&limit=20
```

### Get File Details
```http
GET /api/medical-files/{file_id}
```

### Upload Medical File
```http
POST /api/medical-files/upload
```

---

## 🔐 Authentication & Security

**Current Status:** No authentication required (development mode)

**Coming Soon:**
- JWT token authentication
- User session management
- Role-based access control

---

## 📝 Request/Response Format

### Content Types
- **Request**: `application/json`
- **Response**: `application/json`
- **Streaming**: `text/event-stream`

### Common Headers
```http
Content-Type: application/json
Accept: application/json
```

### Error Responses

**400 Bad Request:**
```json
{
  "detail": "Invalid request parameters"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

---

## 🚀 Getting Started

### 1. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Create a Digital Twin
```bash
curl -X POST "http://localhost:8000/api/digital-twin/users/user_123/create"
```

### 3. Add Health Data
```bash
curl -X POST "http://localhost:8000/api/digital-twin/users/user_123/data" \
  -H "Content-Type: application/json" \
  -d '{"domain": "biomarkers", "field": "cholesterol", "value": 220, "unit": "mg/dL"}'
```

### 4. Get Recommendations
```bash
curl "http://localhost:8000/api/recommendations/user_123"
```

### 5. Start Chat Session
```bash
curl -X POST "http://localhost:8000/api/chat/sessions?user_id=user_123&title=Health Chat"
```

---

## 💰 AWS Bedrock Costs

### Model Pricing (per 1K tokens)
- **Titan Text Lite**: $0.0003 input / $0.0004 output
- **Titan Text Express**: $0.0008 input / $0.0016 output  
- **Claude 3 Haiku**: $0.00025 input / $0.00125 output

### Estimated Monthly Costs
- **100 conversations/day**: ~$0.81/month (Titan Lite)
- **500 conversations/day**: ~$4.05/month (Titan Lite)
- **1000 conversations/day**: ~$8.10/month (Titan Lite)

---

## 🧪 Test Users Available

- **user_001_29f** - 29F with comprehensive medical data
- **user_003_31m** - 31M with OCR medical data
- **user_004_31m** - 31M with OCR medical data
- **user_007_27f** - 27F with basic health package
- **user_009_26f** - 26F with women's health panel
- **user_011_34f** - 34F with comprehensive health package

---

## 📞 Support

For API questions or issues:
- Check interactive docs: http://localhost:8000/docs
- Review this documentation
- Contact the development team

---

**Last Updated:** January 8, 2024  
**API Version:** 2.0  
**Documentation Status:** ✅ Complete
