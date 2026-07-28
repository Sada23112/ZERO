"""Project ZERO — Voice Subsystem Manager & Hardware Device Enumerator."""

from typing import List, Optional, Dict, Any
from voice.base import BaseSTTProvider, BaseTTSProvider, AudioDevice, VoiceDefinition
from voice.stt import SystemSTTProvider, MockSTTProvider
from voice.tts import Pyttsx3TTSProvider, MockTTSProvider
from zero_logging import logger

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False


class VoiceManager:
    """Central Manager for Voice hardware, STT/TTS providers, and audio settings."""

    def __init__(self, stt_provider: Optional[BaseSTTProvider] = None, tts_provider: Optional[BaseTTSProvider] = None):
        self.stt_provider: BaseSTTProvider = stt_provider or SystemSTTProvider()
        self.tts_provider: BaseTTSProvider = tts_provider or Pyttsx3TTSProvider()
        self.muted: bool = False

    def list_microphones(self) -> List[AudioDevice]:
        """Enumerate connected input microphone devices."""
        devices: List[AudioDevice] = []
        if SOUNDDEVICE_AVAILABLE:
            try:
                all_devs = sd.query_devices()
                default_in = sd.default.device[0] if isinstance(sd.default.device, (list, tuple)) else None
                for i, d in enumerate(all_devs):
                    if d.get("max_input_channels", 0) > 0:
                        devices.append(
                            AudioDevice(
                                id=i,
                                name=str(d.get("name", f"Microphone {i}")),
                                max_input_channels=d.get("max_input_channels", 0),
                                default_sample_rate=int(d.get("default_samplerate", 44100)),
                                is_default=(i == default_in)
                            )
                        )
            except Exception as err:
                logger.warning(f"Error querying microphone devices: {err}")

        if not devices:
            devices.append(AudioDevice(id=0, name="System Default Microphone", max_input_channels=1, is_default=True))

        return devices

    def list_speakers(self) -> List[AudioDevice]:
        """Enumerate connected output speaker devices."""
        devices: List[AudioDevice] = []
        if SOUNDDEVICE_AVAILABLE:
            try:
                all_devs = sd.query_devices()
                default_out = sd.default.device[1] if isinstance(sd.default.device, (list, tuple)) else None
                for i, d in enumerate(all_devs):
                    if d.get("max_output_channels", 0) > 0:
                        devices.append(
                            AudioDevice(
                                id=i,
                                name=str(d.get("name", f"Speaker {i}")),
                                max_output_channels=d.get("max_output_channels", 0),
                                default_sample_rate=int(d.get("default_samplerate", 44100)),
                                is_default=(i == default_out)
                            )
                        )
            except Exception as err:
                logger.warning(f"Error querying speaker devices: {err}")

        if not devices:
            devices.append(AudioDevice(id=0, name="System Default Speaker", max_output_channels=2, is_default=True))

        return devices

    def list_voices(self) -> List[VoiceDefinition]:
        """Enumerate available TTS voices."""
        return self.tts_provider.list_voices()
