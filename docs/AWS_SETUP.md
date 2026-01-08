# AWS Bedrock Integration Setup

## 🚀 Quick Setup

### 1. AWS Configuration
```bash
# Install AWS CLI if not already installed
pip install boto3

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region (us-east-1)
```

### 2. Enable Bedrock Models
```bash
# Go to AWS Console > Bedrock > Model Access
# Enable these models:
# - amazon.titan-text-lite-v1 (cheapest)
# - amazon.titan-text-express-v1 (balanced)
# - anthropic.claude-3-haiku-20240307-v1:0 (premium)
```

### 3. Test Integration
```bash
# Test the configuration
python3 test_aws_integration.py

# Test via API
curl -X POST "http://localhost:8000/api/admin/llm/test" \
  -H "Content-Type: application/json" \
  -d '{"test_prompt": "Hello, how can you help with my health?"}'
```

## 💰 Cost Analysis

### Monthly Costs (100 conversations/day)
- **Titan Text Lite**: ~$0.81/month (recommended for MVP)
- **Titan Text Express**: ~$1.92/month (better quality)
- **Claude 3 Haiku**: ~$1.05/month (best accuracy)

### Model Switching
```bash
# Switch to different model via API
curl -X PUT "http://localhost:8000/api/admin/llm/config" \
  -H "Content-Type: application/json" \
  -d '{"model_id": "amazon.titan-text-express-v1", "temperature": 0.5}'
```

## 🔧 Configuration

Edit `config/llm_config.json`:
```json
{
  "llm": {
    "provider": "aws_bedrock",
    "model_id": "amazon.titan-text-lite-v1",
    "region": "us-east-1",
    "max_tokens": 1000,
    "temperature": 0.7,
    "streaming": true
  },
  "fallback_models": [
    "amazon.titan-text-express-v1",
    "anthropic.claude-3-haiku-20240307-v1:0"
  ]
}
```

## 📊 Admin Endpoints

- `GET /api/admin/llm/config` - Get current configuration
- `PUT /api/admin/llm/config` - Update model settings
- `GET /api/admin/llm/models` - List available models
- `POST /api/admin/llm/test` - Test LLM connection

## 🎯 Ready to Use!

The health chat assistant now uses AWS Bedrock with:
- ✅ Cost-effective pricing (starting at $0.81/month)
- ✅ Multiple model options
- ✅ Streaming responses
- ✅ Automatic fallbacks
- ✅ Easy model switching
