"""Project ZERO — OS-Wide Project Discovery & Workspace Manager (Phase 7)."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DiscoveredProject(BaseModel):
    """Metadata representing an OS-wide discovered software project."""

    name: str
    path: str
    project_type: str  # 'Flutter', 'Python', 'Node', 'Rust', 'C++', 'Java'
    key_file: str


class OSWorkspaceManager:
    """Discovers software engineering projects across host operating system drives."""

    PROJECT_INDICATORS = {
        "pubspec.yaml": "Flutter",
        "pyproject.toml": "Python",
        "requirements.txt": "Python",
        "package.json": "Node / JavaScript",
        "Cargo.toml": "Rust",
        "CMakeLists.txt": "C++",
        "pom.xml": "Java"
    }

    def discover_projects(self, search_root: Optional[Path] = None, max_depth: int = 3) -> List[DiscoveredProject]:
        """Scan OS drive for engineering projects."""
        base_dir = search_root or Path.home()
        projects: List[DiscoveredProject] = []

        try:
            for root, dirs, files in os.walk(base_dir):
                # Calculate depth
                rel_p = Path(root).relative_to(base_dir)
                if len(rel_p.parts) > max_depth:
                    dirs.clear()
                    continue

                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "node_modules", "AppData", "Windows", "Library"]]

                for indicator, p_type in self.PROJECT_INDICATORS.items():
                    if indicator in files:
                        proj = DiscoveredProject(
                            name=Path(root).name,
                            path=root,
                            project_type=p_type,
                            key_file=indicator
                        )
                        projects.append(proj)
                        dirs.clear()  # Don't recurse into discovered project subdirectories
                        break
        except Exception:
            pass

        return projects
