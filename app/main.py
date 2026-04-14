from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
from .models import ChatRequest
import json

app = FastAPI(title="AI Support Backend - Phase 0")

@app.get("/health")
async def health():
    return {"status": "ok", "python": "3.12"}

@app.post("/support/chat")
async def chat(request: ChatRequest):
    async def event_stream():
        # Симуляция RAG (пока заглушка)
        chunks = [
            "RESPONSE.",
            "SOURCES."
        ]
        for chunk in chunks:
            yield f"data: {json.dumps({'content': chunk})}\n\n"
            await asyncio.sleep(0.3)
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")