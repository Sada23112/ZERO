"""Unit tests for Terminal execution tool."""

import pytest
import sys
from pathlib import Path
from tools.terminal import RunCommandTool


@pytest.mark.asyncio
async def test_run_command_tool_success(tmp_path: Path):
    tool = RunCommandTool(workspace_root=tmp_path)
    
    # Run python --version
    res = await tool.execute("call_term_1", {"command": f"{sys.executable} --version"})
    assert res.success is True
    assert "Python" in res.output or "Python" in (res.error or "")


@pytest.mark.asyncio
async def test_run_command_tool_timeout(tmp_path: Path):
    tool = RunCommandTool(workspace_root=tmp_path, default_timeout=1)
    
    # Run python script that sleeps for 3 seconds
    cmd = f'{sys.executable} -c "import time; time.sleep(3)"'
    res = await tool.execute("call_term_2", {"command": cmd, "timeout": 1})
    assert res.success is False
    assert "timed out" in res.error
