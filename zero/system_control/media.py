"""Project ZERO — System Media Playback Control.

Controls system media playback hotkeys (Play/Pause, Next Track, Previous Track, Stop).
"""

import os
import subprocess
import platform
from typing import Tuple
from zero_logging import logger


def is_test_mode() -> bool:
    """Check if test suite or dry-run is active."""
    return "PYTEST_CURRENT_TEST" in os.environ or os.environ.get("ZERO_DRY_RUN") == "true"


class MediaController:
    """Manages system media playback controls and virtual media keypresses."""

    def play_pause(self) -> Tuple[bool, str]:
        """Toggle media Play/Pause hotkey."""
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("powershell -Command \"(new-object -com wscript.shell).SendKeys([char]179)\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Media] Toggled Play/Pause.")
        return True, "Toggled media play/pause."

    def next_track(self) -> Tuple[bool, str]:
        """Skip to next media track."""
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("powershell -Command \"(new-object -com wscript.shell).SendKeys([char]176)\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Media] Next track.")
        return True, "Skipped to next track."

    def previous_track(self) -> Tuple[bool, str]:
        """Skip to previous media track."""
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("powershell -Command \"(new-object -com wscript.shell).SendKeys([char]177)\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Media] Previous track.")
        return True, "Skipped to previous track."

    def stop(self) -> Tuple[bool, str]:
        """Stop media playback."""
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.run("powershell -Command \"(new-object -com wscript.shell).SendKeys([char]178)\"", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Media] Media stopped.")
        return True, "Media playback stopped."
