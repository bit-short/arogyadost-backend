from typing import AsyncIterator, List, Optional
import asyncio
import json
from datetime import datetime

from .models import ChatContext, Message, StreamEvent, StreamEventType


class LLMOrchestrator:
    """Orchestrates LLM interactions with streaming support."""
    
    def __init__(self):
        self.system_prompt = self._build_system_prompt()
    
    async def generate_response(
        self, 
        context: ChatContext, 
        user_message: str
    ) -> AsyncIterator[StreamEvent]:
        """Generate streaming response from LLM."""
        
        try:
            # Build the full prompt
            prompt = self._build_prompt(context, user_message)
            
            # Yield thinking event
            yield StreamEvent(
                event_type=StreamEventType.THINKING,
                data="Analyzing your health data and generating response..."
            )
            
            # Simulate LLM response generation
            response_text = await self._generate_mock_response(context, user_message)
            
            # Stream the response token by token
            words = response_text.split()
            current_response = ""
            
            for i, word in enumerate(words):
                current_response += word + " "
                
                # Simulate streaming delay
                await asyncio.sleep(0.05)  # 50ms delay between words
                
                yield StreamEvent(
                    event_type=StreamEventType.TOKEN,
                    data=word + " "
                )
            
            # Yield completion event
            yield StreamEvent(
                event_type=StreamEventType.COMPLETE,
                data=current_response.strip()
            )
            
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
    
    async def _generate_mock_response(self, context: ChatContext, user_message: str) -> str:
        """Generate a mock response based on context and user message."""
        # This is a simplified mock implementation
        # In production, this would call an actual LLM API
        
        user_message_lower = user_message.lower()
        digital_twin = context.digital_twin_summary
        
        # Check for specific health topics
        if "cholesterol" in user_message_lower:
            biomarkers = digital_twin.get("latest_biomarkers", {}).get("key_markers", {})
            if "cholesterol" in biomarkers:
                chol_data = biomarkers["cholesterol"]
                return f"""Based on your recent test results, your cholesterol level is {chol_data['value']} {chol_data['unit']}, which is {chol_data['status']} (reference range: {chol_data['ref_range']}). 

This elevated level increases your cardiovascular risk. I recommend:
1. Dietary changes: reduce saturated fats, increase fiber
2. Regular exercise: aim for 150 minutes of moderate activity weekly
3. Follow up with your doctor about potential statin therapy
4. Retest in 6-8 weeks to monitor progress

**Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice. Please consult with your healthcare provider for personalized treatment recommendations."""
            else:
                return "I don't see recent cholesterol results in your data. For accurate cholesterol assessment, I recommend getting a lipid panel test. Would you like me to explain what cholesterol levels mean for your health?"
        
        elif "diabetes" in user_message_lower or "glucose" in user_message_lower:
            conditions = digital_twin.get("active_conditions", [])
            has_diabetes_condition = any("diabetes" in c["condition"].lower() for c in conditions)
            
            if has_diabetes_condition:
                return """I see you have an active diabetes-related condition. Managing diabetes involves several key areas:

1. **Blood Sugar Monitoring**: Regular glucose checks as recommended by your doctor
2. **Medication Adherence**: Take prescribed medications consistently
3. **Diet Management**: Focus on complex carbs, portion control, and consistent meal timing
4. **Physical Activity**: Regular exercise helps improve insulin sensitivity
5. **Regular Check-ups**: HbA1c testing every 3 months, annual eye and foot exams

Based on your health profile, I'd recommend discussing your current management plan with your healthcare team. Are there specific aspects of diabetes management you'd like to discuss?

**Medical Disclaimer**: This is general guidance only. Always follow your healthcare provider's specific recommendations for diabetes management."""
            else:
                biomarkers = digital_twin.get("latest_biomarkers", {}).get("key_markers", {})
                if "glucose" in biomarkers:
                    glucose_data = biomarkers["glucose"]
                    return f"Your recent glucose level was {glucose_data['value']} {glucose_data['unit']} ({glucose_data['status']}). This may indicate prediabetes or diabetes risk. I strongly recommend consulting with your healthcare provider for proper evaluation and management."
                else:
                    return "For diabetes risk assessment, I'd recommend getting a fasting glucose test and HbA1c. These tests help evaluate your blood sugar control over time."
        
        elif "vitamin d" in user_message_lower:
            biomarkers = digital_twin.get("latest_biomarkers", {}).get("key_markers", {})
            if "vitamin_d" in biomarkers:
                vit_d_data = biomarkers["vitamin_d"]
                return f"""Your vitamin D level is {vit_d_data['value']} {vit_d_data['unit']}, which is {vit_d_data['status']} (reference range: {vit_d_data['ref_range']}).

Low vitamin D can affect:
- Bone health and calcium absorption
- Immune system function
- Mood and energy levels

Recommendations:
1. **Supplementation**: Typically 1000-2000 IU daily (consult your doctor for exact dose)
2. **Sun exposure**: 10-15 minutes of midday sun several times per week
3. **Dietary sources**: Fatty fish, fortified foods, egg yolks
4. **Retest**: Check levels again in 8-12 weeks after starting supplementation

**Medical Disclaimer**: Please consult your healthcare provider for personalized vitamin D supplementation recommendations."""
            else:
                return "I don't see recent vitamin D results in your data. Vitamin D deficiency is common and can be easily tested and treated. Would you like me to explain the importance of vitamin D for your health?"
        
        elif any(word in user_message_lower for word in ["hello", "hi", "hey"]):
            age = digital_twin.get("demographics", {}).get("age", "")
            conditions = digital_twin.get("active_conditions", [])
            
            greeting = f"Hello! I'm your health chat assistant. "
            if age:
                greeting += f"I have access to your health profile and can provide personalized guidance. "
            
            if conditions:
                condition_names = [c["condition"] for c in conditions]
                greeting += f"I see you're managing {', '.join(condition_names)}. "
            
            greeting += "How can I help you with your health today?"
            return greeting
        
        else:
            # Generic health response
            return """I'm here to help with your health questions! I can provide personalized guidance based on your biomarker results, medical conditions, and health goals.

Some things I can help with:
- Interpreting your lab results
- Discussing your medical conditions
- Lifestyle recommendations
- Medication questions (though always consult your doctor)
- Health goal planning

What specific health topic would you like to discuss?

**Medical Disclaimer**: I provide educational information only and cannot replace professional medical advice. Always consult with your healthcare provider for medical decisions."""
