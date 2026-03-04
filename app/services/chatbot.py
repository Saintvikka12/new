"""Simple chatbot orchestration with optional OpenAI-compatible endpoint support."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Iterable


SYSTEM_PROMPT = (
    "You are a helpful, safe AI assistant. Provide concise responses, "
    "and ask follow-up questions when requirements are ambiguous."
)


@dataclass
class ChatTurn:
    role: str
    content: str


@dataclass
class ChatSession:
    history: list[ChatTurn] = field(default_factory=list)

    def append(self, role: str, content: str) -> None:
        self.history.append(ChatTurn(role=role, content=content))

    def as_messages(self) -> list[dict[str, str]]:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend({"role": turn.role, "content": turn.content} for turn in self.history)
        return messages


class ChatbotEngine:
    """A pluggable engine that uses a deterministic fallback when no API key exists."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")

    def generate(self, prompt: str, history: Iterable[dict[str, str]] | None = None) -> str:
        cleaned = prompt.strip()
        if not cleaned:
            return "Please send a message so I can help you."

        if self.api_key:
            return self._openai_compatible_response(cleaned, history)

        return self._fallback_response(cleaned)

    def _openai_compatible_response(
        self, prompt: str, history: Iterable[dict[str, str]] | None
    ) -> str:
        """Keep a local fallback behavior even when key is present.

        In production, replace with a direct provider SDK call.
        """
        return (
            "API-key mode detected. Wire this method to your preferred LLM provider "
            "(OpenAI, Azure, local vLLM, etc.) for high-quality responses. "
            f"For now, here's a useful start: {self._fallback_response(prompt)}"
        )

    def _fallback_response(self, prompt: str) -> str:
        lower = prompt.lower()
        if "build" in lower and "chatbot" in lower:
            return (
                "To build a robust chatbot, define your target users, design tool access, "
                "store conversation memory, and add moderation and observability."
            )
        if "music" in lower or "song" in lower:
            return (
                "Great idea—music generation works best with three stages: lyric planning, "
                "melody/chord generation, and audio rendering."
            )
        if "hello" in lower or "hi" in lower:
            return "Hi! I can help with product planning, coding, and creative generation."

        return (
            "I understand. If you share your goal, constraints, and preferred tech stack, "
            "I can produce a concrete implementation plan."
        )
