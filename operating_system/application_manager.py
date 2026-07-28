"""Project ZERO — Application Manager & Launcher (Phase 7)."""

import os
import sys
import shutil
import subprocess
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional, List
from zero_logging import logger


class ApplicationManager:
    """Detects and controls desktop applications (VS Code, Chrome, Explorer, Discord, Spotify)."""

    COMMON_APPS = {
        "vs code": ["code", "code.cmd", "code.exe"],
        "vscode": ["code", "code.cmd", "code.exe"],
        "chrome": ["chrome", "chrome.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
        "file explorer": ["explorer.exe", "explorer"],
        "explorer": ["explorer.exe", "explorer"],
        "spotify": ["spotify", "spotify.exe"],
        "discord": ["discord", "discord.exe"],
        "blender": ["blender", "blender.exe"],
        "photoshop": ["photoshop", "photoshop.exe"]
    }

    def launch_application(self, app_name: str) -> bool:
        """Locate executable and launch desktop application."""
        clean_name = app_name.lower().strip()
        logger.info(f"Attempting to launch application: {clean_name}")

        # Check File Explorer special case
        if clean_name in ["file explorer", "explorer"]:
            os.startfile(str(Path.home())) if hasattr(os, "startfile") else subprocess.Popen(["explorer"])
            return True

        executables = self.COMMON_APPS.get(clean_name, [clean_name, f"{clean_name}.exe"])

        for exe in executables:
            # Check PATH
            path_loc = shutil.which(exe)
            if path_loc:
                try:
                    subprocess.Popen([path_loc])
                    logger.info(f"Launched application '{app_name}' via PATH: {path_loc}")
                    return True
                except Exception:
                    pass

            # Check direct file path
            if os.path.exists(exe):
                try:
                    subprocess.Popen([exe])
                    logger.info(f"Launched application '{app_name}' via direct path: {exe}")
                    return True
                except Exception:
                    pass

        # Fallback to browser URL launch for web apps if executable missing
        if "chrome" in clean_name or "browser" in clean_name:
            webbrowser.open("https://google.com")
            return True

        logger.warning(f"Could not find executable for application '{app_name}'.")
        return False
