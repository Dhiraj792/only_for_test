# Backend Development Guide

## Overview

The Legal Advisor backend is built with FastAPI, providing a modern, async Python API with built-in validation, CORS support, and comprehensive error handling.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app & endpoints (154 lines)
│   └── rag.py               # RAG system implementation (125 lines)
├── run.py                   # Entry point script
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── __init__.py              # Package marker
```

## Architecture

### main.py
**FastAPI application with REST endpoints**

#### Key Features:
- **CORS Middleware**: Handles cross-origin requests
- **Input Validation**: Pydantic models with validators
- **Error Handling**: HTTPException with descriptive messages
- **Documentation**: Automatic OpenAPI/Swagger docs

#### Pydantic Models

**IngestRequest**
```python
class IngestRequest(BaseModel):
    doc_id: str  # Max 255 chars, alphanumeric
    text: str    # 10 to 1M characters
```

**ChatRequest**
```python
class ChatRequest(BaseModel):
    message: str  # 1-5000 chars, trimmed
    jurisdiction: str  # Default: "US"
    practice_area: str  # Default: "general"
```

**ChatResponse**
```python
class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    disclaimer: str
```

**Citation**
```python
class Citation(BaseModel):
    doc_id: str
    chunk_id: int
    score: float
```

#### Endpoints

**GET /health**
- Readiness check
- Response: `{"status": "ok", "version": "1.0.0"}`

**POST /ingest**
- Ingest a legal document
- Request: `IngestRequest`
- Response: `{"status": "indexed", "chunks": int, "doc_id": str, "message": str}`
- Validation:
  - `doc_id`: Alphanumeric, hyphens, underscores only
  - `text`: Minimum 10 chars, max 1M chars

**POST /chat**
- Query the legal advisor
- Request: `ChatRequest`
- Response: `ChatResponse`
- Validation:
  - Message: Non-empty, trimmed
  - Jurisdiction: 2-50 chars
  - Practice area: 1-50 chars
- Error handling:
  - Empty results: Return fallback message
  - API errors: 500 with descriptive message

**GET /stats**
- System statistics
- Response: `{"total_chunks": int, "indexed": bool, "message": str}`

### rag.py
**Retrieval-Augmented Generation system**

#### InMemoryLegalRAG Class

**Components:**
- `_chunks: List[Chunk]` - Indexed document chunks
- `_vectorizer: TfidfVectorizer` - Text vectorization
- `_matrix` - TF-IDF sparse matrix

**Methods:**

```python
def ingest(doc_id: str, text: str, chunk_size: int = 700) -> int:
    """Split text and index chunks"""
    # Returns number of chunks created
    
