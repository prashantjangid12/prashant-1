"""Configuration values for the local AI assistant."""
from pathlib import Path

# Wake phrases can be expanded if you want command-gating instead of processing everything.
WAKE_WORDS = ["jarvis", "assistant"]

# Audio behavior
LISTEN_TIMEOUT_SECONDS = 3
PHRASE_TIME_LIMIT_SECONDS = 8
MICROPHONE_SAMPLE_RATE = 16_000

# TTS behavior
VOICE_RATE = "+0%"  # edge-tts style rate value
VOICE_VOLUME = "+0%"
VOICE_NAME = "en-US-JennyNeural"  # realistic built-in Microsoft neural voice

# Whisper model options: tiny, base, small, medium, large
WHISPER_MODEL_SIZE = "base"

# Runtime files
APP_ROOT = Path(__file__).resolve().parent
DATA_DIR = APP_ROOT / "data"
MEMORY_FILE = DATA_DIR / "memory.json"

# If True, assistant asks for a confirmation before dangerous OS power commands.
CONFIRM_POWER_ACTIONS = True
