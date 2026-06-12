"""AI service - OpenAI GPT-4o-mini integration for chat responses."""

from typing import List, Dict
import os
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # cheapest model

SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant. Answer concisely and accurately. "
    "Be respectful. Keep responses natural and conversational."
)


def _get_client() -> OpenAI:
    api_key = OPENAI_API_KEY
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Set it via environment variable or a .env file. "
            "Get one at https://platform.openai.com/api-keys"
        )
    return OpenAI(api_key=api_key)


def get_ai_response(message, conversation_history=None):
    client = _get_client()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if conversation_history:
        messages.extend(conversation_history[-10:])  # keep last 10 for cost control
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content


def get_conversation_context(db, conversation_id):
    from app.models.message import Message

    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .limit(20)
        .all()
    )
    return [
        {"role": "user" if m.sender == "user" else "assistant", "content": m.content}
        for m in msgs
    ]
