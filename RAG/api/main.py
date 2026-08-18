"""Single-endpoint FastAPI app for the MSME compliance RAG chatbot."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from generation.llm_client import generate_answer
from ingestion.embed_and_store import embed_texts, get_chroma_collection
from retrieval.filters import build_where_filter
from retrieval.hybrid_search import hybrid_search
from retrieval.rerank import rerank

PROFILES_PATH = Path(__file__).resolve().parent.parent / "profiles" / "sample_profiles.json"
PROFILES = json.loads(PROFILES_PATH.read_text())

app = FastAPI(title="MSME Compliance RAG Chatbot")


class ChatRequest(BaseModel):
    business_id: str
    question: str


class SourceOut(BaseModel):
    source_name: str
    last_verified_date: str
    source_url: str = ""


class ChatResponse(BaseModel):
    answer: str
    grounded: bool
    sources: list[SourceOut]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    profile = PROFILES.get(req.business_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"Unknown business_id: {req.business_id}")

    try:
        collection = get_chroma_collection()
        query_embedding = embed_texts([req.question])[0]

        where = build_where_filter(state=profile["state"], industry=profile["industry"])
        candidates = hybrid_search(collection, req.question, query_embedding, where=where, top_k=10)
        top_chunks = rerank(req.question, candidates, top_n=4)

        result = generate_answer(req.question, profile, top_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat pipeline failed: {e}")

    return ChatResponse(
        answer=result.get("answer", ""),
        grounded=result.get("grounded", False),
        sources=[SourceOut(**s) for s in result.get("sources", [])],
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def chat_ui():
    return FileResponse(Path(__file__).resolve().parent / "static_chat.html")
