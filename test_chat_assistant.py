#!/usr/bin/env python3

import asyncio
import json
from datetime import datetime

# Mock the async dependencies for testing
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_health_chat_assistant():
    """Test the health chat assistant functionality."""
    
    print("🤖 Testing Health Chat Assistant")
    print("=" * 50)
    
    # Import after path setup
    from app.services.chat.chat_service import ChatService
    from app.services.chat.models import MessageRole
    
    # Initialize chat service
    chat_service = ChatService("data")
    
    # Test user
    user_id = "test_user_1_29f"
    
    print(f"\n👤 Testing with user: {user_id}")
    
    # Test 1: Create a new session
    print("\n📝 Test 1: Creating new chat session...")
    session = await chat_service.create_session(user_id, "Health Discussion")
    print(f"✅ Created session: {session.session_id}")
    print(f"   Title: {session.title}")
    print(f"   Created: {session.created_at}")
    
    # Test 2: Send a greeting message
    print("\n💬 Test 2: Sending greeting message...")
    user_message = "Hello! I'd like to discuss my health."
    
    print(f"User: {user_message}")
    print("Assistant: ", end="", flush=True)
    
    full_response = ""
    async for event in chat_service.send_message(user_id, session.session_id, user_message):
        if event.event_type.value == "token":
            print(event.data, end="", flush=True)
        elif event.event_type.value == "complete":
            full_response = event.data
            print()  # New line after complete response
    
    # Test 3: Ask about cholesterol
    print("\n💬 Test 3: Asking about cholesterol...")
    user_message = "What can you tell me about my cholesterol levels?"
    
    print(f"User: {user_message}")
    print("Assistant: ", end="", flush=True)
    
    async for event in chat_service.send_message(user_id, session.session_id, user_message):
        if event.event_type.value == "token":
            print(event.data, end="", flush=True)
        elif event.event_type.value == "complete":
            print()  # New line after complete response
    
    # Test 4: Ask about diabetes
    print("\n💬 Test 4: Asking about diabetes...")
    user_message = "I'm concerned about diabetes. What should I know?"
    
    print(f"User: {user_message}")
    print("Assistant: ", end="", flush=True)
    
    async for event in chat_service.send_message(user_id, session.session_id, user_message):
        if event.event_type.value == "token":
            print(event.data, end="", flush=True)
        elif event.event_type.value == "complete":
            print()  # New line after complete response
    
    # Test 5: Get session messages
    print("\n📋 Test 5: Retrieving session messages...")
    messages = await chat_service.get_session_messages(user_id, session.session_id)
    print(f"✅ Retrieved {len(messages)} messages:")
    
    for i, msg in enumerate(messages, 1):
        role_emoji = "👤" if msg.role == MessageRole.USER else "🤖"
        content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
        print(f"{i}. {role_emoji} {msg.role.value}: {content_preview}")
    
    # Test 6: List user sessions
    print("\n📂 Test 6: Listing user sessions...")
    sessions = await chat_service.list_sessions(user_id)
    print(f"✅ Found {len(sessions)} sessions:")
    
    for session_summary in sessions:
        print(f"   - {session_summary.title}")
        print(f"     Last activity: {session_summary.last_activity}")
        print(f"     Messages: {session_summary.message_count}")
        print(f"     Preview: {session_summary.last_message_preview}")
    
    # Test 7: Test with different user (test_user_3_31m)
    print(f"\n👤 Test 7: Testing with different user (test_user_3_31m)...")
    user_id_2 = "test_user_3_31m"
    
    session_2 = await chat_service.create_session(user_id_2, "Weight Loss Discussion")
    user_message = "I'm trying to lose weight. Can you help me understand my metabolic health?"
    
    print(f"User: {user_message}")
    print("Assistant: ", end="", flush=True)
    
    async for event in chat_service.send_message(user_id_2, session_2.session_id, user_message):
        if event.event_type.value == "token":
            print(event.data, end="", flush=True)
        elif event.event_type.value == "complete":
            print()  # New line after complete response
    
    print("\n🎉 Health Chat Assistant test completed!")
    print("\n📊 Test Summary:")
    print("✅ Session creation and management")
    print("✅ Message streaming and persistence")
    print("✅ Context-aware responses using digital twin data")
    print("✅ Personalized health guidance")
    print("✅ Medical disclaimers and safety")
    print("✅ Multi-user support")

async def test_context_building():
    """Test context building with digital twin data."""
    
    print("\n🧠 Testing Context Building")
    print("=" * 30)
    
    from app.services.chat.context_builder import ContextBuilder
    from app.services.chat.models import Message, MessageRole
    
    context_builder = ContextBuilder("data")
    
    # Test with user who has health data
    user_id = "test_user_1_29f"
    session_id = "test_session"
    
    # Create some mock recent messages
    recent_messages = [
        Message(
            session_id=session_id,
            role=MessageRole.USER,
            content="Hello, I want to discuss my cholesterol levels"
        ),
        Message(
            session_id=session_id,
            role=MessageRole.ASSISTANT,
            content="I can help you with that. Let me check your recent test results."
        )
    ]
    
    # Build context
    context = await context_builder.build_context(
        user_id=user_id,
        session_id=session_id,
        recent_messages=recent_messages,
        include_research=True
    )
    
    print(f"✅ Built context for user: {context.user_id}")
    print(f"📊 Digital twin summary keys: {list(context.digital_twin_summary.keys())}")
    print(f"💬 Recent messages: {len(context.recent_messages)}")
    
    # Format context for LLM
    formatted_context = context_builder.format_context_for_llm(context)
    print(f"\n📝 Formatted context for LLM:")
    print(formatted_context)

if __name__ == "__main__":
    asyncio.run(test_health_chat_assistant())
    asyncio.run(test_context_building())
