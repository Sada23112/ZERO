"""Project ZERO — Clipboard Subsystem Control.

Manages system clipboard reading, writing, and clearing.
"""

import subprocess
import platform
from typing import Tuple
from zero_logging import logger


class ClipboardController:
    """Manages system clipboard operations."""

    def __init__(self) -> None:
        self._in_memory_clip: str = "Project ZERO System Clipboard"

    def read_clipboard(self) -> str:
        """Read current text from system clipboard."""
        if platform.system() == "Windows":
            try:
                res = subprocess.run("powershell -Command Get-Clipboard", shell=True, capture_output=True, text=True)
                if res.returncode == 0 and res.stdout:
                    self._in_memory_clip = res.stdout.strip()
            except Exception:
                pass
        return self._in_memory_clip

    def write_clipboard(self, text: str) -> Tuple[bool, str]:
        """Copy text string to system clipboard."""
        self._in_memory_clip = text
        if platform.system() == "Windows":
            try:
                cmd = f"powershell -Command \"Set-Clipboard -Value '{text}'\""
                subprocess.run(cmd, shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Clipboard] Written to clipboard.")
        return True, f"Copied '{text[:30]}...' to clipboard."

    def clear_clipboard(self) -> Tuple[bool, str]:
        """Clear system clipboard contents."""
        self._in_memory_clip = ""
        if platform.system() == "Windows":
            try:
                subprocess.run("powershell -Command Clear-Clipboard", shell=True, capture_output=True)
            except Exception:
                pass
        return True, "Clipboard cleared."
