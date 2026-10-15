from . import llm

KINDS = ("notes", "flashcards", "quiz")

SYSTEM = (
    "You are IQRHA, a friendly study tutor. Use ONLY the provided material. "
    "Explain in simple, clear language a student can learn quickly. Reply with valid JSON only."
)

TASKS = {
    "notes": (
        "Create easy-to-learn study notes. JSON shape: "
        '{"title": str, "summary": str (3-4 simple sentences), '
        '"sections": [{"heading": str, "points": [str]}], '
        '"key_terms": [{"term": str, "definition": str}]}'
    ),
    "flashcards": (
        "Create {n} flashcards covering the most important ideas. JSON shape: "
        '{"cards": [{"front": str, "back": str}]}'
    ),
    "quiz": (
        "Create {n} multiple-choice questions for a final assessment, mixed difficulty. "
        "Each has exactly 4 options. JSON shape: "
        '{"questions": [{"question": str, "options": [str, str, str, str], '
        '"answer": int (index 0-3), "explanation": str}]}'
    ),
}


def generate(kind: str, context: str, n: int = 10) -> dict:
    task = TASKS[kind].replace("{n}", str(n))
    data = llm.chat_json(SYSTEM, f"{task}\n\nMATERIAL:\n{context}")
    if kind == "quiz":
        data["questions"] = [
            q
            for q in data.get("questions", [])
            if isinstance(q.get("options"), list)
            and len(q["options"]) == 4
            and isinstance(q.get("answer"), int)
            and 0 <= q["answer"] < 4
        ]
    return data


def answer(question: str, chunks: list[str]) -> str:
    context = "\n---\n".join(chunks)
    system = (
        "You are IQRHA, a study tutor. Answer using only the material. "
        "If the answer isn't in it, say so. Keep it short and clear."
    )
    return llm.chat_text(system, f"MATERIAL:\n{context}\n\nQUESTION: {question}")
