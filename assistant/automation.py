"""Desktop automation helpers (mouse, keyboard, typing)."""
from __future__ import annotations

import time

import keyboard
import pyautogui

# Keep actions safe by allowing users to move mouse to top-left to abort pyautogui automation.
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


def move_mouse(x: int, y: int, duration: float = 0.3) -> None:
    pyautogui.moveTo(x, y, duration=duration)


def click_mouse(button: str = "left") -> None:
    pyautogui.click(button=button)


def press_key(key_name: str) -> None:
    keyboard.press_and_release(key_name)


def hotkey(*keys: str) -> None:
    pyautogui.hotkey(*keys)


def type_text(text: str, interval: float = 0.02) -> None:
    pyautogui.write(text, interval=interval)


def wait(seconds: float) -> None:
    time.sleep(seconds)
