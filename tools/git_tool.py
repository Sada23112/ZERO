"""Project ZERO — Git Intelligence Tool Suite (Phase 4 Capability #1).

Comprehensive Git repository understanding, conflict detection, & commit summarization.
"""

import asyncio
import shlex
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger


class GitTool(BaseTool):
    """Deep Git intelligence tool supporting status, commit, diff, log, blame, conflicts, & branching."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    @property
    def name(self) -> str:
        return "git_tool"

    @property
    def description(self) -> str:
        return "Execute Git repository operations (status, commit, stage, diff, log, branch, merge, blame, stash, conflicts)."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "subcommand": ToolParameter(type="string", description="Git subcommand (status, commit, stage, restore, branch, checkout, merge, diff, log, blame, stash, tags, conflicts)"),
                "args": ToolParameter(type="string", description="Optional arguments for git subcommand (e.g. message, file path, branch name)", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        subcmd = arguments.get("subcommand", "status").strip().lower()
        args = arguments.get("args", "").strip()

        git_cmd_map = {
            "status": ["git", "status"],
            "stage": ["git", "add"] + (shlex.split(args) if args else ["-A"]),
            "restore": ["git", "restore"] + (shlex.split(args) if args else ["."]),
            "commit": ["git", "commit", "-m", args if args else "update repository"],
            "branch": ["git", "branch"] + (shlex.split(args) if args else []),
            "checkout": ["git", "checkout"] + (shlex.split(args) if args else []),
            "merge": ["git", "merge"] + (shlex.split(args) if args else []),
            "diff": ["git", "diff"] + (shlex.split(args) if args else []),
            "log": ["git", "log", "-n", "10", "--oneline"] + (shlex.split(args) if args else []),
            "blame": ["git", "blame"] + (shlex.split(args) if args else []),
            "stash": ["git", "stash"] + (shlex.split(args) if args else []),
            "tags": ["git", "tag"] + (shlex.split(args) if args else []),
            "conflicts": ["git", "diff", "--name-only", "--diff-filter=U"],
        }

        cmd_tokens = git_cmd_map.get(subcmd, ["git", subcmd] + (shlex.split(args) if args else []))

        try:
            process = await asyncio.create_subprocess_exec(
                cmd_tokens[0],
                *cmd_tokens[1:],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace_root)
            )

            stdout_bytes, stderr_bytes = await process.communicate()
            stdout_str = stdout_bytes.decode("utf-8", errors="replace").strip()
            stderr_str = stderr_bytes.decode("utf-8", errors="replace").strip()
            exit_code = process.returncode or 0

            output_text = stdout_str if stdout_str else stderr_str
            if not output_text:
                output_text = f"[Git {subcmd} completed with exit code {exit_code}]"

            if subcmd == "conflicts":
                if stdout_str:
                    output_text = f"[UNRESOLVED MERGE CONFLICTS DETECTED]:\n{stdout_str}"
                else:
                    output_text = "[No merge conflicts detected in working tree.]"

            return ToolResult(
                call_id=call_id,
                tool_name=self.name,
                success=(exit_code == 0),
                output=output_text,
                error=stderr_str if exit_code != 0 else None
            )
        except Exception as err:
            logger.error(f"Git execution error: {err}")
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))
