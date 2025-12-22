# Aarogyadost Backend

FastAPI backend for the Aarogyadost healthcare application.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

API will be available at http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Endpoints

### Health Data
- `GET /api/health/biomarkers` - Get health categories and scores
- `GET /api/health/recommendations` - Get recommended actions
- `GET /api/health/metrics` - Get health metrics
- `GET /api/health/status` - Get overall health status
- `GET /api/biomarkers/{id}` - Get detailed biomarker data

### Doctors & Labs
- `GET /api/doctors` - Get list of doctors
- `GET /api/doctors/{id}` - Get doctor details
- `GET /api/labs` - Get list of labs
- `GET /api/labs/{id}` - Get lab details

### Chat
- `GET /api/chat/threads` - Get chat threads
- `POST /api/chat/message` - Send chat message
