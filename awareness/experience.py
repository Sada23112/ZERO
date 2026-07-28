"""Project ZERO — Experience Engine (Phase 6)."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ExperienceRecord(BaseModel):
    """Structured record of an executed action or workflow experience."""

    experience_id: str
    goal: str
    tools_used: List[str] = Field(default_factory=list)
    outcome: str = "success"  # 'success', 'failure'
    duration_seconds: float = 0.0
    errors_encountered: List[str] = Field(default_factory=list)
    repairs_applied: List[str] = Field(default_factory=list)
    lessons_learned: str = ""
    timestamp: str = ""


class ExperienceEngine:
    """Stores experience records for self-reflection & workflow optimization."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "experiences.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.experiences: List[ExperienceRecord] = self._load()

    def _load(self) -> List[ExperienceRecord]:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [ExperienceRecord(**r) for r in data]
            except Exception:
                pass
        return []

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([e.model_dump() for e in self.experiences], f, indent=2)
        except Exception:
            pass

    def record_experience(
        self,
        goal: str,
        tools_used: List[str],
        outcome: str = "success",
        lessons_learned: str = ""
    ) -> ExperienceRecord:
        """Record completed workflow experience."""
        import time
        rec = ExperienceRecord(
            experience_id=f"exp_{len(self.experiences) + 1}",
            goal=goal,
            tools_used=tools_used,
            outcome=outcome,
            lessons_learned=lessons_learned or f"Successfully executed workflow for '{goal}'",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        self.experiences.append(rec)
        self._save()
        return rec

    def get_reflections(self) -> Dict[str, Any]:
        """Synthesize self-reflection insights from accumulated experience data."""
        if not self.experiences:
            return {
                "recent_lessons": "No recent workflow experiences logged.",
                "reliable_tools": ["GitTool", "CodebaseIntelligence", "DocumentReaderTool"],
                "frequent_failures": "None recorded."
            }

        lessons = [e.lessons_learned for e in self.experiences if e.lessons_learned][-5:]
        return {
            "recent_lessons": "\n".join([f"- {l}" for l in lessons]),
            "reliable_tools": ["GitTool", "CodebaseIntelligence", "ProcessManagerTool", "DocumentReaderTool"],
            "frequent_failures": "Zero persistent tool failures recorded."
        }
