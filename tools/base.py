"""Project ZERO — Base Tool Framework Interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from models.tool import ToolDefinition, ToolResult
from zero_logging import logger


class BaseTool(ABC):
    """Abstract interface for extensible Project ZERO tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool identifier name (e.g. 'system_info', 'file_read')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human and LLM readable description of tool functionality."""
        pass

    @abstractmethod
    def get_definition(self) -> ToolDefinition:
        """Return JSON-RPC / Pydantic schema parameter definition for tool."""
        pass

    @abstractmethod
    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        """Execute the tool with given argument dictionary."""
        pass
