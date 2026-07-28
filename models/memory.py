"""Project ZERO — Cognitive Memory Domain Schema."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid


class MemoryCategory(str, Enum):
    USER_PREFERENCE = "user_preference"
    PROJECT_FACT = "project_fact"
    SYSTEM_INSTRUCTION = "system_instruction"
    GENERAL = "general"


class MemoryRecord(BaseModel):
    """Memory entry stored in persistent key-value & vector index."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    key: str = Field(description="Unique key or search topic")
    value: str = Field(description="Memory content string")
    category: MemoryCategory = Field(default=MemoryCategory.GENERAL)
    tags: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)
