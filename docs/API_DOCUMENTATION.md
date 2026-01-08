# Aarogyadost API Documentation v2.1

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

## 👥 User Management API (New)

Full CRUD operations for user management with Digital Brain Integration.

### Create User
```http
POST /api/users/
```

**Request Body:**
```json
{
  "user_id": "new_user_123",
  "display_name": "John Doe"
}
```

**Response (201):**
```json
{
  "user_info": {
    "user_id": "new_user_123",
    "display_name": "John Doe",
    "created_at": "2025-01-08T10:30:00Z",
    "updated_at": "2025-01-08T10:30:00Z",
    "data_completeness": 0.0
  },
  "digital_twin_created": true,
  "message": "User 'new_user_123' created successfully"
}
```

### List All Users
```http
GET /api/users/
```

**Response:**
```json
{
  "users": [
    {
      "user_id": "new_user_123",
      "display_name": "John Doe",
      "created_at": "2025-01-08T10:30:00Z",
      "updated_at": "2025-01-08T10:30:00Z",
      "data_completeness": 75.5
    }
  ],
  "total_count": 1,
  "message": "Retrieved 1 users successfully"
}
```

### Select/Switch Active User
```http
PUT /api/users/select
```

**Request Body:**
```json
{
  "user_id": "test_user_1_29f"
}
```

**Response:**
```json
{
  "selected_user": {
    "user_id": "test_user_1_29f",
    "display_name": "test_user_1_29f (29F)",
    "created_at": "2025-01-08T10:30:00Z",
    "updated_at": "2025-01-08T10:30:00Z",
    "data_completeness": 100.0
  },
  "digital_twin_loaded": true,
  "message": "User 'test_user_1_29f' selected successfully"
}
```

### Get User by ID
```http
GET /api/users/{user_id}
```

**Response:**
```json
{
  "user_id": "test_user_1_29f",
  "display_name": "test_user_1_29f (29F)",
  "created_at": "2025-01-08T10:30:00Z",
  "updated_at": "2025-01-08T10:30:00Z",
  "data_completeness": 100.0
}
```

### Delete User
```http
DELETE /api/users/{user_id}
```

**Response:**
```json
{
  "deleted": true,
  "user_id": "new_user_123",
  "message": "User 'new_user_123' deleted successfully"
}
```

*Note: Cannot delete the hardcoded user.*

### Update Display Name
```http
PUT /api/users/{user_id}/display-name
```

**Request Body:**
```json
{
  "display_name": "Jane Doe"
}
```

**Response:**
```json
{
  "updated": true,
  "user_id": "new_user_123",
  "new_display_name": "Jane Doe",
  "message": "Display name updated successfully"
}
```

### Get User Statistics
```http
GET /api/users/stats/overview
```

**Response:**
```json
{
  "total_users": 7,
  "average_completeness": 85.5,
  "completeness_distribution": {
    "high": 3,
    "medium": 2,
    "low": 2
  },
  "storage_stats": {
    "cache_enabled": true,
    "cache_size": 5
  },
  "message": "User statistics retrieved successfully"
}
```

---

## 👥 User Selection API (Legacy)

### Get Available Users
```http
GET /api/users/available
```

**Response:**
```json
{
  "users": [
    {
      "user_id": "hardcoded",
      "display_name": "Default (Hardcoded)",
      "is_hardcoded": true,
      "demographics": {
        "age": 35,
        "gender": "M",
        "location": {"city": "Mumbai", "country": "India"}
      },
      "health_profile": {
        "bmi": 24.5,
        "biological_age": 32.0,
        "blood_type": "O+"
      },
      "goals": [
        {
          "goal_id": "g1",
          "type": "fitness",
          "target": "Improve cardiovascular health",
          "status": "active"
        }
      ],
      "data_availability": {
        "biomarkers": true,
        "medical_history": true,
        "lifestyle": true,
        "ai_interactions": false,
        "interventions": false,
        "completeness_score": 85.0
      }
    },
    {
      "user_id": "test_user_1_29f",
      "display_name": "test_user_1_29f (29F)",
      "is_hardcoded": false,
      "demographics": {
        "age": 29,
        "gender": "F"
      },
      "data_availability": {
        "biomarkers": true,
        "medical_history": true,
        "lifestyle": true,
        "ai_interactions": true,
        "interventions": true,
        "completeness_score": 100.0
      }
    }
  ],
  "total_count": 7,
  "hardcoded_user_id": "hardcoded"
}
```

### Select Active User
```http
POST /api/users/select
```

**Request Body:**
```json
{
  "user_id": "test_user_1_29f"
}
```

