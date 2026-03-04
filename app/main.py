from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.services.chatbot import ChatbotEngine
from app.services.music_generator import SongGenerator, SongIdea


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class MusicRequest(BaseModel):
    genre: str = Field(default="pop")
    mood: str = Field(default="uplifting")
    theme: str = Field(default="hope")


app = FastAPI(title="Creator AI Studio", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = ChatbotEngine()
song_generator = SongGenerator()

static_dir = Path(__file__).parent / "static"
audio_dir = static_dir / "generated"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.post("/api/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    response = chatbot.generate(request.message)
    return {"response": response}


@app.post("/api/music")
def music(request: MusicRequest) -> dict[str, str]:
    idea = SongIdea(genre=request.genre, mood=request.mood, theme=request.theme)
    lyrics = song_generator.generate_lyrics(idea)
    notes = song_generator.generate_melody()
    file_name = f"song-{uuid4().hex[:8]}.wav"
    output_file = song_generator.synthesize_wave(notes, audio_dir / file_name)

    return {
        "lyrics": lyrics,
        "audio_url": f"/static/generated/{output_file.name}",
        "notes_count": str(len(notes)),
    }
