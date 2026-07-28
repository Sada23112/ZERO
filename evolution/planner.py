"""Project ZERO — Evolution Planner (Phase 5)."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from evolution.architect import CapabilityArchitecturalSpec


class EvolutionPlan(BaseModel):
    """Execution plan detailing steps required to build a missing capability."""

    capability_name: str
    description: str
    steps: List[str] = Field(default_factory=list)


class EvolutionPlanner:
    """Generates multi-step evolution plans for missing capabilities."""

    def create_plan(self, spec: CapabilityArchitecturalSpec) -> EvolutionPlan:
        """Build structured execution plan."""
        return EvolutionPlan(
            capability_name=spec.capability_name,
            description=spec.description,
            steps=[
                "1. Resolve and verify external dependencies",
                "2. Generate production Python code inheriting BaseTool",
                "3. Synthesize automated Pytest test suite",
                "4. Execute sandbox isolated validation & static security scan",
                "5. Install capability into tools/dynamic/ package",
                "6. Register capability in ToolRegistry & persistent store",
                "7. Execute capability immediately to fulfill user request"
            ]
        )