**Response:**
```json
{
  "message": "Successfully selected user: test_user_1_29f",
  "selected_user": {
    "user_id": "test_user_1_29f",
    "display_name": "test_user_1_29f (29F)",
    "is_hardcoded": false,
    "demographics": {
      "age": 29,
      "gender": "F"
    }
  },
  "is_hardcoded": false
}
```

### Get Current User
```http
GET /api/users/current
```

**Response:**
```json
{
  "active_user": {
    "user_id": "test_user_1_29f",
    "display_name": "test_user_1_29f (29F)",
    "is_hardcoded": false,
    "demographics": {
      "age": 29,
      "gender": "F"
    },
    "data_availability": {
      "biomarkers": true,
      "medical_history": true,
      "lifestyle": true,
      "ai_interactions": true,
      "interventions": true,
      "completeness_score": 100.0
    }
  },
  "is_default": false
}
```

### Get User by ID
```http
GET /api/users/{user_id}
```

### List User IDs
```http
GET /api/users/
```

**Response:**
```json
{
  "user_ids": ["hardcoded", "test_user_1_29f", "test_user_2_29m", "test_user_3_31m", "test_user_4_31m", "test_user_5_55f", "test_user_6_65m"],
  "current_user": "test_user_1_29f",
  "total_count": 7
}
```

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

### 1. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Select a Test User (Optional)
```bash
# Local
curl -X POST "http://localhost:8000/api/users/select" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user_1_29f"}'

# Dev Environment
curl -X POST "https://api-dev.arogyadost.in/api/users/select" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user_1_29f"}'
```

### 3. Create a Digital Twin
```bash
# Local
curl -X POST "http://localhost:8000/api/digital-twin/users/test_user_1_29f/create"

# Dev Environment
curl -X POST "https://api-dev.arogyadost.in/api/digital-twin/users/test_user_1_29f/create"
```

### 4. Add Health Data
```bash
# Local
curl -X POST "http://localhost:8000/api/digital-twin/users/test_user_1_29f/data" \
  -H "Content-Type: application/json" \
  -d '{"domain": "biomarkers", "field": "cholesterol", "value": 220, "unit": "mg/dL"}'

# Dev Environment  
curl -X POST "https://api-dev.arogyadost.in/api/digital-twin/users/test_user_1_29f/data" \
  -H "Content-Type: application/json" \
  -d '{"domain": "biomarkers", "field": "cholesterol", "value": 220, "unit": "mg/dL"}'
```

### 5. Get Recommendations
```bash
# Local
curl "http://localhost:8000/api/recommendations/test_user_1_29f"

# Dev Environment
curl "https://api-dev.arogyadost.in/api/recommendations/test_user_1_29f"
```

### 6. Start Chat Session
```bash
# Local
curl -X POST "http://localhost:8000/api/chat/sessions?user_id=test_user_1_29f&title=Health Chat"

# Dev Environment
curl -X POST "https://api-dev.arogyadost.in/api/chat/sessions?user_id=test_user_1_29f&title=Health Chat"
```

---

## 💰 AWS Bedrock Costs

### Model Pricing (per 1K tokens)
- **Titan Text Lite**: $0.0003 input / $0.0004 output (~$0.81/month for 100 conversations/day)
- **Titan Text Express**: $0.0008 input / $0.0016 output
- **Claude 3 Haiku**: $0.00025 input / $0.00125 output

---

## 🧪 Test Users Available

- **hardcoded** - Default user with mock data (85% completeness)
- **test_user_1_29f** - 29F with comprehensive medical data (100% completeness)
- **test_user_2_29m** - 29M, fitness focused profile
- **test_user_3_31m** - 31M, weight loss and metabolic health
- **test_user_4_31m** - 31M, longevity optimization
- **test_user_5_55f** - 55F, hormonal balance and bone health
- **test_user_6_65m** - 65M, senior health profile

### User Selection UI
Access the interactive user selection interface at:
- **Local**: http://localhost:8000/static/user-selection.html
- **Dev**: https://api-dev.arogyadost.in/static/user-selection.html

The UI provides:
- Visual user cards with demographics and health data
- Data availability indicators and completeness scores
- One-click user switching for development testing
- Active user highlighting and confirmation

---

---

## 🗄️ Database API (New)

Direct database access endpoints for user data.

### Get All Users from Database
```http
GET /api/db/users
```

**Response:**
```json
{
  "users": [...],
  "count": 7
}
```

### Get User from Database
```http
GET /api/db/users/{user_id}
```

### Get User Biomarkers by Category
```http
GET /api/db/users/{user_id}/biomarkers
```

**Response:**
```json
{
  "user_id": "test_user_1_29f",
  "biomarkers": {
    "lipid_panel": [...],
    "metabolic": [...],
    "vitamins": [...]
  },
  "total_count": 25
}
```

