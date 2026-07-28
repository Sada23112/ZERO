"""Project ZERO — Voice Subsystem Package (Phase 3A)."""

from voice.base import BaseSTTProvider, BaseTTSProvider, AudioDevice, VoiceDefinition
from voice.stt import SystemSTTProvider, MockSTTProvider
from voice.tts import Pyttsx3TTSProvider, MockTTSProvider
from voice.listener import AudioRecorder, ActiveListener
from voice.manager import VoiceManager

__all__ = [
    "BaseSTTProvider",
    "BaseTTSProvider",
    "AudioDevice",
    "VoiceDefinition",
    "SystemSTTProvider",
    "MockSTTProvider",
    "Pyttsx3TTSProvider",
    "MockTTSProvider",
    "AudioRecorder",
    "ActiveListener",
    "VoiceManager",
]
