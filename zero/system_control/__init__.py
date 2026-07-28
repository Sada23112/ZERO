"""Project ZERO — Operating System Control & Device Integration Package.

Provides hardware, audio, network, Bluetooth, power, displays, email, calendar, application management,
device inventory, and permission enforcement.
"""

from zero.system_control.system_permissions import SystemPermissionManager, PermissionLevel
from zero.system_control.bluetooth import BluetoothController
from zero.system_control.wifi import WiFiManager
from zero.system_control.network import NetworkManager
from zero.system_control.email import EmailManager
from zero.system_control.calendar import CalendarManager
from zero.system_control.contacts import ContactsManager
from zero.system_control.notifications import NotificationsManager
from zero.system_control.volume import VolumeController
from zero.system_control.brightness import BrightnessController
from zero.system_control.power import PowerController
from zero.system_control.camera import CameraController
from zero.system_control.microphone import MicrophoneController
from zero.system_control.printer import PrinterController
from zero.system_control.usb import USBController
from zero.system_control.display import DisplayController
from zero.system_control.media import MediaController
from zero.system_control.clipboard_sync import ClipboardController
from zero.system_control.window_manager import WindowManager
from zero.system_control.device_manager import DeviceManager
from zero.system_control.system_control_manager import SystemControlManager, system_control_manager

__all__ = [
    "SystemPermissionManager",
    "PermissionLevel",
    "BluetoothController",
    "WiFiManager",
    "NetworkManager",
    "EmailManager",
    "CalendarManager",
    "ContactsManager",
    "NotificationsManager",
    "VolumeController",
    "BrightnessController",
    "PowerController",
    "CameraController",
    "MicrophoneController",
    "PrinterController",
    "USBController",
    "DisplayController",
    "MediaController",
    "ClipboardController",
    "WindowManager",
    "DeviceManager",
    "SystemControlManager",
    "system_control_manager",
]
