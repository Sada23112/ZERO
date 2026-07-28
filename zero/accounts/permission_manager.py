"""Project ZERO — Connected Account Permission Manager.

Enforces granular permission levels for external service actions (Medium, Sensitive, Critical).
"""

from typing import Tuple, Optional, Dict
from zero_logging import logger
from zero.system_control.system_permissions import PermissionLevel


class AccountPermissionManager:
    """Evaluates permission requirements for connected account actions."""

    def __init__(self) -> None:
        self._action_levels: Dict[str, PermissionLevel] = {
            # Medium
            "read_calendar": PermissionLevel.MEDIUM,
            "create_event": PermissionLevel.MEDIUM,
            "browse_repos": PermissionLevel.MEDIUM,
            "read_slack": PermissionLevel.MEDIUM,
            "play_spotify": PermissionLevel.MEDIUM,

            # Sensitive
            "read_email": PermissionLevel.SENSITIVE,
            "send_email": PermissionLevel.SENSITIVE,
            "reply_email": PermissionLevel.SENSITIVE,
            "draft_email": PermissionLevel.SENSITIVE,
            "upload_drive": PermissionLevel.SENSITIVE,
            "create_issue": PermissionLevel.SENSITIVE,

            # Critical
            "delete_email": PermissionLevel.CRITICAL,
            "delete_drive_file": PermissionLevel.CRITICAL,
            "delete_repo": PermissionLevel.CRITICAL,
            "revoke_account": PermissionLevel.CRITICAL,
        }

    def get_level(self, action: str) -> PermissionLevel:
        """Get safety permission level for action."""
        return self._action_levels.get(action.lower().strip(), PermissionLevel.SENSITIVE)

    def check_permission(self, action: str, account_email: str, details: Optional[str] = None) -> Tuple[bool, str]:
        """Check if action is authorized or requires confirmation."""
        level = self.get_level(action)
        if level == PermissionLevel.CRITICAL:
            msg = f"[CRITICAL ACTION] Action '{action}' on account '{account_email}' requires explicit confirmation." + (f" Details: {details}" if details else "")
            logger.warning(msg)
            return True, msg
        elif level == PermissionLevel.SENSITIVE:
            msg = f"[SENSITIVE ACTION] Executing '{action}' on account '{account_email}'." + (f" Details: {details}" if details else "")
            logger.info(msg)
            return True, msg
        return True, "Authorized."
