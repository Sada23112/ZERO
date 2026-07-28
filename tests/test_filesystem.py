"""Unit tests for Filesystem tools & security path containment."""

import pytest
from pathlib import Path
from tools.filesystem import ReadFileTool, WriteFileTool, ListDirectoryTool, SearchFilesTool, FileInfoTool


@pytest.fixture
def temp_workspace(tmp_path: Path):
    # Create sample files
    (tmp_path / "hello.txt").write_text("Hello Project ZERO", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "code.py").write_text("print('hello')", encoding="utf-8")
    return tmp_path


@pytest.mark.asyncio
async def test_read_file_tool(temp_workspace: Path):
    tool = ReadFileTool(workspace_root=temp_workspace)
    res = await tool.execute("call_1", {"path": str(temp_workspace / "hello.txt")})
    assert res.success is True
    assert "Hello Project ZERO" in res.output


@pytest.mark.asyncio
async def test_write_file_tool(temp_workspace: Path):
    tool = WriteFileTool(workspace_root=temp_workspace)
    target = temp_workspace / "output.txt"
    res = await tool.execute("call_2", {"path": str(target), "content": "Written file content"})
    assert res.success is True
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "Written file content"


@pytest.mark.asyncio
async def test_write_file_tool_security_path_containment(temp_workspace: Path):
    tool = WriteFileTool(workspace_root=temp_workspace)
    outside_path = temp_workspace.parent / "unauthorized.txt"
    res = await tool.execute("call_3", {"path": str(outside_path), "content": "Illegal write"})
    assert res.success is False
    assert "Access denied" in res.error


@pytest.mark.asyncio
async def test_list_directory_tool(temp_workspace: Path):
    tool = ListDirectoryTool(workspace_root=temp_workspace)
    res = await tool.execute("call_4", {"path": str(temp_workspace)})
    assert res.success is True
    assert "[FILE] hello.txt" in res.output
    assert "[DIR] sub" in res.output


@pytest.mark.asyncio
async def test_file_info_tool(temp_workspace: Path):
    tool = FileInfoTool(workspace_root=temp_workspace)
    res = await tool.execute("call_5", {"path": str(temp_workspace / "hello.txt")})
    assert res.success is True
    assert "hello.txt" in res.output
    assert "Lines: 1" in res.output
