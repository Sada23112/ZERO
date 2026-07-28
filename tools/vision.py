"""Project ZERO — Screenshot & Vision Capture Tool (Phase 4 Capability #5)."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False


class VisionCaptureTool(BaseTool):
    """Tool to capture desktop screenshots, active window bounds, or custom region snapshots."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = (output_dir or (Path.cwd() / "data" / "screenshots")).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def name(self) -> str:
        return "vision_capture"

    @property
    def description(self) -> str:
        return "Capture a desktop screenshot or region snapshot and save to disk."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "filename": ToolParameter(type="string", description="Optional output image filename", required=False),
                "monitor": ToolParameter(type="integer", description="Monitor index (default 1)", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        filename = arguments.get("filename", f"screenshot_{call_id}.png")
        if not filename.endswith(".png"):
            filename = f"{filename}.png"

        target_file = self.output_dir / filename

        if MSS_AVAILABLE:
            try:
                with mss.mss() as sct:
                    monitor_idx = arguments.get("monitor", 1)
                    if monitor_idx < len(sct.monitors):
                        mon = sct.monitors[monitor_idx]
                    else:
                        mon = sct.monitors[0]

                    sct_img = sct.grab(mon)
                    if PIL_AVAILABLE:
                        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                        img.save(target_file)
                    else:
                        mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(target_file))

                logger.info(f"Captured screenshot: {target_file}")
                return ToolResult(
                    call_id=call_id,
                    tool_name=self.name,
                    success=True,
                    output=f"Screenshot saved to: {target_file}"
                )
            except Exception as err:
                logger.error(f"Failed capturing screenshot with mss: {err}")
                return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))

        return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="mss library is required for screenshot capture.")
