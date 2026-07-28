"""Project ZERO — Download Manager Subsystem (Phase 4 Capability #8)."""

from pathlib import Path
from typing import Dict, Any, Optional
import httpx
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger


class DownloadManagerTool(BaseTool):
    """Tool to download remote files with progress tracking, categorization, & auto-naming."""

    def __init__(self, download_dir: Optional[Path] = None):
        self.download_dir = (download_dir or (Path.cwd() / "data" / "downloads")).resolve()
        self.download_dir.mkdir(parents=True, exist_ok=True)

    @property
    def name(self) -> str:
        return "download_file"

    @property
    def description(self) -> str:
        return "Download a file from HTTP/HTTPS URL with auto-naming & progress tracking."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "url": ToolParameter(type="string", description="File URL to download"),
                "filename": ToolParameter(type="string", description="Optional output filename", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        url = arguments.get("url")
        if not url:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'url' is required.")

        custom_name = arguments.get("filename")
        if not custom_name:
            custom_name = url.split("/")[-1].split("?")[0] or f"download_{call_id}.bin"

        target_file = self.download_dir / custom_name

        try:
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                async with client.stream("GET", url) as response:
                    if response.status_code != 200:
                        return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"HTTP {response.status_code} download error.")

                    total_bytes = int(response.headers.get("Content-Length", 0))
                    downloaded_bytes = 0

                    with open(target_file, "wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=8192):
                            f.write(chunk)
                            downloaded_bytes += len(chunk)

            logger.info(f"Downloaded file: {target_file} ({downloaded_bytes} bytes)")
            return ToolResult(
                call_id=call_id,
                tool_name=self.name,
                success=True,
                output=f"Successfully downloaded file: {target_file.name} ({downloaded_bytes} bytes)\nSaved to: {target_file}"
            )
        except Exception as err:
            logger.error(f"Download failed for {url}: {err}")
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))
