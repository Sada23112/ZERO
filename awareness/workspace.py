"""Project ZERO — Workspace & Project Awareness (Phase 6)."""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional


class WorkspaceAwareness:
    """Detects active workspace, repository, git branch, modified files, & test status."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def get_workspace_info(self) -> Dict[str, Any]:
        """Collect current workspace state."""
        branch = self._get_git_branch()
        modified = self._get_recently_modified_files()

        return {
            "workspace_root": str(self.workspace_root),
            "project_name": self.workspace_root.name,
            "git_branch": branch,
            "recently_modified_files": modified,
            "has_pytest": (self.workspace_root / "pytest.ini").exists() or (self.workspace_root / "tests").exists()
        }

    def _get_git_branch(self) -> str:
        """Fetch active git branch name."""
        try:
            res = subprocess.run(["git", "branch", "--show-current"], cwd=str(self.workspace_root), capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
        return "main"

    def _get_recently_modified_files(self, limit: int = 5) -> List[str]:
        """Return list of most recently modified files in workspace."""
        modified_files = []
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "node_modules", "data", "build"]]
                for f in files:
                    if f.endswith((".py", ".json", ".md", ".toml", ".txt")):
                        fp = Path(root, f)
                        modified_files.append((fp, fp.stat().st_mtime))

            modified_files.sort(key=lambda x: x[1], reverse=True)
            return [str(fp[0].relative_to(self.workspace_root)) for fp in modified_files[:limit]]
        except Exception:
            return []
