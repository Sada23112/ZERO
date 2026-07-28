"""Project ZERO — Terminal Execution Tool.

Safely executes shell commands using asyncio subprocess exec without shell=True.
Captures stdout, stderr, exit code, and runtime duration with configurable timeout.
"""

import os
import asyncio
import shlex
from pathlib import Path
from typing import Dict, Any, Optional
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger


class RunCommandTool(BaseTool):
    """Tool to execute terminal shell commands asynchronously without shell=True."""

    def __init__(self, workspace_root: Optional[Path] = None, default_timeout: int = 30):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.default_timeout = default_timeout

    @property
    def name(self) -> str:
        return "run_command"

    @property
    def description(self) -> str:
        return "Execute a terminal CLI command (e.g. 'pytest', 'git status') safely and capture output."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "command": ToolParameter(type="string", description="Command string to execute (e.g. 'pytest')"),
                "cwd": ToolParameter(type="string", description="Working directory path", required=False),
                "timeout": ToolParameter(type="integer", description="Execution timeout in seconds", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        cmd_str = arguments.get("command")
        if not cmd_str or not cmd_str.strip():
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'command' is required.")

        cwd_str = arguments.get("cwd")
        timeout_val = arguments.get("timeout", self.default_timeout)

        # Resolve working directory safely
        target_cwd = self.workspace_root
        if cwd_str:
            target_cwd = Path(cwd_str).resolve()
            if not target_cwd.exists():
                return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Working directory does not exist: {cwd_str}")

        # Parse command args safely using shlex (posix=False on Windows to preserve backslashes)
        try:
            is_posix = (os.name != "nt")
            cmd_tokens = shlex.split(cmd_str, posix=is_posix)
            # Remove any double quotes added by non-posix split
            cmd_tokens = [t.strip('"\'') for t in cmd_tokens]
        except Exception as parse_err:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Failed to parse command: {parse_err}")

        if not cmd_tokens:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Parsed command string is empty.")

        try:
            process = await asyncio.create_subprocess_exec(
                cmd_tokens[0],
                *cmd_tokens[1:],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(target_cwd)
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(),
                    timeout=float(timeout_val)
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return ToolResult(
                    call_id=call_id,
                    tool_name=self.name,
                    success=False,
                    error=f"Command execution timed out after {timeout_val} seconds."
                )

            stdout_str = stdout_bytes.decode("utf-8", errors="replace").strip()
            stderr_str = stderr_bytes.decode("utf-8", errors="replace").strip()
            exit_code = process.returncode or 0

            output_combined = []
            if stdout_str:
                output_combined.append(stdout_str)
            if stderr_str:
                output_combined.append(f"[stderr]\n{stderr_str}")

            result_output = "\n".join(output_combined) if output_combined else "[Process finished with no output]"

            return ToolResult(
                call_id=call_id,
                tool_name=self.name,
                success=(exit_code == 0),
                output=result_output,
                error=stderr_str if exit_code != 0 else None
            )

        except Exception as err:
            logger.error(f"Error executing subprocess command '{cmd_str}': {err}")
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))
