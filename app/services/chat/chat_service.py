from typing import AsyncIterator, Optional
import uuid
from datetime import datetime

from .models import (
    ChatSession, ChatSessionSummary, Message, MessageRole, 
    StreamEvent, ChatRequest, ChatResponse
)
from .session_manager import SessionManager
from .message_store import MessageStore
from .context_builder import ContextBuilder
from .llm_orchestrator import LLMOrchestrator


class ChatService:
    """Main chat service orchestrating all chat interactions."""
    
    def __init__(self, data_dir: str = "data"):
        self.session_manager = SessionManager(f"{data_dir}/chat")
        self.message_store = MessageStore(f"{data_dir}/chat")
        self.context_builder = ContextBuilder(data_dir)
        self.llm_orchestrator = LLMOrchestrator()
    
    async def send_message(
        self, 
        user_id: str, 
        session_id: Optional[str], 
        message: str
    ) -> AsyncIterator[StreamEvent]:
        """Send a message and stream the assistant's response."""
        
        # Get or create session
        if session_id:
            session = await self.session_manager.get_session(session_id)
            if not session or session.user_id != user_id:
                raise ValueError("Invalid session ID")
        else:
            session = await self.session_manager.create_session(user_id)
            session_id = session.session_id
        
        # Save user message
        user_message = Message(
            session_id=session_id,
            role=MessageRole.USER,
            content=message
        )
        await self.message_store.save_message(user_message)
        
        # Update session activity and message count
        await self.session_manager.update_session_activity(session_id)
        await self.session_manager.increment_message_count(session_id)
        
        # Get recent messages for context
        recent_messages = await self.message_store.get_recent_messages(session_id, count=10)
        
        # Build context
        context = await self.context_builder.build_context(
            user_id=user_id,
            session_id=session_id,
            recent_messages=recent_messages,
            include_research=False  # Can be made configurable
        )
        
        # Generate and stream response
        assistant_message_id = str(uuid.uuid4())
        full_response = ""
        
        async for event in self.llm_orchestrator.generate_response(context, message):
            yield event
            
            if event.event_type.value == "token":
                full_response += event.data
            elif event.event_type.value == "complete":
                full_response = event.data
                
                # Save assistant response
                assistant_message = Message(
                    message_id=assistant_message_id,
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=full_response
                )
                await self.message_store.save_message(assistant_message)
                await self.session_manager.increment_message_count(session_id)
    
    async def create_session(
        self, 
        user_id: str, 
        title: Optional[str] = None
    ) -> ChatSession:
        """Create a new chat session."""
        return await self.session_manager.create_session(user_id, title)
    
    async def get_session(
        self, 
        user_id: str, 
        session_id: str
    ) -> Optional[ChatSession]:
        """Get a chat session with validation."""
        session = await self.session_manager.get_session(session_id)
        if session and session.user_id == user_id:
            return session
        return None
    
    async def get_session_messages(
        self, 
        user_id: str, 
        session_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> list[Message]:
        """Get messages for a session with user validation."""
        session = await self.get_session(user_id, session_id)
        if not session:
            return []
        
        return await self.message_store.get_messages(session_id, limit, offset)
    
    async def list_sessions(
        self, 
        user_id: str, 
        limit: int = 50
    ) -> list[ChatSessionSummary]:
        """List all chat sessions for a user."""
        return await self.session_manager.list_user_sessions(user_id, limit)
    
    async def delete_session(
        self, 
        user_id: str, 
        session_id: str
    ) -> bool:
        """Delete a chat session and all messages."""
        # Verify ownership
        session = await self.get_session(user_id, session_id)
        if not session:
            return False
        
        # Delete messages and session
        await self.message_store.delete_session_messages(session_id)
        await self.session_manager.delete_session(session_id)
        
        return True
    
    async def update_session_title(
        self, 
        user_id: str, 
        session_id: str, 
        title: str
    ) -> bool:
        """Update session title."""
        session = await self.get_session(user_id, session_id)
        if not session:
            return False
        
        session.title = title
        await self.session_manager._save_session(session)
        return True
