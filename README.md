# Aarogyadost Backend

FastAPI backend for the Aarogyadost healthcare application with digital twin system, biological age prediction, personalized health recommendations, and AI-powered health chat assistant.

## 🚀 Key Features

### 🧬 Digital Twin System
- **Structured Health Data**: Multi-domain health data storage (demographics, biomarkers, medical history, lifestyle, genetics)
- **Temporal Tracking**: Historical data points with timestamps and units
- **Data Completeness**: Track missing fields and completeness percentages across domains
- **Flexible Schema**: Dynamic field addition and state management

### 🧠 Biological Age Prediction
- **Evidence-Based Calculation**: Multi-category age assessment using longevity research
- **Category Breakdown**: Metabolic, cardiovascular, inflammatory, hormonal, and organ function ages
- **Confidence Scoring**: Data quality and completeness metrics
- **Actionable Insights**: Personalized recommendations to reduce biological age

### 💊 Health Recommendations Engine
- **Rule-Based System**: Biomarker, condition, demographic, and temporal rules
- **Priority Scoring**: Intelligent high/medium/low priority assignment
- **Category Grouping**: Organized by blood tests, lifestyle, and monitoring
- **Personalized Output**: User-specific recommendations based on digital twin data

### 💬 AI Health Chat Assistant
- **LLM-Powered Conversations**: Natural language health discussions using AWS Bedrock
- **Streaming Responses**: Real-time token-by-token response delivery via Server-Sent Events
- **Digital Twin Integration**: Personalized responses using actual user health data
- **Session Management**: Persistent conversation history and multi-session support
- **Medical Safety**: Built-in disclaimers and safety guidelines

### 👥 User Selection System
- **Multi-User Testing**: Switch between different test user profiles for development
- **Data Availability Indicators**: Visual indicators of available health data
- **Interactive UI**: Web-based user selection with modern interface
- **Hardcoded Fallback**: Default user with mock data for testing

### ⚙️ Admin & Configuration
- **AWS Bedrock Integration**: Cost-effective LLM models starting at $0.81/month
- **Model Switching**: Real-time configuration updates for different AI models
- **Performance Monitoring**: Connection testing and usage analytics

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

### Core Documentation
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference with endpoints, request/response examples
- **[Architecture Overview](docs/API_ARCHITECTURE.md)** - System design, data flow, and technical specifications
- **[Deployment Guide](docs/DEPLOYMENT.md)** - AWS Elastic Beanstalk deployment instructions
- **[CI/CD Setup](docs/CI-CD-SETUP.md)** - GitHub Actions automated deployment configuration

### Feature Documentation
- **[Digital Twin & Biological Age](docs/DIGITAL_TWIN_AND_BIOLOGICAL_AGE.md)** - Digital twin system and biological age prediction engine
- **[Recommendations Engine](docs/RECOMMENDATIONS_ENGINE.md)** - Rule-based health recommendations system

## Live Deployments

### Development Environment
- **Custom Domain**: https://api-dev.arogyadost.in
- **API Docs**: https://api-dev.arogyadost.in/docs
- **ReDoc**: https://api-dev.arogyadost.in/redoc
- **User Selection UI**: https://api-dev.arogyadost.in/static/user-selection.html
- **Elastic Beanstalk URL**: http://aarogyadost-dev.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com

### Production Environment
- **Custom Domain**: https://api.arogyadost.in
- **API Docs**: https://api.arogyadost.in/docs
- **ReDoc**: https://api.arogyadost.in/redoc
- **Elastic Beanstalk URL**: http://aarogyadost-prod.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com

### SSL & Security
- **HTTPS Enabled**: Full SSL encryption with custom domains
- **SSL Certificate**: Wildcard certificate for *.arogyadost.in
- **Mixed Content Resolved**: Web apps can securely access HTTPS APIs

## Local Development

### Setup
```bash
# Clone repository
git clone <repository-url>
cd aarogyadost-backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (for chat assistant)
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region (us-east-1)
```

### Run
```bash
# Start development server
uvicorn main:app --reload
```

API will be available at http://localhost:8000

### Local API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **User Selection UI**: http://localhost:8000/static/user-selection.html

### Quick Start Example

