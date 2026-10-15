from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import db, generators, parser, vectorstore
from .config import settings

app = FastAPI(title="IQRHA API")
app.add_middleware(
    CORSMiddleware, allow_origins=settings.origins, allow_methods=["*"], allow_headers=["*"]
)
db.init()

MAX_BYTES = 10 * 1024 * 1024
MAX_CONTEXT = 12000


class Question(BaseModel):
    question: str


def get_context(doc_id: int, text: str) -> str:
    if len(text) <= MAX_CONTEXT:
        return text
    chunks = vectorstore.top_chunks(doc_id, "main concepts, definitions, key facts, processes", k=12)
    return "\n\n".join(chunks)[:MAX_CONTEXT]


def need_doc(doc_id: int) -> dict:
    doc = db.get_document(doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/documents")
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "File too large (max 10 MB)")
    try:
        text = parser.extract_text(file.filename or "", data)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception:
        raise HTTPException(422, "Could not read this file.")
    if len(text) < 50:
        raise HTTPException(422, "Couldn't find enough text in this file.")
    text = text[:150000]
    doc_id = db.add_document(file.filename, text)
    vectorstore.add_chunks(doc_id, text)
    return {"id": doc_id, "name": file.filename, "chars": len(text)}


@app.get("/api/documents")
def documents():
    return db.list_documents()


@app.get("/api/documents/{doc_id}/outputs/{kind}")
def cached(doc_id: int, kind: str):
    need_doc(doc_id)
    return {"data": db.get_output(doc_id, kind)}


@app.post("/api/documents/{doc_id}/generate/{kind}")
def generate(doc_id: int, kind: str, count: int = 10):
    if kind not in generators.KINDS:
        raise HTTPException(404, "Unknown output type")
    doc = need_doc(doc_id)
    count = max(3, min(count, 25))
    context = get_context(doc_id, doc["text"])
    try:
        data = generators.generate(kind, context, count)
    except RuntimeError as e:
        raise HTTPException(500, str(e))
    except Exception:
        raise HTTPException(502, "The AI service failed. Please try again.")
    db.save_output(doc_id, kind, data)
    return {"data": data}


@app.post("/api/documents/{doc_id}/ask")
def ask(doc_id: int, body: Question):
    need_doc(doc_id)
    if not body.question.strip():
        raise HTTPException(400, "Question is empty")
    try:
        chunks = vectorstore.top_chunks(doc_id, body.question, k=5)
        return {"answer": generators.answer(body.question, chunks)}
    except RuntimeError as e:
        raise HTTPException(500, str(e))
    except Exception:
        raise HTTPException(502, "The AI service failed. Please try again.")
