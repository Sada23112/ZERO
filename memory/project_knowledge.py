"""Project ZERO — Persistent Project Knowledge Store (Phase 4 Capability #14)."""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ProjectKnowledgeRecord(BaseModel):
    """Persistent per-project knowledge repository."""

    project_name: str
    architecture: str = "Standard Architecture"
    decisions: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    coding_style: str = "Clean Code & Type Safety"
    known_bugs: List[str] = Field(default_factory=list)
    build_instructions: str = "pip install -r requirements.txt; python main.py"


class ProjectKnowledgeStore:
    """Manages persistent knowledge records per project repository."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "project_knowledge.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.record: ProjectKnowledgeRecord = self._load()

    def _load(self) -> ProjectKnowledgeRecord:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return ProjectKnowledgeRecord(**data)
            except Exception:
                pass
        return ProjectKnowledgeRecord(project_name="Project ZERO")

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.record.model_dump(), f, indent=2)
        except Exception:
            pass

    def add_decision(self, decision_text: str):
        """Record an architectural decision."""
        self.record.decisions.append(decision_text)
        self._save()

    def add_known_bug(self, bug_description: str):
        """Record a known bug or issue."""
        self.record.known_bugs.append(bug_description)
        self._save()
