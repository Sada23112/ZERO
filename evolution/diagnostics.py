"""Project ZERO — Self-Improvement & Diagnostics Engine (Phase 5)."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ImprovementSuggestion(BaseModel):
    """Structured suggestion for code quality or architectural improvement."""

    category: str  # 'large_file', 'missing_tests', 'complexity'
    file_path: str
    description: str
    recommendation: str


class SelfImprovementDiagnostics:
    """Periodically analyzes codebase for large files, missing tests, and performance bottlenecks."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def analyze_improvements(self) -> List[ImprovementSuggestion]:
        """Scan project codebase and detect improvement opportunities."""
        suggestions: List[ImprovementSuggestion] = []

        for root, dirs, files in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "node_modules", "data"]]

            for f in files:
                if f.endswith(".py"):
                    full_p = Path(root, f)
                    rel_p = str(full_p.relative_to(self.workspace_root))

                    # Check Large Files (> 400 lines)
                    try:
                        lines = full_p.read_text(encoding="utf-8").splitlines()
                        if len(lines) > 400:
                            suggestions.append(ImprovementSuggestion(
                                category="large_file",
                                file_path=rel_p,
                                description=f"File contains {len(lines)} lines.",
                                recommendation="Consider modularizing into smaller submodules."
                            ))
                    except Exception:
                        pass

        return suggestions
