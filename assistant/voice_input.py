"""Voice input layer using Whisper (preferred) or speech_recognition fallback."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

import speech_recognition as sr

from config import (
    LISTEN_TIMEOUT_SECONDS,
    MICROPHONE_SAMPLE_RATE,
    PHRASE_TIME_LIMIT_SECONDS,
    WHISPER_MODEL_SIZE,
)

try:
    import whisper
except Exception:  # pragma: no cover - optional dependency fallback
    whisper = None


class VoiceInput:
    """Handles microphone capture and speech-to-text."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.microphone = sr.Microphone(sample_rate=MICROPHONE_SAMPLE_RATE)
        self.whisper_model = whisper.load_model(WHISPER_MODEL_SIZE) if whisper else None

    def _listen_audio(self) -> Optional[sr.AudioData]:
        """Capture audio from microphone."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=LISTEN_TIMEOUT_SECONDS,
                    phrase_time_limit=PHRASE_TIME_LIMIT_SECONDS,
                )
                return audio
            except sr.WaitTimeoutError:
                return None

    def _transcribe_with_whisper(self, audio: sr.AudioData) -> str:
        """Transcribe speech with local Whisper model."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            wav_path = Path(temp_wav.name)
            temp_wav.write(audio.get_wav_data())

        try:
            result = self.whisper_model.transcribe(str(wav_path), fp16=False)
            return result.get("text", "").strip().lower()
        finally:
            if wav_path.exists():
                wav_path.unlink()

    def _transcribe_with_google(self, audio: sr.AudioData) -> str:
        """Fallback transcription using speech_recognition cloud recognizer."""
        try:
            return self.recognizer.recognize_google(audio).strip().lower()
        except sr.UnknownValueError:
            return ""

    def listen_for_command(self) -> str:
        """Listen once and return recognized text."""
        audio = self._listen_audio()
        if audio is None:
            return ""

        try:
            if self.whisper_model is not None:
                return self._transcribe_with_whisper(audio)
            return self._transcribe_with_google(audio)
        except Exception:
            return ""
