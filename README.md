# Personal AI Assistant for Windows (Python)

This project provides a **local voice-controlled AI assistant** for Windows that can:

- Continuously listen via microphone
- Convert speech to text (Whisper preferred, `speech_recognition` fallback)
- Speak back with a realistic human-like voice (`edge-tts` neural voices)
- Open apps, websites, folders, and run programs
- Automate keyboard/mouse actions
- Repeat the last command
- Save command memory in JSON

## Project Structure

```text
assistant/
  main.py
  voice_input.py
  voice_output.py
  commands.py
  memory.py
  automation.py
  config.py
```

## 1) Prerequisites

- Windows 10/11
- Python 3.10+
- Working microphone and speaker/headphones

## 2) Install Dependencies

From the project root, run:

```bash
pip install openai-whisper speechrecognition pyaudio edge-tts playsound==1.2.2 pyautogui keyboard
```

### Optional fallback TTS

If you want offline fallback voice output (less natural):

```bash
pip install pyttsx3
```

> Note: `pyaudio` installation can fail on some systems. If it does, install a compatible wheel for your Python version.

## 3) Configure Voice + Behavior

Edit `assistant/config.py` to customize:

- `WHISPER_MODEL_SIZE` (`tiny`, `base`, `small`, `medium`, `large`)
- `VOICE_NAME` (for example `en-US-JennyNeural`, `en-US-GuyNeural`)
- `VOICE_RATE`
- `LISTEN_TIMEOUT_SECONDS`, `PHRASE_TIME_LIMIT_SECONDS`

## 4) Run the Assistant

```bash
python assistant/main.py
```

When it starts, you should hear: **"Assistant is online and listening."**

The assistant then runs in an infinite loop until you say:

- `exit`
- `quit`
- `stop assistant`

## 5) Example Voice Commands

- `open chrome`
- `open youtube`
- `open vs code`
- `open file explorer`
- `type hello this is a test`
- `press enter`
- `hotkey ctrl+s`
- `move mouse to 500 400`
- `click`
- `right click`
- `run program notepad`
- `shutdown pc`
- `restart pc`
- `open my project folder`
- `repeat`

## 6) Memory System

Memory is saved in:

- `assistant/data/memory.json`

It stores:

- `last_command`
- recent `history`
- top `frequent` commands

## 7) Notes for Best Results

- Speak clearly and pause briefly between commands.
- Use a headset mic in noisy rooms.
- Whisper model `base` gives a good speed/accuracy tradeoff.
- `edge-tts` requires internet access to fetch neural voice audio.

## 8) Safety Notes

- Power commands (`shutdown`, `restart`) ask for confirmation by voice.
- PyAutoGUI failsafe is enabled: move mouse to top-left corner to abort automation.
