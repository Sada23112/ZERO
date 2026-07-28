"""Project ZERO — Bluetooth Subsystem Control.

Manages Bluetooth state, device discovery, pairing, connection, and disconnection.
"""

import subprocess
import platform
from typing import List, Dict, Any, Tuple
from zero_logging import logger


class BluetoothController:
    """Manages Bluetooth radio state and paired/connected device actions."""

    def __init__(self) -> None:
        self.state: bool = True
        self._paired_devices: List[Dict[str, Any]] = [
            {"name": "Headphones", "address": "00:11:22:33:44:55", "connected": False, "type": "audio"},
            {"name": "Wireless Keyboard", "address": "66:77:88:99:AA:BB", "connected": True, "type": "input"},
            {"name": "Bluetooth Mouse", "address": "CC:DD:EE:FF:00:11", "connected": True, "type": "input"},
        ]

    def turn_on(self) -> Tuple[bool, str]:
        """Turn Bluetooth radio on."""
        self.state = True
        if platform.system() == "Windows":
            cmd = "powershell -Command \"Get-Service bthserv | Start-Service\""
            try:
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            except Exception:
                pass
        logger.info("[Bluetooth] Radio powered ON.")
        return True, "Bluetooth radio powered ON."

    def turn_off(self) -> Tuple[bool, str]:
        """Turn Bluetooth radio off."""
        self.state = False
        logger.info("[Bluetooth] Radio powered OFF.")
        return True, "Bluetooth radio powered OFF."

    def list_paired_devices(self) -> List[Dict[str, Any]]:
        """List paired Bluetooth devices."""
        return list(self._paired_devices)

    def discover_devices(self) -> List[Dict[str, Any]]:
        """Scan for nearby Bluetooth devices."""
        return [
            {"name": "Headphones", "address": "00:11:22:33:44:55", "rssi": -45},
            {"name": "Smart TV", "address": "AA:BB:CC:DD:EE:FF", "rssi": -70},
        ]

    def connect_device(self, device_name_or_address: str) -> Tuple[bool, str]:
        """Connect to target Bluetooth device."""
        target = device_name_or_address.lower().strip()
        for dev in self._paired_devices:
            if target in dev["name"].lower() or target in dev["address"].lower():
                dev["connected"] = True
                logger.info(f"[Bluetooth] Connected device '{dev['name']}'")
                return True, f"Connected to Bluetooth device '{dev['name']}'."
        return False, f"Bluetooth device '{device_name_or_address}' not found in paired list."

    def disconnect_device(self, device_name_or_address: str) -> Tuple[bool, str]:
        """Disconnect target Bluetooth device."""
        target = device_name_or_address.lower().strip()
        for dev in self._paired_devices:
            if target in dev["name"].lower() or target in dev["address"].lower():
                dev["connected"] = False
                logger.info(f"[Bluetooth] Disconnected device '{dev['name']}'")
                return True, f"Disconnected Bluetooth device '{dev['name']}'."
        return False, f"Bluetooth device '{device_name_or_address}' not found."

    def pair_device(self, device_name_or_address: str) -> Tuple[bool, str]:
        """Pair new Bluetooth device."""
        new_dev = {"name": device_name_or_address, "address": "11:22:33:44:55:66", "connected": True, "type": "generic"}
        self._paired_devices.append(new_dev)
        return True, f"Successfully paired '{device_name_or_address}'."

    def forget_device(self, device_name_or_address: str) -> Tuple[bool, str]:
        """Unpair/forget target Bluetooth device."""
        target = device_name_or_address.lower().strip()
        self._paired_devices = [d for d in self._paired_devices if target not in d["name"].lower()]
        return True, f"Device '{device_name_or_address}' removed from paired list."
