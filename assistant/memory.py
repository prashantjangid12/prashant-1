"""Simple JSON-backed memory for command history and frequently used commands."""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from config import MEMORY_FILE


@dataclass
class AssistantMemory:
    """Stores and retrieves assistant memory from disk."""

    memory_file: Path = MEMORY_FILE
    data: Dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict:
        if not self.memory_file.exists():
            return {"last_command": "", "history": [], "frequent": {}}

        try:
            with self.memory_file.open("r", encoding="utf-8") as file:
                payload = json.load(file)
            payload.setdefault("last_command", "")
            payload.setdefault("history", [])
            payload.setdefault("frequent", {})
            return payload
        except (json.JSONDecodeError, OSError):
            # Reset a corrupt file safely.
            return {"last_command": "", "history": [], "frequent": {}}

    def _save(self) -> None:
        with self.memory_file.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2)

    def save_command(self, command: str) -> None:
        command = command.strip()
        if not command:
            return

        self.data["last_command"] = command
        history: List[str] = self.data.get("history", [])
        history.append(command)
        self.data["history"] = history[-200:]  # keep recent 200 for lightweight storage

        counter = Counter(self.data.get("history", []))
        self.data["frequent"] = dict(counter.most_common(20))
        self._save()

    def get_last_command(self) -> str:
        return self.data.get("last_command", "")

    def get_frequent_commands(self) -> Dict[str, int]:
        return self.data.get("frequent", {})
