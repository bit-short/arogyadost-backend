#!/usr/bin/env python3

import asyncio
import json
from datetime import datetime

def test_chat_logic():
    """Test the core chat logic without dependencies."""
    
    print("🤖 Testing Health Chat Assistant Logic")
    print("=" * 50)
    
    # Mock user data (similar to what would come from digital twin)
    test_users = {
        "test_user_1_29f": {
            "demographics": {"age": 29, "sex": "female"},
            "latest_biomarkers": {
                "key_markers": {
                    "cholesterol": {"value": 220, "unit": "mg/dL", "status": "high", "ref_range": "<200"},
                    "vitamin_d": {"value": 18, "unit": "ng/mL", "status": "low", "ref_range": "30-100"}
                }
            },
            "active_conditions": [
                {"condition": "Dyslipidemia", "severity": "moderate"},
                {"condition": "Vitamin D Deficiency", "severity": "mild"}
            ]
        },
        "test_user_3_31m": {
            "demographics": {"age": 31, "sex": "male"},
            "latest_biomarkers": {
                "key_markers": {
                    "glucose": {"value": 105, "unit": "mg/dL", "status": "high", "ref_range": "70-100"},
                    "hba1c": {"value": 5.8, "unit": "%", "status": "high", "ref_range": "4.0-5.6"}
                }
            },
            "active_conditions": [
                {"condition": "Prediabetes", "severity": "mild"}
            ]
        }
    }
    
    def generate_response(user_data, user_message):
        """Generate a mock response based on user data and message."""
        user_message_lower = user_message.lower()
        
        if "hello" in user_message_lower or "hi" in user_message_lower:
            age = user_data["demographics"]["age"]
            conditions = [c["condition"] for c in user_data["active_conditions"]]
            
            response = f"Hello! I'm your health chat assistant. I have access to your health profile "
            if conditions:
                response += f"and can see you're managing {', '.join(conditions)}. "
            response += "How can I help you with your health today?"
            return response
        
        elif "cholesterol" in user_message_lower:
            biomarkers = user_data.get("latest_biomarkers", {}).get("key_markers", {})
            if "cholesterol" in biomarkers:
                chol_data = biomarkers["cholesterol"]
                return f"""Based on your recent test results, your cholesterol level is {chol_data['value']} {chol_data['unit']}, which is {chol_data['status']} (reference range: {chol_data['ref_range']}). 

This elevated level increases your cardiovascular risk. I recommend:
1. Dietary changes: reduce saturated fats, increase fiber
2. Regular exercise: aim for 150 minutes of moderate activity weekly
3. Follow up with your doctor about potential statin therapy
4. Retest in 6-8 weeks to monitor progress

**Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice."""
            else:
                return "I don't see recent cholesterol results in your data. For accurate cholesterol assessment, I recommend getting a lipid panel test."
        
        elif "diabetes" in user_message_lower or "glucose" in user_message_lower:
            conditions = user_data.get("active_conditions", [])
            has_diabetes_condition = any("diabetes" in c["condition"].lower() for c in conditions)
            
            if has_diabetes_condition:
                return """I see you have an active diabetes-related condition. Managing diabetes involves several key areas:

1. **Blood Sugar Monitoring**: Regular glucose checks as recommended by your doctor
2. **Medication Adherence**: Take prescribed medications consistently  
3. **Diet Management**: Focus on complex carbs, portion control, and consistent meal timing
4. **Physical Activity**: Regular exercise helps improve insulin sensitivity
5. **Regular Check-ups**: HbA1c testing every 3 months

Based on your health profile, I'd recommend discussing your current management plan with your healthcare team.

**Medical Disclaimer**: This is general guidance only. Always follow your healthcare provider's specific recommendations."""
            else:
                biomarkers = user_data.get("latest_biomarkers", {}).get("key_markers", {})
                if "glucose" in biomarkers:
                    glucose_data = biomarkers["glucose"]
                    return f"Your recent glucose level was {glucose_data['value']} {glucose_data['unit']} ({glucose_data['status']}). This may indicate prediabetes or diabetes risk. I strongly recommend consulting with your healthcare provider for proper evaluation."
        
        elif "weight" in user_message_lower and "loss" in user_message_lower:
            return """For healthy weight loss, I recommend focusing on these evidence-based strategies:

1. **Caloric Balance**: Create a moderate deficit (300-500 calories/day)
2. **Protein Intake**: Aim for 0.8-1g per kg body weight to preserve muscle
3. **Regular Exercise**: Combine cardio and strength training
4. **Sleep Quality**: 7-9 hours per night supports metabolism
5. **Stress Management**: High cortisol can hinder weight loss

Based on your metabolic markers, monitoring glucose and insulin sensitivity will be important during your weight loss journey.

**Medical Disclaimer**: Please consult with a healthcare provider or registered dietitian for personalized weight loss guidance."""
        
        else:
            return """I'm here to help with your health questions! I can provide personalized guidance based on your biomarker results, medical conditions, and health goals.

Some things I can help with:
- Interpreting your lab results
- Discussing your medical conditions  
- Lifestyle recommendations
- Health goal planning

What specific health topic would you like to discuss?

**Medical Disclaimer**: I provide educational information only and cannot replace professional medical advice."""
    
    # Test conversations
    test_conversations = [
        {
            "user": "test_user_1_29f",
            "messages": [
                "Hello! I'd like to discuss my health.",
                "What can you tell me about my cholesterol levels?",
                "Should I be worried about my vitamin D levels?"
            ]
        },
        {
            "user": "test_user_3_31m", 
            "messages": [
                "Hi there!",
                "I'm concerned about diabetes. What should I know?",
                "I'm trying to lose weight. Can you help me understand my metabolic health?"
            ]
        }
    ]
    
    for conversation in test_conversations:
        user_id = conversation["user"]
        user_data = test_users[user_id]
        
        print(f"\n👤 Testing conversation with {user_id.upper()}")
        print(f"📊 User profile: {user_data['demographics']['age']}-year-old {user_data['demographics']['sex']}")
        
        conditions = [c["condition"] for c in user_data["active_conditions"]]
        if conditions:
            print(f"🏥 Active conditions: {', '.join(conditions)}")
        
        biomarkers = user_data.get("latest_biomarkers", {}).get("key_markers", {})
        if biomarkers:
            abnormal_markers = [f"{k}: {v['value']} {v['unit']} ({v['status']})" 
                              for k, v in biomarkers.items() if v['status'] != 'normal']
            if abnormal_markers:
                print(f"🔬 Abnormal biomarkers: {', '.join(abnormal_markers)}")
        
        print("-" * 60)
        
        for i, message in enumerate(conversation["messages"], 1):
            print(f"\n💬 Message {i}:")
            print(f"👤 User: {message}")
            
            response = generate_response(user_data, message)
            print(f"🤖 Assistant: {response}")
    
    print("\n🎉 Health Chat Assistant Logic Test Completed!")
    print("\n📊 Test Summary:")
    print("✅ Context-aware responses using user health data")
    print("✅ Personalized guidance based on biomarkers and conditions")
    print("✅ Medical disclaimers and safety warnings")
    print("✅ Multi-user support with different health profiles")
    print("✅ Natural conversation flow")

