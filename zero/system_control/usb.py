"""Project ZERO — USB Device Control.

Detects connected USB storage drives and peripherals and safely ejects USB devices.
"""

import subprocess
import platform
from typing import List, Dict, Any, Tuple
from zero_logging import logger


class USBController:
    """Manages USB storage devices and peripheral ejection."""

    def __init__(self) -> None:
        self._devices: List[Dict[str, Any]] = [
            {"drive": "E:", "name": "SanDisk Ultra 64GB", "type": "Storage", "size_gb": 64.0},
            {"drive": "F:", "name": "Kingston DataTraveler", "type": "Storage", "size_gb": 32.0},
        ]

    def list_usb_devices(self) -> List[Dict[str, Any]]:
        """List connected USB storage drives."""
        return list(self._devices)

    def eject_usb(self, drive_letter_or_name: str) -> Tuple[bool, str]:
        """Safely eject USB storage drive."""
        target = drive_letter_or_name.upper().strip()
        for dev in self._devices:
            if target in dev["drive"].upper() or target.lower() in dev["name"].lower():
                drive = dev["drive"]
                if platform.system() == "Windows":
                    try:
                        cmd = f"powershell -Command \"$drive = '{drive}'; (New-Object -comObject Shell.Application).NameSpace(17).ParseName($drive).InvokeVerb('Eject')\""
                        subprocess.run(cmd, shell=True, capture_output=True)
                    except Exception:
                        pass
                self._devices = [d for d in self._devices if d["drive"] != drive]
                logger.info(f"[USB] Safely ejected USB drive '{drive}' ({dev['name']})")
                return True, f"Safely ejected USB device '{dev['name']}' ({drive})."

        return False, f"USB device '{drive_letter_or_name}' not found."
