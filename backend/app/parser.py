import io

from docx import Document
from pypdf import PdfReader


def extract_text(name: str, data: bytes) -> str:
    ext = "." + name.lower().rsplit(".", 1)[-1] if "." in name else ""
    if ext == ".pdf":
        text = "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)
    elif ext == ".docx":
        text = "\n".join(p.text for p in Document(io.BytesIO(data)).paragraphs)
    elif ext in (".txt", ".md"):
        text = data.decode("utf-8", "ignore")
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, TXT or MD.")
    return text.strip()
