from typing import List, Optional
from datetime import datetime, timedelta
import json
import asyncio
from pathlib import Path

from .models import Message, ChatSession, MessageRole


class MessageStore:
    """Handles persistence of chat messages and sessions."""
    
    def __init__(self, data_dir: str = "data/chat"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_message(self, message: Message) -> bool:
        """Save a message to storage."""
        try:
            session_file = self.data_dir / f"session_{message.session_id}.json"
            
            # Load existing messages
            messages = []
            if session_file.exists():
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    messages = data.get('messages', [])
            
            # Add new message
            message_dict = message.dict()
            message_dict['timestamp'] = message.timestamp.isoformat()
            messages.append(message_dict)
            
            # Save back to file
            session_data = {
                'session_id': message.session_id,
                'messages': messages,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving message: {e}")
            return False
    
    async def get_messages(
        self, 
        session_id: str, 
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Message]:
        """Retrieve messages for a session."""
        try:
            session_file = self.data_dir / f"session_{session_id}.json"
            
            if not session_file.exists():
                return []
            
            with open(session_file, 'r') as f:
                data = json.load(f)
                messages_data = data.get('messages', [])
            
            # Convert to Message objects
            messages = []
            for msg_data in messages_data:
                msg_data['timestamp'] = datetime.fromisoformat(msg_data['timestamp'])
                messages.append(Message(**msg_data))
            
            # Sort by timestamp
            messages.sort(key=lambda x: x.timestamp)
            
            # Apply pagination
            if offset:
                messages = messages[offset:]
            if limit:
                messages = messages[:limit]
            
            return messages
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []
    
    async def delete_session_messages(self, session_id: str) -> bool:
        """Delete all messages for a session."""
        try:
            session_file = self.data_dir / f"session_{session_id}.json"
            if session_file.exists():
                session_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting session messages: {e}")
            return False
    
    async def update_message(self, message_id: str, content: str) -> bool:
        """Update message content (for partial responses)."""
        try:
            # Find the session containing this message
            for session_file in self.data_dir.glob("session_*.json"):
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    messages = data.get('messages', [])
                
                # Find and update the message
                for msg in messages:
                    if msg.get('message_id') == message_id:
                        msg['content'] = content
                        msg['timestamp'] = datetime.now().isoformat()
                        
                        # Save back to file
                        data['last_updated'] = datetime.now().isoformat()
                        with open(session_file, 'w') as f:
                            json.dump(data, f, indent=2)
                        return True
            
            return False
        except Exception as e:
            print(f"Error updating message: {e}")
            return False
    
    async def get_recent_messages(self, session_id: str, count: int = 10) -> List[Message]:
        """Get the most recent messages from a session."""
        messages = await self.get_messages(session_id)
        return messages[-count:] if messages else []
