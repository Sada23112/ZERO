"""Unit tests for tool framework and system tools."""

import pytest
from tools.system import SystemInfoTool, PingTool
from tools.registry import ToolRegistry


@pytest.mark.asyncio
async def test_ping_tool():
    tool = PingTool()
    def_data = tool.get_definition()
    assert def_data.name == "ping"

    result = await tool.execute("call_1", {"message": "hello"})
    assert result.success is True
    assert "hello" in result.output


@pytest.mark.asyncio
async def test_tool_registry():
    registry = ToolRegistry()
    ping_tool = PingTool()
    registry.register_tool(ping_tool)

    fetched = registry.get_tool("ping")
    assert fetched is not None

    res = await registry.execute_tool("call_2", "ping", {"message": "test_ping"})
    assert res.success is True
    assert "test_ping" in res.output
