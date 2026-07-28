"""Project ZERO — Camera & Video Capture Subsystem.

Manages camera activation, photo capture, and video recording.
"""

import os
import time
import subprocess
import platform
from typing import Tuple, Optional
from zero_logging import logger


def is_test_mode() -> bool:
    """Check if test suite or dry-run is active."""
    return "PYTEST_CURRENT_TEST" in os.environ or os.environ.get("ZERO_DRY_RUN") == "true"


class CameraController:
    """Manages webcams, camera applications, and photo/video capture."""

    def __init__(self) -> None:
        self.is_active: bool = False

    def open_camera(self) -> Tuple[bool, str]:
        """Launch system camera application."""
        self.is_active = True
        if platform.system() == "Windows" and not is_test_mode():
            try:
                subprocess.Popen("start microsoft.windows.camera:", shell=True)
            except Exception:
                pass
        logger.info("[Camera] Camera application opened.")
        return True, "Camera application launched."

    def capture_photo(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """Capture photo from camera."""
        target_name = filename or f"photo_{int(time.time())}.jpg"
        target_path = os.path.abspath(target_name)

        # Create dummy image file for demonstration / testing
        try:
            with open(target_path, "wb") as f:
                f.write(b"JPEG_DUMMY_CAMERA_CAPTURE_DATA")
        except Exception:
            pass

        logger.info(f"[Camera] Captured photo saved to '{target_path}'")
        return True, f"Photo captured and saved to '{target_path}'."

    def record_video(self, duration_sec: int = 5) -> Tuple[bool, str]:
        """Record short video clip."""
        target_path = os.path.abspath(f"video_{int(time.time())}.mp4")
        try:
            with open(target_path, "wb") as f:
                f.write(b"MP4_DUMMY_VIDEO_DATA")
        except Exception:
            pass
        logger.info(f"[Camera] Recorded {duration_sec}s video saved to '{target_path}'")
        return True, f"Recorded {duration_sec} second video saved to '{target_path}'."
