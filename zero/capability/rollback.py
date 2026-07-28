"""Project ZERO — Capability Rollback System.

Reverts capability upgrades, provider switches, planner replacements, or configuration changes
to previous stable state snapshots.
"""

from typing import Tuple, Optional, Dict, Any, List
from zero_logging import logger
from zero.capability.registry import CapabilityRegistry, CapabilityCategory


class CapabilityRollbackEngine:
    """Manages snapshot history and atomic rollback of ZERO capabilities."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry
        # Stack of active binding snapshots for history
        self._history_stack: List[Dict[str, Any]] = []

    def save_checkpoint(self, label: str = "checkpoint") -> Dict[str, Any]:
        """Save a snapshot of current active capabilities and registry state."""
        snap = self.registry.snapshot()
        snap["label"] = label
        self._history_stack.append(snap)
        logger.info(f"[Rollback] Created checkpoint '{label}'. History size: {len(self._history_stack)}")
        return snap

    def rollback_last_upgrade(self) -> Tuple[bool, str]:
        """Rollback last capability upgrade or switch."""
        if not self._history_stack:
            return False, "No rollback checkpoints available in history."

        last_snap = self._history_stack.pop()
        self.registry.restore_snapshot(last_snap)
        label = last_snap.get("label", "previous checkpoint")
        logger.info(f"[Rollback] Rolled back to checkpoint '{label}'.")
        return True, f"Successfully rolled back to '{label}'."

    def rollback_provider(self) -> Tuple[bool, str]:
        """Revert active provider to gemini or previous provider."""
        self.registry.set_active(CapabilityCategory.PROVIDER, "gemini")
        return True, "Provider rolled back to default (gemini)."

    def rollback_capability(self, category: str, target_name: Optional[str] = None) -> Tuple[bool, str]:
        """Rollback target category or specific capability."""
        cat_key = category.lower().strip()
        manifests = self.registry.list_capabilities(cat_key)
        if not manifests:
            return False, f"No capabilities registered under category '{category}'."

        if target_name:
            if self.registry.set_active(cat_key, target_name):
                return True, f"Capability '{category}:{target_name}' restored as active."

        # Fallback switch to first available manifest
        first_name = manifests[0].name
        self.registry.set_active(cat_key, first_name)
        return True, f"Capability '{category}' rolled back to '{first_name}'."
