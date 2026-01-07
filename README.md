# Aarogyadost Backend

FastAPI backend for the Aarogyadost healthcare application.

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference with endpoints, request/response examples
- **[Architecture Overview](docs/API_ARCHITECTURE.md)** - System design, data flow, and technical specifications
- **[Deployment Guide](docs/DEPLOYMENT.md)** - AWS Elastic Beanstalk deployment instructions
- **[CI/CD Setup](docs/CI-CD-SETUP.md)** - GitHub Actions automated deployment configuration

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
pip install -r requirements.txt
```

### Run
```bash
uvicorn main:app --reload
```

API will be available at http://localhost:8000

### Local API Documentation
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

## Deployment

### Automatic Deployment (CI/CD)
- **Push to `dev` branch** → Auto-deploys to development environment
- **Push to `main` branch** → Auto-deploys to production environment

### Manual Deployment
See `docs/DEPLOYMENT.md` for detailed deployment instructions.

### CI/CD Setup
See `docs/CI-CD-SETUP.md` for GitHub Actions configuration.

## Architecture

- **Platform**: AWS Elastic Beanstalk
- **Runtime**: Python 3.11 on Amazon Linux 2023
- **Region**: ap-south-1 (Mumbai)
- **Instance**: t3.micro (Free Tier eligible)
- **Database**: Mock data (no external database required)
