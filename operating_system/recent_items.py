"""Project ZERO — Recent Activity Tracker (Phase 7)."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class RecentItemsTracker:
    """Tracks recent OS downloads, documents, screenshots, and archives."""

    @staticmethod
    def get_recent_downloads(limit: int = 5) -> List[Path]:
        """Fetch list of most recently downloaded files in Downloads directory."""
        downloads_dir = Path.home() / "Downloads"
        if not downloads_dir.exists():
            return []

        files = []
        try:
            for item in downloads_dir.iterdir():
                if item.is_file() and not item.name.startswith("."):
                    files.append((item, item.stat().st_mtime))

            files.sort(key=lambda x: x[1], reverse=True)
            return [f[0] for f in files[:limit]]
        except Exception:
            return []
