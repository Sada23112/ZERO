"""Project ZERO — Isolated Execution Sandbox (Phase 5)."""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from zero_logging import logger


class ExecutionSandbox:
    """Isolated temporary workspace for validating and testing generated capabilities before installation."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = (base_dir or (Path.cwd() / "data" / "sandbox")).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.active_sandbox_path: Optional[Path] = None

    def create_sandbox(self, sandbox_name: str = "temp_evo") -> Path:
        """Create an isolated temporary workspace directory."""
        self.active_sandbox_path = Path(tempfile.mkdtemp(prefix=f"{sandbox_name}_", dir=str(self.base_dir)))
        logger.info(f"Created execution sandbox workspace: {self.active_sandbox_path}")
        return self.active_sandbox_path

    def write_sandbox_file(self, filename: str, content: str) -> Path:
        """Write generated code or test file into active sandbox workspace."""
        if not self.active_sandbox_path:
            self.create_sandbox()

        target_file = self.active_sandbox_path / filename
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")
        return target_file

    def cleanup(self):
        """Clean up and remove sandbox directory after validation or failure."""
        if self.active_sandbox_path and self.active_sandbox_path.exists():
            try:
                shutil.rmtree(self.active_sandbox_path)
                logger.info(f"Cleaned up sandbox workspace: {self.active_sandbox_path}")
            except Exception as err:
                logger.warning(f"Error cleaning up sandbox: {err}")
            finally:
                self.active_sandbox_path = None
