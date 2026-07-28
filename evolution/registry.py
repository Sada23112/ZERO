"""Project ZERO — Dynamic Capability Registry (Phase 5)."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from evolution.metadata import CapabilityMetadata
from zero_logging import logger


class CapabilityRegistryStore:
    """Persistent registry store for dynamically generated tools and capabilities."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "dynamic_capabilities.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.capabilities: Dict[str, CapabilityMetadata] = self._load()

    def _load(self) -> Dict[str, CapabilityMetadata]:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {k: CapabilityMetadata(**v) for k, v in data.items()}
            except Exception:
                pass
        return {}

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump({k: v.model_dump() for k, v in self.capabilities.items()}, f, indent=2)
        except Exception:
            pass

    def register_capability(self, meta: CapabilityMetadata):
        """Register a newly generated capability."""
        self.capabilities[meta.name] = meta
        self._save()
        logger.info(f"Registered capability in registry: {meta.name} v{meta.version}")

    def get_capability(self, name: str) -> Optional[CapabilityMetadata]:
        """Fetch metadata for a registered capability."""
        return self.capabilities.get(name)

    def deactivate_capability(self, name: str) -> bool:
        """Mark capability as inactive (rollback state)."""
        if name in self.capabilities:
            self.capabilities[name].is_active = False
            self._save()
            return True
        return False

    def list_capabilities(self) -> List[CapabilityMetadata]:
        """List active capabilities."""
        return [c for c in self.capabilities.values() if c.is_active]
