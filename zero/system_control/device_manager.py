"""Project ZERO — Central Device Inventory Manager.

Discovers and inventories all attached system devices (USB, Bluetooth, Displays, Audio, Printers, Storage).
"""

from typing import Dict, List, Any
from zero_logging import logger
from zero.system_control.bluetooth import BluetoothController
from zero.system_control.usb import USBController
from zero.system_control.display import DisplayController
from zero.system_control.volume import VolumeController
from zero.system_control.microphone import MicrophoneController
from zero.system_control.printer import PrinterController


class DeviceManager:
    """Central device discovery and hardware status reporter."""

    def __init__(self) -> None:
        self.bluetooth = BluetoothController()
        self.usb = USBController()
        self.display = DisplayController()
        self.audio_out = VolumeController()
        self.audio_in = MicrophoneController()
        self.printer = PrinterController()

    def detect_all_devices(self) -> Dict[str, List[Dict[str, Any]]]:
        """Detect and aggregate all system devices across subsystems."""
        return {
            "bluetooth": self.bluetooth.list_paired_devices(),
            "usb_storage": self.usb.list_usb_devices(),
            "monitors": self.display.detect_monitors(),
            "audio_outputs": [{"name": dev, "active": (dev == self.audio_out.active_device)} for dev in self.audio_out.list_output_devices()],
            "audio_inputs": [{"name": dev, "active": (dev == self.audio_in.active_input)} for dev in self.audio_in.list_input_devices()],
            "printers": self.printer.list_printers(),
        }

    def get_device_summary(self) -> str:
        """Return human-readable summary of attached devices."""
        all_devs = self.detect_all_devices()
        lines = [
            "=== Connected System Devices Summary ===",
            f"• Bluetooth Devices ({len(all_devs['bluetooth'])} paired)",
            f"• USB Storage ({len(all_devs['usb_storage'])} attached)",
            f"• Monitors ({len(all_devs['monitors'])} detected)",
            f"• Audio Output ({self.audio_out.active_device})",
            f"• Audio Input ({self.audio_in.active_input})",
            f"• Printers ({len(all_devs['printers'])} available)",
        ]
        return "\n".join(lines)
