"""Groq (OpenAI-compatible) client for structured field extraction —
same provider choice as the RAG module's generation client.
"""
import json
import os

from openai import OpenAI

from structuring.prompt_builder import SYSTEM_PROMPT, build_user_message

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_TOKENS = 1024
TEMPERATURE = 0.0


def extract_fields(raw_text: str, schema_fields: dict) -> dict:
    client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url=GROQ_BASE_URL)
    user_message = build_user_message(raw_text, schema_fields)

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

    raw_output = response.choices[0].message.content.strip()
    return json.loads(raw_output)