```python
import httpx

base_url = "http://localhost:8000"

# 1. Select a test user (optional - defaults to hardcoded user)
httpx.post(f"{base_url}/api/users/select", json={"user_id": "test_user_1_29f"})

# 2. Create a digital twin
httpx.post(f"{base_url}/api/digital-twin/users/test_user_1_29f/create")

# 3. Add biomarker data
httpx.post(
    f"{base_url}/api/digital-twin/users/test_user_1_29f/data",
    json={
        "domain": "biomarkers",
        "field": "hba1c",
        "value": 5.8,
        "unit": "%"
    }
)

# 4. Predict biological age
response = httpx.post(
    f"{base_url}/api/biological-age/users/test_user_1_29f/predict"
)
print(response.json())

# 5. Get health recommendations
response = httpx.get(
    f"{base_url}/api/recommendations/test_user_1_29f"
)
print(response.json())

# 6. Start a health chat session
chat_response = httpx.post(
    f"{base_url}/api/chat/sessions?user_id=test_user_1_29f&title=Health Discussion"
)
session_id = chat_response.json()["session_id"]

# 7. Send a chat message
httpx.post(
    f"{base_url}/api/chat/message?user_id=test_user_1_29f",
    json={"message": "What should I know about my health?", "session_id": session_id}
)
```

### Testing

```bash
# Run validation tests
python3 test_user_selection_logic.py    # User selection system
python3 test_recommendations.py          # Recommendations engine  
python3 test_chat_logic.py              # Chat assistant
python3 test_aws_integration.py         # AWS Bedrock integration

# Run all tests (when available)
pytest

# Run specific test suites
pytest tests/unit                 # Unit tests
pytest tests/property             # Property-based tests
pytest tests/integration          # Integration tests
```

## 📡 Available Endpoints

### 👥 User Management (CRUD)
- `POST /api/users/` - Create new user with digital twin
- `GET /api/users/` - List all users
- `PUT /api/users/select` - Select/switch active user
- `GET /api/users/{user_id}` - Get user by ID
- `DELETE /api/users/{user_id}` - Delete user
- `PUT /api/users/{user_id}/display-name` - Update display name
- `GET /api/users/stats/overview` - Get user statistics

### 👥 User Selection (Legacy)
- `GET /api/users/available` - List all available test users
- `POST /api/users/select` - Select active test user
- `GET /api/users/current` - Get currently active user
- `GET /static/user-selection.html` - Interactive user selection UI

### 🧬 Digital Twin Management
- `POST /api/digital-twin/users/{user_id}/create` - Create digital twin
- `POST /api/digital-twin/users/{user_id}/data` - Add health data
- `GET /api/digital-twin/users/{user_id}/data/{domain}/{field}` - Get specific data
- `GET /api/digital-twin/users/{user_id}/domains/{domain}` - Get domain data
- `GET /api/digital-twin/users/{user_id}/missing-fields` - Get missing fields
- `GET /api/digital-twin/users/{user_id}/completeness` - Get data completeness
- `GET /api/digital-twin/users/{user_id}/profile` - Get complete profile

### 🧠 Biological Age Prediction
- `POST /api/biological-age/users/{user_id}/predict` - Predict biological age
- `POST /api/biological-age/users/{user_id}/insights` - Get age insights
- `GET /api/biological-age/users/available` - List available users
- `POST /api/biological-age/users/all/predict` - Predict all users

### 💊 Health Recommendations
- `GET /api/recommendations/{user_id}` - Get personalized recommendations
- `GET /api/recommendations/{user_id}/summary` - Get recommendations summary

### 💬 Health Chat Assistant
- `POST /api/chat/sessions` - Create new chat session
- `GET /api/chat/sessions` - List user chat sessions
- `GET /api/chat/sessions/{session_id}` - Get session details
- `GET /api/chat/sessions/{session_id}/messages` - Get session messages
- `POST /api/chat/sessions/{session_id}/messages` - Send message with streaming
- `DELETE /api/chat/sessions/{session_id}` - Delete chat session
- `POST /api/chat/message` - Send simple message (non-streaming)

### ⚙️ Admin & Configuration
- `GET /api/admin/llm/config` - Get LLM configuration
- `PUT /api/admin/llm/config` - Update LLM settings
- `GET /api/admin/llm/models` - List available models
- `POST /api/admin/llm/test` - Test LLM connection

### 🗄️ Database API
- `GET /api/db/users` - Get all users from database
- `GET /api/db/users/{user_id}` - Get user from database
- `GET /api/db/users/{user_id}/biomarkers` - Get biomarkers by category
- `GET /api/db/users/{user_id}/medical-history` - Get medical history
- `GET /api/db/users/{user_id}/full` - Get complete user data
- `GET /api/db/users/{user_id}/routines` - Get auto-computed routines
- `GET /api/db/users/{user_id}/health-scores` - Get computed health scores
- `POST /api/db/users/{user_id}/recompute` - Force recompute derived data

