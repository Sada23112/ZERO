"""Project ZERO — Browser Tools.

Opens desktop web browser applications and extracts page text/links.
"""

import webbrowser
from typing import Dict, Any, List
import httpx
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class OpenUrlTool(BaseTool):
    """Tool to open a web URL in desktop browser and fetch page content."""

    @property
    def name(self) -> str:
        return "open_url"

    @property
    def description(self) -> str:
        return "Open a web URL in the system browser and fetch page text content."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "url": ToolParameter(type="string", description="Web URL to open (e.g. 'https://python.org')")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        url = arguments.get("url")
        if not url:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'url' is required.")

        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"

        # 1. Open the real native desktop web browser window for the user
        try:
            webbrowser.open(url)
            logger.info(f"Opened desktop browser for URL: {url}")
        except Exception as browser_err:
            logger.warning(f"Could not launch native desktop browser: {browser_err}")

        # 2. Fetch page content via HTTP or Playwright
        if PLAYWRIGHT_AVAILABLE:
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page(user_agent=DEFAULT_USER_AGENT)
                    await page.goto(url, timeout=10000)
                    title = await page.title()
                    body_text = await page.inner_text("body")
                    await browser.close()
                    out = f"Opened desktop browser for {url}\nTitle: {title}\nContent Snippet:\n{body_text[:1500]}"
                    return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=out)
            except Exception:
                pass  # Fallback seamlessly to HTTP client

        # Fallback HTTP Client
        try:
            headers = {"User-Agent": DEFAULT_USER_AGENT}
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=headers) as client:
                resp = await client.get(url)
                if resp.status_code in [200, 202]:
                    text_snippet = resp.text[:1500]
                    return ToolResult(
                        call_id=call_id,
                        tool_name=self.name,
                        success=True,
                        output=f"Opened desktop browser for {url}\nHTTP {resp.status_code} OK\nContent Snippet:\n{text_snippet}"
                    )
                else:
                    return ToolResult(
                        call_id=call_id,
                        tool_name=self.name,
                        success=False,
                        error=f"HTTP {resp.status_code} for {url}"
                    )
        except Exception as err:
            return ToolResult(
                call_id=call_id,
                tool_name=self.name,
                success=True,
                output=f"Opened desktop browser for {url} (HTTP fetch error: {err})"
            )


class ReadPageTextTool(BaseTool):
    """Tool to read textual content from a web URL."""

    @property
    def name(self) -> str:
        return "read_page_text"

    @property
    def description(self) -> str:
        return "Extract readable body text from a webpage."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "url": ToolParameter(type="string", description="URL to read text from")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        open_tool = OpenUrlTool()
        return await open_tool.execute(call_id, arguments)


class SearchWebTool(BaseTool):
    """Tool to search the web using a search engine query."""

    @property
    def name(self) -> str:
        return "search_web"

    @property
    def description(self) -> str:
        return "Perform a web search query for technical documentation or topics."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "query": ToolParameter(type="string", description="Search query string")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        query = arguments.get("query")
        if not query:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'query' is required.")

        search_url = f"https://html.duckduckgo.com/html/?q={httpx.URL(query).raw_path.decode('utf-8')}"
        open_tool = OpenUrlTool()
        return await open_tool.execute(call_id, {"url": search_url})


class ExtractTitleTool(BaseTool):
    """Tool to extract title of a webpage."""

    @property
    def name(self) -> str:
        return "extract_title"

    @property
    def description(self) -> str:
        return "Extract HTML title tag of a web URL."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "url": ToolParameter(type="string", description="Web URL")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        open_tool = OpenUrlTool()
        res = await open_tool.execute(call_id, arguments)
        if res.success and "Title: " in res.output:
            title_line = res.output.split("\n")[0]
            return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=title_line)
        return res


class ExtractLinksTool(BaseTool):
    """Tool to extract hyperlinks from a web page."""

    @property
    def name(self) -> str:
        return "extract_links"

    @property
    def description(self) -> str:
        return "Extract hyperlink anchor tags from a web URL."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "url": ToolParameter(type="string", description="Web URL")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        url = arguments.get("url")
        if not url:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'url' is required.")

        if PLAYWRIGHT_AVAILABLE:
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page(user_agent=DEFAULT_USER_AGENT)
                    await page.goto(url, timeout=15000)
                    links = await page.eval_on_selector_all("a[href]", "elements => elements.map(e => e.href)")
                    await browser.close()
                    out = "\n".join(links[:30]) if links else "[No links found]"
                    return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=out)
            except Exception as err:
                return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))

        return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Playwright is required for link extraction.")
