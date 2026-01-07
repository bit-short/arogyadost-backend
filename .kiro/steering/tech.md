---
inclusion: always
---

# Technology Stack

## Core Framework

- **Backend**: FastAPI (Python 3.11)
- **Server**: Uvicorn with async support
- **Validation**: Pydantic v2 for request/response models

## Infrastructure

- **Cloud**: AWS (ap-south-1 Mumbai region)
- **Deployment**: Elastic Beanstalk on Amazon Linux 2023
- **Instance**: t3.micro (Free Tier)
- **Storage**: S3 for medical document storage
- **SSL**: Wildcard certificate (*.arogyadost.in)

## Database & Queue (Configured, Not Yet Active)

- **ORM**: SQLAlchemy 2.0+ with Alembic migrations
- **Database**: SQLite (dev), PostgreSQL-ready
- **Task Queue**: Celery with Redis backend
- **Retry Logic**: Tenacity for resilient operations

## Testing

- **Framework**: pytest with pytest-asyncio
- **Property Testing**: Hypothesis for robust validation
- **HTTP Testing**: httpx for async API tests
- **AWS Mocking**: moto for S3 service tests

## Common Commands

```bash
# Local development
pip install -r requirements.txt
uvicorn main:app --reload

# Testing
pytest                                    # Run all tests
pytest tests/unit                         # Unit tests only
pytest tests/property                     # Property-based tests
pytest -v                                 # Verbose output

# Database migrations (when active)
alembic revision --autogenerate -m "description"
alembic upgrade head

# API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Deployment

- **Dev**: Push to `dev` branch → auto-deploy to api-dev.arogyadost.in
- **Prod**: Push to `main` branch → auto-deploy to api.arogyadost.in
- **CI/CD**: GitHub Actions workflows in `.github/`
