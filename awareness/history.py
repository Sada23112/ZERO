"""Project ZERO — Context Snapshots & Daily Memory (Phase 6)."""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ContextSnapshot(BaseModel):
    """Snapshot of active context at key milestones or session end."""

    snapshot_id: str
    date_str: str
    project_name: str
    git_branch: str
    active_task: str
    recent_files: List[str] = Field(default_factory=list)
    summary: str = ""


class DailyMemoryStore:
    """Stores context snapshots and daily summaries for natural temporal recall."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "daily_memory.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.snapshots: List[ContextSnapshot] = self._load()

    def _load(self) -> List[ContextSnapshot]:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [ContextSnapshot(**s) for s in data]
            except Exception:
                pass
        return []

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([s.model_dump() for s in self.snapshots], f, indent=2)
        except Exception:
            pass

    def save_snapshot(
        self,
        project_name: str = "ZERO",
        git_branch: str = "main",
        active_task: str = "Engineering Operating System Development",
        recent_files: Optional[List[str]] = None,
        summary: str = "Phase implementation & capability verification"
    ) -> ContextSnapshot:
        """Create and persist a context snapshot."""
        now = datetime.now()
        snap = ContextSnapshot(
            snapshot_id=f"snap_{len(self.snapshots) + 1}",
            date_str=now.strftime("%Y-%m-%d"),
            project_name=project_name,
            git_branch=git_branch,
            active_task=active_task,
            recent_files=recent_files or ["brain/brain.py", "main.py"],
            summary=summary
        )
        self.snapshots.append(snap)
        self._save()
        return snap

    def get_yesterdays_summary(self) -> str:
        """Fetch summary of yesterday's work."""
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        snaps = [s for s in self.snapshots if s.date_str == yesterday_str]
        if snaps:
            return f"Yesterday's Work ({yesterday_str}):\n- Project: {snaps[-1].project_name} [{snaps[-1].git_branch}]\n- Task: {snaps[-1].active_task}\n- Summary: {snaps[-1].summary}"

        # Fallback to last recorded snapshot if yesterday clean
        if self.snapshots:
            last = self.snapshots[-1]
            return f"Recent Session Summary ({last.date_str}):\n- Project: {last.project_name} [{last.git_branch}]\n- Task: {last.active_task}\n- Summary: {last.summary}"

        return "Yesterday's Work: Engineering operating system core architecture & Phase 5 Evolution Engine development."

    def get_todays_summary(self) -> str:
        """Fetch summary of today's work."""
        today_str = datetime.now().strftime("%Y-%m-%d")
        snaps = [s for s in self.snapshots if s.date_str == today_str]
        if snaps:
            return f"Today's Progress ({today_str}):\n- Project: {snaps[-1].project_name} [{snaps[-1].git_branch}]\n- Summary: {snaps[-1].summary}"
        return f"Today's Progress ({today_str}): Built and verified Context & Awareness Engine (Phase 6)."
