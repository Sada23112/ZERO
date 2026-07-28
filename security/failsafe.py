"""Project ZERO — Failsafe Security System (Phase 4 Capability #25).

Provides destructive action previews, user confirmation prompts, and safe rollbacks.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from pydantic import BaseModel, Field
from zero_logging import logger


class ActionPreview(BaseModel):
    """Structured preview of a pending file or system action."""

    action_type: str
    target_path: Optional[str] = None
    description: str
    is_destructive: bool = False
    affected_items: List[str] = Field(default_factory=list)
    backup_path: Optional[str] = None


class FailsafeSystem:
    """Failsafe system preventing unauthorized or accidental destructive actions."""

    def __init__(self, backup_dir: Optional[Path] = None, require_confirmation: bool = True):
        self.backup_dir = (backup_dir or (Path.cwd() / "data" / "backups")).resolve()
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.require_confirmation = require_confirmation

    def preview_action(self, action_type: str, description: str, target_path: Optional[str] = None, is_destructive: bool = False) -> ActionPreview:
        """Generate a preview summary for a pending action."""
        affected = [target_path] if target_path else []
        return ActionPreview(
            action_type=action_type,
            target_path=target_path,
            description=description,
            is_destructive=is_destructive,
            affected_items=affected
        )

    def create_safety_backup(self, target_path: Path) -> Optional[Path]:
        """Create a safety backup copy before modifying or deleting a target file/folder."""
        if not target_path.exists():
            return None

        try:
            timestamp_str = str(int(Path(target_path).stat().st_mtime))
            safe_name = f"{target_path.name}_{timestamp_str}.bak"
            backup_file = self.backup_dir / safe_name

            if target_path.is_file():
                shutil.copy2(target_path, backup_file)
            elif target_path.is_dir():
                shutil.copytree(target_path, backup_file, dirs_exist_ok=True)

            logger.info(f"Failsafe backup created: {backup_file}")
            return backup_file
        except Exception as err:
            logger.warning(f"Failed to create failsafe backup for {target_path}: {err}")
            return None

    def confirm_action(self, preview: ActionPreview, confirm_callback: Optional[Callable[[ActionPreview], bool]] = None) -> bool:
        """Prompt for confirmation if action is marked destructive."""
        if not preview.is_destructive or not self.require_confirmation:
            return True

        if confirm_callback:
            return confirm_callback(preview)

        return True
