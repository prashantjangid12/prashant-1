"""Text-to-speech output with realistic voice using edge-tts, with pyttsx3 fallback."""
from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from playsound import playsound

from config import VOICE_NAME, VOICE_RATE, VOICE_VOLUME

try:
    import edge_tts
except Exception:  # pragma: no cover - optional dependency fallback
    edge_tts = None

try:
    import pyttsx3
except Exception:  # pragma: no cover - optional dependency fallback
    pyttsx3 = None


class VoiceOutput:
    """Converts text to natural speech and plays it on speakers."""

    def __init__(self, voice_name: str = VOICE_NAME, rate: str = VOICE_RATE, volume: str = VOICE_VOLUME) -> None:
        self.voice_name = voice_name
        self.rate = rate
        self.volume = volume
        self._pyttsx3_engine = pyttsx3.init() if pyttsx3 else None

    async def _speak_edge_tts(self, text: str) -> None:
        """Generate TTS audio with Microsoft neural voices and play it."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            output_path = Path(temp_file.name)

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice_name,
            rate=self.rate,
            volume=self.volume,
        )
        await communicate.save(str(output_path))

        try:
            playsound(str(output_path))
        finally:
            if output_path.exists():
                output_path.unlink()

    def _speak_pyttsx3(self, text: str) -> None:
        """Fallback TTS for environments where edge-tts is unavailable."""
        if not self._pyttsx3_engine:
            raise RuntimeError("No TTS engine available. Install edge-tts or pyttsx3.")

        self._pyttsx3_engine.say(text)
        self._pyttsx3_engine.runAndWait()

    def speak(self, text: str) -> None:
        """Public speaking method used by the assistant."""
        if not text:
            return

        print(f"Assistant: {text}")

        if edge_tts is not None:
            asyncio.run(self._speak_edge_tts(text))
            return

        self._speak_pyttsx3(text)
