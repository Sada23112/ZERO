"""Project ZERO — Evolution Engine Metadata & Models (Phase 5)."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CapabilityMetadata(BaseModel):
    """Metadata schema representing a dynamically generated or installed capability."""

    name: str
    version: str = "1.0.0"
    description: str
    author: str = "ZERO Evolution Engine"
    reason_created: str
    dependencies: List[str] = Field(default_factory=list)
    files_created: List[str] = Field(default_factory=list)
    created_at: str = ""
    success_count: int = 0
    failure_count: int = 0
    is_active: bool = True
    backup_path: Optional[str] = None


class EvolutionStepLog(BaseModel):
    """Step execution log inside the Evolution Pipeline."""

    step_name: str
    success: bool
    details: str = ""
    timestamp: str = ""
