"""Project ZERO — Unit Tests for Phase 9 Operating System Control & Device Integration."""

import pytest
import os
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
from zero.system_control.system_control_manager import SystemControlManager


def test_permission_manager():
    perms = SystemPermissionManager()
    assert perms.get_tier("get_battery") == PermissionLevel.SAFE
    assert perms.get_tier("toggle_bluetooth") == PermissionLevel.MEDIUM
    assert perms.get_tier("send_email") == PermissionLevel.SENSITIVE
    assert perms.get_tier("shutdown_pc") == PermissionLevel.CRITICAL

    auth, _ = perms.check_permission("get_battery")
    assert auth is True

    perms.grant_permission("shutdown_pc")
    auth2, _ = perms.check_permission("shutdown_pc")
    assert auth2 is True


def test_bluetooth_controller():
    bt = BluetoothController()
    succ, _ = bt.turn_on()
    assert succ is True
    succ2, _ = bt.connect_device("Headphones")
    assert succ2 is True
    devices = bt.list_paired_devices()
    assert len(devices) >= 1


def test_wifi_and_network_manager():
    wifi = WiFiManager()
    net = NetworkManager()

    succ, _ = wifi.enable()
    assert succ is True
    networks = wifi.scan_networks()
    assert len(networks) >= 1

    ip_cfg = net.get_ip_config()
    assert "ip_address" in ip_cfg


def test_email_manager():
    email = EmailManager()
    succ, _ = email.send_email("test@example.com", "Test Subject", "Test Body")
    assert succ is True

    succ2, _ = email.reply_latest("Thanks")
    assert succ2 is True

    unread = email.read_unread()
    assert isinstance(unread, list)


def test_calendar_and_contacts():
    cal = CalendarManager()
    contacts = ContactsManager()

    succ, _ = cal.create_event("Team Standup", "09:00 AM", day="tomorrow")
    assert succ is True

    events = cal.read_schedule("tomorrow")
    assert len(events) >= 1

    contact = contacts.lookup_contact("Alice")
    assert contact is not None
    assert "alice@example.com" in contact["email"]


def test_audio_and_brightness():
    vol = VolumeController()
    bright = BrightnessController()
    mic = MicrophoneController()

    succ1, _ = vol.set_volume(75)
    assert succ1 is True
    assert vol.get_volume() == 75

    succ2, _ = bright.set_brightness(80)
    assert succ2 is True
    assert bright.get_brightness() == 80

    succ3, _ = mic.mute_microphone()
    assert succ3 is True
    assert mic.is_muted() is True


def test_power_display_camera_printer():
    power = PowerController()
    disp = DisplayController()
    cam = CameraController()
    printer = PrinterController()

    succ1, _ = power.lock_pc()
    assert succ1 is True

    monitors = disp.detect_monitors()
    assert len(monitors) >= 1

    succ2, _ = cam.open_camera()
    assert succ2 is True

    printers = printer.list_printers()
    assert len(printers) >= 1


def test_device_and_system_control_manager():
    mgr = SystemControlManager()

    # Bluetooth command
    res1 = mgr.process_system_command("Turn on Bluetooth.")
    assert "[Phase 9 Bluetooth]" in res1

    # Connect headphones
    res2 = mgr.process_system_command("Connect my headphones.")
    assert "[Phase 9 Bluetooth]" in res2

    # Volume/Brightness commands
    res3 = mgr.process_system_command("Increase brightness to 70%.")
    assert "[Phase 9 Brightness]" in res3

    # Microphone command
    res4 = mgr.process_system_command("Mute my microphone.")
    assert "[Phase 9 Microphone]" in res4

    # Lock PC command
    res5 = mgr.process_system_command("Lock my PC.")
    assert "[Phase 9 Power]" in res5
