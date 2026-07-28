"""Project ZERO — Operating System Metadata Indexer (Phase 7)."""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from operating_system.file_classifier import FileClassifier


class FileMetadata(BaseModel):
    """Metadata record representing an indexed file on the OS."""

    name: str
    path: str
    extension: str
    size_bytes: int
    modified_at: float
    category: str


class FilesystemIndexer:
    """Indexes OS user directories (Desktop, Documents, Downloads, Projects) metadata."""

    def __init__(self, index_file: Optional[Path] = None):
        self.index_file = (index_file or (Path.cwd() / "data" / "os_metadata_index.json")).resolve()
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        self.index: Dict[str, FileMetadata] = self._load()

    def _load(self) -> Dict[str, FileMetadata]:
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {k: FileMetadata(**v) for k, v in data.items()}
            except Exception:
                pass
        return {}

    def _save(self):
        try:
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump({k: v.model_dump() for k, v in self.index.items()}, f, indent=2)
        except Exception:
            pass

    def index_directory(self, target_dir: Path, max_files: int = 500) -> int:
        """Scan directory and index file metadata."""
        count = 0
        if not target_dir.exists():
            return 0

        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "node_modules", "AppData", "Windows", "Program Files"]]

            for f in files:
                if count >= max_files:
                    break
                fp = Path(root, f)
                try:
                    stat = fp.stat()
                    meta = FileMetadata(
                        name=f,
                        path=str(fp),
                        extension=fp.suffix.lower(),
                        size_bytes=stat.st_size,
                        modified_at=stat.st_mtime,
                        category=FileClassifier.classify(f)
                    )
                    self.index[str(fp)] = meta
                    count += 1
                except Exception:
                    pass

        self._save()
        return count
