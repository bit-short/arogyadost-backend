# Aarogyadost Backend Deployment Guide

## Overview

The Aarogyadost backend is deployed on AWS Elastic Beanstalk using a FastAPI application. This guide covers the deployment process, architecture, and management.

## Architecture

```
Developer → Git Push → EB CLI → AWS Elastic Beanstalk → EC2 Instance
                                      ↓
                               Application Load Balancer (Prod only)
                                      ↓
                               Your FastAPI App (Port 8000)
```

## Current Deployment

- **Platform**: AWS Elastic Beanstalk
- **Region**: ap-south-1 (Mumbai)
- **Runtime**: Python 3.11 on Amazon Linux 2023
- **Instance Type**: t3.micro (Free Tier)
- **Environment**: Single instance (no load balancer for cost savings)

### Live URLs
- **Dev Environment**: `http://aarogyadost-dev.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com`
- **API Documentation**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc`

## Deployment Files

### Required Files
- `Procfile` - Tells Beanstalk how to start your app
- `requirements.txt` - Python dependencies
- `.ebextensions/01_python.config` - Beanstalk configuration
- `.ebignore` - Files to exclude from deployment

### File Contents

**Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port 8000
```

**.ebextensions/01_python.config**
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: main:app
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.micro
```

## Deployment Process

### Initial Setup (One-time)
```bash
# Install EB CLI
pipx install awsebcli

# Initialize application
eb init -p python-3.11 aarogyadost-backend --region ap-south-1

# Create environment
eb create aarogyadost-dev --instance-type t3.micro --single
```

### Regular Deployments
```bash
# Deploy code changes
eb deploy

# Check deployment status
eb status

# View application logs
eb logs

# Open app in browser
eb open
```

## Environment Management

### Switch Between Environments
```bash
# List environments
eb list

# Switch to dev
eb use aarogyadost-dev

# Switch to prod (when created)
eb use aarogyadost-prod
```

### Create Production Environment
```bash
# Create prod with load balancer and auto-scaling
eb create aarogyadost-prod --instance-type t3.small

# Or create prod without load balancer (cheaper)
eb create aarogyadost-prod --instance-type t3.micro --single
```

## Configuration Management

### Environment Variables
```bash
# Set environment variables
eb setenv DATABASE_URL=your-db-url API_KEY=your-key

# View current environment variables
eb printenv
```

### Scaling
```bash
# Scale instances (prod environment only)
eb scale 2

# Enable auto-scaling
eb config
# Then modify auto-scaling settings in the editor
```

## Monitoring & Debugging

### View Logs
```bash
# Real-time logs
eb logs --all

# Download log bundle
eb logs --zip
```

### SSH Access
```bash
# SSH into instance
eb ssh
```

### Health Monitoring
```bash
# Check environment health
eb health

# Detailed status
eb status --verbose
```

## Cost Optimization

### Current Costs (Mumbai Region)
- **Dev Environment**: FREE (t3.micro free tier)
- **Prod Environment**: 
  - With load balancer: ~$25/month
  - Single instance: ~$8.50/month (after free tier)

### Cost-Saving Tips
1. Use `--single` flag to avoid load balancer costs
2. Use t3.micro instances (free tier eligible)
3. Terminate unused environments: `eb terminate env-name`
4. Use spot instances for dev: `--enable-spot`

## Troubleshooting

### Common Issues

**Deployment Fails**
```bash
# Check logs for errors
eb logs

# Validate configuration
eb config save
```

**App Not Starting**
- Check Procfile syntax
- Verify requirements.txt has all dependencies
- Check Python version compatibility

**502/503 Errors**
- App not binding to correct port (should be 8000)
- Check if app starts locally: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Health Check Endpoint
Beanstalk expects your app to respond to health checks on `/`. Current setup:
- Root endpoint returns FastAPI default response
- All API endpoints under `/api/`

## Security Considerations

### Current Setup
- Single instance (no load balancer) = direct EC2 access
- CORS enabled for all origins (development only)
- No HTTPS (HTTP only)

### Production Recommendations
- Enable load balancer for HTTPS termination
- Restrict CORS origins
- Use environment variables for secrets
- Enable AWS WAF for protection

## Backup & Recovery

### Code Backup
- Code is in Git repository
- Beanstalk keeps application versions

### Environment Recreation
```bash
# Save current configuration
eb config save

# Recreate environment using saved config
eb create new-env --cfg saved-config-name
```

## CI/CD Integration

### Automatic Deployment (Current)
- **`dev` branch** → Auto-deploys to `aarogyadost-dev`
- **`main` branch** → Auto-deploys to `aarogyadost-prod`

See `CI-CD-SETUP.md` for configuration details.

### Manual Deployment (Backup)
```bash
eb use aarogyadost-dev    # or aarogyadost-prod
eb deploy
```

## Next Steps

1. **Add Database**: RDS PostgreSQL/MySQL or DynamoDB
2. **Enable HTTPS**: Add load balancer and SSL certificate
3. **Monitoring**: CloudWatch logs and metrics
4. **Caching**: ElastiCache Redis for performance
5. **CDN**: CloudFront for static assets

## Quick Reference

```bash
# Essential commands
eb status          # Check environment status
eb deploy          # Deploy code changes
eb logs            # View logs
eb open            # Open in browser
eb terminate       # Delete environment (careful!)

# Environment switching
eb list            # List environments
eb use env-name    # Switch environment

# Configuration
eb config          # Edit environment config
eb setenv KEY=val  # Set environment variable
eb printenv        # Show environment variables
```
