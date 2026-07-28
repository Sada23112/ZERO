"""Project ZERO — Security & Permission Guard (Phase 7)."""

from pathlib import Path
from typing import Optional


class PermissionManager:
    """Guards against unauthorized destructive actions (deletion, overwriting)."""

    DESTRUCTIVE_ACTIONS = ["delete", "remove", "overwrite", "truncate", "format"]

    @classmethod
    def is_destructive_action(cls, action_description: str) -> bool:
        """Check if an action is potentially destructive."""
        desc = action_description.lower().strip()
        return any(word in desc for word in cls.DESTRUCTIVE_ACTIONS)

    @classmethod
    def require_confirmation(cls, action_description: str, target_path: Optional[Path] = None) -> str:
        """Return confirmation prompt message."""
        target_str = f" for '{target_path}'" if target_path else ""
        return f"[CONFIRMATION REQUIRED]: Action '{action_description}'{target_str} is destructive. Type 'yes' or 'confirm' to execute."