### Get User Medical History
```http
GET /api/db/users/{user_id}/medical-history
```

### Get Complete User Data
```http
GET /api/db/users/{user_id}/full
```

### Get User Routines (Auto-Computed)
```http
GET /api/db/users/{user_id}/routines
```

**Response:**
```json
{
  "user_id": "test_user_1_29f",
  "daily_routine": [...],
  "weekly_routine": [...]
}
```

### Get User Health Scores
```http
GET /api/db/users/{user_id}/health-scores
```

### Force Recompute Derived Data
```http
POST /api/db/users/{user_id}/recompute
```

**Response:**
```json
{
  "user_id": "test_user_1_29f",
  "recomputed": true,
  "summary": {
    "daily_routine": 5,
    "weekly_routine": 3,
    "health_scores": "computed"
  }
}
```

---

## 🏥 Health Check API (New)

Health check endpoints for monitoring system components.

### Database Health
```http
GET /api/health/database
```

**Response:**
```json
{
  "status": "healthy",
  "service": "database",
  "users_count": 7,
  "cache_stats": {
    "enabled": true,
    "size": 5
  },
  "timestamp": "2025-01-08T10:30:00Z"
}
```

### Storage Health
```http
GET /api/health/storage
```

**Response:**
```json
{
  "status": "healthy",
  "service": "storage",
  "cache_enabled": true,
  "cache_size": 5,
  "timestamp": "2025-01-08T10:30:00Z"
}
```

### Digital Brain Overall Health
```http
GET /api/health/digital-brain
```

**Response:**
```json
{
  "status": "healthy",
  "service": "digital_brain",
  "components": {
    "database": "healthy",
    "storage": "healthy"
  },
  "timestamp": "2025-01-08T10:30:00Z"
}
```

---

## 📊 Metrics API

### Get Metric Details
```http
GET /api/metrics/{metric_id}
```

**Available Metrics:** `cholesterol`, `blood_sugar`, `vitamins`, `hormones`, `inflammation`

**Response:**
```json
{
  "id": "cholesterol",
  "title": "Cholesterol Panel",
  "subtitle": "Last 12 months trend",
  "status": "attention",
  "metrics": [
    {"name": "Total", "value": "186", "normalRange": "< 200", "color": "#3B82F6"},
    {"name": "LDL", "value": "107", "normalRange": "< 100", "color": "#F97316"},
    {"name": "HDL", "value": "67", "normalRange": "> 40", "color": "#22C55E"}
  ],
  "chartData": [...],
  "insights": [...],
  "recommendations": [...]
}
```

---

## 🎯 Actions API (New)

### Get Action Details
```http
GET /api/actions/{action_id}
```

**Response:**
```json
{
  "id": "1",
  "title": "Start Zone 2 cardio training",
  "icon": "Activity",
  "overview": "Zone 2 cardio training improves mitochondrial function...",
  "benefits": ["Improves mitochondrial function", "Increases VO2 max", ...],
  "howItHelps": "Your current VO2 max of 42 mL/kg/min...",
  "nextSteps": ["Calculate your Zone 2 heart rate", ...],
  "isTodo": true,
  "todoItems": [
    {"label": "Calculate your Zone 2 heart rate range", "checked": false}
  ],
  "personalizedSummary": {
    "improving": [...],
    "declining": [...]
  }
}
```

---

## 📅 Routines API (New)

### Get Daily Routine
```http
GET /api/routines/daily
```

**Response:** Array of daily routine items (supplements, exercises, etc.)
*Note: Returns data only for hardcoded user, empty array for others.*

### Get Weekly Routine
```http
GET /api/routines/weekly
```

**Response:** Array of weekly routine items
*Note: Returns data only for hardcoded user, empty array for others.*

---

## 🧬 Mock Biological Age API (New)

### Get Mock Biological Age
```http
GET /api/biological-age/mock/{user_id}
```

**Response:**
```json
{
  "user_id": "user_001_29f",
  "chronological_age": 32,
  "biological_age": 29,
  "age_difference": -3,
  "longevity_score": 87
}
```
*Note: Mock endpoint for frontend testing without digital twin.*

---

## 📝 Test Users Available

| User ID | Age | Gender | Data Available |
|---------|-----|--------|----------------|
| hardcoded | 35 | M | Full mock data |
| test_user_1_29f | 29 | F | Biomarkers, lifestyle, medical history |
| test_user_3_31m | 31 | M | Medical history |
| test_user_5_55f | 55 | F | Medical history |
| test_user_6_65m | 65 | M | Medical history |

---

**Last Updated:** January 9, 2025 | **API Version:** 2.1 | **Status:** ✅ Complete
