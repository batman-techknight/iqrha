TEXT = ("Photosynthesis is the process by which plants convert light into chemical energy. " * 3).encode()


def upload(client):
    return client.post("/api/documents", files={"file": ("bio.txt", TEXT, "text/plain")})


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_upload_and_list(client):
    r = upload(client)
    assert r.status_code == 200
    assert any(d["id"] == r.json()["id"] for d in client.get("/api/documents").json())


def test_rejects_bad_type(client):
    r = client.post("/api/documents", files={"file": ("x.exe", b"abc" * 30, "application/octet-stream")})
    assert r.status_code == 400


def test_rejects_tiny_file(client):
    r = client.post("/api/documents", files={"file": ("a.txt", b"hi", "text/plain")})
    assert r.status_code == 422


def test_flashcards_generate_and_cache(client, fake_llm):
    fake_llm({"cards": [{"front": "What is photosynthesis?", "back": "Light to energy"}]})
    doc_id = upload(client).json()["id"]
    r = client.post(f"/api/documents/{doc_id}/generate/flashcards?count=5")
    assert r.status_code == 200
    cached = client.get(f"/api/documents/{doc_id}/outputs/flashcards").json()["data"]
    assert cached["cards"][0]["back"] == "Light to energy"


def test_quiz_drops_malformed_questions(client, fake_llm):
    good = {"question": "Q?", "options": ["a", "b", "c", "d"], "answer": 2, "explanation": "e"}
    bad = {"question": "Bad", "options": ["a", "b"], "answer": 5, "explanation": "e"}
    fake_llm({"questions": [good, bad]})
    doc_id = upload(client).json()["id"]
    data = client.post(f"/api/documents/{doc_id}/generate/quiz").json()["data"]
    assert len(data["questions"]) == 1


def test_unknown_kind_and_missing_doc(client):
    assert client.post("/api/documents/1/generate/nope").status_code == 404
    assert client.post("/api/documents/9999/generate/notes").status_code == 404


def test_ask(client, fake_llm):
    fake_llm()
    doc_id = upload(client).json()["id"]
    r = client.post(f"/api/documents/{doc_id}/ask", json={"question": "Why?"})
    assert r.json()["answer"] == "Because science."
