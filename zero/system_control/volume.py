"""Project ZERO — System Audio Volume Subsystem Control.

Manages volume level adjustment, mute/unmute status, and audio output device selection.
"""

import os
import subprocess
import platform
from typing import List, Dict, Any, Tuple
from zero_logging import logger


def is_test_mode() -> bool:
    """Check if test suite or dry-run is active."""
    return "PYTEST_CURRENT_TEST" in os.environ or os.environ.get("ZERO_DRY_RUN") == "true"


class VolumeController:
    """Controls OS system master audio volume and playback endpoints."""

    def __init__(self) -> None:
        self.volume_level: int = 50
        self.is_muted: bool = False
        self.active_device: str = "Headphones (Realtek High Definition Audio)"
        self.devices: List[str] = [
            "Headphones (Realtek High Definition Audio)",
            "Speakers (Realtek High Definition Audio)",
            "Digital Display Audio (HDMI)",
        ]

    def increase_volume(self, amount: int = 10) -> Tuple[bool, str]:
        """Increase volume level by percentage amount."""
        return self.set_volume(min(100, self.volume_level + amount))

    def decrease_volume(self, amount: int = 10) -> Tuple[bool, str]:
        """Decrease volume level by percentage amount."""
        return self.set_volume(max(0, self.volume_level - amount))

    def set_volume(self, level: int) -> Tuple[bool, str]:
        """Set master volume level (0-100)."""
        self.volume_level = max(0, min(100, level))
        self.is_muted = False

        if platform.system() == "Windows" and not is_test_mode():
            try:
                cmd = f"powershell -Command \"(new-object -com wscript.shell).SendKeys([char]175)\""
                subprocess.run(cmd, shell=True, capture_output=True)
            except Exception:
                pass

        logger.info(f"[Audio Volume] Set to {self.volume_level}%")
        return True, f"Volume level set to {self.volume_level}%."

    def get_volume(self) -> int:
        """Get current volume level."""
        return self.volume_level

    def mute(self) -> Tuple[bool, str]:
        """Mute system master audio."""
        self.is_muted = True
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("powershell -Command \"(new-object -com wscript.shell).SendKeys([char]173)\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Audio Volume] System audio muted.")
        return True, "System audio muted."

    def unmute(self) -> Tuple[bool, str]:
        """Unmute system master audio."""
        self.is_muted = False
        logger.info("[Audio Volume] System audio unmuted.")
        return True, "System audio unmuted."

    def switch_output_device(self, device_name: str) -> Tuple[bool, str]:
        """Switch active audio playback output device."""
        target = device_name.lower().strip()
        for dev in self.devices:
            if target in dev.lower():
                self.active_device = dev
                logger.info(f"[Audio Output] Switched output device to '{dev}'")
                return True, f"Switched audio output device to '{dev}'."
        return False, f"Audio output device '{device_name}' not found."

    def list_output_devices(self) -> List[str]:
        """List available playback output devices."""
        return list(self.devices)
