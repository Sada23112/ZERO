"""Project ZERO — Capability Registry.

Central registry tracking capabilities, manifests, health status, active bindings,
and snapshot state.
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from zero_logging import logger


class CapabilityCategory(str, Enum):
    """Supported capability categories in ZERO."""

    PROVIDER = "provider"
    MEMORY = "memory"
    PLANNER = "planner"
    VOICE = "voice"
    VISION = "vision"
    OCR = "ocr"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    STORAGE = "storage"
    LOGGER = "logger"
    EXPORTER = "exporter"
    PARSER = "parser"
    TOOL = "tool"
    SKILL = "skill"
    WORKFLOW = "workflow"
    REASONER = "reasoner"
    BROWSER = "browser"
    AUTOMATION = "automation"

    @classmethod
    def from_str(cls, val: str) -> "CapabilityCategory":
        """Convert string to CapabilityCategory safely."""
        val_lower = val.lower().strip()
        for member in cls:
            if member.value == val_lower:
                return member
        # Fallback default if custom
        return cls.PROVIDER


@dataclass
class CapabilityManifest:
    """Metadata manifest describing a registered capability."""

    name: str
    category: CapabilityCategory
    version: str = "1.0.0"
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)
    entry_point: str = ""
    health_status: str = "healthy"  # healthy, degraded, unhealthy, disabled
    supported_commands: List[str] = field(default_factory=list)
    enabled: bool = True
    instance: Optional[Any] = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to serializable dict."""
        return {
            "name": self.name,
            "category": self.category.value if isinstance(self.category, CapabilityCategory) else str(self.category),
            "version": self.version,
            "description": self.description,
            "dependencies": self.dependencies,
            "configuration": self.configuration,
            "entry_point": self.entry_point,
            "health_status": self.health_status,
            "supported_commands": self.supported_commands,
            "enabled": self.enabled,
            "created_at": self.created_at,
        }


class CapabilityRegistry:
    """Registry maintaining active and registered capability instances and metadata."""

    def __init__(self) -> None:
        # Category -> Name -> CapabilityManifest
        self._capabilities: Dict[str, Dict[str, CapabilityManifest]] = {}
        # Category -> Active Capability Name
        self._active: Dict[str, str] = {}
        # History snapshots for rollback
        self._history: List[Dict[str, Any]] = []

    def _cat_key(self, category: Union[CapabilityCategory, str]) -> str:
        if isinstance(category, CapabilityCategory):
            return category.value
        return str(category).lower().strip()

    def register(self, manifest: CapabilityManifest, instance: Optional[Any] = None) -> None:
        """Register a capability manifest and optional live instance."""
        cat_key = self._cat_key(manifest.category)
        if cat_key not in self._capabilities:
            self._capabilities[cat_key] = {}

        if instance is not None:
            manifest.instance = instance

        name_key = manifest.name.lower()
        self._capabilities[cat_key][name_key] = manifest
        logger.info(f"[Registry] Registered capability: {manifest.category.value if isinstance(manifest.category, CapabilityCategory) else manifest.category}:{manifest.name} v{manifest.version}")

        # Set active if no active capability exists for this category
        if cat_key not in self._active:
            self._active[cat_key] = name_key

    def unregister(self, category: Union[CapabilityCategory, str], name: str) -> Optional[CapabilityManifest]:
        """Remove a capability from registry."""
        cat_key = self._cat_key(category)
        name_key = name.lower()
        if cat_key in self._capabilities and name_key in self._capabilities[cat_key]:
            manifest = self._capabilities[cat_key].pop(name_key)
            if self._active.get(cat_key) == name_key:
                remaining = list(self._capabilities[cat_key].keys())
                self._active[cat_key] = remaining[0] if remaining else ""
            logger.info(f"[Registry] Unregistered capability: {cat_key}:{name}")
            return manifest
        return None

    def set_active(self, category: Union[CapabilityCategory, str], name: str) -> bool:
        """Set active capability for category."""
        cat_key = self._cat_key(category)
        name_key = name.lower()
        if cat_key in self._capabilities and name_key in self._capabilities[cat_key]:
            self._active[cat_key] = name_key
            logger.info(f"[Registry] Switched active {cat_key} -> {name}")
            return True
        logger.warning(f"[Registry] Capability {cat_key}:{name} not registered. Cannot switch active.")
        return False

    def get_active(self, category: Union[CapabilityCategory, str]) -> Optional[Any]:
        """Retrieve live instance of active capability in category."""
        manifest = self.get_active_manifest(category)
        return manifest.instance if manifest else None

    def get_active_manifest(self, category: Union[CapabilityCategory, str]) -> Optional[CapabilityManifest]:
        """Retrieve manifest of active capability in category."""
        cat_key = self._cat_key(category)
        active_name = self._active.get(cat_key)
        if active_name and cat_key in self._capabilities:
            return self._capabilities[cat_key].get(active_name)
        return None

    def get(self, category: Union[CapabilityCategory, str], name: Optional[str] = None) -> Optional[Any]:
        """Retrieve instance by category and optional name (defaults to active)."""
        if name:
            manifest = self.get_manifest(category, name)
            return manifest.instance if manifest else None
        return self.get_active(category)

    def get_manifest(self, category: Union[CapabilityCategory, str], name: str) -> Optional[CapabilityManifest]:
        """Retrieve manifest by category and name."""
        cat_key = self._cat_key(category)
        return self._capabilities.get(cat_key, {}).get(name.lower())

    def list_capabilities(self, category: Optional[Union[CapabilityCategory, str]] = None) -> List[CapabilityManifest]:
        """List manifests optionally filtered by category."""
        if category:
            cat_key = self._cat_key(category)
            return list(self._capabilities.get(cat_key, {}).values())
        result = []
        for cat_dict in self._capabilities.values():
            result.extend(cat_dict.values())
        return result

    def snapshot(self) -> Dict[str, Any]:
        """Create state snapshot for rollback."""
        active_copy = dict(self._active)
        caps_copy: Dict[str, List[Dict[str, Any]]] = {}
        for cat, caps in self._capabilities.items():
            caps_copy[cat] = [m.to_dict() for m in caps.values()]

        snap = {
            "timestamp": time.time(),
            "active": active_copy,
            "capabilities": caps_copy,
        }
        self._history.append(snap)
        return snap

    def restore_snapshot(self, snapshot_data: Dict[str, Any]) -> None:
        """Restore active bindings and manifests from snapshot."""
        if "active" in snapshot_data:
            self._active = dict(snapshot_data["active"])
        logger.info("[Registry] Restored registry snapshot.")
