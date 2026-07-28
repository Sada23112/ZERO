"""Project ZERO — Research Notebook Subsystem (Phase 4 Capability #17)."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ResearchNote(BaseModel):
    """Structured research notebook entry."""

    id: str
    title: str
    topic: str
    content: str
    citations: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    created_at: str = ""


class ResearchNotebook:
    """Organizes research notes, experiments, ideas, bookmarks, & citations."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "research_notebook.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.notes: List[ResearchNote] = self._load()

    def _load(self) -> List[ResearchNote]:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [ResearchNote(**item) for item in data]
            except Exception:
                pass
        return []

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([n.model_dump() for n in self.notes], f, indent=2)
        except Exception:
            pass

    def add_note(self, title: str, topic: str, content: str, citations: Optional[List[str]] = None, tags: Optional[List[str]] = None) -> ResearchNote:
        """Add a new research note entry to notebook."""
        note = ResearchNote(
            id=f"note_{len(self.notes) + 1}",
            title=title,
            topic=topic,
            content=content,
            citations=citations or [],
            tags=tags or []
        )
        self.notes.append(note)
        self._save()
        return note

    def search_notes(self, query: str) -> List[ResearchNote]:
        """Search notebook entries matching query string."""
        q_lower = query.lower()
        return [
            n for n in self.notes
            if q_lower in n.title.lower() or q_lower in n.topic.lower() or q_lower in n.content.lower()
        ]
