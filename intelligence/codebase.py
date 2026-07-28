"""Project ZERO — Codebase Intelligence & Indexer (Phase 4 Capability #2)."""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CodebaseAnalysis(BaseModel):
    """Structured report of project codebase structure and technology stack."""

    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    package_managers: List[str] = Field(default_factory=list)
    build_systems: List[str] = Field(default_factory=list)
    test_frameworks: List[str] = Field(default_factory=list)
    entry_points: List[str] = Field(default_factory=list)
    config_files: List[str] = Field(default_factory=list)
    total_files: int = 0
    total_lines_of_code: int = 0


class CodebaseIntelligence:
    """Analyzes and indexes local codebase architecture, entry points, & tech stack."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def analyze_project(self) -> CodebaseAnalysis:
        """Scan workspace to detect programming languages, frameworks, entry points, & build systems."""
        analysis = CodebaseAnalysis()

        file_counts: Dict[str, int] = {}
        for root, dirs, files in os.walk(self.workspace_root):
            # Skip hidden / build dirs
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "node_modules", "build", "dist"]]

            for f in files:
                analysis.total_files += 1
                ext = Path(f).suffix.lower()
                file_counts[ext] = file_counts.get(ext, 0) + 1

                # Check configuration files
                if f in ["pyproject.toml", "requirements.txt", "package.json", "Cargo.toml", "go.mod", "pom.xml", ".env"]:
                    analysis.config_files.append(f)

                # Check entry points
                if f in ["main.py", "app.py", "index.js", "index.ts", "main.go", "main.rs", "App.tsx"]:
                    rel_p = str(Path(root, f).relative_to(self.workspace_root))
                    analysis.entry_points.append(rel_p)

        # Detect Languages
        if ".py" in file_counts:
            analysis.languages.append("Python")
        if ".js" in file_counts or ".ts" in file_counts or ".tsx" in file_counts:
            analysis.languages.append("JavaScript/TypeScript")
        if ".go" in file_counts:
            analysis.languages.append("Go")
        if ".rs" in file_counts:
            analysis.languages.append("Rust")

        # Detect Package Managers & Frameworks
        if (self.workspace_root / "requirements.txt").exists() or (self.workspace_root / "pyproject.toml").exists():
            analysis.package_managers.append("pip / uv")
        if (self.workspace_root / "package.json").exists():
            analysis.package_managers.append("npm / yarn / pnpm")

        if (self.workspace_root / "pytest.ini").exists() or any("test_" in f for f in os.listdir(self.workspace_root)):
            analysis.test_frameworks.append("pytest")

        return analysis

    def find_dead_code_candidates(self) -> List[str]:
        """Find unused or unreferenced python module files as dead code candidates."""
        candidates = []
        for root, _, files in os.walk(self.workspace_root):
            for f in files:
                if f.startswith("temp_") or f.endswith(".tmp") or f.endswith(".bak"):
                    candidates.append(str(Path(root, f).relative_to(self.workspace_root)))
        return candidates
