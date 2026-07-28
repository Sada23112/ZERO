"""Project ZERO — Tool Registry Subsystem."""

from typing import Dict, Optional, List
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult
from zero_logging import logger


class ToolRegistry:
    """Registry managing tool registrations and execution routing."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool instance."""
        self._tools[tool.name.lower()] = tool
        logger.debug(f"Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Look up tool by name."""
        return self._tools.get(name.lower())

    def list_tools(self) -> List[ToolDefinition]:
        """List metadata definitions for all registered tools."""
        return [tool.get_definition() for tool in self._tools.values()]

    async def execute_tool(self, call_id: str, tool_name: str, arguments: Dict) -> ToolResult:
        """Execute a registered tool by name with arguments."""
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(
                call_id=call_id,
                tool_name=tool_name,
                success=False,
                error=f"Tool '{tool_name}' is not registered."
            )
        try:
            return await tool.execute(call_id, arguments)
        except Exception as err:
            logger.error(f"Error executing tool '{tool_name}': {err}")
            return ToolResult(
                call_id=call_id,
                tool_name=tool_name,
                success=False,
                error=f"Execution error: {str(err)}"
            )


# Global singleton Tool Registry instance
tool_registry = ToolRegistry()
