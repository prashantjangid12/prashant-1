"""Command parsing and execution for the AI desktop assistant."""
from __future__ import annotations

import os
import re
import subprocess
import webbrowser
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

from config import CONFIRM_POWER_ACTIONS
import automation


class CommandExecutor:
    """Maps spoken commands to concrete desktop actions."""

    def __init__(self) -> None:
        self.apps: Dict[str, str] = {
            "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "google chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "vscode": r"C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
            "vs code": r"C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
            "file explorer": "explorer",
            "explorer": "explorer",
            "notepad": "notepad",
            "calculator": "calc",
        }

    def execute(self, command: str, confirm_callback: Optional[Callable[[str], bool]] = None) -> Tuple[bool, str]:
        """Execute one normalized command and return (success, spoken_feedback)."""
        command = command.strip().lower()
        if not command:
            return False, "I didn't catch a command."

        if command.startswith("open "):
            target = command.replace("open ", "", 1).strip()
            return self._handle_open(target)

        if command.startswith("type "):
            text = command.replace("type ", "", 1)
            automation.type_text(text)
            return True, f"Typing: {text}"

        if command.startswith("press "):
            key_name = command.replace("press ", "", 1)
            automation.press_key(key_name)
            return True, f"Pressed {key_name}"

        if command.startswith("hotkey "):
            keys = [key.strip() for key in command.replace("hotkey ", "", 1).split("+") if key.strip()]
            if not keys:
                return False, "No hotkey was provided."
            automation.hotkey(*keys)
            return True, f"Executed hotkey {' + '.join(keys)}"

        move_match = re.match(r"move mouse to\s+(\d+)\s+(\d+)", command)
        if move_match:
            x, y = int(move_match.group(1)), int(move_match.group(2))
            automation.move_mouse(x, y)
            return True, f"Moved mouse to {x}, {y}."

        if command in {"click", "left click"}:
            automation.click_mouse("left")
            return True, "Clicked."

        if command == "right click":
            automation.click_mouse("right")
            return True, "Right clicked."

        if command in {"shutdown pc", "shutdown"}:
            if CONFIRM_POWER_ACTIONS and confirm_callback and not confirm_callback("shutdown"):
                return False, "Shutdown cancelled."
            subprocess.run("shutdown /s /t 5", shell=True, check=False)
            return True, "Shutting down your PC in 5 seconds."

        if command in {"restart pc", "restart"}:
            if CONFIRM_POWER_ACTIONS and confirm_callback and not confirm_callback("restart"):
                return False, "Restart cancelled."
            subprocess.run("shutdown /r /t 5", shell=True, check=False)
            return True, "Restarting your PC in 5 seconds."

        if command.startswith("run program "):
            program = command.replace("run program ", "", 1).strip()
            subprocess.Popen(program, shell=True)
            return True, f"Running {program}."

        return False, "Sorry, I don't know that command yet."

    def _handle_open(self, target: str) -> Tuple[bool, str]:
        """Open app, folder, or website based on spoken target."""
        if not target:
            return False, "Please tell me what to open."

        if target in self.apps:
            app_cmd = os.path.expandvars(self.apps[target])
            try:
                subprocess.Popen(app_cmd, shell=True)
                return True, f"Opening {target} now."
            except OSError:
                return False, f"I couldn't open {target}."

        if target.startswith("http") or ".com" in target or ".org" in target or ".net" in target:
            url = target if target.startswith("http") else f"https://{target}"
            webbrowser.open(url)
            return True, f"Opening {target}."

        if target.startswith("my ") and "folder" in target:
            # Example: "open my project folder"
            folder_name = target.replace("open ", "").replace("my ", "").replace("folder", "").strip()
            if not folder_name:
                folder_path = str(Path.home())
            else:
                folder_path = str(Path.home() / folder_name)
            subprocess.Popen(f'explorer "{folder_path}"')
            return True, f"Opening {folder_name or 'home'} folder."

        candidate = Path(target)
        if candidate.exists() and candidate.is_dir():
            os.startfile(candidate)  # type: ignore[attr-defined]
            return True, f"Opening folder {target}."

        # Friendly shortcuts for common sites
        common_sites = {
            "youtube": "https://youtube.com",
            "google": "https://google.com",
            "github": "https://github.com",
        }
        if target in common_sites:
            webbrowser.open(common_sites[target])
            return True, f"Opening {target}."

        return False, f"I couldn't find {target}."
