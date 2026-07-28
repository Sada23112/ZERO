"""Project ZERO — Text-to-Speech (TTS) Providers."""

import asyncio
from typing import Optional, List
from voice.base import BaseTTSProvider, VoiceDefinition
from zero_logging import logger

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class MockTTSProvider(BaseTTSProvider):
    """Mock Text-to-Speech provider for hardware-independent testing."""

    def __init__(self):
        self.spoken_texts: List[str] = []
        self.is_playing: bool = False

    @property
    def name(self) -> str:
        return "mock"

    async def speak(self, text: str, voice_id: Optional[str] = None, speed: float = 1.0) -> None:
        """Record spoken text without outputting to physical speaker hardware."""
        self.is_playing = True
        self.spoken_texts.append(text)
        logger.debug(f"[MockTTS] Spoke: '{text}'")
        self.is_playing = False

    def stop(self) -> None:
        """Interrupt playback."""
        self.is_playing = False

    def list_voices(self) -> List[VoiceDefinition]:
        return [
            VoiceDefinition(id="mock_voice_en", name="Mock English Voice", languages=["en-US"], gender="neutral"),
            VoiceDefinition(id="mock_voice_uk", name="Mock British Voice", languages=["en-GB"], gender="female"),
        ]


class Pyttsx3TTSProvider(BaseTTSProvider):
    """Offline cross-platform Text-to-Speech provider using pyttsx3."""

    def __init__(self):
        self._engine = None

    @property
    def name(self) -> str:
        return "pyttsx3"

    async def speak(self, text: str, voice_id: Optional[str] = None, speed: float = 1.0) -> None:
        """Synthesize and speak text via system sound output."""
        if not text or not text.strip() or not PYTTSX3_AVAILABLE:
            return

        loop = asyncio.get_running_loop()

        def _do_speak():
            try:
                try:
                    import pythoncom
                    pythoncom.CoInitialize()
                except Exception:
                    pass

                engine = pyttsx3.init()
                if voice_id:
                    try:
                        engine.setProperty("voice", voice_id)
                    except Exception:
                        pass
                try:
                    rate = engine.getProperty("rate")
                    engine.setProperty("rate", int(rate * speed))
                except Exception:
                    pass
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as err:
                logger.warning(f"pyttsx3 speech synthesis error: {err}")

        await loop.run_in_executor(None, _do_speak)

    def stop(self) -> None:
        """Immediately stop speech engine playback."""
        if self._engine:
            try:
                self._engine.stop()
            except Exception:
                pass

    def list_voices(self) -> List[VoiceDefinition]:
        """List system-installed TTS voices."""
        result: List[VoiceDefinition] = []
        if self._engine:
            try:
                voices = self._engine.getProperty("voices")
                for v in voices:
                    result.append(
                        VoiceDefinition(
                            id=str(v.id),
                            name=str(v.name),
                            languages=[str(lang) for lang in getattr(v, "languages", ["en-US"])],
                            gender=getattr(v, "gender", None)
                        )
                    )
            except Exception as err:
                logger.warning(f"Failed to enumerate voices: {err}")

        if not result:
            result.append(VoiceDefinition(id="default", name="System Default Voice", languages=["en-US"]))

        return result
