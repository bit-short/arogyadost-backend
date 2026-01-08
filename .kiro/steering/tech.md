---
inclusion: always
---

# Technology Stack

## Core Framework

- **Backend**: FastAPI (Python 3.11) with async/await support
- **Server**: Uvicorn with async support
- **Validation**: Pydantic v2 for request/response models
- **Type Hints**: Full type annotation coverage

## Data & Storage

- **Digital Twin**: In-memory storage with domain-based organization
- **Temporal Data**: Timestamp-based health data tracking
- **Future Database**: PostgreSQL-ready with SQLAlchemy 2.0+
- **Document Storage**: S3 for medical document storage (configured)

## Infrastructure

- **Cloud**: AWS (ap-south-1 Mumbai region)
- **Deployment**: Elastic Beanstalk on Amazon Linux 2023
- **Instance**: t3.micro (Free Tier)
- **Storage**: S3 for medical document storage
- **SSL**: Wildcard certificate (*.arogyadost.in)

## Health Analytics

- **Biological Age Engine**: Evidence-based multi-category age calculation
- **Recommendation Engine**: Rule-based health recommendations system
- **Digital Twin System**: Multi-domain health data management
- **Biomarker Analysis**: Comprehensive health marker evaluation

## Database & Queue (Configured, Not Yet Active)

- **ORM**: SQLAlchemy 2.0+ with Alembic migrations
- **Database**: SQLite (dev), PostgreSQL-ready
- **Task Queue**: Celery with Redis backend
- **Retry Logic**: Tenacity for resilient operations

## Testing

- **Framework**: pytest with pytest-asyncio
- **Property Testing**: Hypothesis for robust validation and edge case discovery
- **HTTP Testing**: httpx for async API tests
- **AWS Mocking**: moto for S3 service tests
- **Coverage**: pytest-cov for code coverage analysis

## Common Commands

```bash
# Local development
pip install -r requirements.txt
uvicorn main:app --reload

# Testing
pytest                                    # Run all tests
pytest tests/unit                         # Unit tests only
pytest tests/property                     # Property-based tests
pytest tests/integration                  # Integration tests
pytest -v                                 # Verbose output
pytest --cov=app                          # With coverage

# Database migrations (when active)
alembic revision --autogenerate -m "description"
alembic upgrade head

# API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Code Organization

```
app/
├── models/              # Pydantic models and domain objects
│   └── digital_twin.py  # Digital twin data structures
├── routers/             # API endpoint handlers
│   ├── digital_twin.py
│   ├── biological_age.py
│   └── recommendations.py
├── services/            # Business logic and engines
│   ├── biological_age/
│   │   ├── calculator.py
│   │   ├── engine.py
│   │   └── biomarker_normalizer.py
│   └── recommendations/
│       ├── engine.py
│       ├── digital_twin_analyzer.py
│       ├── recommendation_builder.py
│       ├── priority_scorer.py
│       ├── biomarker_rules.py
│       ├── condition_rules.py
│       ├── demographic_rules.py
│       └── temporal_rules.py
└── storage/             # Data persistence layer
    └── digital_twins.py

tests/
├── unit/                # Unit tests
├── property/            # Property-based tests
└── integration/         # Integration tests

datasets/                # Test data and user datasets
├── biomarkers/
├── lifestyle/
├── medical_history/
├── interventions/
└── ai_interactions/
```

## Deployment

- **Dev**: Push to `dev` branch → auto-deploy to api-dev.arogyadost.in
- **Prod**: Push to `main` branch → auto-deploy to api.arogyadost.in
- **CI/CD**: GitHub Actions workflows in `.github/`
