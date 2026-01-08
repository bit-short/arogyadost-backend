# Technology Stack & Build System

## Core Technologies

- **Framework**: FastAPI with async/await support
- **Runtime**: Python 3.11 on Amazon Linux 2023
- **Database**: SQLite with SQLAlchemy ORM and Alembic migrations
- **AI Integration**: AWS Bedrock for LLM services (Titan, Claude models)
- **Deployment**: AWS Elastic Beanstalk (ap-south-1 region)
- **Instance**: t3.micro (Free Tier eligible)

## Key Dependencies

- **FastAPI**: 0.104.1 - Web framework
- **Pydantic**: 2.5.0 - Data validation and serialization
- **SQLAlchemy**: 2.0.0+ - Database ORM
- **Boto3**: 1.34.0+ - AWS SDK
- **Uvicorn**: 0.24.0 - ASGI server

## Testing Stack

- **pytest**: 7.4.0+ - Test framework
- **pytest-asyncio**: 0.23.0+ - Async test support
- **Hypothesis**: 6.92.0+ - Property-based testing
- **httpx**: 0.26.0+ - HTTP client for testing
- **moto**: 4.2.0+ - AWS service mocking

## Development Commands

### Local Development
```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn main:app --reload

# API will be available at http://localhost:8000
```

### Testing
```bash
# Run all tests
python run_tests.py

# Run specific test suites
pytest tests/unit                 # Unit tests
pytest tests/property             # Property-based tests
pytest tests/integration          # Integration tests

# Run with coverage
pytest --cov=app tests/
```

### Database Operations
```bash
# Initialize database
python -c "from app.database import init_db; init_db()"

# Run migrations (when available)
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Validation & Health Checks
```bash
# Validate project structure
python validate_project.py

# Test specific functionality
python test_functionality.py
python test_user_selection_logic.py
python test_recommendations.py
```

## Deployment

### Automatic CI/CD
- Push to `dev` branch → Auto-deploys to development environment
- Push to `main` branch → Auto-deploys to production environment

### Manual Deployment
```bash
# Deploy to Elastic Beanstalk
eb deploy

# Check deployment status
eb status
```

## Environment Configuration

### Required Environment Variables
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `AWS_ACCESS_KEY_ID`: AWS credentials for Bedrock
- `AWS_SECRET_ACCESS_KEY`: AWS credentials
- `AWS_DEFAULT_REGION`: AWS region (us-east-1 for Bedrock)

### Optional Configuration
- `DIGITAL_BRAIN_DB_PATH`: Custom database path
- `DIGITAL_BRAIN_CACHE_SIZE`: Cache size (default: 100)
- `DIGITAL_BRAIN_ENABLE_CACHE`: Enable caching (default: true)