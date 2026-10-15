import os
import tempfile

_tmp = tempfile.mkdtemp()
os.environ["DB_PATH"] = os.path.join(_tmp, "test.db")
os.environ["CHROMA_PATH"] = os.path.join(_tmp, "chroma")

import pytest
from fastapi.testclient import TestClient

from app import llm, vectorstore
from app.main import app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(vectorstore, "add_chunks", lambda *a, **k: None)
    monkeypatch.setattr(vectorstore, "top_chunks", lambda *a, **k: ["some chunk"])
    return TestClient(app)


@pytest.fixture
def fake_llm(monkeypatch):
    def _set(payload=None, text="Because science."):
        monkeypatch.setattr(llm, "chat_json", lambda s, u: payload)
        monkeypatch.setattr(llm, "chat_text", lambda s, u: text)

    return _set
