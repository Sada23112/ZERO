"""Project ZERO — System Power Subsystem Control.

Manages workstation lock, sleep, hibernate, restart, shutdown, and user logout.
"""

import os
import subprocess
import platform
from typing import Tuple
from zero_logging import logger


def is_test_mode() -> bool:
    """Check if test suite or dry-run is active."""
    return "PYTEST_CURRENT_TEST" in os.environ or os.environ.get("ZERO_DRY_RUN") == "true"


class PowerController:
    """Manages system power states and security locking."""

    def lock_pc(self) -> Tuple[bool, str]:
        """Lock workstation screen instantly."""
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Power] Workstation locked.")
        return True, "Workstation screen locked."

    def sleep(self) -> Tuple[bool, str]:
        """Put computer into sleep state."""
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("powershell -Command \"Add-Type -Assembly System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Power] Initiating sleep mode.")
        return True, "System entering sleep mode."

    def hibernate(self) -> Tuple[bool, str]:
        """Put computer into hibernate state."""
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("shutdown /h", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Power] Initiating hibernate mode.")
        return True, "System entering hibernate mode."

    def restart(self, confirm: bool = True) -> Tuple[bool, str]:
        """Restart computer."""
        if not confirm:
            return False, "Restart requires explicit confirmation."
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("shutdown /r /t 10 /c \"Restart requested by Project ZERO\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.warning("[Power] Initiating system restart.")
        return True, "System restart scheduled in 10 seconds."

    def shutdown(self, confirm: bool = True) -> Tuple[bool, str]:
        """Shutdown computer."""
        if not confirm:
            return False, "Shutdown requires explicit confirmation."
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("shutdown /s /t 10 /c \"Shutdown requested by Project ZERO\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.warning("[Power] Initiating system shutdown.")
        return True, "System shutdown scheduled in 10 seconds."

    def logout(self, confirm: bool = True) -> Tuple[bool, str]:
        """Logout current user session."""
        if not confirm:
            return False, "Logout requires explicit confirmation."
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("shutdown /l", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Power] User session logoff initiated.")
        return True, "User session logoff initiated."
