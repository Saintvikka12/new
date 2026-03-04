from pathlib import Path

from app.services.chatbot import ChatbotEngine
from app.services.music_generator import SongGenerator, SongIdea


def test_chatbot_fallback_response_non_empty() -> None:
    engine = ChatbotEngine()
    response = engine.generate("hello")
    assert response


def test_song_generator_outputs_lyrics_and_audio(tmp_path: Path) -> None:
    generator = SongGenerator(sample_rate=8_000)
    idea = SongIdea(genre="pop", mood="uplifting", theme="hope")

    lyrics = generator.generate_lyrics(idea)
    assert "Chorus" in lyrics

    notes = generator.generate_melody(measures=1)
    out = generator.synthesize_wave(notes, tmp_path / "song.wav")
    assert out.exists()
    assert out.stat().st_size > 0
