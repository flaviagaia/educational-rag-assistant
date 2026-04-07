from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.generation import build_grounded_answer


BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Educational RAG Assistant", version="0.1.0")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=5)
    top_k: int = Field(default=3, ge=1, le=5)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(request: AskRequest) -> dict:
    return build_grounded_answer(BASE_DIR, query=request.question, top_k=request.top_k)
