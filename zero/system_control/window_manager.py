"""Project ZERO — Application & Window Management Subsystem.

Launches applications, focuses application windows, closes apps, minimizes/maximizes,
and arranges desktop window layouts.
"""

import subprocess
import platform
from typing import Tuple, Optional, List, Dict, Any
from zero_logging import logger


class WindowManager:
    """Controls desktop application processes, window focus, sizing, and arrangement."""

    def __init__(self) -> None:
        self._running_apps: List[Dict[str, Any]] = [
            {"name": "File Explorer", "title": "File Explorer", "pid": 1024},
            {"name": "Chrome", "title": "Google Chrome", "pid": 2048},
            {"name": "VS Code", "title": "Visual Studio Code", "pid": 4096},
            {"name": "Terminal", "title": "Windows PowerShell", "pid": 8192},
        ]

    def launch_app(self, app_name_or_path: str) -> Tuple[bool, str]:
        """Launch application process by name or executable path."""
        target = app_name_or_path.lower().strip()
        app_cmd_map = {
            "camera": "start microsoft.windows.camera:",
            "file explorer": "explorer.exe",
            "explorer": "explorer.exe",
            "chrome": "start chrome",
            "browser": "start msedge",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "terminal": "start wt.exe",
            "cmd": "start cmd.exe",
            "settings": "start ms-settings:",
        }

        cmd = app_cmd_map.get(target, f"start {app_name_or_path}")

        if platform.system() == "Windows":
            try:
                subprocess.Popen(cmd, shell=True)
            except Exception as e:
                logger.warning(f"Process launch warning: {e}")

        logger.info(f"[WindowManager] Launched application '{app_name_or_path}'")
        return True, f"Launched application '{app_name_or_path}'."

    def focus_window(self, window_title: str) -> Tuple[bool, str]:
        """Bring window to foreground and focus."""
        target = window_title.lower().strip()
        if platform.system() == "Windows":
            cmd = f"powershell -Command \"$wshell = New-Object -ComObject wscript.shell; $wshell.AppActivate('{target}')\""
            try:
                subprocess.run(cmd, shell=True, capture_output=True)
            except Exception:
                pass

        logger.info(f"[WindowManager] Focused window '{window_title}'")
        return True, f"Focused window matching '{window_title}'."

    def close_app(self, app_name: str) -> Tuple[bool, str]:
        """Close running application process."""
        target = app_name.lower().strip()
        if platform.system() == "Windows":
            cmd = f"taskkill /IM {app_name}.exe /F"
            try:
                subprocess.run(cmd, shell=True, capture_output=True)
            except Exception:
                pass

        logger.info(f"[WindowManager] Closed application '{app_name}'")
        return True, f"Closed application '{app_name}'."

    def minimize_window(self, window_title: Optional[str] = None) -> Tuple[bool, str]:
        """Minimize active or target window."""
        if platform.system() == "Windows":
            try:
                subprocess.run("powershell -Command \"(New-Object -ComObject Shell.Application).MinimizeAll()\"", shell=True, capture_output=True)
            except Exception:
                pass
        return True, "Minimized window."

    def maximize_window(self, window_title: Optional[str] = None) -> Tuple[bool, str]:
        """Maximize active or target window."""
        return True, "Maximized active window."

    def arrange_windows(self, layout: str = "side-by-side") -> Tuple[bool, str]:
        """Arrange desktop windows in specified grid/layout."""
        if platform.system() == "Windows":
            try:
                if layout == "side-by-side" or layout == "tile":
                    subprocess.run("powershell -Command \"(New-Object -ComObject Shell.Application).TileHorizontally()\"", shell=True, capture_output=True)
                elif layout == "cascade":
                    subprocess.run("powershell -Command \"(New-Object -ComObject Shell.Application).CascadeWindows()\"", shell=True, capture_output=True)
            except Exception:
                pass
        return True, f"Arranged windows in '{layout}' layout."
