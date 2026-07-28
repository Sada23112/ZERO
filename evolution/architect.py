"""Project ZERO — Architectural Specification Generator (Phase 5)."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CapabilityArchitecturalSpec(BaseModel):
    """Architectural blueprint specification for a new capability."""

    capability_name: str
    class_name: str
    module_filename: str
    description: str
    required_dependencies: List[str] = Field(default_factory=list)
    parameters: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class ArchitecturalGenerator:
    """Designs architecture specifications for missing capabilities."""

    def design_capability(self, capability_name: str, description: str) -> CapabilityArchitecturalSpec:
        """Create architectural blueprint specification."""
        clean_name = capability_name.lower().replace(" ", "_").replace("-", "_")

        # Format ClassName
        words = clean_name.split("_")
        class_name = "".join(w.title() for w in words) + "Tool"

        deps = []
        if "pdf" in clean_name:
            deps = ["pypdf"]
        elif "qr" in clean_name:
            deps = ["qrcode"]
        elif "powerpoint" in clean_name or "pptx" in clean_name:
            deps = ["python-pptx"]
        elif "epub" in clean_name:
            deps = ["ebooklib"]
        elif "excel" in clean_name:
            deps = ["openpyxl"]

        params = {
            "input_text": {"type": "string", "description": "Input text or target path", "required": False},
            "output_path": {"type": "string", "description": "Output file path", "required": False}
        }

        return CapabilityArchitecturalSpec(
            capability_name=clean_name,
            class_name=class_name,
            module_filename=f"{clean_name}.py",
            description=description,
            required_dependencies=deps,
            parameters=params
        )
