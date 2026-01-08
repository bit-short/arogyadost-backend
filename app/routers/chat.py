from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from typing import Optional, List
import json
import asyncio

from app.services.chat.chat_service import ChatService
from app.services.chat.models import (
    ChatRequest, ChatSession, ChatSessionSummary, Message, StreamEvent
)
from app.middleware.translation import get_translator, get_language

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize chat service
chat_service = ChatService()


@router.post("/sessions")
async def create_chat_session(user_id: str = "hardcoded", title: Optional[str] = None):
    """Create a new chat session."""
    try:
        session = await chat_service.create_session(user_id, title)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions")
async def list_chat_sessions(user_id: str = "hardcoded", limit: int = 50) -> List[ChatSessionSummary]:
    """List all chat sessions for a user."""
    try:
        return await chat_service.list_sessions(user_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}")
async def get_chat_session(session_id: str, user_id: str) -> ChatSession:
    """Get a specific chat session."""
    try:
        session = await chat_service.get_session(user_id, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: str, 
    user_id: str,
    limit: Optional[int] = None,
    offset: int = 0
) -> List[Message]:
    """Get messages for a chat session."""
    try:
        messages = await chat_service.get_session_messages(user_id, session_id, limit, offset)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: str, user_id: str):
    """Delete a chat session and all its messages."""
    try:
        success = await chat_service.delete_session(user_id, session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/sessions/{session_id}/title")
async def update_session_title(session_id: str, user_id: str, title: str):
    """Update session title."""
    try:
        success = await chat_service.update_session_title(user_id, session_id, title)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Title updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/messages")
async def send_message_streaming(
    session_id: str,
    user_id: str,
    request: ChatRequest,
    http_request: Request
):
    """Send a message and stream the response using Server-Sent Events."""
    
    # Get language from request
    language = get_language(http_request)
    t = get_translator(http_request)
    
    async def event_stream():
        try:
            # Send initial session info with language context
            session_info = {
                "session_id": session_id,
                "user_id": user_id,
                "language": language,
                "timestamp": "2024-01-08T03:35:00Z"
            }
            yield f"data: {json.dumps({'type': 'session_info', 'data': session_info})}\n\n"
            
            # Add language context to chat request
            request.language = language
            
            # Stream the chat response
            async for event in chat_service.send_message(user_id, session_id, request.message, language=language):
                event_data = {
                    "type": event.event_type.value,
                    "data": event.data,
                    "timestamp": event.timestamp.isoformat()
                }
                yield f"data: {json.dumps(event_data)}\n\n"
                
                # Small delay to ensure proper streaming
                await asyncio.sleep(0.01)
            
            # Send completion signal
            yield f"data: {json.dumps({'type': 'stream_end'})}\n\n"
            
        except Exception as e:
            error_message = t('chat.responses.error') if hasattr(t, '__call__') else f"Error processing message: {str(e)}"
            error_data = {
                "type": "error",
                "data": error_message,
                "timestamp": "2024-01-08T03:35:00Z"
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )


@router.post("/message")
async def send_message_simple(request: ChatRequest, user_id: str = "hardcoded"):
    """Send a message and get a simple JSON response (non-streaming)."""
    try:
        # Collect all streaming events
        full_response = ""
        session_id = request.session_id
        
        async for event in chat_service.send_message(user_id, session_id, request.message):
            if event.event_type.value == "complete":
                full_response = event.data
                if not session_id:
                    # Extract session_id from context if it was created
                    session_id = "new_session"  # This would be properly handled in production
        
        return {
            "session_id": session_id,
            "message": full_response,
            "timestamp": "2024-01-08T03:35:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
