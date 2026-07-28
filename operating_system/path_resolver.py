"""Project ZERO — Natural Language Path Resolver (Phase 7)."""

import os
from pathlib import Path
from typing import Optional, List
from operating_system.file_classifier import FileClassifier


class PathResolver:
    """Resolves natural language folder/file descriptions to concrete filesystem paths."""

    @staticmethod
    def get_standard_directory(name: str) -> Optional[Path]:
        """Resolve standard OS user directory names."""
        home = Path.home()
        n = name.lower().strip()

        # Check direct and OneDrive locations for Desktop/Documents
        desktop = home / "Desktop" if (home / "Desktop").exists() else (home / "OneDrive" / "Desktop" if (home / "OneDrive" / "Desktop").exists() else home)
        documents = home / "Documents" if (home / "Documents").exists() else (home / "OneDrive" / "Documents" if (home / "OneDrive" / "Documents").exists() else home)
        downloads = home / "Downloads" if (home / "Downloads").exists() else home

        dir_map = {
            "desktop": desktop,
            "downloads": downloads,
            "documents": documents,
            "pictures": home / "Pictures" if (home / "Pictures").exists() else home,
            "videos": home / "Videos" if (home / "Videos").exists() else home,
            "music": home / "Music" if (home / "Music").exists() else home,
            "home": home,
            "user home": home,
            "temp": Path(os.environ.get("TEMP", "/tmp"))
        }

        target = dir_map.get(n)
        if target:
            return target
        return None

    @classmethod
    def resolve_newest_file(cls, category: Optional[str] = None, search_dir: Optional[Path] = None) -> Optional[Path]:
        """Find the newest modified file in a directory (defaulting to Downloads or Home)."""
        base_dir = search_dir or (Path.home() / "Downloads")
        if not base_dir.exists():
            base_dir = Path.home()

        extensions = FileClassifier.get_extensions_for_category(category) if category else None

        candidates = []
        try:
            for item in base_dir.iterdir():
                if item.is_file():
                    if extensions is None or item.suffix.lower() in extensions:
                        candidates.append((item, item.stat().st_mtime))

            if candidates:
                candidates.sort(key=lambda x: x[1], reverse=True)
                return candidates[0][0]
        except Exception:
            pass

        return None
