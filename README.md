# Aarogyadost Backend

FastAPI backend for the Aarogyadost healthcare application with digital twin system, biological age prediction, and personalized health recommendations.

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

# Install dependencies
pip install -r requirements.txt
```

### Run
```bash
# Start development server
uvicorn main:app --reload
```

API will be available at http://localhost:8000

### Local API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Quick Start Example

```python
import httpx

base_url = "http://localhost:8000"

# 1. Create a digital twin
httpx.post(f"{base_url}/api/digital-twin/users/user123/create")

# 2. Add demographic data
httpx.post(
    f"{base_url}/api/digital-twin/users/user123/data",
    json={"domain": "demographics", "field": "age", "value": 35}
)

# 3. Add biomarker data
httpx.post(
    f"{base_url}/api/digital-twin/users/user123/data",
    json={
        "domain": "biomarkers",
        "field": "hba1c",
        "value": 5.8,
        "unit": "%"
    }
)

# 4. Predict biological age
response = httpx.post(
    f"{base_url}/api/biological-age/users/user123/predict"
)
print(response.json())

# 5. Get health recommendations
response = httpx.get(
    f"{base_url}/api/recommendations/user123"
)
print(response.json())
```

### Testing

```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/unit                 # Unit tests
pytest tests/property             # Property-based tests
pytest tests/integration          # Integration tests

# Run with coverage
pytest --cov=app

# Run with verbose output
pytest -v
```

## 🚀 Key Features

### Digital Twin System
- **Structured Health Data**: Multi-domain health data storage (demographics, biomarkers, medical history, lifestyle, genetics)
- **Temporal Tracking**: Historical data points with timestamps and units
- **Data Completeness**: Track missing fields and completeness percentages across domains
- **Flexible Schema**: Dynamic field addition and state management

### Biological Age Prediction
- **Evidence-Based Calculation**: Multi-category age assessment using longevity research
- **Category Breakdown**: Metabolic, cardiovascular, inflammatory, hormonal, and organ function ages
- **Confidence Scoring**: Data quality and completeness metrics
- **Actionable Insights**: Personalized recommendations to reduce biological age

### Health Recommendations Engine
- **Rule-Based System**: Biomarker, condition, demographic, and temporal rules
- **Priority Scoring**: Intelligent high/medium/low priority assignment
- **Category Grouping**: Organized by blood tests, lifestyle, and monitoring
- **Personalized Output**: User-specific recommendations based on digital twin data

### Medical Document Management
- **File Organization**: Specialty and category-based organization
- **OCR Processing**: Automated text extraction from medical documents
- **AI Analysis**: Intelligent summary and key findings extraction
- **Context-Aware Chat**: File-specific health guidance

### Health Analytics
- **Biomarker Tracking**: Comprehensive health data analysis
- **Longevity Focus**: Biological age assessment and optimization
- **Status Monitoring**: Real-time health status updates

## 📡 Available Endpoints

### Digital Twin Management
- `POST /api/digital-twin/users/{user_id}/create` - Create digital twin
- `POST /api/digital-twin/users/{user_id}/data` - Add health data
- `GET /api/digital-twin/users/{user_id}/data/{domain}/{field}` - Get specific data
- `GET /api/digital-twin/users/{user_id}/domains/{domain}` - Get domain data
- `GET /api/digital-twin/users/{user_id}/missing-fields` - Get missing fields
- `GET /api/digital-twin/users/{user_id}/completeness` - Get data completeness
- `GET /api/digital-twin/users/{user_id}/profile` - Get complete profile

### Biological Age Prediction
- `POST /api/biological-age/users/{user_id}/predict` - Predict biological age
- `POST /api/biological-age/users/{user_id}/insights` - Get age insights
- `GET /api/biological-age/users/available` - List available users
- `POST /api/biological-age/users/all/predict` - Predict all users

### Health Recommendations
- `GET /api/recommendations/{user_id}` - Get personalized recommendations
- `GET /api/recommendations/{user_id}/summary` - Get recommendations summary

### Health Data (Legacy Mock Data)
- `GET /api/health/biomarkers` - Get health categories and scores
- `GET /api/health/recommendations` - Get recommended actions  
- `GET /api/health/metrics` - Get health metrics
- `GET /api/health/status` - Get overall health status
- `GET /api/biomarkers/{id}` - Get detailed biomarker data

### Medical Files
- `GET /api/medical-files/categories` - Get file categories
- `GET /api/medical-files/specialties` - Get medical specialties
- `GET /api/medical-files/by-specialty/{specialty}` - Get files by specialty
- `GET /api/medical-files/by-category/{category}` - Get files by category
- `GET /api/medical-files` - Get all files (with filters)
- `GET /api/medical-files/{file_id}` - Get file details
- `POST /api/medical-files/upload` - Upload medical file

### Doctors & Labs
- `GET /api/doctors` - Get list of doctors
- `GET /api/doctors/{id}` - Get doctor details
- `GET /api/labs` - Get list of labs
- `GET /api/labs/{id}` - Get lab details

### Chat
- `GET /api/chat/threads` - Get chat threads
- `POST /api/chat/message` - Send chat message (with file context support)

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
- **Storage**: In-memory digital twins + S3 for documents
- **Testing**: pytest with Hypothesis for property-based testing

### Project Structure
```
app/
├── models/              # Pydantic models and data structures
│   └── digital_twin.py  # Digital twin domain model
├── routers/             # API route handlers
│   ├── digital_twin.py  # Digital twin endpoints
│   ├── biological_age.py # Biological age endpoints
│   └── recommendations.py # Recommendations endpoints
├── services/            # Business logic
│   ├── biological_age/  # Age calculation engine
│   └── recommendations/ # Recommendation engine
└── storage/             # Data storage layer

tests/
├── unit/                # Unit tests
├── property/            # Property-based tests (Hypothesis)
└── integration/         # Integration tests

datasets/                # Test data and user datasets
├── biomarkers/
├── lifestyle/
├── medical_history/
├── interventions/
└── ai_interactions/
```