def retrieve(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Retrieve top-k relevant chunks"""
    # Returns sorted by cosine similarity score
    
def get_stats() -> Dict[str, Any]:
    """Get system statistics"""
```

**Algorithm: TF-IDF + Cosine Similarity**
1. **Vectorization**: TF-IDF converts text to sparse vectors
2. **Query**: Transform user query to same vector space
3. **Similarity**: Compute cosine similarity between query and all chunks
4. **Ranking**: Return top-k chunks sorted by score

**Performance:**
- Indexing: O(n*m) where n=chunks, m=vocab
- Query: O(k*n) similarity computations
- Memory: Sparse matrix, efficient for large documents

## Configuration

### Environment Variables (.env)

```
# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# RAG
RAG_TOP_K=3
RAG_CHUNK_SIZE=700
```

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For Production:**
```python
allow_origins=os.getenv("CORS_ORIGINS", "").split(",")
```

## Development Setup

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Run Development Server

```bash
python run.py
# Starts on http://localhost:8000
```

### With Auto-Reload

```bash
python run.py  # Already configured in run.py
```

### Interactive API Docs

Navigate to: `http://localhost:8000/docs`
- Swagger UI for testing endpoints
- Automatic schema documentation
- Try-it-out feature

## API Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Ingest Document
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "us-contract-law",
    "text": "A contract is a binding agreement between parties..."
  }'
```

### Query Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What makes a contract valid?",
    "jurisdiction": "US",
    "practice_area": "contract"
  }'
```

### Get Stats
```bash
curl http://localhost:8000/stats
```

## Error Handling

### Input Validation
Pydantic validators catch invalid input:

```python
@validator("message")
def validate_message(cls, v):
    if len(v.strip()) == 0:
        raise ValueError("Message cannot be empty")
    return v.strip()
```

### HTTP Exceptions
```python
try:
    count = rag.ingest(doc_id, text)
except Exception as e:
    raise HTTPException(
        status_code=500, 
        detail=f"Failed to ingest: {str(e)}"
    )
```

### Response Codes
- `200`: Success
- `400`: Validation error
- `422`: Unprocessable entity (Pydantic validation)
- `500`: Server error

## Performance Optimization

### TF-IDF Configuration
```python
TfidfVectorizer(
    stop_words="english",      # Ignore common words
    max_features=5000,         # Limit vocabulary
    lowercase=True,            # Normalize text
    strip_accents="unicode",   # Remove accents
)
```

### Chunking Strategy
- Default size: 700 characters
- Configurable per document
- Keeps context window reasonable

### Caching (Future)
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def retrieve_cached(query: str, top_k: int = 3):
    return rag.retrieve(query, top_k)
```

## Testing

### Unit Tests (pytest)

```bash
pip install pytest pytest-asyncio
```

```python
# test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ingest():
    response = client.post("/ingest", json={
        "doc_id": "test-doc",
        "text": "This is a test document with enough content."
    })
    assert response.status_code == 200
    assert "chunks" in response.json()

def test_chat():
    # First ingest
    client.post("/ingest", json={
        "doc_id": "test",
        "text": "Contracts require agreement between parties."
    })
    
    # Then query
    response = client.post("/chat", json={
        "message": "What is a contract?",
        "jurisdiction": "US"
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
```

### Run Tests
```bash
pytest -v
```

## Production Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

### Build & Run
```bash
docker build -t legal-advisor .
docker run -p 8000:8000 legal-advisor
```

### Environment for Production
```bash
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
CORS_ORIGINS=https://yourdomain.com
```

### Gunicorn (Production ASGI Server)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## Monitoring & Logging

### Add Logging
```python
import logging

logger = logging.getLogger(__name__)

@app.post("/chat")
def chat(payload: ChatRequest) -> ChatResponse:
    logger.info(f"Chat request: {payload.message}")
    # ...
    logger.error(f"Chat failed: {str(e)}")
```

### Metrics (Future)
- Request count
- Response time
- Error rate
- Cache hit rate
- Document ingestion rate

## Security Best Practices

### 1. CORS (Cross-Origin Resource Sharing)
```python
# Current (DEV): allow_origins=["*"]
# Production: Configure specific origins
```

### 2. Input Validation
- All endpoints use Pydantic
- Type hints enforce correctness
- Max length constraints prevent abuse

### 3. Rate Limiting (Future)
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
def chat(...):
    pass
```

### 4. API Key Authentication (Future)
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/chat", security=security)
def chat(credentials: HTTPAuthCredentials):
    if credentials.credentials != VALID_KEY:
        raise HTTPException(401)
    # ...
```

### 5. Request Timeout
```python
import asyncio

@app.post("/chat")
async def chat(payload: ChatRequest):
    try:
        result = await asyncio.wait_for(
            process_query(payload),
            timeout=30.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(504, "Request timeout")
```

## Troubleshooting

### Import Errors
```bash
# Check Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"

# Or run from project root
python -m backend.run
```

### Memory Issues
- Reduce `max_features` in TfidfVectorizer
- Implement chunking strategy
- Use streaming for large documents

### Slow Queries
- Check document count with `/stats`
- Reduce `top_k` parameter
- Add query caching

## Future Enhancements

- Vector embeddings (semantic search)
- Semantic cache for repeated queries
- Document metadata extraction
- Async document processing
- Database storage instead of in-memory
- Real-time document updates
- Query analytics
- A/B testing framework
