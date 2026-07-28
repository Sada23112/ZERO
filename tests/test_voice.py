"""Unit tests for Phase 3A Voice Subsystem, STT/TTS Providers, ActiveListener, & VoiceManager."""

import pytest
from pathlib import Path
from voice.base import VoiceDefinition, AudioDevice
from voice.stt import MockSTTProvider, SystemSTTProvider
from voice.tts import MockTTSProvider, Pyttsx3TTSProvider
from voice.listener import AudioRecorder, ActiveListener
from voice.manager import VoiceManager
from brain.brain import Brain
from memory.database import DatabaseManager


@pytest.fixture
def mock_brain(tmp_path: Path):
    db_file = tmp_path / "voice_brain_test.db"
    db_manager = DatabaseManager(str(db_file))
    return Brain(db_manager=db_manager)


@pytest.mark.asyncio
async def test_mock_stt_provider():
    stt = MockSTTProvider(predefined_text="open github")
    assert stt.name == "mock"
    transcription = await stt.transcribe(b"\x00\x00\x00\x00")
    assert transcription == "open github"


@pytest.mark.asyncio
async def test_mock_tts_provider():
    tts = MockTTSProvider()
    assert tts.name == "mock"
    await tts.speak("Hello from ZERO voice synthesis")
    assert len(tts.spoken_texts) == 1
    assert tts.spoken_texts[0] == "Hello from ZERO voice synthesis"
    assert tts.is_playing is False

    voices = tts.list_voices()
    assert len(voices) >= 2
    assert voices[0].id == "mock_voice_en"


def test_audio_recorder_rms_calculation():
    recorder = AudioRecorder()
    # Test RMS calculation on silence (all zeros)
    silence_bytes = b"\x00\x00" * 100
    rms_silence = recorder.calculate_rms(silence_bytes)
    assert rms_silence == 0.0


@pytest.mark.asyncio
async def test_active_listener_loop(mock_brain: Brain):
    stt = MockSTTProvider(predefined_text="stop listening")
    tts = MockTTSProvider()
    listener = ActiveListener(brain=mock_brain, stt_provider=stt, tts_provider=tts)

    user_speeches = []
    zero_responses = []

    def on_user(text):
        user_speeches.append(text)

    def on_zero(resp):
        zero_responses.append(resp)

    # Mock phrase recording to return non-empty audio
    async def mock_record(max_duration_sec=8.0):
        if not listener.is_listening:
            return b""
        return b"\x01\x00" * 50

    listener.recorder.record_phrase = mock_record

    await listener.start_listening_loop(on_user_speech=on_user, on_zero_response=on_zero)

    assert len(user_speeches) == 1
    assert user_speeches[0] == "stop listening"
    assert "Stopping active voice listening" in tts.spoken_texts[0]
    assert listener.is_listening is False


def test_voice_manager_enumeration():
    stt = MockSTTProvider()
    tts = MockTTSProvider()
    manager = VoiceManager(stt_provider=stt, tts_provider=tts)

    mics = manager.list_microphones()
    assert len(mics) >= 1
    assert isinstance(mics[0], AudioDevice)

    speakers = manager.list_speakers()
    assert len(speakers) >= 1
    assert isinstance(speakers[0], AudioDevice)

    voices = manager.list_voices()
    assert len(voices) >= 1
    assert isinstance(voices[0], VoiceDefinition)
