"""Project ZERO — Capability Detector & Meta-Reasoning Engine (Phase 5)."""

from typing import Dict, Any, Optional, Tuple
from tools.registry import tool_registry
from evolution.registry import CapabilityRegistryStore


class CapabilityDetectionResult:
    """Outcome of meta-reasoning capability inspection."""

    def __init__(self, action_type: str, tool_name: Optional[str] = None, rationale: str = ""):
        self.action_type = action_type  # 'execute_existing', 'generate_new', 'repair', 'none'
        self.tool_name = tool_name
        self.rationale = rationale


class CapabilityDetector:
    """Inspects user requests and determines whether to execute existing tool or generate new capability."""

    def __init__(self, dynamic_registry: Optional[CapabilityRegistryStore] = None):
        self.dynamic_registry = dynamic_registry or CapabilityRegistryStore()

    def detect_capability(self, prompt: str) -> CapabilityDetectionResult:
        """Analyze user prompt and classify execution path."""
        p_lower = prompt.lower().strip()

        # 1. Check for Explicit Self-Repair commands
        if p_lower.startswith("repair ") or p_lower in ["repair yourself", "fix yourself"]:
            target = p_lower.replace("repair ", "").strip()
            return CapabilityDetectionResult(
                action_type="repair",
                tool_name=target,
                rationale=f"Self-repair request detected for '{target}'"
            )

        # 2. Check built-in registered tools
        for tool_obj in tool_registry.list_tools():
            t_name = tool_obj.name.lower()
            if t_name in p_lower or tool_obj.description.lower() in p_lower:
                return CapabilityDetectionResult(
                    action_type="execute_existing",
                    tool_name=tool_obj.name,
                    rationale=f"Existing tool '{tool_obj.name}' handles request."
                )

        # 3. Check dynamically generated registered tools
        for cap in self.dynamic_registry.list_capabilities():
            if cap.name.lower() in p_lower:
                return CapabilityDetectionResult(
                    action_type="execute_existing",
                    tool_name=cap.name,
                    rationale=f"Dynamically generated tool '{cap.name}' handles request."
                )

        # 4. Keyword Triggers for Missing Capability Generation
        generation_triggers = [
            ("make a pdf", "pdf_generator", "Generate PDF documents"),
            ("create a pdf", "pdf_generator", "Generate PDF documents"),
            ("generate qr code", "qr_generator", "Generate QR Code image files"),
            ("qr code", "qr_generator", "Generate QR Code image files"),
            ("make powerpoint", "powerpoint_generator", "Generate PowerPoint (.pptx) presentations"),
            ("create powerpoint", "powerpoint_generator", "Generate PowerPoint (.pptx) presentations"),
            ("read epub", "epub_reader", "Read and parse EPUB e-books"),
            ("open explorer", "explorer_tool", "Launch Windows File Explorer"),
            ("open file explorer", "explorer_tool", "Launch Windows File Explorer"),
            ("create excel exporter", "excel_exporter", "Export data to Excel .xlsx spreadsheets")
        ]

        for trigger_phrase, cap_name, desc in generation_triggers:
            if trigger_phrase in p_lower:
                return CapabilityDetectionResult(
                    action_type="generate_new",
                    tool_name=cap_name,
                    rationale=desc
                )

        # Default: No dynamic generation needed (pass through standard Brain reasoning)
        return CapabilityDetectionResult(
            action_type="none",
            rationale="Prompt handled by standard Brain reasoning flow."
        )
