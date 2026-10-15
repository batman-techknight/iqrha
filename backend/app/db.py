import json
import sqlite3
from contextlib import contextmanager

from .config import settings


@contextmanager
def conn():
    c = sqlite3.connect(settings.db_path)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()


def init():
    with conn() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS outputs (
                doc_id INTEGER NOT NULL,
                kind TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (doc_id, kind)
            );
            """
        )


def add_document(name: str, text: str) -> int:
    with conn() as c:
        cur = c.execute("INSERT INTO documents (name, text) VALUES (?, ?)", (name, text))
        return cur.lastrowid


def list_documents():
    with conn() as c:
        rows = c.execute(
            "SELECT id, name, length(text) AS chars, created_at FROM documents ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def get_document(doc_id: int):
    with conn() as c:
        row = c.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
        return dict(row) if row else None


def save_output(doc_id: int, kind: str, data: dict):
    with conn() as c:
        c.execute(
            "INSERT OR REPLACE INTO outputs (doc_id, kind, data) VALUES (?, ?, ?)",
            (doc_id, kind, json.dumps(data)),
        )


def get_output(doc_id: int, kind: str):
    with conn() as c:
        row = c.execute(
            "SELECT data FROM outputs WHERE doc_id = ? AND kind = ?", (doc_id, kind)
        ).fetchone()
        return json.loads(row["data"]) if row else None
