from fastapi import FastAPI

from app.routers.support import router as support_router

app = FastAPI(title="AI Support Backend - Phase 0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "python": "3.12"}


app.include_router(support_router)