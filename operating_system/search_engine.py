"""Project ZERO — Operating System Search Engine & Disambiguator (Phase 7)."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from operating_system.filesystem_indexer import FilesystemIndexer, FileMetadata
from operating_system.file_classifier import FileClassifier


class OSSearchResult:
    """Outcome of OS search query."""

    def __init__(self, matches: List[FileMetadata], needs_disambiguation: bool = False, message: str = ""):
        self.matches = matches
        self.needs_disambiguation = needs_disambiguation
        self.message = message


class OSSearchEngine:
    """Fast OS metadata search with disambiguation when multiple files match."""

    def __init__(self, indexer: Optional[FilesystemIndexer] = None):
        self.indexer = indexer or FilesystemIndexer()

    def search(self, query: str, category: Optional[str] = None, max_results: int = 20) -> OSSearchResult:
        """Search OS index for files matching query or category."""
        q = query.lower().strip()
        results: List[FileMetadata] = []

        # If index empty, populate from Desktop & Downloads
        if not self.indexer.index:
            self.indexer.index_directory(Path.home() / "Downloads", max_files=100)
            self.indexer.index_directory(Path.home() / "Desktop", max_files=100)

        for meta in self.indexer.index.values():
            name_match = q in meta.name.lower() or q in meta.path.lower()
            cat_match = category is None or meta.category.lower() == category.lower()

            if name_match and cat_match:
                results.append(meta)

        # Sort by modification time descending
        results.sort(key=lambda x: x.modified_at, reverse=True)

        if len(results) > 1 and "newest" not in q and "latest" not in q:
            lines = [f"{i+1}. {m.name} ({m.path})" for i, m in enumerate(results[:5])]
            msg = f"I found {len(results)} matching files. Which one did you mean?\n" + "\n".join(lines)
            return OSSearchResult(matches=results, needs_disambiguation=True, message=msg)

        return OSSearchResult(matches=results, needs_disambiguation=False, message=f"Found {len(results)} matching file(s).")
