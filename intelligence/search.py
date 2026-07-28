"""Project ZERO — Semantic Code Search Engine (Phase 4 Capability #3)."""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """Structured code search match item."""

    file_path: str
    line_number: int
    line_content: str
    match_type: str  # 'symbol', 'function', 'class', 'todo', 'string'


class SemanticSearchEngine:
    """Fast workspace-wide semantic code search engine."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def search_pattern(self, pattern: str, match_type: str = "string", limit: int = 50) -> List[SearchResult]:
        """Search workspace files for regex/string pattern matches."""
        results: List[SearchResult] = []
        regex = re.compile(pattern, re.IGNORECASE)

        for root, dirs, files in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "node_modules", "build", "dist"]]

            for f in files:
                if len(results) >= limit:
                    break

                ext = Path(f).suffix.lower()
                if ext not in [".py", ".md", ".json", ".yaml", ".yml", ".toml", ".txt", ".js", ".ts", ".html"]:
                    continue

                full_p = Path(root, f)
                try:
                    with open(full_p, "r", encoding="utf-8", errors="ignore") as fp:
                        for line_idx, line in enumerate(fp, 1):
                            if regex.search(line):
                                rel_path = str(full_p.relative_to(self.workspace_root))
                                results.append(
                                    SearchResult(
                                        file_path=rel_path,
                                        line_number=line_idx,
                                        line_content=line.strip(),
                                        match_type=match_type
                                    )
                                )
                                if len(results) >= limit:
                                    break
                except Exception:
                    pass

        return results

    def search_functions(self, func_name: str) -> List[SearchResult]:
        """Search function definitions matching function name pattern."""
        return self.search_pattern(rf"def\s+{func_name}\b", match_type="function")

    def search_classes(self, class_name: str) -> List[SearchResult]:
        """Search class definitions matching class name pattern."""
        return self.search_pattern(rf"class\s+{class_name}\b", match_type="class")

    def search_todos(self) -> List[SearchResult]:
        """Search all TODO and FIXME comments across codebase."""
        return self.search_pattern(r"(TODO|FIXME)\b", match_type="todo")
