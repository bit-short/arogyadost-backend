---
inclusion: always
---

# Project Structure

## Directory Organization

```
/
├── app/                      # Application code
│   ├── api/                  # API route handlers (future)
│   ├── models/               # Pydantic models for requests/responses
│   ├── services/             # Business logic (S3, upload handling)
│   ├── workers/              # Celery task workers (future)
│   ├── config.py             # Environment configuration
│   └── database.py           # SQLAlchemy models and session management
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── property/             # Property-based tests (Hypothesis)
│   ├── test_data/            # Sample medical documents for testing
│   └── conftest.py           # Pytest fixtures and configuration
├── migrations/               # Alembic database migrations
├── docs/                     # Project documentation
├── .ebextensions/            # AWS Elastic Beanstalk configuration
├── main.py                   # FastAPI application entry point
├── cors_config.py            # CORS configuration
└── requirements.txt          # Python dependencies
```

## Key Files

- **main.py**: FastAPI app with all endpoint definitions and mock data
- **app/config.py**: Settings loaded from environment variables via Pydantic
- **app/database.py**: SQLAlchemy models (Document, Biomarker, OCRProcessingLog)
- **cors_config.py**: Centralized CORS setup for cross-origin requests
- **Dockerfile**: Container definition for deployment
- **Procfile**: Process configuration for Elastic Beanstalk

## Architectural Patterns

### Current (MVP)
- Mock data embedded in `main.py` for rapid prototyping
- Stateless API design with no database dependencies
- Async endpoints with simulated delays for realistic UX

### Future (Production-Ready)
- Database-backed persistence with SQLAlchemy models
- Celery workers for async OCR processing
- S3 integration for document storage
- Separate route modules in `app/api/`

## Code Conventions

- **Models**: Pydantic models in `app/models/` for API contracts
- **Services**: Business logic isolated in `app/services/`
- **Database**: SQLAlchemy models use UUID primary keys, soft deletes via relationships
- **Async**: All endpoints use `async def` for non-blocking I/O
- **Testing**: Property-based tests for validation logic, unit tests for services
- **Configuration**: Environment-based settings, never hardcode credentials
