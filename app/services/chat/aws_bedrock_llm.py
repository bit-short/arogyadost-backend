import json
import boto3
from typing import AsyncIterator, Dict, Any, Optional
from pathlib import Path
import asyncio
from datetime import datetime

from .models import StreamEvent, StreamEventType


class AWSBedrockLLM:
    """AWS Bedrock LLM integration with streaming support."""
    
    def __init__(self, config_path: str = "config/llm_config.json"):
        self.config = self._load_config(config_path)
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=self.config["llm"]["region"]
        )
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load LLM configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default config if file doesn't exist
            return {
                "llm": {
                    "provider": "aws_bedrock",
                    "model_id": "amazon.titan-text-lite-v1",
                    "region": "us-east-1",
                    "max_tokens": 1000,
                    "temperature": 0.7,
                    "streaming": True
                }
            }
    
    async def generate_streaming_response(self, prompt: str) -> AsyncIterator[StreamEvent]:
        """Generate streaming response from AWS Bedrock."""
        try:
            # Prepare request body based on model type
            model_id = self.config["llm"]["model_id"]
            
            if "titan" in model_id:
                body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": self.config["llm"]["max_tokens"],
                        "temperature": self.config["llm"]["temperature"],
                        "stopSequences": []
                    }
                }
            elif "claude" in model_id:
                body = {
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": self.config["llm"]["max_tokens"],
                    "temperature": self.config["llm"]["temperature"]
                }
            else:
                # Generic format
                body = {
                    "prompt": prompt,
                    "max_tokens": self.config["llm"]["max_tokens"],
                    "temperature": self.config["llm"]["temperature"]
                }
            
            # Make streaming request
            if self.config["llm"]["streaming"]:
                yield StreamEvent(
                    event_type=StreamEventType.THINKING,
                    data="Connecting to AWS Bedrock..."
                )
                
                response = self.bedrock_client.invoke_model_with_response_stream(
                    modelId=model_id,
                    body=json.dumps(body)
                )
                
                # Process streaming response
                full_text = ""
                for event in response['body']:
                    chunk = json.loads(event['chunk']['bytes'])
                    
                    if "titan" in model_id:
                        if 'outputText' in chunk:
                            token = chunk['outputText']
                            full_text += token
                            yield StreamEvent(
                                event_type=StreamEventType.TOKEN,
                                data=token
                            )
                    elif "claude" in model_id:
                        if chunk.get('type') == 'content_block_delta':
                            token = chunk.get('delta', {}).get('text', '')
                            full_text += token
                            yield StreamEvent(
                                event_type=StreamEventType.TOKEN,
                                data=token
                            )
                    
                    # Small delay for realistic streaming
                    await asyncio.sleep(0.01)
                
                yield StreamEvent(
                    event_type=StreamEventType.COMPLETE,
                    data=full_text
                )
            else:
                # Non-streaming fallback
                response = self.bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                
                if "titan" in model_id:
                    text = response_body.get('results', [{}])[0].get('outputText', '')
                elif "claude" in model_id:
                    text = response_body.get('content', [{}])[0].get('text', '')
                else:
                    text = response_body.get('completion', '')
                
                # Simulate streaming for non-streaming models
                words = text.split()
                for word in words:
                    yield StreamEvent(
                        event_type=StreamEventType.TOKEN,
                        data=word + " "
                    )
                    await asyncio.sleep(0.05)
                
                yield StreamEvent(
                    event_type=StreamEventType.COMPLETE,
                    data=text
                )
                
        except Exception as e:
            # Try fallback models
            for fallback_model in self.config.get("fallback_models", []):
                try:
                    self.config["llm"]["model_id"] = fallback_model
                    async for event in self.generate_streaming_response(prompt):
                        yield event
                    return
                except:
                    continue
            
            # If all models fail, return error
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                data=f"AWS Bedrock error: {str(e)}"
            )
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get current model configuration."""
        return {
            "provider": self.config["llm"]["provider"],
            "model_id": self.config["llm"]["model_id"],
            "region": self.config["llm"]["region"],
            "max_tokens": self.config["llm"]["max_tokens"],
            "temperature": self.config["llm"]["temperature"]
        }
    
    def update_model_config(self, **kwargs) -> None:
        """Update model configuration."""
        for key, value in kwargs.items():
            if key in self.config["llm"]:
                self.config["llm"][key] = value
        
        # Reinitialize client if region changed
        if "region" in kwargs:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.config["llm"]["region"]
            )
