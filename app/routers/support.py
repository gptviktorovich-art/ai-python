from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..models import ChatRequest
from ..rag import retrieve, add_documents
import asyncio
import json

router = APIRouter()

# При запуске сервера сразу добавляем тестовые документы
add_documents([
    "Для сброса пароля перейдите по ссылке в письме, которое мы отправили на вашу корпоративную почту.",
    "Проблемы с VPN? Убедитесь, что установлен актуальный сертификат и клиент OpenVPN. Перезапустите приложение.",
    "Ticket создаётся автоматически в Jira. Номер SUP-XXXX. Оператор свяжется с вами в течение 15 минут."
], metadatas=[
    {"source": "wiki_password"},
    {"source": "wiki_vpn"},
    {"source": "jira"}
])


@router.post("/chat")
async def chat(request: ChatRequest):
    """RAG-чат техподдержки"""
    async def event_stream():
        # Получаем релевантные чанки из Chroma
        chunks = retrieve(request.message, n_results=3)
        
        for chunk in chunks:
            yield f"data: {json.dumps({'content': chunk})}\n\n"
            await asyncio.sleep(0.35)  # имитация "печатания"
        
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")