"""Project ZERO — OCR & Image Analysis Tool (Phase 4 Capability #6)."""

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


class ImageOCRTool(BaseTool):
    """Tool for OCR text extraction and image metadata analysis."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    @property
    def name(self) -> str:
        return "image_ocr"

    @property
    def description(self) -> str:
        return "Perform OCR text extraction and image property analysis on an image file."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "image_path": ToolParameter(type="string", description="Path to target image file")
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        img_str = arguments.get("image_path")
        if not img_str:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'image_path' is required.")

        target_p = Path(img_str).resolve()
        if not target_p.exists():
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Image file not found: {img_str}")

        info_lines = [f"Image File: {target_p.name}"]

        if PIL_AVAILABLE:
            try:
                with Image.open(target_p) as img:
                    info_lines.append(f"Format: {img.format}")
                    info_lines.append(f"Dimensions: {img.width}x{img.height} pixels")
                    info_lines.append(f"Color Mode: {img.mode}")
            except Exception as err:
                info_lines.append(f"Pillow analysis error: {err}")

        # OCR Fallback / Tesseract hook if installed
        try:
            import pytesseract
            text = pytesseract.image_to_string(Image.open(target_p))
            if text and text.strip():
                info_lines.append(f"\n[Extracted OCR Text]:\n{text.strip()[:1500]}")
        except Exception:
            info_lines.append("\n[OCR Engine: pytesseract not installed or tesseract binary not found in PATH]")

        return ToolResult(
            call_id=call_id,
            tool_name=self.name,
            success=True,
            output="\n".join(info_lines)
        )
