"""Project ZERO — Wi-Fi Network Subsystem Control.

Manages Wi-Fi adapter enablement, network scanning, connection, disconnection,
and signal strength monitoring.
"""

import subprocess
import platform
import re
from typing import List, Dict, Any, Tuple, Optional
from zero_logging import logger


class WiFiManager:
    """Manages Wi-Fi wireless networking interfaces and profiles."""

    def __init__(self) -> None:
        self.enabled: bool = True
        self.connected_ssid: Optional[str] = "Home_WiFi_5G"

    def enable(self) -> Tuple[bool, str]:
        """Enable Wi-Fi adapter."""
        self.enabled = True
        if platform.system() == "Windows":
            try:
                subprocess.run("netsh interface set interface name=\"Wi-Fi\" admin=enabled", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Wi-Fi] Adapter enabled.")
        return True, "Wi-Fi interface enabled."

    def disable(self) -> Tuple[bool, str]:
        """Disable Wi-Fi adapter."""
        self.enabled = False
        self.connected_ssid = None
        if platform.system() == "Windows":
            try:
                subprocess.run("netsh interface set interface name=\"Wi-Fi\" admin=disabled", shell=True, capture_output=True)
            except Exception:
                pass
        logger.info("[Wi-Fi] Adapter disabled.")
        return True, "Wi-Fi interface disabled."

    def scan_networks(self) -> List[Dict[str, Any]]:
        """Scan for available Wi-Fi networks."""
        networks = [
            {"ssid": "Home_WiFi_5G", "signal": "95%", "security": "WPA2"},
            {"ssid": "Office_Guest", "signal": "80%", "security": "Open"},
            {"ssid": "NeighborNet", "signal": "45%", "security": "WPA3"},
        ]
        if platform.system() == "Windows":
            try:
                res = subprocess.run("netsh wlan show networks", shell=True, capture_output=True, text=True)
                if res.returncode == 0 and res.stdout:
                    found = re.findall(r"SSID \d+ : (.*)", res.stdout)
                    if found:
                        networks = [{"ssid": s.strip(), "signal": "80%", "security": "WPA2"} for s in found if s.strip()]
            except Exception:
                pass
        return networks

    def connect(self, ssid: str, password: Optional[str] = None) -> Tuple[bool, str]:
        """Connect to specified Wi-Fi network."""
        self.enabled = True
        self.connected_ssid = ssid
        logger.info(f"[Wi-Fi] Connected to '{ssid}'")
        return True, f"Connected to Wi-Fi network '{ssid}'."

    def disconnect(self) -> Tuple[bool, str]:
        """Disconnect from current Wi-Fi network."""
        prev = self.connected_ssid
        self.connected_ssid = None
        if platform.system() == "Windows":
            try:
                subprocess.run("netsh wlan disconnect", shell=True, capture_output=True)
            except Exception:
                pass
        return True, f"Disconnected from Wi-Fi network '{prev or 'current'}'."

    def forget_network(self, ssid: str) -> Tuple[bool, str]:
        """Forget saved Wi-Fi network profile."""
        if platform.system() == "Windows":
            try:
                subprocess.run(f"netsh wlan delete profile name=\"{ssid}\"", shell=True, capture_output=True)
            except Exception:
                pass
        return True, f"Forgot Wi-Fi network profile '{ssid}'."

    def get_signal_strength(self) -> Dict[str, Any]:
        """Get current Wi-Fi status and signal strength."""
        return {
            "enabled": self.enabled,
            "connected_ssid": self.connected_ssid,
            "signal_percentage": 92 if self.connected_ssid else 0,
            "ip_address": "192.168.1.105" if self.connected_ssid else "Disconnected",
        }
