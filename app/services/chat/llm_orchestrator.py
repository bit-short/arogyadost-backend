from typing import AsyncIterator, List, Optional
import asyncio
import json
from datetime import datetime

from .models import ChatContext, Message, StreamEvent, StreamEventType
from .aws_bedrock_llm import AWSBedrockLLM


class LLMOrchestrator:
    """Orchestrates LLM interactions with AWS Bedrock streaming support."""
    
    def __init__(self, config_path: str = "config/llm_config.json"):
        self.aws_llm = AWSBedrockLLM(config_path)
        self.system_prompt = self._build_system_prompt()
    
    async def generate_response(
        self, 
        context: ChatContext, 
        user_message: str
    ) -> AsyncIterator[StreamEvent]:
        """Generate streaming response from AWS Bedrock."""
        
        try:
            # Build the full prompt
            prompt = self._build_prompt(context, user_message)
            
            # Generate response using AWS Bedrock
            async for event in self.aws_llm.generate_streaming_response(prompt):
                yield event
            
        except Exception as e:
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                data=f"Error generating response: {str(e)}"
            )
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the health chat assistant."""
        return """You are a knowledgeable health chat assistant. Your role is to provide helpful, personalized health guidance based on the user's digital twin data including biomarkers, medical conditions, medications, and lifestyle factors.

IMPORTANT GUIDELINES:
1. Always provide medical disclaimers - you are not a replacement for professional medical advice
2. Reference specific user data when available (biomarker values, conditions, medications)
3. If asked to diagnose conditions, decline and suggest consulting a healthcare provider
4. For emergency symptoms, recommend immediate medical attention
5. Be conversational and supportive while maintaining medical accuracy
6. Include units and reference ranges when discussing biomarker values
7. Explain your reasoning based on the user's specific health data

Remember: You have access to the user's health data, so personalize your responses accordingly."""
    
    def _build_prompt(self, context: ChatContext, user_message: str) -> str:
        """Build the complete prompt for the LLM."""
        prompt_parts = [self.system_prompt]
        
        # Add user context
        context_str = self._format_context(context)
        if context_str:
            prompt_parts.append(f"\nUSER HEALTH CONTEXT:\n{context_str}")
        
        # Add conversation history
        if context.recent_messages:
            prompt_parts.append("\nCONVERSATION HISTORY:")
            for message in context.recent_messages[-5:]:  # Last 5 messages
                role = "User" if message.role.value == "user" else "Assistant"
                prompt_parts.append(f"{role}: {message.content}")
        
        # Add current user message
        prompt_parts.append(f"\nUser: {user_message}")
        prompt_parts.append("\nAssistant:")
        
        return "\n".join(prompt_parts)
    
    def _format_context(self, context: ChatContext) -> str:
        """Format context for the prompt."""
        from .context_builder import ContextBuilder
        builder = ContextBuilder()
        return builder.format_context_for_llm(context)
    
    def get_model_info(self) -> dict:
        """Get current model configuration."""
        return self.aws_llm.get_model_info()
    
    def update_model_config(self, **kwargs) -> None:
        """Update model configuration."""
        self.aws_llm.update_model_config(**kwargs)
