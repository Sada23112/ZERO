"""Project ZERO — Clipboard Management Subsystem (Phase 4 Capability #7)."""

from typing import Dict, Any, Optional, List
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


class ClipboardTool(BaseTool):
    """Tool to inspect, copy, paste, and search system clipboard history."""

    _history: List[str] = []

    @property
    def name(self) -> str:
        return "clipboard"

    @property
    def description(self) -> str:
        return "Manage system clipboard (copy, paste, history, search)."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "action": ToolParameter(type="string", description="Clipboard action: 'copy', 'paste', 'history', 'search'"),
                "text": ToolParameter(type="string", description="Text to copy or search query", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        action = arguments.get("action", "paste").strip().lower()
        text_arg = arguments.get("text", "")

        if not PYPERCLIP_AVAILABLE:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="pyperclip library is not installed.")

        try:
            if action == "copy":
                if not text_arg:
                    return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'text' is required for copy action.")
                pyperclip.copy(text_arg)
                ClipboardTool._history.append(text_arg)
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Copied {len(text_arg)} characters to clipboard.")

            elif action == "paste":
                content = pyperclip.paste()
                if content and (not ClipboardTool._history or ClipboardTool._history[-1] != content):
                    ClipboardTool._history.append(content)
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=content if content else "[Clipboard is empty]")

            elif action == "history":
                if not ClipboardTool._history:
                    return ToolResult(call_id=call_id, tool_name=self.name, success=True, output="[No clipboard history recorded yet]")
                entries = [f"{i+1}. {item[:100]}" for i, item in enumerate(ClipboardTool._history[-10:])]
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output="Clipboard History:\n" + "\n".join(entries))

            elif action == "search":
                matches = [item for item in ClipboardTool._history if text_arg.lower() in item.lower()]
                if not matches:
                    return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"No clipboard history matching '{text_arg}'.")
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Clipboard Search Results:\n" + "\n".join(matches[:5]))

            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Unknown clipboard action '{action}'.")

        except Exception as err:
            logger.error(f"Clipboard operation failed: {err}")
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))
