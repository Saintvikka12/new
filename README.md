# Creator AI Studio

A starter project that combines:

1. **Chatbot assistant** (ChatGPT-like conversational endpoint)
2. **Music/song generator** (Suno-like prototype with lyrics + generated WAV melody)

## Features

- FastAPI backend with two endpoints:
  - `POST /api/chat` for conversational responses
  - `POST /api/music` for lyrics and generated audio
- Single-page web UI for both tools
- Local deterministic fallback logic so the project runs without paid APIs
- Optional API-key mode hook inside `ChatbotEngine` for plugging in external LLM providers

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000

## API examples

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Help me design a chatbot product"}'
```

```bash
curl -X POST http://127.0.0.1:8000/api/music \
  -H 'Content-Type: application/json' \
  -d '{"genre":"edm","mood":"euphoric","theme":"new beginnings"}'
```

## Tests

```bash
pytest
```

## Notes

This is a functional prototype, not a full foundation model. To approach production quality similar to ChatGPT or Suno, add:

- Model serving (LLM + music model)
- Prompt/chain orchestration
- User accounts and storage
- Safety and moderation
- GPU inference pipeline
