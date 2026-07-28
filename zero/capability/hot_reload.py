"""Project ZERO — Hot Reload Engine.

Hot reloads python capabilities dynamically at runtime without process restarts.
"""

import sys
import importlib
from typing import Optional, Tuple, Dict, Any
from zero_logging import logger
from zero.capability.registry import CapabilityRegistry, CapabilityCategory, CapabilityManifest
from zero.capability.runtime_loader import RuntimeLoader


class HotReloader:
    """Manages zero-downtime hot reloading of capabilities."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry

    def reload_capability(
        self,
        category: str,
        name: str,
        file_path: Optional[str] = None,
        code: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Hot-reload a target capability in memory and re-bind active instance."""
        manifest = self.registry.get_manifest(category, name)
        if not manifest:
            return False, f"Capability '{category}:{name}' not found in registry."

        try:
            logger.info(f"[HotReload] Initiating hot-reload for capability '{category}:{name}'...")

            new_instance = None
            if code:
                module_name = f"dynamic_capability_{name.lower()}"
                module = RuntimeLoader.load_module_from_code(code, module_name)
                if manifest.entry_point and ":" in manifest.entry_point:
                    class_name = manifest.entry_point.split(":", 1)[1]
                    cls = RuntimeLoader.load_class_from_module(module, class_name)
                    new_instance = cls()
            elif file_path:
                module_name = f"dynamic_file_{name.lower()}"
                module = RuntimeLoader.load_module_from_file(file_path, module_name)
                if manifest.entry_point and ":" in manifest.entry_point:
                    class_name = manifest.entry_point.split(":", 1)[1]
                    cls = RuntimeLoader.load_class_from_module(module, class_name)
                    new_instance = cls()
            elif manifest.entry_point:
                # Reload existing module
                if ":" in manifest.entry_point:
                    mod_path, class_name = manifest.entry_point.split(":", 1)
                else:
                    mod_path, class_name = manifest.entry_point.rsplit(".", 1)

                if mod_path in sys.modules:
                    mod = sys.modules[mod_path]
                    importlib.reload(mod)
                    cls = getattr(mod, class_name)
                    new_instance = cls()
                else:
                    cls = RuntimeLoader.load_class(manifest.entry_point)
                    new_instance = cls()

            if new_instance is not None:
                manifest.instance = new_instance
                manifest.health_status = "healthy"
                logger.info(f"[HotReload] Successfully hot-reloaded capability '{category}:{name}'")
                return True, f"Capability '{category}:{name}' successfully hot-reloaded."
            else:
                # Re-touch health status
                manifest.health_status = "healthy"
                return True, f"Capability '{category}:{name}' refreshed."

        except Exception as e:
            error_msg = f"Failed to hot reload '{category}:{name}': {e}"
            logger.error(f"[HotReload] {error_msg}")
            manifest.health_status = "degraded"
            return False, error_msg

    def reload_all(self) -> Dict[str, bool]:
        """Hot reload all registered capabilities."""
        results = {}
        for manifest in self.registry.list_capabilities():
            success, msg = self.reload_capability(manifest.category.value, manifest.name)
            results[f"{manifest.category.value}:{manifest.name}"] = success
        return results
