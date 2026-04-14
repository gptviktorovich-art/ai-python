## Phase 0 Week 2 — ChromaDB + RAG

Реализован настоящий Retrieval-Augmented Generation:
- Локальная векторная база Chroma
- Embeddings через sentence-transformers
- Streaming-ответы с релевантными чанками

# ai-python-bootcamp

Phase 0: Python Mastery for AI Engineer  
Проект создан в рамках курса "от Senior Frontend до AI Engineer"

## Как запустить

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Открыть: http://127.0.0.1:8000/docs  
Эндпоинт: `POST /support/chat` (streaming)
