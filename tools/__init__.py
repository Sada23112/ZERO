"""Project ZERO — Tool Registry Package."""

from tools.base import BaseTool
from tools.registry import ToolRegistry, tool_registry
from tools.system import SystemInfoTool, PingTool

# Automatically register default core tools
tool_registry.register_tool(SystemInfoTool())
tool_registry.register_tool(PingTool())

__all__ = [
    "BaseTool",
    "ToolRegistry",
    "tool_registry",
    "SystemInfoTool",
    "PingTool",
]
