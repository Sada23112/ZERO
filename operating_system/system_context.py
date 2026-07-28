"""Project ZERO — OS System Context Coordinator (Phase 7)."""

from pathlib import Path
from typing import Dict, Any, Optional

from operating_system.path_resolver import PathResolver
from operating_system.filesystem_indexer import FilesystemIndexer
from operating_system.search_engine import OSSearchEngine
from operating_system.application_manager import ApplicationManager
from operating_system.storage_manager import StorageManager
from operating_system.workspace_manager import OSWorkspaceManager
from operating_system.recent_items import RecentItemsTracker


class OSSystemContext:
    """Unified Operating System Context Coordinator."""

    def __init__(self):
        self.path_resolver = PathResolver()
        self.indexer = FilesystemIndexer()
        self.search_engine = OSSearchEngine(self.indexer)
        self.app_manager = ApplicationManager()
        self.storage_manager = StorageManager()
        self.workspace_manager = OSWorkspaceManager()
        self.recent_tracker = RecentItemsTracker()

    def get_os_context_summary(self) -> Dict[str, Any]:
        """Summarize current operating system workspace state."""
        recent_dl = self.recent_tracker.get_recent_downloads(limit=3)
        storage = self.storage_manager.get_storage_report()

        return {
            "user_home": str(Path.home()),
            "free_space_gb": storage.free_gb,
            "recent_downloads": [f.name for f in recent_dl],
            "indexed_files_count": len(self.indexer.index)
        }
