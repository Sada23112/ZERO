"""Project ZERO — Archive Tool Suite (Phase 4 Capability #9)."""

import zipfile
import tarfile
from pathlib import Path
from typing import Dict, Any, Optional
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger


class ArchiveTool(BaseTool):
    """Tool to create or extract zip, tar, gzip archives."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    @property
    def name(self) -> str:
        return "archive"

    @property
    def description(self) -> str:
        return "Create or extract Zip and Tar archives."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "action": ToolParameter(type="string", description="Action: 'zip', 'unzip', 'tar', 'untar'"),
                "archive_path": ToolParameter(type="string", description="Archive file path"),
                "target_path": ToolParameter(type="string", description="File or directory path to compress/extract to", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        action = arguments.get("action", "unzip").strip().lower()
        archive_str = arguments.get("archive_path")
        target_str = arguments.get("target_path", ".")

        if not archive_str:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'archive_path' is required.")

        archive_p = Path(archive_str).resolve()
        target_p = Path(target_str).resolve()

        try:
            if action == "unzip":
                if not archive_p.exists():
                    return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Archive not found: {archive_p}")
                with zipfile.ZipFile(archive_p, "r") as zf:
                    zf.extractall(target_p)
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Extracted zip archive to {target_p}")

            elif action == "zip":
                with zipfile.ZipFile(archive_p, "w", zipfile.ZIP_DEFLATED) as zf:
                    if target_p.is_file():
                        zf.write(target_p, target_p.name)
                    elif target_p.is_dir():
                        for root, _, files in os.walk(target_p):
                            for file in files:
                                full_file = Path(root, file)
                                zf.write(full_file, full_file.relative_to(target_p))
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Created zip archive: {archive_p}")

            elif action == "untar":
                if not archive_p.exists():
                    return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Archive not found: {archive_p}")
                with tarfile.open(archive_p, "r:*") as tf:
                    tf.extractall(target_p)
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Extracted tar archive to {target_p}")

            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Unknown archive action '{action}'")

        except Exception as err:
            logger.error(f"Archive operation error: {err}")
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))
