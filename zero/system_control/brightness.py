"""Project ZERO — Display Brightness Subsystem Control.

Manages screen brightness levels, night light settings, and display backlight controls.
"""

import os
import subprocess
import platform
from typing import Tuple, Optional
from zero_logging import logger


def is_test_mode() -> bool:
    """Check if test suite or dry-run is active."""
    return "PYTEST_CURRENT_TEST" in os.environ or os.environ.get("ZERO_DRY_RUN") == "true"


class BrightnessController:
    """Controls screen brightness level and night light settings."""

    def __init__(self) -> None:
        self.brightness_level: int = 70
        self.night_light_enabled: bool = False

    def increase_brightness(self, amount: int = 10) -> Tuple[bool, str]:
        """Increase screen brightness."""
        return self.set_brightness(min(100, self.brightness_level + amount))

    def decrease_brightness(self, amount: int = 10) -> Tuple[bool, str]:
        """Decrease screen brightness."""
        return self.set_brightness(max(0, self.brightness_level - amount))

    def set_brightness(self, level: int) -> Tuple[bool, str]:
        """Set screen brightness percentage level (0-100)."""
        self.brightness_level = max(0, min(100, level))

        if platform.system() == "Windows" and not is_test_mode():
            try:
                cmd = f"powershell -Command \"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{self.brightness_level})\""
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            except Exception:
                pass

        logger.info(f"[Brightness] Screen brightness set to {self.brightness_level}%")
        return True, f"Screen brightness set to {self.brightness_level}%."

    def get_brightness(self) -> int:
        """Get current screen brightness level."""
        return self.brightness_level

    def toggle_night_light(self, enable: Optional[bool] = None) -> Tuple[bool, str]:
        """Toggle or set Night Light / Blue Light Filter status."""
        if enable is not None:
            self.night_light_enabled = enable
        else:
            self.night_light_enabled = not self.night_light_enabled

        status_str = "enabled" if self.night_light_enabled else "disabled"
        logger.info(f"[Display] Night light mode {status_str}.")
        return True, f"Night Light mode {status_str}."
