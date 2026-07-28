"""Project ZERO — Plugin Loader.

Discovers, parses, and loads external capability plugins from manifests and directories.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from zero_logging import logger
from zero.capability.registry import CapabilityRegistry, CapabilityCategory, CapabilityManifest
from zero.capability.runtime_loader import RuntimeLoader


class PluginLoader:
    """Discovers and installs plugin-packaged capabilities."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry

    def scan_plugins(self, directory: str) -> List[CapabilityManifest]:
        """Scan directory for plugin manifests and load them into registry."""
        dir_path = Path(directory).resolve()
        if not dir_path.exists() or not dir_path.is_dir():
            logger.warning(f"[PluginLoader] Directory does not exist: {directory}")
            return []

        loaded_manifests: List[CapabilityManifest] = []
        for child in dir_path.iterdir():
            if child.is_dir():
                manifest_file = child / "plugin.json"
                if not manifest_file.exists():
                    manifest_file = child / "manifest.json"

                if manifest_file.exists():
                    try:
                        manifest = self.load_plugin_from_file(str(manifest_file), base_dir=str(child))
                        if manifest:
                            loaded_manifests.append(manifest)
                    except Exception as e:
                        logger.error(f"[PluginLoader] Failed to load plugin at {child}: {e}")

        return loaded_manifests

    def load_plugin_from_file(self, manifest_file: str, base_dir: Optional[str] = None) -> Optional[CapabilityManifest]:
        """Load single plugin manifest file."""
        path = Path(manifest_file).resolve()
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)

        return self.load_plugin_from_dict(data, base_dir=base_dir or str(path.parent))

    def load_plugin_from_dict(self, data: Dict[str, Any], base_dir: Optional[str] = None) -> CapabilityManifest:
        """Instantiate capability manifest and load code instance from plugin dictionary."""
        name = data.get("name", "unnamed_plugin")
        cat_str = data.get("category", "tool")
        category = CapabilityCategory.from_str(cat_str)
        version = data.get("version", "1.0.0")
        description = data.get("description", "")
        dependencies = data.get("dependencies", [])
        configuration = data.get("configuration", {})
        entry_point = data.get("entry_point", "")
        supported_commands = data.get("supported_commands", [])

        instance = None
        if entry_point and base_dir:
            if ":" in entry_point:
                rel_path, class_name = entry_point.split(":", 1)
                full_path = Path(base_dir) / rel_path
                if full_path.exists():
                    module = RuntimeLoader.load_module_from_file(str(full_path))
                    cls = RuntimeLoader.load_class_from_module(module, class_name)
                    instance = cls()
            else:
                try:
                    cls = RuntimeLoader.load_class(entry_point)
                    instance = cls()
                except Exception as e:
                    logger.warning(f"[PluginLoader] Could not instantiate entry point '{entry_point}': {e}")

        manifest = CapabilityManifest(
            name=name,
            category=category,
            version=version,
            description=description,
            dependencies=dependencies,
            configuration=configuration,
            entry_point=entry_point,
            supported_commands=supported_commands,
            health_status="healthy" if instance is not None else "degraded",
            instance=instance,
        )

        self.registry.register(manifest, instance=instance)
        logger.info(f"[PluginLoader] Installed plugin capability '{category.value}:{name}' v{version}")
        return manifest
