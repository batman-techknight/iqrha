import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    db_path = os.getenv("DB_PATH", "iqrha.db")
    chroma_path = os.getenv("CHROMA_PATH", "chroma_data")
    origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]


settings = Settings()
