from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .rag import InMemoryLegalRAG


app = FastAPI(title="Legal Advisor API", version="0.1.0")
rag = InMemoryLegalRAG()


class IngestRequest(BaseModel):
    doc_id: str = Field(..., description="Unique document identifier")
    text: str = Field(..., description="Full legal text")


class Citation(BaseModel):
    doc_id: str
    chunk_id: int
    score: float


class ChatRequest(BaseModel):
    message: str
    jurisdiction: str = "US"
    practice_area: str = "general"


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    disclaimer: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(payload: IngestRequest) -> dict:
    count = rag.ingest(payload.doc_id, payload.text)
    return {"status": "indexed", "chunks": count}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    hits = rag.retrieve(payload.message, top_k=3)
    citations = [Citation(doc_id=h["doc_id"], chunk_id=h["chunk_id"], score=h["score"]) for h in hits]

    if not hits:
        answer = (
            "I could not find grounded legal text for this question yet. "
            "Please ingest jurisdiction-specific legal documents and try again."
        )
    else:
        snippets = "\n".join(f"- {h['text'][:220]}" for h in hits)
        answer = (
            f"Based on retrieved legal sources for jurisdiction={payload.jurisdiction} and "
            f"practice_area={payload.practice_area}, here is a grounded summary:\n{snippets}"
        )

    return ChatResponse(
        answer=answer,
        citations=citations,
        disclaimer=(
            "This assistant provides general legal information, not legal advice. "
            "Consult a licensed attorney for advice specific to your matter."
        ),
    )
