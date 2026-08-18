"""Thin wrapper around the Groq API (OpenAI-compatible) for grounded
generation with structured (JSON) output.
"""
import json
import os

from openai import OpenAI

from generation.prompt_builder import SYSTEM_PROMPT, build_user_message

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_TOKENS = 1024
TEMPERATURE = 0.2


def generate_answer(question: str, profile: dict, chunks: list[dict]) -> dict:
    client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url=GROQ_BASE_URL)
    user_message = build_user_message(question, profile, chunks)

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw_text = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed = {
            "answer": raw_text,
            "grounded": False,
            "sources": [],
        }

    return parsed
