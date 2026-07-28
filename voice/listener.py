"""Project ZERO — Active Voice Listener & Silence VAD Subsystem."""

import asyncio
import math
import struct
from typing import Optional, Callable, Dict, Any
from voice.base import BaseSTTProvider, BaseTTSProvider
from brain.brain import Brain
from zero_logging import logger

try:
    import sounddevice as sd
    import numpy as np
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False


class AudioRecorder:
    """Microphone audio recorder with automatic silence detection (VAD)."""

    def __init__(
        self,
        sample_rate: int = 16000,
        silence_threshold: float = 300.0,
        silence_duration_sec: float = 1.5,
        device_index: Optional[int] = None
    ):
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold
        self.silence_duration_sec = silence_duration_sec
        self.device_index = device_index
        self.is_recording = False

    def calculate_rms(self, audio_chunk: bytes) -> float:
        """Calculate Root Mean Square (RMS) volume level of audio chunk."""
        if not audio_chunk:
            return 0.0
        count = len(audio_chunk) // 2
        if count == 0:
            return 0.0
        format_str = f"<{count}h"
        try:
            shorts = struct.unpack(format_str, audio_chunk)
            sum_squares = sum(s * s for s in shorts)
            return math.sqrt(sum_squares / count)
        except Exception:
            return 0.0

    async def record_phrase(self, max_duration_sec: float = 10.0) -> bytes:
        """Record audio phrase until silence is detected or max duration is reached."""
        if not SOUNDDEVICE_AVAILABLE:
            logger.info("sounddevice/numpy not available. Returning empty audio bytes.")
            return b""

        recorded_chunks = []
        silent_chunks_count = 0
        chunk_samples = int(self.sample_rate * 0.1) # 100ms chunks
        max_silent_chunks = int(self.silence_duration_sec / 0.1)

        self.is_recording = True

        try:
            def callback(indata, frames, time_info, status):
                if status:
                    logger.debug(f"Audio record status: {status}")
                recorded_chunks.append(indata.copy())

            loop = asyncio.get_running_loop()
            stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
                device=self.device_index,
                callback=callback
            )

            with stream:
                start_time = loop.time()
                while self.is_recording and (loop.time() - start_time) < max_duration_sec:
                    await asyncio.sleep(0.1)
                    if recorded_chunks:
                        latest_data = recorded_chunks[-1]
                        raw_bytes = latest_data.tobytes()
                        rms = self.calculate_rms(raw_bytes)
                        if rms < self.silence_threshold:
                            silent_chunks_count += 1
                        else:
                            silent_chunks_count = 0

                        if silent_chunks_count >= max_silent_chunks and len(recorded_chunks) > 5:
                            logger.info("Automatic silence detected. Stopping phrase recording.")
                            break

        except Exception as err:
            logger.warning(f"Audio recording failed: {err}")
        finally:
            self.is_recording = False

        if recorded_chunks:
            return np.concatenate(recorded_chunks, axis=0).tobytes()
        return b""


class ActiveListener:
    """Active voice conversation loop orchestrator."""

    def __init__(
        self,
        brain: Brain,
        stt_provider: BaseSTTProvider,
        tts_provider: BaseTTSProvider,
        recorder: Optional[AudioRecorder] = None
    ):
        self.brain = brain
        self.stt_provider = stt_provider
        self.tts_provider = tts_provider
        self.recorder = recorder or AudioRecorder()
        self.is_listening = False
        self.muted = False

    def mute(self):
        """Mute voice TTS output."""
        self.muted = True

    def unmute(self):
        """Unmute voice TTS output."""
        self.muted = False

    async def start_listening_loop(self, on_user_speech: Optional[Callable[[str], None]] = None, on_zero_response: Optional[Callable[[str], None]] = None):
        """Run active voice conversation listening loop until stopped."""
        self.is_listening = True
        logger.info("Active voice listening loop started.")

        while self.is_listening:
            try:
                # 1. Record Audio Phrase
                audio_bytes = await self.recorder.record_phrase(max_duration_sec=8.0)
                if not audio_bytes or not self.is_listening:
                    await asyncio.sleep(0.2)
                    continue

                # 2. Transcribe via STT Provider
                user_text = await self.stt_provider.transcribe(audio_bytes)
                user_text_clean = user_text.strip()
                if not user_text_clean:
                    continue

                if on_user_speech:
                    on_user_speech(user_text_clean)

                lower_text = user_text_clean.lower()
                if lower_text in ["stop listening", "exit", "quit", "stop"]:
                    logger.info("Termination phrase recognized. Stopping active listening loop.")
                    self.is_listening = False
                    if not self.muted:
                        await self.tts_provider.speak("Stopping active voice listening.")
                    break

                # 3. Pass transcribed text to Brain
                response_text = await self.brain.process(user_text_clean)
                if on_zero_response:
                    on_zero_response(response_text)

                # 4. Speak response via TTS Provider
                if not self.muted and response_text:
                    await self.tts_provider.speak(response_text)

            except asyncio.CancelledError:
                self.is_listening = False
                break
            except Exception as err:
                logger.error(f"Error in active voice listening loop: {err}")
                await asyncio.sleep(0.5)

    def stop(self):
        """Stop active voice listening loop."""
        self.is_listening = False
        self.tts_provider.stop()
