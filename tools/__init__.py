"""Project ZERO — Tool Registry Package."""

from tools.base import BaseTool
from tools.registry import ToolRegistry, tool_registry
from tools.system import SystemInfoTool, PingTool
from tools.filesystem import ReadFileTool, WriteFileTool, ListDirectoryTool, SearchFilesTool, FileInfoTool
from tools.terminal import RunCommandTool
from tools.browser import OpenUrlTool, ReadPageTextTool, SearchWebTool, ExtractTitleTool, ExtractLinksTool

# Automatically register default core tools
tool_registry.register_tool(SystemInfoTool())
tool_registry.register_tool(PingTool())

# Register filesystem tools
tool_registry.register_tool(ReadFileTool())
tool_registry.register_tool(WriteFileTool())
tool_registry.register_tool(ListDirectoryTool())
tool_registry.register_tool(SearchFilesTool())
tool_registry.register_tool(FileInfoTool())

# Register terminal tools
tool_registry.register_tool(RunCommandTool())

# Register browser tools
tool_registry.register_tool(OpenUrlTool())
tool_registry.register_tool(ReadPageTextTool())
tool_registry.register_tool(SearchWebTool())
tool_registry.register_tool(ExtractTitleTool())
tool_registry.register_tool(ExtractLinksTool())

__all__ = [
    "BaseTool",
    "ToolRegistry",
    "tool_registry",
    "SystemInfoTool",
    "PingTool",
    "ReadFileTool",
    "WriteFileTool",
    "ListDirectoryTool",
    "SearchFilesTool",
    "FileInfoTool",
    "RunCommandTool",
    "OpenUrlTool",
    "ReadPageTextTool",
    "SearchWebTool",
    "ExtractTitleTool",
    "ExtractLinksTool",
]
