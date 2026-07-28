"""Project ZERO — Abstract Voice & Audio Interfaces (Phase 3A)."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, AsyncGenerator
from pydantic import BaseModel, Field


class VoiceDefinition(BaseModel):
    """Metadata representation for text-to-speech voice models."""

    id: str
    name: str
    languages: List[str] = Field(default_factory=lambda: ["en-US"])
    gender: Optional[str] = None


class AudioDevice(BaseModel):
    """Metadata representation for input microphone or output speaker hardware."""

    id: int
    name: str
    max_input_channels: int = 0
    max_output_channels: int = 0
    default_sample_rate: int = 44100
    is_default: bool = False


class BaseSTTProvider(ABC):
    """Abstract Base Class for Speech-to-Text Providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider unique name."""
        pass

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        """Transcribe raw audio PCM/WAV bytes into text string."""
        pass


class BaseTTSProvider(ABC):
    """Abstract Base Class for Text-to-Speech Providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider unique name."""
        pass

    @abstractmethod
    async def speak(self, text: str, voice_id: Optional[str] = None, speed: float = 1.0) -> None:
        """Synthesize and play audio for the given text synchronously or asynchronously."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Immediately interrupt and stop any active audio playback."""
        pass

    @abstractmethod
    def list_voices(self) -> List[VoiceDefinition]:
        """List available voices for this TTS provider."""
        pass
