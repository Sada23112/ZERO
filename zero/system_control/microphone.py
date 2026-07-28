"""Project ZERO — Microphone & Audio Input Subsystem Control.

Manages microphone mute/unmute state and audio input device selection.
"""

from typing import List, Tuple
from zero_logging import logger


class MicrophoneController:
    """Controls microphone audio input capture and mute states."""

    def __init__(self) -> None:
        self.muted: bool = False
        self.active_input: str = "Microphone Array (Realtek High Definition Audio)"
        self.input_devices: List[str] = [
            "Microphone Array (Realtek High Definition Audio)",
            "Headset Microphone (Bluetooth)",
            "USB Condenser Microphone",
        ]

    def mute_microphone(self) -> Tuple[bool, str]:
        """Mute microphone audio input."""
        self.muted = True
        logger.info("[Microphone] Microphone input muted.")
        return True, "Microphone muted."

    def unmute_microphone(self) -> Tuple[bool, str]:
        """Unmute microphone audio input."""
        self.muted = False
        logger.info("[Microphone] Microphone input unmuted.")
        return True, "Microphone unmuted."

    def is_muted(self) -> bool:
        """Check if microphone is muted."""
        return self.muted

    def select_audio_input(self, device_name: str) -> Tuple[bool, str]:
        """Select active microphone input device."""
        target = device_name.lower().strip()
        for dev in self.input_devices:
            if target in dev.lower():
                self.active_input = dev
                logger.info(f"[Microphone] Selected input device '{dev}'")
                return True, f"Selected audio input device '{dev}'."
        return False, f"Microphone device '{device_name}' not found."

    def list_input_devices(self) -> List[str]:
        """List available microphone input devices."""
        return list(self.input_devices)
