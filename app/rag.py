from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from typing import List

# Лёгкая и быстрая модель эмбеддингов (отлично работает на RTX 3070)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Создаём постоянную базу (будет храниться в папке chroma_db)
client = PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="support_kb")


def add_documents(docs: List[str], metadatas: List[dict] | None = None):
    """Добавляем документы в векторную базу (индексация)"""
    if metadatas is None:
        metadatas = [{} for _ in docs]
    
    # Превращаем текст в вектора
    embeddings = embedder.encode(docs).tolist()
    
    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=[f"doc_{i}" for i in range(len(docs))]
    )
    print(f"Added {len(docs)} documents to Chroma")


def retrieve(query: str, n_results: int = 3) -> List[str]:
    """Ищем самые релевантные чанки по запросу пользователя"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]  # возвращаем список строк