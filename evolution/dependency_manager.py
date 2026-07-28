"""Project ZERO — Dynamic Dependency Manager (Phase 5)."""

import sys
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from zero_logging import logger


class DependencyManager:
    """Safely checks, resolves, and installs Python package dependencies automatically."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def check_package_installed(self, package_name: str) -> bool:
        """Check if a Python package is installed in current environment."""
        try:
            import importlib.util
            spec = importlib.util.find_spec(package_name)
            return spec is not None
        except Exception:
            return False

    async def install_package(self, package_name: str) -> bool:
        """Safely install a missing python package via subprocess pip."""
        if self.check_package_installed(package_name):
            logger.info(f"Package '{package_name}' already installed.")
            return True

        logger.info(f"Installing package '{package_name}' automatically...")
        try:
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "pip",
                "install",
                package_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            exit_code = process.returncode or 0

            if exit_code == 0:
                logger.info(f"Successfully installed package '{package_name}'.")
                self._append_to_requirements(package_name)
                return True
            else:
                logger.error(f"Failed installing package '{package_name}': {stderr.decode('utf-8')}")
                return False

        except Exception as err:
            logger.error(f"Error during package installation of '{package_name}': {err}")
            return False

    def _append_to_requirements(self, package_name: str):
        """Append newly installed dependency to project requirements.txt."""
        req_file = self.workspace_root / "requirements.txt"
        if req_file.exists():
            try:
                content = req_file.read_text(encoding="utf-8")
                if package_name not in content:
                    with open(req_file, "a", encoding="utf-8") as f:
                        f.write(f"\n{package_name}\n")
            except Exception:
                pass