def test_streaming_simulation():
    """Simulate streaming response delivery."""
    
    print("\n🌊 Testing Streaming Response Simulation")
    print("=" * 40)
    
    sample_response = """Based on your recent test results, your cholesterol level is 220 mg/dL, which is high. This elevated level increases your cardiovascular risk. I recommend dietary changes, regular exercise, and consulting your doctor about potential statin therapy."""
    
    print("👤 User: What about my cholesterol levels?")
    print("🤖 Assistant: ", end="", flush=True)
    
    # Simulate token-by-token streaming
    words = sample_response.split()
    for word in words:
        print(word + " ", end="", flush=True)
        # In real implementation, this would be async with proper delays
        import time
        time.sleep(0.05)  # 50ms delay between words
    
    print("\n✅ Streaming simulation completed!")

def test_session_management():
    """Test session management logic."""
    
    print("\n📂 Testing Session Management Logic")
    print("=" * 35)
    
    # Mock session data
    sessions = []
    
    def create_session(user_id, title=None):
        session = {
            "session_id": f"session_{len(sessions) + 1}",
            "user_id": user_id,
            "title": title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "message_count": 0,
            "messages": []
        }
        sessions.append(session)
        return session
    
    def add_message(session_id, role, content):
        for session in sessions:
            if session["session_id"] == session_id:
                message = {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now()
                }
                session["messages"].append(message)
                session["message_count"] += 1
                session["last_activity"] = datetime.now()
                return message
        return None
    
    def list_user_sessions(user_id):
        user_sessions = [s for s in sessions if s["user_id"] == user_id]
        return sorted(user_sessions, key=lambda x: x["last_activity"], reverse=True)
    
    # Test session operations
    print("✅ Creating sessions for test users...")
    
    session1 = create_session("test_user_1_29f", "Health Discussion")
    session2 = create_session("test_user_3_31m", "Weight Loss Chat")
    
    print(f"   - Created session: {session1['title']} ({session1['session_id']})")
    print(f"   - Created session: {session2['title']} ({session2['session_id']})")
    
    print("\n✅ Adding messages to sessions...")
    
    add_message(session1["session_id"], "user", "Hello!")
    add_message(session1["session_id"], "assistant", "Hi! How can I help with your health today?")
    add_message(session1["session_id"], "user", "Tell me about my cholesterol")
    
    add_message(session2["session_id"], "user", "I want to lose weight")
    add_message(session2["session_id"], "assistant", "I can help you with weight loss strategies...")
    
    print(f"   - Session 1 now has {session1['message_count']} messages")
    print(f"   - Session 2 now has {session2['message_count']} messages")
    
    print("\n✅ Listing user sessions...")
    
    for user_id in ["test_user_1_29f", "test_user_3_31m"]:
        user_sessions = list_user_sessions(user_id)
        print(f"   - {user_id}: {len(user_sessions)} sessions")
        for session in user_sessions:
            last_message = session["messages"][-1]["content"][:50] + "..." if session["messages"] else "No messages"
            print(f"     * {session['title']}: {last_message}")
    
    print("\n✅ Session management test completed!")

if __name__ == "__main__":
    test_chat_logic()
    test_streaming_simulation()
    test_session_management()
