# Amazon Translate Setup Guide

## Quick Setup for Translation

### 1. AWS Credentials Configuration

You need AWS credentials to use Amazon Translate. Choose one of these methods:

#### Option A: Environment Variables (Recommended for Development)
```bash
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=ap-south-1
```

#### Option B: AWS Credentials File
Create `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here
region = ap-south-1
```

#### Option C: IAM Role (Production/EC2)
If running on AWS infrastructure, attach an IAM role with translate permissions.

### 2. Required AWS Permissions

Your AWS user/role needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "translate:TranslateText"
            ],
            "Resource": "*"
        }
    ]
}
```

### 3. Test the Setup

Run the test script to verify everything works:
```bash
cd arogyadost-backend
python test_translation.py
```

### 4. Cost Optimization

- **Caching**: Translations are cached in memory to reduce API calls
- **Batch Processing**: Consider batching multiple texts for efficiency
- **Cost**: Amazon Translate charges ~$15 per million characters
- **Free Tier**: 2 million characters per month for first 12 months

### 5. Supported Languages

Currently configured for:
- **English (en)**: Source language
- **Hindi (hi)**: Target language  
- **Tamil (ta)**: Target language

### 6. Usage in API

The translation happens automatically when:
1. Client sends `Accept-Language: hi` or `Accept-Language: ta` header
2. API detects non-English language preference
3. Translation service translates supplement names and descriptions

### 7. Frontend Integration

The frontend already supports language switching:
1. Use the `LanguageSwitcher` component
2. Language preference is stored in localStorage
3. API client automatically sends Accept-Language headers

### 8. Troubleshooting

**Translation not working?**
- Check AWS credentials: `aws sts get-caller-identity`
- Verify region is set to `ap-south-1` (Mumbai)
- Check network connectivity to AWS services
- Review CloudWatch logs for translation API errors

**High costs?**
- Monitor translation cache hit rates
- Consider pre-translating common medical terms
- Use shorter, more concise descriptions

### 9. Production Considerations

- **Error Handling**: Falls back to English if translation fails
- **Performance**: Cached translations respond instantly
- **Monitoring**: Log translation requests for cost tracking
- **Security**: Use IAM roles instead of access keys in production