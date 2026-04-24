from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

from .rag import InMemoryLegalRAG


app = FastAPI(
    title="Legal Advisor API",
    version="1.0.0",
    description="AI-powered legal consultation API with retrieval-augmented generation"
)

# Enable CORS for all origins (configure as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = InMemoryLegalRAG()


class IngestRequest(BaseModel):
    doc_id: str = Field(..., description="Unique document identifier", min_length=1, max_length=255)
    text: str = Field(..., description="Full legal text", min_length=10, max_length=1_000_000)

    @validator("doc_id")
    def validate_doc_id(cls, v):
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("doc_id must be alphanumeric with hyphens or underscores")
        return v


class Citation(BaseModel):
    doc_id: str
    chunk_id: int
    score: float


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    jurisdiction: str = Field(default="US", min_length=2, max_length=50)
    practice_area: str = Field(default="general", min_length=1, max_length=50)

    @validator("message")
    def validate_message(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Message cannot be empty or whitespace-only")
        return v.strip()


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    disclaimer: str


@app.get("/health", tags=["Health"])
def health() -> dict:
    """Health check endpoint"""
    return {"status": "ok", "version": "1.0.0"}


@app.post("/ingest", response_model=dict, tags=["Documents"])
def ingest(payload: IngestRequest) -> dict:
    """
    Ingest a legal document for RAG retrieval.
    
    Args:
        payload: Document to ingest (doc_id and text)
    
    Returns:
        Status and number of chunks created
    """
    try:
        count = rag.ingest(payload.doc_id, payload.text)
        return {
            "status": "indexed",
            "chunks": count,
            "doc_id": payload.doc_id,
            "message": f"Successfully indexed {count} chunks"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(payload: ChatRequest) -> ChatResponse:
    """
    Chat with the legal advisor AI.
    
    Args:
        payload: Chat request with message, jurisdiction, and practice area
    
    Returns:
        ChatResponse with answer, citations, and disclaimer
    """
    try:
        # Retrieve relevant legal documents
        hits = rag.retrieve(payload.message, top_k=3)
        citations = [
            Citation(doc_id=h["doc_id"], chunk_id=h["chunk_id"], score=h["score"])
            for h in hits
        ]

        # Generate answer based on retrieved documents
        if not hits:
            answer = (
                "I could not find grounded legal text for this question. "
                "Please ingest jurisdiction-specific legal documents first. "
                f"(Jurisdiction: {payload.jurisdiction}, Practice Area: {payload.practice_area})"
            )
        else:
            snippets = "\n\n".join(
                f"[{i+1}] From {h['doc_id']} (Relevance: {h['score']:.1%}):\n{h['text'][:250]}..."
                for i, h in enumerate(hits)
            )
            answer = (
                f"Based on retrieved legal sources for {payload.jurisdiction} law in {payload.practice_area}:\n\n"
                f"{snippets}\n\n"
                "For a comprehensive answer, please review the full documents above or consult a qualified attorney."
            )

        return ChatResponse(
            answer=answer,
            citations=citations,
            disclaimer=(
                "DISCLAIMER: This assistant provides general legal information only, not legal advice. "
                "The responses are based on ingested documents and should not be relied upon for legal decisions. "
                "Always consult a licensed attorney in your jurisdiction for advice specific to your situation."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat request failed: {str(e)}")


@app.get("/stats", tags=["Admin"])
def get_stats() -> dict:
    """Get RAG system statistics"""
    return {
        "total_chunks": len(rag._chunks),
        "indexed": rag._matrix is not None,
        "message": "System is ready for queries"
    }


