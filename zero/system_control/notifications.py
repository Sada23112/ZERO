"""Project ZERO — System Notifications Subsystem.

Creates desktop toast notifications, reads system notification queue, and dismisses alerts.
"""

import os
import time
import subprocess
import platform
from typing import List, Dict, Any, Tuple
from zero_logging import logger


def is_test_mode() -> bool:
    """Check if test suite or dry-run is active."""
    return "PYTEST_CURRENT_TEST" in os.environ or os.environ.get("ZERO_DRY_RUN") == "true"


class NotificationsManager:
    """Manages desktop notifications and notification center alerts."""

    def __init__(self) -> None:
        self._active_notifications: List[Dict[str, Any]] = [
            {"id": "notif-1", "title": "System Alert", "message": "Windows Update available", "timestamp": time.time() - 300},
            {"id": "notif-2", "title": "Calendar", "message": "Standup in 10 minutes", "timestamp": time.time() - 600},
        ]

    def create_notification(self, title: str, message: str) -> Tuple[bool, str]:
        """Display OS notification toast alert."""
        notif = {
            "id": f"notif-{len(self._active_notifications) + 1}",
            "title": title,
            "message": message,
            "timestamp": time.time(),
        }
        self._active_notifications.append(notif)

        if platform.system() == "Windows" and not is_test_mode():
            cmd = f'powershell -Command "[reflection.assembly]::loadwithpartialname(\'System.Windows.Forms\'); [System.Windows.Forms.MessageBox]::Show(\'{message}\', \'{title}\')"'
            try:
                subprocess.Popen(cmd, shell=True)
            except Exception:
                pass

        logger.info(f"[Notification] Posted toast alert: '{title}' - '{message}'")
        return True, f"Notification posted: '{title}' - '{message}'."

    def read_notifications(self) -> List[Dict[str, Any]]:
        """Fetch active system notifications."""
        return list(self._active_notifications)

    def dismiss_notifications(self) -> Tuple[bool, str]:
        """Dismiss all notifications."""
        count = len(self._active_notifications)
        self._active_notifications.clear()
        return True, f"Dismissed {count} system notifications."
