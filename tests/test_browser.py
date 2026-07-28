"""Unit tests for Playwright & fallback Browser tools."""

import pytest
from tools.browser import OpenUrlTool, SearchWebTool, ExtractTitleTool


@pytest.mark.asyncio
async def test_open_url_tool_http_fallback():
    tool = OpenUrlTool()
    res = await tool.execute("call_b1", {"url": "https://httpbin.org/get"})
    assert res.success is True
    assert "httpbin.org" in res.output or "200 OK" in res.output


@pytest.mark.asyncio
async def test_search_web_tool():
    tool = SearchWebTool()
    res = await tool.execute("call_b2", {"query": "python"})
    assert res.success is True
    assert "Content" in res.output or "200 OK" in res.output
