"""Project ZERO — Reversible Evolution & Rollback Engine (Phase 5)."""

import os
from pathlib import Path
from typing import Optional, List
from evolution.registry import CapabilityRegistryStore
from tools.registry import tool_registry
from zero_logging import logger


class RollbackEngine:
    """Reverts evolutions, deactivates tools, and restores previous capability state."""

    def __init__(self, workspace_root: Optional[Path] = None, registry_store: Optional[CapabilityRegistryStore] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.registry_store = registry_store or CapabilityRegistryStore()

    def rollback_capability(self, capability_name: str) -> bool:
        """Rollback and deactivate a dynamically installed capability."""
        try:
            meta = self.registry_store.get_capability(capability_name)
            if not meta:
                logger.warning(f"Capability '{capability_name}' not found in registry.")
                return False

            # Deactivate in registry
            self.registry_store.deactivate_capability(capability_name)

            # Remove from ToolRegistry
            if capability_name in tool_registry.list_tools():
                del tool_registry._tools[capability_name]

            # Remove installed dynamic tool file if exists
            target_file = self.workspace_root / "tools" / "dynamic" / f"{capability_name}.py"
            if target_file.exists():
                try:
                    os.remove(target_file)
                except Exception:
                    pass

            logger.info(f"Successfully rolled back capability '{capability_name}'")
            return True

        except Exception as err:
            logger.error(f"Failed rolling back capability '{capability_name}': {err}")
            return False

    def rollback_last_evolution(self) -> bool:
        """Rollback the most recently installed dynamic capability."""
        caps = self.registry_store.list_capabilities()
        if not caps:
            logger.warning("No active evolutions to rollback.")
            return False

        last_cap = caps[-1]
        return self.rollback_capability(last_cap.name)
