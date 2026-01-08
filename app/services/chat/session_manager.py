from typing import List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

from .models import ChatSession, ChatSessionSummary


class SessionManager:
    """Manages chat session lifecycle and metadata."""
    
    def __init__(self, data_dir: str = "data/chat"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_file = self.data_dir / "sessions.json"
    
    async def create_session(
        self, 
        user_id: str, 
        title: Optional[str] = None
    ) -> ChatSession:
        """Create a new chat session."""
        session = ChatSession(
            user_id=user_id,
            title=title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        # Save session metadata
        await self._save_session(session)
        return session
    
    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieve session by ID."""
        sessions = await self._load_sessions()
        
        for session_data in sessions:
            if session_data.get('session_id') == session_id:
                session_data['created_at'] = datetime.fromisoformat(session_data['created_at'])
                session_data['last_activity'] = datetime.fromisoformat(session_data['last_activity'])
                return ChatSession(**session_data)
        
        return None
    
    async def update_session_activity(self, session_id: str) -> None:
        """Update last_activity timestamp for a session."""
        sessions = await self._load_sessions()
        
        for session_data in sessions:
            if session_data.get('session_id') == session_id:
                session_data['last_activity'] = datetime.now().isoformat()
                break
        
        await self._save_sessions(sessions)
    
    async def list_user_sessions(
        self, 
        user_id: str, 
        limit: int = 50
    ) -> List[ChatSessionSummary]:
        """List all sessions for a user."""
        sessions = await self._load_sessions()
        
        # Filter by user and convert to summaries
        user_sessions = []
        for session_data in sessions:
            if session_data.get('user_id') == user_id and not session_data.get('is_archived', False):
                # Get last message preview
                last_message_preview = await self._get_last_message_preview(session_data['session_id'])
                
                summary = ChatSessionSummary(
                    session_id=session_data['session_id'],
                    title=session_data.get('title'),
                    last_message_preview=last_message_preview,
                    last_activity=datetime.fromisoformat(session_data['last_activity']),
                    message_count=session_data.get('message_count', 0)
                )
                user_sessions.append(summary)
        
        # Sort by last activity (most recent first)
        user_sessions.sort(key=lambda x: x.last_activity, reverse=True)
        
        return user_sessions[:limit]
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session and mark for cleanup."""
        sessions = await self._load_sessions()
        
        # Remove session from list
        sessions = [s for s in sessions if s.get('session_id') != session_id]
        await self._save_sessions(sessions)
        
        return True
    
    async def archive_inactive_sessions(self, days_inactive: int = 30) -> int:
        """Archive sessions inactive for specified days."""
        sessions = await self._load_sessions()
        cutoff_date = datetime.now() - timedelta(days=days_inactive)
        archived_count = 0
        
        for session_data in sessions:
            last_activity = datetime.fromisoformat(session_data['last_activity'])
            if last_activity < cutoff_date and not session_data.get('is_archived', False):
                session_data['is_archived'] = True
                archived_count += 1
        
        await self._save_sessions(sessions)
        return archived_count
    
    async def increment_message_count(self, session_id: str) -> None:
        """Increment message count for a session."""
        sessions = await self._load_sessions()
        
        for session_data in sessions:
            if session_data.get('session_id') == session_id:
                session_data['message_count'] = session_data.get('message_count', 0) + 1
                break
        
        await self._save_sessions(sessions)
    
    async def _save_session(self, session: ChatSession) -> None:
        """Save a single session to storage."""
        sessions = await self._load_sessions()
        
        # Convert session to dict
        session_dict = session.dict()
        session_dict['created_at'] = session.created_at.isoformat()
        session_dict['last_activity'] = session.last_activity.isoformat()
        
        # Add or update session
        existing_index = None
        for i, s in enumerate(sessions):
            if s.get('session_id') == session.session_id:
                existing_index = i
                break
        
        if existing_index is not None:
            sessions[existing_index] = session_dict
        else:
            sessions.append(session_dict)
        
        await self._save_sessions(sessions)
    
    async def _load_sessions(self) -> List[dict]:
        """Load all sessions from storage."""
        try:
            if self.sessions_file.exists():
                with open(self.sessions_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading sessions: {e}")
            return []
    
    async def _save_sessions(self, sessions: List[dict]) -> None:
        """Save sessions to storage."""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    async def _get_last_message_preview(self, session_id: str) -> str:
        """Get preview of last message in session."""
        try:
            session_file = self.data_dir / f"session_{session_id}.json"
            if session_file.exists():
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    messages = data.get('messages', [])
                    if messages:
                        last_message = messages[-1]
                        content = last_message.get('content', '')
                        # Return first 100 characters
                        return content[:100] + "..." if len(content) > 100 else content
            return "No messages yet"
        except Exception:
            return "No messages yet"
