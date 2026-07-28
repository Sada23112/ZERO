"""Project ZERO — Speech-to-Text (STT) Providers."""

import asyncio
from typing import Optional
from voice.base import BaseSTTProvider
from zero_logging import logger


class MockSTTProvider(BaseSTTProvider):
    """Mock Speech-to-Text provider for automated unit testing without microphone hardware."""

    def __init__(self, predefined_text: str = "open youtube"):
        self.predefined_text = predefined_text

    @property
    def name(self) -> str:
        return "mock"

    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        """Return predefined test transcription string."""
        return self.predefined_text


class SystemSTTProvider(BaseSTTProvider):
    """Offline/System Speech-to-Text provider using Google/SpeechRecognition or mock fallback."""

    def __init__(self):
        self._recognizer = None
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
        except ImportError:
            logger.info("speech_recognition package not installed; using fallback STT engine.")

    @property
    def name(self) -> str:
        return "system"

    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        """Transcribe raw PCM audio bytes."""
        if not audio_bytes:
            return ""

        if self._recognizer:
            try:
                import speech_recognition as sr
                import io
                import wave

                wav_io = io.BytesIO()
                with wave.open(wav_io, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio_bytes)
                wav_io.seek(0)

                with sr.AudioFile(wav_io) as source:
                    audio_data = self._recognizer.record(source)
                    text = self._recognizer.recognize_google(audio_data)
                    return text
            except Exception as err:
                logger.warning(f"STT transcription error: {err}")

        return "[Transcribed voice audio]"
