# Project Structure & Organization

## Root Level Structure

```
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── Procfile               # Heroku/deployment process file
├── .ebextensions/         # AWS Elastic Beanstalk configuration
├── apprunner.yaml         # AWS App Runner configuration
└── cors_config.py         # CORS configuration
```

## Application Structure (`app/`)

### Core Application
```
app/
├── __init__.py            # App package initialization
├── database.py            # Database configuration and session management
├── routers/               # API route handlers (FastAPI routers)
├── models/                # Pydantic models and data structures
├── services/              # Business logic and service layer
├── storage/               # Data persistence layer
├── config/                # Configuration modules
├── middleware/            # Custom middleware (translation, etc.)
└── utils/                 # Reusable utility functions and services
```

### API Routes (`app/routers/`)
- **digital_twin.py** - Digital twin CRUD operations
- **biological_age.py** - Age prediction endpoints
- **recommendations.py** - Health recommendations API
- **chat.py** - AI chat assistant endpoints
- **users.py** - User selection and management
- **admin.py** - Admin and configuration endpoints
- **health.py** - Health check endpoints
- **db_users.py** - Database user operations

### Data Models (`app/models/`)
- **digital_twin.py** - Core digital twin domain model
- **user_profile.py** - User selection models
- **user_management.py** - User CRUD models
- **computed_models.py** - Computed health data models
- **db_models.py** - SQLAlchemy database models

### Business Logic (`app/services/`)
```
services/
├── biological_age/       # Age calculation engine
│   ├── calculator.py     # Core calculation logic
│   ├── engine.py         # Main prediction engine
│   └── biomarker_normalizer.py
├── recommendations/      # Recommendation engine
│   ├── engine.py         # Main recommendation engine
│   ├── biomarker_rules.py
│   ├── condition_rules.py
│   └── priority_scorer.py
├── chat/                 # AI chat system
│   ├── chat_service.py   # Main chat orchestration
│   ├── aws_bedrock_llm.py # AWS Bedrock integration
│   ├── context_builder.py # Chat context management
│   └── session_manager.py # Session persistence
└── user_*.py            # User-related services
```

### Utilities (`app/utils/`)
- **translation.py** - AWS Translate service for multilingual support

## Data & Configuration

### Datasets (`datasets/`)
```
datasets/
├── users/               # User profile data
├── biomarkers/          # Biomarker test data
├── medical_history/     # Medical history data
├── lifestyle/           # Lifestyle data
├── interventions/       # Health interventions
└── ai_interactions/     # Chat history data
```

### Configuration (`config/`)
- **llm_config.json** - LLM model configuration

### Static Assets (`static/`)
- **user-selection.html** - Interactive user selection UI

## Testing Structure (`tests/`)

```
tests/
├── unit/                # Unit tests for individual components
├── property/            # Property-based tests (Hypothesis)
├── integration/         # Integration tests
└── test_data/           # Test datasets and fixtures
```

## Architecture Patterns

### Layered Architecture
1. **Router Layer** - FastAPI route handlers, request/response validation
2. **Service Layer** - Business logic, orchestration between components
3. **Storage Layer** - Data persistence, database operations
4. **Model Layer** - Data structures, validation, domain models

### Key Design Patterns
- **Repository Pattern** - Data access abstraction in storage layer
- **Service Pattern** - Business logic encapsulation
- **Factory Pattern** - Digital twin creation and management
- **Strategy Pattern** - Multiple recommendation rule types
- **Observer Pattern** - Health data change notifications

### Naming Conventions
- **Files**: snake_case (e.g., `user_service.py`)
- **Classes**: PascalCase (e.g., `DigitalTwin`, `BiologicalAgeEngine`)
- **Functions/Variables**: snake_case (e.g., `get_user_data`, `user_id`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DATABASE_URL`)
- **API Endpoints**: kebab-case (e.g., `/api/digital-twin`)

### File Organization Rules
- One main class per file in services and models
- Group related functionality in subdirectories
- Keep router files focused on single domain
- Separate database models from Pydantic models
- Use `__init__.py` files for package exports

### Import Conventions
- Absolute imports from app root (e.g., `from app.models.digital_twin import DigitalTwin`)
- Group imports: standard library, third-party, local
- Use specific imports over wildcard imports