from datetime import datetime
from typing import Optional, List, Dict, Any, AsyncIterator
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class StreamEventType(str, Enum):
    TOKEN = "token"
    COMPLETE = "complete"
    ERROR = "error"
    THINKING = "thinking"


class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    message_count: int = 0
    is_archived: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatSessionSummary(BaseModel):
    session_id: str
    title: Optional[str]
    last_message_preview: str
    last_activity: datetime
    message_count: int


class ChatContext(BaseModel):
    user_id: str
    session_id: str
    recent_messages: List[Message]
    digital_twin_summary: Dict[str, Any]
    relevant_documents: List[Dict[str, Any]] = Field(default_factory=list)
    research_context: Optional[str] = None


class StreamEvent(BaseModel):
    event_type: StreamEventType
    data: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ResearchResult(BaseModel):
    query: str
    sources: List[str]
    summary: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    include_research: bool = False


class ChatResponse(BaseModel):
    session_id: str
    message_id: str
    content: str
    timestamp: datetime
    research_performed: bool = False
    research_results: Optional[ResearchResult] = None
