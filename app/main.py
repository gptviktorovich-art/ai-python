from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.models import HealthResponse
from app.routers.support import router as support_router

app = FastAPI(title="AI Support Backend - Phase 0")
FRONTEND_INDEX = Path("frontend/index.html")


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="ai-support-backend", python="3.12")


@app.get("/", include_in_schema=False)
async def frontend() -> FileResponse:
    return FileResponse(FRONTEND_INDEX)


app.include_router(support_router)