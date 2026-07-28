"""Project ZERO — Operating System Intelligence Package (Phase 7)."""

from operating_system.file_classifier import FileClassifier
from operating_system.path_resolver import PathResolver
from operating_system.filesystem_indexer import FilesystemIndexer, FileMetadata
from operating_system.search_engine import OSSearchEngine, OSSearchResult
from operating_system.application_manager import ApplicationManager
from operating_system.desktop_environment import DesktopEnvironment
from operating_system.storage_manager import StorageManager, StorageReport
from operating_system.workspace_manager import OSWorkspaceManager, DiscoveredProject
from operating_system.process_manager import OSProcessManager
from operating_system.permission_manager import PermissionManager
from operating_system.recent_items import RecentItemsTracker
from operating_system.system_context import OSSystemContext

__all__ = [
    "FileClassifier",
    "PathResolver",
    "FilesystemIndexer",
    "FileMetadata",
    "OSSearchEngine",
    "OSSearchResult",
    "ApplicationManager",
    "DesktopEnvironment",
    "StorageManager",
    "StorageReport",
    "OSWorkspaceManager",
    "DiscoveredProject",
    "OSProcessManager",
    "PermissionManager",
    "RecentItemsTracker",
    "OSSystemContext",
]
