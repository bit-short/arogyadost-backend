from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.chat.llm_orchestrator import LLMOrchestrator

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Initialize LLM orchestrator
llm_orchestrator = LLMOrchestrator()


@router.get("/llm/config")
async def get_llm_config() -> Dict[str, Any]:
    """Get current LLM configuration."""
    try:
        return llm_orchestrator.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/llm/config")
async def update_llm_config(config: Dict[str, Any]):
    """Update LLM configuration."""
    try:
        llm_orchestrator.update_model_config(**config)
        return {"message": "LLM configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/llm/models")
async def list_available_models():
    """List available AWS Bedrock models."""
    return {
        "cheap_models": [
            {
                "model_id": "amazon.titan-text-lite-v1",
                "name": "Amazon Titan Text Lite",
                "cost": "Very Low",
                "description": "Lightweight model for basic text generation"
            },
            {
                "model_id": "amazon.titan-text-express-v1", 
                "name": "Amazon Titan Text Express",
                "cost": "Low",
                "description": "Balanced performance and cost"
            }
        ],
        "premium_models": [
            {
                "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
                "name": "Claude 3 Haiku",
                "cost": "Medium",
                "description": "Fast, accurate responses"
            },
            {
                "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
                "name": "Claude 3 Sonnet", 
                "cost": "High",
                "description": "High-quality responses"
            }
        ]
    }


@router.post("/llm/test")
async def test_llm_connection(test_prompt: str = "Hello, how are you?"):
    """Test LLM connection with a simple prompt."""
    try:
        from app.services.chat.models import ChatContext, Message
        from app.services.chat.context_builder import ContextBuilder
        
        # Create minimal context for testing
        context = ChatContext(
            user_id="test_user",
            session_id="test_session", 
            recent_messages=[],
            digital_twin_summary={"user_id": "test_user"}
        )
        
        # Test the LLM
        response_text = ""
        async for event in llm_orchestrator.generate_response(context, test_prompt):
            if event.event_type.value == "complete":
                response_text = event.data
                break
            elif event.event_type.value == "error":
                raise Exception(event.data)
        
        return {
            "status": "success",
            "test_prompt": test_prompt,
            "response": response_text[:200] + "..." if len(response_text) > 200 else response_text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM test failed: {str(e)}")
