"""Unit tests for Phase 7 Operating System Intelligence."""

import pytest
from pathlib import Path
from operating_system.file_classifier import FileClassifier
from operating_system.path_resolver import PathResolver
from operating_system.filesystem_indexer import FilesystemIndexer
from operating_system.search_engine import OSSearchEngine
from operating_system.application_manager import ApplicationManager
from operating_system.storage_manager import StorageManager
from operating_system.workspace_manager import OSWorkspaceManager
from operating_system.permission_manager import PermissionManager
from operating_system.recent_items import RecentItemsTracker
from brain.brain import Brain


def test_file_classifier():
    assert FileClassifier.classify("sample.pdf") == "documents"
    assert FileClassifier.classify("app.py") == "code"
    assert FileClassifier.classify("archive.zip") == "archives"


def test_path_resolver():
    desktop = PathResolver.get_standard_directory("desktop")
    assert desktop is not None
    assert desktop.name.lower() == "desktop"

    home = PathResolver.get_standard_directory("user home")
    assert home is not None


def test_indexer_and_search(tmp_path: Path):
    (tmp_path / "doc1.pdf").write_text("dummy doc 1", encoding="utf-8")
    (tmp_path / "doc2.pdf").write_text("dummy doc 2", encoding="utf-8")

    index_file = tmp_path / "os_idx.json"
    indexer = FilesystemIndexer(index_file=index_file)
    count = indexer.index_directory(tmp_path)
    assert count >= 2

    search_engine = OSSearchEngine(indexer=indexer)
    res = search_engine.search("doc")
    assert len(res.matches) >= 2
    assert res.needs_disambiguation is True


def test_application_manager():
    app_manager = ApplicationManager()
    assert app_manager.launch_application("file explorer") is True


def test_storage_manager():
    mgr = StorageManager()
    rep = mgr.get_storage_report()
    assert rep.total_gb > 0
    assert rep.free_gb > 0


def test_workspace_manager(tmp_path: Path):
    (tmp_path / "my_flutter_app").mkdir()
    (tmp_path / "my_flutter_app" / "pubspec.yaml").write_text("name: flutter_app", encoding="utf-8")

    wm = OSWorkspaceManager()
    projects = wm.discover_projects(search_root=tmp_path)
    assert len(projects) == 1
    assert projects[0].project_type == "Flutter"


def test_permission_manager():
    assert PermissionManager.is_destructive_action("delete file.txt") is True
    assert PermissionManager.is_destructive_action("read file.txt") is False


@pytest.mark.asyncio
async def test_brain_os_triggers():
    brain = Brain()

    res1 = await brain.process("Open Downloads")
    assert "Opened OS directory" in res1

    res2 = await brain.process("Launch File Explorer")
    assert "Launched application" in res2

    res3 = await brain.process("Show largest folders")
    assert "Storage Intelligence Analytics" in res3
