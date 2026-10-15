# IQRHA – Personalized AI Study Assistant

Upload notes (PDF, DOCX, TXT, MD) → get easy notes, flashcards, a final-test quiz, and document Q&A.

Stack: FastAPI · SQLite · ChromaDB · Groq (free LLM API) · React (Vite) · pytest

## Run locally

Backend (Python 3.11 recommended):

    cd backend
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env             # add your GROQ_API_KEY (free at console.groq.com)
    uvicorn app.main:app --reload --port 8000

Tests:

    cd backend && pytest -v

Frontend (Node 18+):

    cd frontend
    npm install
    npm run dev                      # http://localhost:5173

## Deploy

1. Push to GitHub.
2. Backend on Render: root dir `backend`, build `pip install -r requirements.txt`,
   start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`,
   env: GROQ_API_KEY, LLM_MODEL, PYTHON_VERSION=3.11.9.
3. Frontend on Vercel: root dir `frontend`, env `VITE_API_URL=<your Render URL>`.
4. On Render set `CORS_ORIGINS=<your Vercel URL>` and redeploy.

Note: Render free tier has an ephemeral disk, so data resets on restart/redeploy.
