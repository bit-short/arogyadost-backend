# GitHub Actions CI/CD Setup

## Overview
Automatic deployment is configured for:
- **`dev` branch** → `aarogyadost-dev` environment
- **`main` branch** → `aarogyadost-prod` environment

## Environment URLs
- **Dev**: `http://aarogyadost-dev.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com`
- **Prod**: `http://aarogyadost-prod.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com`

## Required GitHub Secrets

You need to add these secrets to your GitHub repository:

### 1. Get AWS Credentials
```bash
# Check your current AWS credentials
aws configure list

# Or create new IAM user with these permissions:
# - AWSElasticBeanstalkFullAccess
# - AmazonS3FullAccess
```

### 2. Add Secrets to GitHub
Go to: **GitHub Repository → Settings → Secrets and variables → Actions**

Add these secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

## How It Works

### Deployment Triggers
```bash
# Deploy to DEV
git checkout dev
git add .
git commit -m "dev changes"
git push origin dev

# Deploy to PROD  
git checkout main
git merge dev          # or direct changes
git push origin main
```

### Workflow Process
1. **Code Push** → GitHub detects branch
2. **Environment Setup** → Ubuntu runner with Python 3.11
3. **EB CLI Install** → Installs AWS EB CLI
4. **AWS Auth** → Uses your GitHub secrets
5. **Deploy** → Runs `eb deploy` to correct environment
6. **Status** → Shows deployment result

## Branch Strategy

### Recommended Workflow
```bash
# Feature development
git checkout -b feature/new-api
# ... make changes ...
git push origin feature/new-api

# Merge to dev for testing
git checkout dev
git merge feature/new-api
git push origin dev          # 🚀 Auto-deploys to DEV

# After testing, promote to prod
git checkout main
git merge dev
git push origin main         # 🚀 Auto-deploys to PROD
```

## Monitoring Deployments

### GitHub Actions
- Go to **Actions** tab in your repository
- View deployment logs and status
- See which environment was deployed

### AWS Console
- Check Elastic Beanstalk console
- View deployment history
- Monitor application health

## Manual Override (if needed)

If you need to deploy manually:
```bash
# Switch environment
eb use aarogyadost-dev    # or aarogyadost-prod

# Deploy current code
eb deploy

# Check status
eb status
```

## Troubleshooting

### Deployment Fails
1. Check GitHub Actions logs
2. Verify AWS credentials in secrets
3. Ensure branch names match (`dev`, `main`)

### AWS Permissions Error
Your IAM user needs these policies:
- `AWSElasticBeanstalkFullAccess`
- `AmazonS3FullAccess`
- `AmazonEC2ReadOnlyAccess`

### Environment Not Found
If environments don't exist:
```bash
# Recreate environments
eb create aarogyadost-dev --instance-type t3.micro --single
eb create aarogyadost-prod --instance-type t3.micro --single
```

## Cost Impact
- **GitHub Actions**: Free (2000 minutes/month)
- **AWS**: Same as before (~$0 with free tier)
- **Total**: No additional costs

## Next Steps
1. Add AWS credentials to GitHub secrets
2. Push to `dev` branch to test
3. Merge to `main` for production deployment
4. Monitor via GitHub Actions tab
