"""Project ZERO — Desktop Shell Environment Manager (Phase 7)."""

import os
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional


class DesktopEnvironment:
    """Provides desktop shell interaction helpers (open file, open folder, launch URL)."""

    @staticmethod
    def open_path(path: Path) -> bool:
        """Open a file or directory with default native system application."""
        if not path.exists():
            return False

        try:
            if hasattr(os, "startfile"):
                os.startfile(str(path))
            else:
                subprocess.Popen(["xdg-open" if os.name != "mac" else "open", str(path)])
            return True
        except Exception:
            return False

    @staticmethod
    def open_url(url: str) -> bool:
        """Launch web browser for URL."""
        return webbrowser.open(url)
