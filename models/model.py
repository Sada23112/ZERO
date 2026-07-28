"""Project ZERO — Provider Model Domain Schema."""

from typing import List, Optional
from pydantic import BaseModel, Field


class DiscoveredModel(BaseModel):
    """Metadata for a model dynamically discovered from an LLM provider API."""

    id: str = Field(description="Unique model identifier (e.g. 'gemini-2.0-flash')")
    display_name: str = Field(description="Human-readable name")
    version: str = Field(default="latest", description="Model version")
    description: Optional[str] = Field(default=None, description="Model description")
    input_token_limit: Optional[int] = Field(default=None, description="Max input context tokens")
    output_token_limit: Optional[int] = Field(default=None, description="Max response output tokens")
    supported_methods: List[str] = Field(default_factory=list, description="Supported API capabilities")
