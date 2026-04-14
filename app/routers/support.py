import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models import ChatRequest

router = APIRouter(prefix="/support", tags=["support"])


def _sse_payload(data: dict[str, str], event: str | None = None) -> str:
    chunks: list[str] = []
    if event:
        chunks.append(f"event: {event}")
    chunks.append(f"data: {json.dumps(data, ensure_ascii=False)}")
    return "\n".join(chunks) + "\n\n"


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    async def event_stream() -> AsyncGenerator[str, None]:
        message = request.message.strip() or "empty message"
        parts = [
            f"Echo: {message}",
            "This is a streaming response chunk.",
            "Sources: [placeholder]",
        ]

        yield _sse_payload({"status": "start"}, event="status")
        for idx, part in enumerate(parts, start=1):
            yield _sse_payload({"content": part, "index": str(idx)}, event="chunk")
            await asyncio.sleep(0.3)
        yield _sse_payload({"status": "done"}, event="status")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
