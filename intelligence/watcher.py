"""Project ZERO — File Watcher Subsystem (Phase 4 Capability #11)."""

import time
from pathlib import Path
from typing import Callable, Optional, List
from zero_logging import logger

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class ZeroFileWatcherHandler(FileSystemEventHandler if WATCHDOG_AVAILABLE else object):
    """Event handler capturing file modification, creation, and deletion events."""

    def __init__(self, callback: Optional[Callable[[str, str], None]] = None):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and self.callback:
            self.callback("modified", event.src_path)

    def on_created(self, event):
        if not event.is_directory and self.callback:
            self.callback("created", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and self.callback:
            self.callback("deleted", event.src_path)


class WorkspaceFileWatcher:
    """Monitors workspace directories for live file changes."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self._observer = None

    def start_watching(self, callback: Optional[Callable[[str, str], None]] = None):
        """Start monitoring workspace folder for live changes."""
        if WATCHDOG_AVAILABLE:
            try:
                handler = ZeroFileWatcherHandler(callback=callback)
                self._observer = Observer()
                self._observer.schedule(handler, str(self.workspace_root), recursive=True)
                self._observer.start()
                logger.info(f"File watcher started monitoring: {self.workspace_root}")
            except Exception as err:
                logger.warning(f"Failed starting watchdog observer: {err}")
        else:
            logger.warning("watchdog package not installed; file watcher disabled.")

    def stop_watching(self):
        """Stop file watcher observer."""
        if self._observer:
            try:
                self._observer.stop()
                self._observer.join()
                logger.info("File watcher stopped.")
            except Exception:
                pass
