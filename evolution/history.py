"""Project ZERO — Evolution History Store (Phase 5)."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from evolution.metadata import CapabilityMetadata


class EvolutionHistoryRecord(BaseModel):
    """Historical audit record of an evolution event."""

    record_id: str
    action_type: str  # 'generate', 'repair', 'rollback', 'upgrade'
    capability_name: str
    user_prompt: str
    status: str       # 'success', 'failed', 'rolled_back'
    timestamp: str = ""
    metadata: Optional[CapabilityMetadata] = None


class EvolutionHistoryStore:
    """Persistent audit log store for all capability evolutions."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "evolution_history.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.records: List[EvolutionHistoryRecord] = self._load()

    def _load(self) -> List[EvolutionHistoryRecord]:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [EvolutionHistoryRecord(**r) for r in data]
            except Exception:
                pass
        return []

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([r.model_dump() for r in self.records], f, indent=2)
        except Exception:
            pass

    def add_record(self, action_type: str, capability_name: str, user_prompt: str, status: str, metadata: Optional[CapabilityMetadata] = None) -> EvolutionHistoryRecord:
        """Record an evolution audit log entry."""
        rec = EvolutionHistoryRecord(
            record_id=f"evo_{len(self.records) + 1}",
            action_type=action_type,
            capability_name=capability_name,
            user_prompt=user_prompt,
            status=status,
            metadata=metadata
        )
        self.records.append(rec)
        self._save()
        return rec
