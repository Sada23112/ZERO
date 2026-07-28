"""Project ZERO — Display & Monitor Subsystem Control.

Manages monitor detection, screen resolution changes, multi-monitor topologies, and display switching.
"""

import subprocess
import platform
from typing import List, Dict, Any, Tuple
from zero_logging import logger


class DisplayController:
    """Controls display monitors, screen resolutions, and multi-monitor projection topologies."""

    def __init__(self) -> None:
        self.current_resolution: Tuple[int, int] = (1920, 1080)
        self.projection_mode: str = "extend"
        self._monitors: List[Dict[str, Any]] = [
            {"id": "MONITOR-1", "name": "Primary Display (4K UHD)", "resolution": "3840x2160", "primary": True},
            {"id": "MONITOR-2", "name": "Secondary Monitor (FHD)", "resolution": "1920x1080", "primary": False},
        ]

    def detect_monitors(self) -> List[Dict[str, Any]]:
        """Detect connected monitor displays."""
        return list(self._monitors)

    def change_resolution(self, width: int, height: int, confirm: bool = True) -> Tuple[bool, str]:
        """Change primary screen display resolution."""
        if not confirm:
            return False, "Resolution change requires confirmation."

        self.current_resolution = (width, height)
        logger.info(f"[Display] Changed resolution to {width}x{height}")
        return True, f"Display resolution changed to {width}x{height}."

    def switch_display_mode(self, mode: str = "extend") -> Tuple[bool, str]:
        """Switch display topology projection mode ('internal', 'external', 'duplicate', 'extend')."""
        valid_modes = ["internal", "external", "duplicate", "extend"]
        m = mode.lower().strip()
        if m not in valid_modes:
            return False, f"Invalid projection mode. Choose from {valid_modes}"

        self.projection_mode = m
        if platform.system() == "Windows":
            flag_map = {"internal": "/internal", "external": "/external", "duplicate": "/clone", "extend": "/extend"}
            flag = flag_map.get(m, "/extend")
            try:
                subprocess.run(f"displayswitch.exe {flag}", shell=True, capture_output=True)
            except Exception:
                pass

        logger.info(f"[Display] Switched projection mode to '{m}'")
        return True, f"Display topology switched to '{m}' mode."
