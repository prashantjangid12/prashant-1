"""Entry point for the personal AI voice assistant."""
from __future__ import annotations

import time

from commands import CommandExecutor
from memory import AssistantMemory
from voice_input import VoiceInput
from voice_output import VoiceOutput


class PersonalAssistant:
    """Coordinates listening, command execution, memory, and speech output."""

    def __init__(self) -> None:
        self.voice_input = VoiceInput()
        self.voice_output = VoiceOutput()
        self.memory = AssistantMemory()
        self.executor = CommandExecutor()

    def _confirm_action(self, action_name: str) -> bool:
        self.voice_output.speak(f"Do you want me to {action_name} the PC? Please say yes or no.")
        answer = self.voice_input.listen_for_command()
        return answer in {"yes", "confirm", "go ahead", "do it"}

    def run_forever(self) -> None:
        """Run the assistant in always-on mode."""
        self.voice_output.speak("Assistant is online and listening.")

        while True:
            command = self.voice_input.listen_for_command()
            if not command:
                time.sleep(0.2)
                continue

            print(f"Heard: {command}")

            if command in {"exit", "quit", "stop assistant"}:
                self.voice_output.speak("Goodbye.")
                break

            if command == "repeat":
                last = self.memory.get_last_command()
                if not last:
                    self.voice_output.speak("I don't have a previous command to repeat yet.")
                    continue
                self.voice_output.speak("Repeating last command.")
                success, message = self.executor.execute(last, confirm_callback=self._confirm_action)
                self.voice_output.speak(message)
                if success:
                    self.memory.save_command(last)
                continue

            success, message = self.executor.execute(command, confirm_callback=self._confirm_action)
            self.voice_output.speak(message)

            if success:
                self.memory.save_command(command)


if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.run_forever()
