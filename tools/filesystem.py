"""Project ZERO — Filesystem Tools.

Provides safe file reading, writing, listing, searching, and info inspection.
Path safety checks prevent accidental writes outside designated workspace bounds.
"""

from pathlib import Path
import os
import glob
from typing import Dict, Any, List, Optional
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger


class BaseFilesystemTool(BaseTool):
    """Base class for filesystem tools with security path containment checks."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def _resolve_safe_path(self, target_path_str: str, allow_outside_read: bool = True) -> Path:
        """Resolve target path and verify workspace containment for write operations."""
        resolved = Path(target_path_str).resolve()

        # For write operations or strict isolation, verify path is inside workspace_root
        if not allow_outside_read and not str(resolved).startswith(str(self.workspace_root)):
            raise PermissionError(f"Access denied: Path '{resolved}' is outside workspace '{self.workspace_root}'.")

        return resolved


class ReadFileTool(BaseFilesystemTool):
    """Tool to read text content from a local file."""

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read textual contents of a file given its relative or absolute path."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "path": ToolParameter(type="string", description="Relative or absolute file path to read")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        path_str = arguments.get("path")
        if not path_str:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'path' is required.")

        try:
            target_path = self._resolve_safe_path(path_str, allow_outside_read=True)
            if not target_path.exists():
                return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"File not found: {path_str}")

            if not target_path.is_file():
                return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Path is not a file: {path_str}")

            content = target_path.read_text(encoding="utf-8", errors="replace")
            return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=content)
        except Exception as err:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))


class WriteFileTool(BaseFilesystemTool):
    """Tool to create or overwrite a file within workspace bounds."""

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Write text content to a file inside the workspace directory."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "path": ToolParameter(type="string", description="File path to write"),
                "content": ToolParameter(type="string", description="Text content to write")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        path_str = arguments.get("path")
        content = arguments.get("content", "")
        if not path_str:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'path' is required.")

        try:
            target_path = self._resolve_safe_path(path_str, allow_outside_read=False)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding="utf-8")
            return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Successfully wrote {len(content)} bytes to {path_str}")
        except Exception as err:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))


class ListDirectoryTool(BaseFilesystemTool):
    """Tool to list directory contents."""

    @property
    def name(self) -> str:
        return "list_directory"

    @property
    def description(self) -> str:
        return "List files and subdirectories within a directory path."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "path": ToolParameter(type="string", description="Directory path to list (defaults to '.')", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        path_str = arguments.get("path", ".")
        try:
            target_path = self._resolve_safe_path(path_str, allow_outside_read=True)
            if not target_path.exists() or not target_path.is_dir():
                return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Directory not found: {path_str}")

            items = []
            for entry in target_path.iterdir():
                kind = "DIR" if entry.is_dir() else "FILE"
                size = f"{entry.stat().st_size} bytes" if entry.is_file() else ""
                items.append(f"[{kind}] {entry.name} {size}".strip())

            output_str = "\n".join(sorted(items)) if items else "[Empty Directory]"
            return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=output_str)
        except Exception as err:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))


class SearchFilesTool(BaseFilesystemTool):
    """Tool to search files by glob pattern or keyword."""

    @property
    def name(self) -> str:
        return "search_files"

    @property
    def description(self) -> str:
        return "Search for files matching glob pattern or text content in directory."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "pattern": ToolParameter(type="string", description="Glob pattern (e.g. '*.py' or '**/*.md')"),
                "path": ToolParameter(type="string", description="Base directory to search (defaults to '.')", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        pattern = arguments.get("pattern", "*")
        path_str = arguments.get("path", ".")
        try:
            target_path = self._resolve_safe_path(path_str, allow_outside_read=True)
            search_glob = str(target_path / pattern)
            matches = glob.glob(search_glob, recursive=True)

            rel_matches = [os.path.relpath(m, str(self.workspace_root)) for m in matches[:50]]
            out_text = "\n".join(rel_matches) if rel_matches else "[No files found matching pattern]"
            return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=out_text)
        except Exception as err:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))


class FileInfoTool(BaseFilesystemTool):
    """Tool to inspect file metadata."""

    @property
    def name(self) -> str:
        return "file_info"

    @property
    def description(self) -> str:
        return "Retrieve size, line count, and metadata for a file."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "path": ToolParameter(type="string", description="File path to inspect")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        path_str = arguments.get("path")
        if not path_str:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'path' is required.")

        try:
            target_path = self._resolve_safe_path(path_str, allow_outside_read=True)
            if not target_path.exists():
                return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Path not found: {path_str}")

            stat = target_path.stat()
            line_count = 0
            if target_path.is_file():
                try:
                    line_count = len(target_path.read_text(encoding="utf-8", errors="replace").splitlines())
                except Exception:
                    line_count = 0

            info = (
                f"Path: {target_path.name}\n"
                f"Type: {'Directory' if target_path.is_dir() else 'File'}\n"
                f"Size: {stat.st_size} bytes\n"
                f"Lines: {line_count}\n"
                f"Modified: {stat.st_mtime}"
            )
            return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=info)
        except Exception as err:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))
