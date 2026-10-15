import json

from openai import OpenAI

from .config import settings

_client = None


def client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is not set on the server.")
        _client = OpenAI(api_key=settings.groq_api_key, base_url="https://api.groq.com/openai/v1")
    return _client


def chat_json(system: str, user: str) -> dict:
    r = client().chat.completions.create(
        model=settings.model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    return json.loads(r.choices[0].message.content)


def chat_text(system: str, user: str) -> str:
    r = client().chat.completions.create(
        model=settings.model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.3,
    )
    return r.choices[0].message.content.strip()
