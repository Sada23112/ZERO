"""Project ZERO — Initial Core System Tools."""

import platform
import sys
from typing import Dict, Any
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter


class SystemInfoTool(BaseTool):
    """Tool returning host environment diagnostic information."""

    @property
    def name(self) -> str:
        return "system_info"

    @property
    def description(self) -> str:
        return "Retrieve OS platform, Python version, and system runtime information."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={}
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        info_str = (
            f"OS: {platform.system()} {platform.release()} ({platform.machine()})\n"
            f"Python: {sys.version.split()[0]}\n"
            f"Platform Node: {platform.node()}"
        )
        return ToolResult(
            call_id=call_id,
            tool_name=self.name,
            success=True,
            output=info_str
        )


class PingTool(BaseTool):
    """Tool for connectivity diagnostic tests."""

    @property
    def name(self) -> str:
        return "ping"

    @property
    def description(self) -> str:
        return "Simple tool echo ping diagnostic."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "message": ToolParameter(type="string", description="Echo message string", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        msg = arguments.get("message", "pong")
        return ToolResult(
            call_id=call_id,
            tool_name=self.name,
            success=True,
            output=f"Echo: {msg}"
        )
