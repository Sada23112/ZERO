"""Project ZERO — Reusable Prompt Library (Phase 4 Capability #18)."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PromptTemplate(BaseModel):
    """Reusable prompt template model."""

    name: str
    content: str
    tags: List[str] = Field(default_factory=list)
    version: int = 1


class PromptLibrary:
    """Stores, versions, and searches reusable prompt templates."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "prompt_library.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.prompts: Dict[str, PromptTemplate] = self._load()

    def _load(self) -> Dict[str, PromptTemplate]:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {k: PromptTemplate(**v) for k, v in data.items()}
            except Exception:
                pass
        return {}

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump({k: v.model_dump() for k, v in self.prompts.items()}, f, indent=2)
        except Exception:
            pass

    def add_prompt(self, name: str, content: str, tags: Optional[List[str]] = None) -> PromptTemplate:
        """Add or update a versioned prompt template."""
        version = 1
        if name in self.prompts:
            version = self.prompts[name].version + 1

        tmpl = PromptTemplate(name=name, content=content, tags=tags or [], version=version)
        self.prompts[name] = tmpl
        self._save()
        return tmpl

    def search_prompts(self, query: str) -> List[PromptTemplate]:
        """Search prompt templates by name or tags."""
        q_lower = query.lower()
        return [
            p for p in self.prompts.values()
            if q_lower in p.name.lower() or any(q_lower in t.lower() for t in p.tags)
        ]