### 🏥 Health Check API
- `GET /api/health/database` - Database connectivity check
- `GET /api/health/storage` - Storage layer health
- `GET /api/health/digital-brain` - Overall digital brain health

### 📊 Health Data (Legacy Mock Data)
- `GET /api/health/biomarkers` - Get health categories and scores
- `GET /api/health/recommendations` - Get recommended actions  
- `GET /api/health/metrics` - Get health metrics
- `GET /api/health/status` - Get overall health status
- `GET /api/biomarkers/{id}` - Get detailed biomarker data

### 📁 Medical Files
- `GET /api/medical-files/categories` - Get file categories
- `GET /api/medical-files/specialties` - Get medical specialties
- `GET /api/medical-files/by-specialty/{specialty}` - Get files by specialty
- `GET /api/medical-files/by-category/{category}` - Get files by category
- `GET /api/medical-files` - Get all files (with filters)
- `GET /api/medical-files/{file_id}` - Get file details
- `POST /api/medical-files/upload` - Upload medical file

### 👨‍⚕️ Doctors & Labs
- `GET /api/doctors` - Get list of doctors
- `GET /api/doctors/{id}` - Get doctor details
- `GET /api/labs` - Get list of labs
- `GET /api/labs/{id}` - Get lab details

## 💰 AWS Bedrock Integration

### Cost-Effective AI Models
- **Titan Text Lite**: $0.0003/$0.0004 per 1K tokens (~$0.81/month for 100 conversations/day)
- **Titan Text Express**: $0.0008/$0.0016 per 1K tokens (better quality)
- **Claude 3 Haiku**: $0.00025/$0.00125 per 1K tokens (premium accuracy)

### Model Management
- Real-time model switching via admin API
- Automatic fallback handling
- Cost monitoring and optimization
- Regional deployment support

## 🧪 Test Users Available

- **test_user_1_29f** - 29F, comprehensive medical data (100% completeness)
- **test_user_2_29m** - 29M, fitness focused profile
- **test_user_3_31m** - 31M, weight loss and metabolic health
- **test_user_4_31m** - 31M, longevity optimization
- **test_user_5_55f** - 55F, hormonal balance and bone health
- **test_user_6_65m** - 65M, senior health profile
- **hardcoded** - Default user with mock data for fallback

## Deployment

### Automatic Deployment (CI/CD)
- **Push to `dev` branch** → Auto-deploys to development environment
- **Push to `main` branch** → Auto-deploys to production environment

### Manual Deployment
See `docs/DEPLOYMENT.md` for detailed deployment instructions.

### CI/CD Setup
See `docs/CI-CD-SETUP.md` for GitHub Actions configuration.

## 🏗️ Architecture

- **Platform**: AWS Elastic Beanstalk
- **Runtime**: Python 3.11 on Amazon Linux 2023
- **Framework**: FastAPI with async/await support
- **Region**: ap-south-1 (Mumbai)
- **Instance**: t3.micro (Free Tier eligible)
- **AI Integration**: AWS Bedrock for LLM services
- **Storage**: In-memory digital twins + JSON file persistence
- **Testing**: pytest with Hypothesis for property-based testing

### Project Structure
```
app/
├── models/              # Pydantic models and data structures
│   ├── user_profile.py  # User selection models
│   └── digital_twin.py  # Digital twin domain model
├── routers/             # API route handlers
│   ├── users.py         # User selection endpoints
│   ├── digital_twin.py  # Digital twin endpoints
│   ├── biological_age.py # Biological age endpoints
│   ├── recommendations.py # Recommendations endpoints
│   ├── chat.py          # Health chat assistant
│   └── admin.py         # Admin and configuration
├── services/            # Business logic
│   ├── user_context.py  # User selection management
│   ├── biological_age/  # Age calculation engine
│   ├── recommendations/ # Recommendation engine
│   └── chat/            # Chat assistant services
└── static/              # Static files and UI

config/                  # Configuration files
├── llm_config.json      # LLM model configuration

datasets/                # Test data and user datasets
├── users/               # User profiles
├── biomarkers/          # Biomarker data
├── lifestyle/           # Lifestyle data
├── medical_history/     # Medical history
├── interventions/       # Health interventions
└── ai_interactions/     # Chat history

tests/
├── unit/                # Unit tests
├── property/            # Property-based tests (Hypothesis)
└── integration/         # Integration tests
```
