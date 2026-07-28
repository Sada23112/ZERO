"""Project ZERO — Capability Installer (Phase 5)."""

import sys
import shutil
import importlib
from pathlib import Path
from typing import Dict, Any, Optional
from tools.base import BaseTool
from tools.registry import tool_registry
import tools.dynamic
from evolution.registry import CapabilityRegistryStore
from evolution.metadata import CapabilityMetadata
from zero_logging import logger


class CapabilityInstaller:
    """Installs validated capability files from sandbox into project workspace and registers tool."""

    def __init__(self, workspace_root: Optional[Path] = None, registry_store: Optional[CapabilityRegistryStore] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.dynamic_tools_dir = self.workspace_root / "tools" / "dynamic"
        self.dynamic_tools_dir.mkdir(parents=True, exist_ok=True)
        self.registry_store = registry_store or CapabilityRegistryStore()

    def install_capability(
        self,
        capability_name: str,
        class_name: str,
        code_content: str,
        dependencies: Optional[list] = None,
        reason: str = "User Request"
    ) -> Optional[CapabilityMetadata]:
        """Move validated capability code into tools/dynamic/ and register tool."""
        try:
            filename = f"{capability_name}.py"
            target_file = self.dynamic_tools_dir / filename
            target_file.write_text(code_content, encoding="utf-8")

            # Ensure workspace dynamic tools path is in tools.dynamic.__path__
            dir_str = str(self.dynamic_tools_dir)
            if hasattr(tools.dynamic, "__path__") and dir_str not in tools.dynamic.__path__:
                tools.dynamic.__path__.append(dir_str)

            # Dynamically import and instantiate tool class
            module_path = f"tools.dynamic.{capability_name}"
            mod = importlib.import_module(module_path)
            importlib.reload(mod)

            tool_cls = getattr(mod, class_name)
            tool_instance: BaseTool = tool_cls(workspace_root=self.workspace_root)

            # Register in ToolRegistry
            tool_registry.register_tool(tool_instance)

            # Record in CapabilityRegistryStore
            meta = CapabilityMetadata(
                name=capability_name,
                description=tool_instance.description,
                reason_created=reason,
                dependencies=dependencies or [],
                files_created=[str(target_file.relative_to(self.workspace_root))]
            )
            self.registry_store.register_capability(meta)

            logger.info(f"Successfully installed and registered dynamic capability '{capability_name}'")
            return meta

        except Exception as err:
            logger.error(f"Failed installing capability '{capability_name}': {err}")
            return None
