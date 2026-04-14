from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    response: str
    sources: list[str] | None = None


class HealthResponse(BaseModel):
    status: str
    service: str
    python: str