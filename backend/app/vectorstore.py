import chromadb

from .config import settings

_col = None


def col():
    global _col
    if _col is None:
        client = chromadb.PersistentClient(path=settings.chroma_path)
        _col = client.get_or_create_collection("iqrha")  # default local MiniLM embeddings
    return _col


def chunk(text: str, size: int = 1000, overlap: int = 150):
    out, i = [], 0
    while i < len(text):
        out.append(text[i : i + size])
        i += size - overlap
    return out


def add_chunks(doc_id: int, text: str):
    chunks = chunk(text)
    col().add(
        ids=[f"{doc_id}-{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[{"doc_id": doc_id}] * len(chunks),
    )


def top_chunks(doc_id: int, query: str, k: int = 6):
    res = col().query(query_texts=[query], n_results=k, where={"doc_id": doc_id})
    return res["documents"][0]
