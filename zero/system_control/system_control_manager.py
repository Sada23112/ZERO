"""Project ZERO — Central Operating System Control Manager.

Orchestrates OS control subsystems, handles natural language system commands,
and enforces safety permissions.
"""

import re
from typing import Optional, Tuple, Dict, Any
from zero_logging import logger

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


class SystemControlManager:
    """Central manager delegating natural language OS control commands safely."""

    def __init__(self) -> None:
        self.permissions = SystemPermissionManager()
        self.bluetooth = BluetoothController()
        self.wifi = WiFiManager()
        self.network = NetworkManager()
        self.email = EmailManager()
        self.calendar = CalendarManager()
        self.contacts = ContactsManager()
        self.notifications = NotificationsManager()
        self.volume = VolumeController()
        self.brightness = BrightnessController()
        self.power = PowerController()
        self.camera = CameraController()
        self.microphone = MicrophoneController()
        self.printer = PrinterController()
        self.usb = USBController()
        self.display = DisplayController()
        self.media = MediaController()
        self.clipboard = ClipboardController()
        self.window_manager = WindowManager()
        self.device_manager = DeviceManager()

    def process_system_command(self, prompt: str) -> Optional[str]:
        """Parse and execute OS control commands safely."""
        clean_p = prompt.strip()
        cmd = clean_p.lower()

        # 1. Bluetooth Commands
        if "bluetooth" in cmd:
            if "on" in cmd or "enable" in cmd:
                auth, _ = self.permissions.check_permission("toggle_bluetooth")
                if auth:
                    _, msg = self.bluetooth.turn_on()
                    return f"[Phase 9 Bluetooth] {msg}"

            if "off" in cmd or "disable" in cmd:
                auth, _ = self.permissions.check_permission("toggle_bluetooth")
                if auth:
                    _, msg = self.bluetooth.turn_off()
                    return f"[Phase 9 Bluetooth] {msg}"

            if "connect" in cmd:
                dev_match = re.search(r"connect\s+(?:my\s+)?([a-z0-9_\s-]+)", cmd)
                dev_name = dev_match.group(1).replace("bluetooth", "").strip() if dev_match else "Headphones"
                if not dev_name:
                    dev_name = "Headphones"
                _, msg = self.bluetooth.connect_device(dev_name)
                return f"[Phase 9 Bluetooth] {msg}"

            if "disconnect" in cmd:
                dev_match = re.search(r"disconnect\s+(?:my\s+)?([a-z0-9_\s-]+)", cmd)
                dev_name = dev_match.group(1).replace("bluetooth", "").strip() if dev_match else "Headphones"
                _, msg = self.bluetooth.disconnect_device(dev_name)
                return f"[Phase 9 Bluetooth] {msg}"

        if "connect my headphones" in cmd or "connect headphones" in cmd or "connect earbuds" in cmd:
            _, msg = self.bluetooth.connect_device("Headphones")
            return f"[Phase 9 Bluetooth] {msg}"

        # 2. Wi-Fi & Network Commands
        if "wi-fi" in cmd or "wifi" in cmd or "wi fi" in cmd:
            if "enable" in cmd or "on" in cmd:
                _, msg = self.wifi.enable()
                return f"[Phase 9 Wi-Fi] {msg}"
            if "disable" in cmd or "off" in cmd:
                _, msg = self.wifi.disable()
                return f"[Phase 9 Wi-Fi] {msg}"
            if "scan" in cmd:
                nets = self.wifi.scan_networks()
                net_names = ", ".join(n["ssid"] for n in nets)
                return f"[Phase 9 Wi-Fi Scan] Available networks: {net_names}"
            if "restart" in cmd:
                _, msg = self.network.restart_network()
                return f"[Phase 9 Network] {msg}"

        # 3. Audio & Volume Commands
        if "volume" in cmd or "speakers" in cmd or "sound" in cmd:
            num_match = re.search(r"(\d+)", cmd)
            if num_match and ("set" in cmd or "to" in cmd):
                val = int(num_match.group(1))
                _, msg = self.volume.set_volume(val)
                return f"[Phase 9 Audio] {msg}"
            if "increase" in cmd or "up" in cmd or "louder" in cmd:
                val = int(num_match.group(1)) if num_match else 10
                _, msg = self.volume.increase_volume(val)
                return f"[Phase 9 Audio] {msg}"
            if "decrease" in cmd or "down" in cmd or "lower" in cmd:
                val = int(num_match.group(1)) if num_match else 10
                _, msg = self.volume.decrease_volume(val)
                return f"[Phase 9 Audio] {msg}"
            if "switch to speakers" in cmd or "speakers" in cmd:
                _, msg = self.volume.switch_output_device("Speakers")
                return f"[Phase 9 Audio Output] {msg}"

        if "mute" in cmd and "microphone" not in cmd and "mic" not in cmd:
            _, msg = self.volume.mute()
            return f"[Phase 9 Audio] {msg}"

        if "unmute" in cmd and "microphone" not in cmd and "mic" not in cmd:
            _, msg = self.volume.unmute()
            return f"[Phase 9 Audio] {msg}"

        # 4. Microphone Commands
        if "microphone" in cmd or "mic" in cmd:
            if "mute" in cmd:
                _, msg = self.microphone.mute_microphone()
                return f"[Phase 9 Microphone] {msg}"
            if "unmute" in cmd:
                _, msg = self.microphone.unmute_microphone()
                return f"[Phase 9 Microphone] {msg}"

        # 5. Brightness & Display Commands
        if "brightness" in cmd:
            num_match = re.search(r"(\d+)", cmd)
            if num_match:
                val = int(num_match.group(1))
                _, msg = self.brightness.set_brightness(val)
                return f"[Phase 9 Brightness] {msg}"
            if "increase" in cmd or "up" in cmd or "higher" in cmd:
                val = int(num_match.group(1)) if num_match else 10
                _, msg = self.brightness.increase_brightness(val)
                return f"[Phase 9 Brightness] {msg}"
            if "decrease" in cmd or "down" in cmd or "lower" in cmd:
                val = int(num_match.group(1)) if num_match else 10
                _, msg = self.brightness.decrease_brightness(val)
                return f"[Phase 9 Brightness] {msg}"

        # 6. Email Commands
        if "email" in cmd or "send" in cmd or "inbox" in cmd:
            if "reply to" in cmd or "reply" in cmd:
                auth, _ = self.permissions.check_permission("send_email")
                if auth:
                    _, msg = self.email.reply_latest("Thank you for the update. Received.")
                    return f"[Phase 9 Email] {msg}"

            if "draft" in cmd:
                _, msg = self.email.save_draft("alice@example.com", "Draft Subject", "Draft content")
                return f"[Phase 9 Email] {msg}"

            if "send" in cmd:
                target = "Alice"
                recipient_addr = "alice@example.com"
                if "manager" in cmd:
                    target = "Manager"
                    recipient_addr = "manager@corp.com"
                
                auth, details = self.permissions.check_permission("send_email", context_details=f"Recipient: {target}")
                if auth:
                    _, msg = self.email.send_email(recipient_addr, "Project ZERO Report", "Here is today's report.")
                    return f"[Phase 9 Email] {msg}"

            if "find emails" in cmd or "search" in cmd:
                sender_match = re.search(r"from\s+([a-z0-9_\s-]+)", cmd)
                sender = sender_match.group(1).strip() if sender_match else "Google"
                msgs = self.email.search_sender(sender)
                return f"[Phase 9 Email Search] Found {len(msgs)} messages from {sender}."

        # 7. Calendar Commands
        if "calendar" in cmd or "meeting" in cmd or "schedule" in cmd:
            if "schedule" in cmd or "create" in cmd:
                _, msg = self.calendar.create_event("New Meeting", "10:00 AM", day="tomorrow")
                return f"[Phase 9 Calendar] {msg}"
            if "move" in cmd or "reschedule" in cmd:
                day_target = "Friday" if "friday" in cmd else "tomorrow"
                _, msg = self.calendar.move_meeting("Standup", "03:00 PM", new_day=day_target)
                return f"[Phase 9 Calendar] {msg}"
            if "what's on" in cmd or "today" in cmd or "read" in cmd:
                events = self.calendar.read_schedule("today")
                evt_titles = ", ".join(f"{e['title']} at {e['start']}" for e in events)
                return f"[Phase 9 Calendar] Today's schedule: {evt_titles or 'No meetings remaining.'}"

        # 8. Power Commands
        if "lock" in cmd and ("pc" in cmd or "computer" in cmd or "screen" in cmd or "my pc" in cmd):
            _, msg = self.power.lock_pc()
            return f"[Phase 9 Power] {msg}"

        if "restart pc" in cmd or "restart computer" in cmd:
            auth, _ = self.permissions.check_permission("restart_pc")
            if auth:
                _, msg = self.power.restart(confirm=True)
                return f"[Phase 9 Power] {msg}"

        if "shutdown pc" in cmd or "shutdown computer" in cmd:
            auth, _ = self.permissions.check_permission("shutdown_pc")
            if auth:
                _, msg = self.power.shutdown(confirm=True)
                return f"[Phase 9 Power] {msg}"

        # 9. Camera Commands
        if "open camera" in cmd or "camera" in cmd:
            auth, _ = self.permissions.check_permission("capture_photo")
            if auth:
                _, msg = self.camera.open_camera()
                return f"[Phase 9 Camera] {msg}"

        # 10. Printer Commands
        if "print" in cmd:
            _, msg = self.printer.print_document("report.pdf")
            return f"[Phase 9 Printer] {msg}"

        # 11. Application Control Commands
        if "open" in cmd or "launch" in cmd:
            app_match = re.search(r"(?:open|launch)\s+([a-z0-9_\s-]+)", cmd)
            app_name = app_match.group(1).strip() if app_match else "File Explorer"
            if app_name not in ["downloads", "desktop", "documents", "pictures", "music", "videos", "home"]:
                _, msg = self.window_manager.launch_app(app_name)
                return f"[Phase 9 Application Control] {msg}"

        return None


# Global singleton instance of SystemControlManager
system_control_manager = SystemControlManager()
