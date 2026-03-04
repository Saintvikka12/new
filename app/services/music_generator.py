"""Song generation utilities: lyrics + simple waveform synthesis."""

from __future__ import annotations

import math
import random
import struct
import wave
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SongIdea:
    genre: str
    mood: str
    theme: str


class SongGenerator:
    def __init__(self, sample_rate: int = 44_100) -> None:
        self.sample_rate = sample_rate

    def generate_lyrics(self, idea: SongIdea) -> str:
        chorus = (
            f"In this {idea.mood} light, we rise and sing\\n"
            f"{idea.theme} in our hearts, like a golden string\\n"
            "Hold on tight, let the night unfold\\n"
            f"A {idea.genre} dream in a story told"
        )
        verse = (
            f"Verse 1:\\n"
            f"Streetlights paint the air in shades of {idea.mood},\\n"
            f"Every step we take redraws the map of {idea.theme}.\\n"
            "We turn our silence into sparks of sound,\\n"
            "And find tomorrow in the rhythm we have found."
        )
        return f"{verse}\\n\\nChorus:\\n{chorus}"

    def generate_melody(self, measures: int = 8) -> list[tuple[float, float]]:
        scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]
        notes: list[tuple[float, float]] = []
        for _ in range(measures * 4):
            freq = random.choice(scale)
            duration = random.choice([0.25, 0.5, 0.75])
            notes.append((freq, duration))
        return notes

    def synthesize_wave(self, notes: list[tuple[float, float]], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(output_path), "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)

            for freq, duration in notes:
                frames = int(duration * self.sample_rate)
                for frame in range(frames):
                    amp = int(12_000 * math.sin(2 * math.pi * freq * frame / self.sample_rate))
                    wav_file.writeframes(struct.pack("<h", amp))
        return output_path
