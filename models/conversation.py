"""Project ZERO — Conversation & Message Domain Schema."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """Message object representing a turn in a conversation session."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = Field(description="Parent session ID")
    role: MessageRole = Field(description="Sender role")
    content: str = Field(description="Textual message payload")
    model: Optional[str] = Field(default=None, description="Model used for generation")
    tokens: Optional[int] = Field(default=None, description="Token consumption count")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Session(BaseModel):
    """Conversation Session container."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(default="New Session")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
