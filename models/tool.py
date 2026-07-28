"""Project ZERO — Tool Framework Domain Schema."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid


class ToolParameter(BaseModel):
    """Schema for a tool parameter input."""

    type: str = Field(description="JSON schema data type (string, integer, boolean, object)")
    description: str = Field(description="Parameter description")
    required: bool = Field(default=True)


class ToolDefinition(BaseModel):
    """Metadata definition for registering a tool with LLMs."""

    name: str = Field(description="Tool identifier")
    description: str = Field(description="Tool intent description")
    parameters: Dict[str, ToolParameter] = Field(default_factory=dict)


class ToolCall(BaseModel):
    """Invocation request for executing a tool."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tool_name: str = Field(description="Target tool name")
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """Execution output from running a tool."""

    call_id: str = Field(description="Matching ToolCall ID")
    tool_name: str = Field(description="Target tool name")
    success: bool = Field(default=True)
    output: str = Field(default="")
    error: Optional[str] = Field(default=None)
