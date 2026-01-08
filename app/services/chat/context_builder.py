from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
from pathlib import Path

from .models import ChatContext, Message
from ..recommendations.digital_twin_analyzer import DigitalTwinAnalyzer


class ContextBuilder:
    """Builds context for LLM requests by combining conversation history and digital twin data."""
    
    def __init__(self, data_dir: str = "data"):
        self.digital_twin_analyzer = DigitalTwinAnalyzer(data_dir)
        self.cache = {}  # Simple in-memory cache
    
    async def build_context(
        self, 
        user_id: str, 
        session_id: str, 
        recent_messages: List[Message],
        include_research: bool = False
    ) -> ChatContext:
        """Build comprehensive context for LLM request."""
        
        # Get digital twin summary
        digital_twin_summary = await self._get_digital_twin_summary(user_id)
        
        # Get relevant documents (if any)
        relevant_documents = await self._get_relevant_documents(user_id, recent_messages)
        
        # Build research context if requested
        research_context = None
        if include_research:
            research_context = await self._build_research_context(recent_messages)
        
        return ChatContext(
            user_id=user_id,
            session_id=session_id,
            recent_messages=recent_messages,
            digital_twin_summary=digital_twin_summary,
            relevant_documents=relevant_documents,
            research_context=research_context
        )
    
    async def _get_digital_twin_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summarized digital twin data for context."""
        cache_key = f"digital_twin_{user_id}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(minutes=30):  # 30-minute cache
                return cached_data
        
        try:
            # Load digital twin data
            digital_twin = self.digital_twin_analyzer.load_user_data(user_id)
            
            # Create summary for LLM context
            summary = {
                "user_id": user_id,
                "demographics": {
                    "age": digital_twin.demographics.age,
                    "sex": digital_twin.demographics.sex
                },
                "latest_biomarkers": {},
                "active_conditions": [],
                "medications": [],
                "family_history": [],
                "health_goals": []
            }
            
            # Add latest biomarkers
            if digital_twin.latest_biomarkers:
                summary["latest_biomarkers"] = {
                    "test_date": digital_twin.latest_biomarkers.test_date.isoformat(),
                    "key_markers": {}
                }
                
                # Extract key biomarkers
                for category, markers in digital_twin.latest_biomarkers.categories.items():
                    for marker_name, marker_value in markers.items():
                        if marker_value.status in ["high", "low"]:  # Only abnormal values
                            summary["latest_biomarkers"]["key_markers"][marker_name] = {
                                "value": marker_value.value,
                                "unit": marker_value.unit,
                                "status": marker_value.status,
                                "ref_range": marker_value.ref_range
                            }
            
            # Add active conditions
            for condition in digital_twin.conditions:
                if condition.status == "active":
                    summary["active_conditions"].append({
                        "condition": condition.condition,
                        "severity": getattr(condition, 'severity', None)
                    })
            
            # Add current medications
            for medication in digital_twin.medications:
                summary["medications"].append({
                    "name": medication.name,
                    "dosage": medication.dosage
                })
            
            # Add family history
            for family_condition in digital_twin.family_history:
                summary["family_history"].append({
                    "condition": family_condition.condition,
                    "relation": family_condition.relation
                })
            
            # Add health goals
            for goal in digital_twin.goals:
                summary["health_goals"].append({
                    "goal": goal.goal,
                    "priority": goal.priority
                })
            
            # Cache the summary
            self.cache[cache_key] = (summary, datetime.now())
            
            return summary
            
        except Exception as e:
            print(f"Error building digital twin summary: {e}")
            return {
                "user_id": user_id,
                "error": "Digital twin data unavailable"
            }
    
    async def _get_relevant_documents(
        self, 
        user_id: str, 
        recent_messages: List[Message]
    ) -> List[Dict[str, Any]]:
        """Get documents relevant to the conversation."""
        # For now, return empty list
        # In a full implementation, this would analyze recent messages
        # and retrieve relevant lab reports, medical documents, etc.
        return []
    
    async def _build_research_context(self, recent_messages: List[Message]) -> str:
        """Build research context from recent messages."""
        # Extract key medical terms and topics from recent messages
        medical_topics = []
        
        for message in recent_messages[-3:]:  # Last 3 messages
            if message.role.value == "user":
                # Simple keyword extraction (in production, use NLP)
                content = message.content.lower()
                medical_keywords = [
                    "cholesterol", "diabetes", "blood pressure", "vitamin d",
                    "thyroid", "glucose", "insulin", "heart", "liver", "kidney"
                ]
                
                for keyword in medical_keywords:
                    if keyword in content:
                        medical_topics.append(keyword)
        
        if medical_topics:
            return f"Recent medical topics discussed: {', '.join(set(medical_topics))}"
        
        return None
    
    def format_context_for_llm(self, context: ChatContext) -> str:
        """Format context into a string suitable for LLM prompt."""
        context_parts = []
        
        # User demographics
        demographics = context.digital_twin_summary.get("demographics", {})
        if demographics:
            age = demographics.get("age", "unknown")
            sex = demographics.get("sex", "unknown")
            context_parts.append(f"User: {age}-year-old {sex}")
        
        # Active conditions
        conditions = context.digital_twin_summary.get("active_conditions", [])
        if conditions:
            condition_names = [c["condition"] for c in conditions]
            context_parts.append(f"Active conditions: {', '.join(condition_names)}")
        
        # Key biomarkers
        biomarkers = context.digital_twin_summary.get("latest_biomarkers", {})
        if biomarkers and biomarkers.get("key_markers"):
            marker_info = []
            for marker, data in biomarkers["key_markers"].items():
                marker_info.append(f"{marker}: {data['value']} {data['unit']} ({data['status']})")
            if marker_info:
                test_date = biomarkers.get("test_date", "unknown date")
                context_parts.append(f"Recent abnormal biomarkers ({test_date}): {', '.join(marker_info)}")
        
        # Medications
        medications = context.digital_twin_summary.get("medications", [])
        if medications:
            med_names = [m["name"] for m in medications]
            context_parts.append(f"Current medications: {', '.join(med_names)}")
        
        # Family history
        family_history = context.digital_twin_summary.get("family_history", [])
        if family_history:
            family_conditions = [f"{fh['condition']} ({fh['relation']})" for fh in family_history]
            context_parts.append(f"Family history: {', '.join(family_conditions)}")
        
        # Research context
        if context.research_context:
            context_parts.append(f"Research context: {context.research_context}")
        
        return "\n".join(context_parts) if context_parts else "No specific health data available."
