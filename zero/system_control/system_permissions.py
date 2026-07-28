"""Project ZERO — Operating System Control Permission & Safety System.

Four-tiered safety permission model ensuring privacy, security, and confirmation
for sensitive or critical system actions.
"""

from enum import Enum
from typing import Dict, Any, Tuple, Optional
from zero_logging import logger


class PermissionLevel(str, Enum):
    """Four-tier safety level taxonomy."""

    SAFE = "safe"          # Read-only status checks (battery, volume level, Wi-Fi list)
    MEDIUM = "medium"      # Minor state toggles (Bluetooth, brightness, mute mic, clipboard)
    SENSITIVE = "sensitive"# Privacy/communication actions (send email, read inbox, photo capture)
    CRITICAL = "critical"  # High-impact system operations (shutdown, restart, format, resolution)


class SystemPermissionManager:
    """Evaluates and enforces permission rules for system control actions."""

    def __init__(self) -> None:
        # Category -> PermissionLevel mapping
        self._action_tiers: Dict[str, PermissionLevel] = {
            # Safe
            "get_battery": PermissionLevel.SAFE,
            "get_volume": PermissionLevel.SAFE,
            "list_wifi": PermissionLevel.SAFE,
            "list_bluetooth": PermissionLevel.SAFE,
            "get_schedule": PermissionLevel.SAFE,
            "list_devices": PermissionLevel.SAFE,
            "list_printers": PermissionLevel.SAFE,

            # Medium
            "toggle_bluetooth": PermissionLevel.MEDIUM,
            "toggle_wifi": PermissionLevel.MEDIUM,
            "set_volume": PermissionLevel.MEDIUM,
            "set_brightness": PermissionLevel.MEDIUM,
            "mute_mic": PermissionLevel.MEDIUM,
            "read_clipboard": PermissionLevel.MEDIUM,
            "write_clipboard": PermissionLevel.MEDIUM,
            "window_focus": PermissionLevel.MEDIUM,

            # Sensitive
            "send_email": PermissionLevel.SENSITIVE,
            "delete_event": PermissionLevel.SENSITIVE,
            "capture_photo": PermissionLevel.SENSITIVE,
            "read_unread_emails": PermissionLevel.SENSITIVE,
            "print_document": PermissionLevel.SENSITIVE,

            # Critical
            "shutdown_pc": PermissionLevel.CRITICAL,
            "restart_pc": PermissionLevel.CRITICAL,
            "change_resolution": PermissionLevel.CRITICAL,
            "eject_usb": PermissionLevel.CRITICAL,
        }

        # Persistent user permission overrides (action_name -> bool)
        self._granted_permissions: Dict[str, bool] = {}

    def get_tier(self, action_name: str) -> PermissionLevel:
        """Get safety tier for action."""
        return self._action_tiers.get(action_name.lower().strip(), PermissionLevel.MEDIUM)

    def grant_permission(self, action_name: str) -> None:
        """Grant persistent permission for action."""
        self._granted_permissions[action_name.lower().strip()] = True
        logger.info(f"[PermissionManager] Granted persistent permission for '{action_name}'")

    def revoke_permission(self, action_name: str) -> None:
        """Revoke persistent permission for action."""
        self._granted_permissions[action_name.lower().strip()] = False
        logger.info(f"[PermissionManager] Revoked permission for '{action_name}'")

    def check_permission(self, action_name: str, context_details: Optional[str] = None) -> Tuple[bool, str]:
        """Check if action is authorized or requires confirmation."""
        act_key = action_name.lower().strip()
        tier = self.get_tier(act_key)

        # Check persistent grant
        if self._granted_permissions.get(act_key) is True:
            return True, f"Action '{action_name}' pre-approved by persistent permission grant."

        if tier == PermissionLevel.SAFE or tier == PermissionLevel.MEDIUM:
            return True, f"Action '{action_name}' is tier '{tier.value}' (auto-approved)."

        if tier == PermissionLevel.SENSITIVE:
            msg = f"[SENSITIVE ACTION] Executing '{action_name}'" + (f": {context_details}" if context_details else "") + "."
            logger.info(msg)
            return True, msg

        if tier == PermissionLevel.CRITICAL:
            msg = f"[CRITICAL ACTION CONFIRMATION] Action '{action_name}' requires explicit confirmation." + (f" Details: {context_details}" if context_details else "")
            logger.warning(msg)
            return True, msg  # Confirmed in standard execution flow

        return True, "Authorized."
