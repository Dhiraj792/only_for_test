# Legal Advisor - AI-Powered Legal Consultation Platform

An industry-ready legal consultation chatbot powered by Retrieval-Augmented Generation (RAG). This platform provides instant legal advice with supporting citations from ingested legal documents.

## Features

✨ **Core Features**
- AI-powered legal consultation with retrieval-augmented generation
- Citation tracking and source attribution
- Multi-jurisdiction support (US, Canada, UK, Australia, International)
- Practice area filtering (Contract, Criminal, Family, Employment, Corporate, IP)
- Chat history with persistent storage
- Dark mode support
- Mobile-responsive design
- Production-ready error handling and validation

## Project Structure

```
.
├── frontend/                    # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/         # Reusable React components
│   │   │   ├── ChatInput.tsx   # Message input with auto-resize
│   │   │   ├── Filters.tsx     # Jurisdiction & practice area selectors
│   │   │   ├── ResponseDisplay.tsx  # Answer & citations display
│   │   │   └── ChatHistory.tsx # Conversation history manager
│   │   ├── lib/
│   │   │   └── utils.ts        # Utility functions (cn helper)
│   │   ├── App.tsx             # Main application component
│   │   ├── main.tsx            # React entry point
│   │   └── globals.css         # Tailwind directives & design tokens
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   └── package.json
│
├── backend/                     # FastAPI + Python
│   ├── app/
│   │   ├── main.py            # FastAPI application with CORS
│   │   └── rag.py             # RAG system (TF-IDF + similarity)
│   ├── run.py                 # Entry point for running server
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Example environment variables
│   └── __init__.py
│
└── README.md
```

## Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS 3** - Utility-first styling
- **Vite** - Fast build tool and dev server
- **Lucide React** - Icon library
- **LocalStorage** - Persistent chat history

### Backend
- **FastAPI 0.115** - Modern Python web framework
- **Pydantic** - Data validation
- **Scikit-learn** - TF-IDF vectorization & similarity
- **NumPy** - Numerical computing
- **Uvicorn** - ASGI server
- **Python 3.8+** - Runtime

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.8+
- npm or yarn

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run.py
```

The API will be available at `http://localhost:8000`

### Environment Configuration

Backend `.env` file (optional):
```
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## API Documentation

### Endpoints

#### Health Check
```
GET /health
```
Returns server status.

#### Ingest Document
```
POST /ingest
Content-Type: application/json

{
  "doc_id": "us-contract-law-2024",
  "text": "Full legal document text..."
}
```
Ingests a legal document and splits it into retrievable chunks.

#### Chat
```
POST /chat
Content-Type: application/json

{
  "message": "What are the key requirements for a valid contract?",
  "jurisdiction": "US",
  "practice_area": "contract"
}
```
Queries the legal advisor and returns answers with citations.

**Response:**
```json
{
  "answer": "Based on retrieved legal sources...",
  "citations": [
    {
      "doc_id": "us-contract-law-2024",
      "chunk_id": 0,
      "score": 0.85
    }
  ],
  "disclaimer": "This assistant provides general legal information..."
}
```

#### Statistics
```
GET /stats
```
Returns RAG system statistics.

## Component Documentation

### Frontend Components

#### ChatInput
Textarea with auto-resizing, Ctrl+Enter submit, and loading state.
- Props: `onSend`, `disabled`, `isLoading`
- Features: Auto-expand, keyboard shortcuts, accessibility

#### ResponseDisplay
Displays AI-generated legal answer with citations and disclaimer.
- Props: `answer`, `citations`, `disclaimer`
- Features: Citation numbering, relevance scores, styled disclaimer

#### Filters
Jurisdiction and practice area selection dropdowns.
- Props: `jurisdiction`, `practiceArea`, change handlers, `disabled`
- Options: 5 jurisdictions × 7 practice areas

#### ChatHistory
Persistent chat history sidebar with delete and restore capabilities.
- Props: `messages`, selection/deletion handlers, `currentMessageId`
- Storage: LocalStorage (no server required)

### Backend Modules

#### RAG (Retrieval-Augmented Generation)
- **InMemoryLegalRAG class**: Main RAG system
- **Methods**:
  - `ingest()`: Split and index documents
  - `retrieve()`: Return top-k relevant chunks
  - `get_stats()`: System statistics
- **Algorithm**: TF-IDF with cosine similarity

## Key Improvements Made

### Frontend
- ✅ Professional component architecture (4 reusable components)
- ✅ Tailwind CSS + design tokens for consistent styling
- ✅ Dark mode support with CSS custom properties
- ✅ Mobile-first responsive design
- ✅ Persistent chat history with localStorage
- ✅ Proper TypeScript types and interfaces
- ✅ Accessibility features (ARIA labels, semantic HTML)
- ✅ Loading states and error handling

### Backend
- ✅ CORS middleware enabled for cross-origin requests
- ✅ Pydantic validators for input validation
- ✅ Comprehensive error handling with HTTP exceptions
- ✅ Request/response documentation
- ✅ Improved answer generation with better formatting
- ✅ Enhanced RAG module with documentation and stats
- ✅ Config file support (.env)

## Development Workflow

### Running Locally

1. **Terminal 1 - Backend:**
```bash
cd backend
python run.py
# API at http://localhost:8000
```

2. **Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# App at http://localhost:5173
```

3. **Test API:**
   - Access Swagger UI: http://localhost:8000/docs
   - Ingest a sample document via `/ingest`
   - Query via the frontend or API

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
# Output: dist/
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python run.py --host 0.0.0.0 --port 8000
```

## Example Usage

### Ingest a Legal Document

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "contract-law-basics",
    "text": "A contract is a legally binding agreement..."
  }'
```

### Query the Legal Advisor

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What makes a contract valid?",
    "jurisdiction": "US",
    "practice_area": "contract"
  }'
```

## Error Handling

The application includes comprehensive error handling:

- **Frontend**: Try-catch blocks, error state management, user-friendly messages
- **Backend**: HTTP exception handling, input validation, detailed error responses
- **API**: RESTful status codes (200, 400, 500) with descriptive messages

## Performance Considerations

- TF-IDF vectorization is computed at ingestion time for fast retrieval
- Chat history stored in browser localStorage (no server roundtrips)
- Lazy component rendering with React
- Tailwind CSS purges unused styles in production
- Vite provides code splitting and lazy loading

## Security Considerations

⚠️ **Important for Production:**
- CORS is currently open to all origins (`allow_origins=["*"]`)
- Configure `CORS_ORIGINS` in .env for production
- Validate and sanitize all user inputs
- Never expose sensitive legal information
- Implement authentication/authorization for production
- Use HTTPS in production
- Consider rate limiting and request throttling
- Add API key authentication

## Future Enhancements

- Vector embeddings (OpenAI, HuggingFace) for better semantic search
- Multi-document Q&A with context awareness
- User authentication and personal legal histories
- Export functionality (PDF, Word)
- Real-time collaboration features
- Improved RAG with parent document retrieval
- Legal document summarization
- Citation link previews
- Analytics dashboard

## Troubleshooting

### CORS Error
- Ensure backend CORS middleware is enabled
- Check `CORS_ORIGINS` environment variable
- Frontend proxy configured in vite.config.ts

### Empty Results
- Verify documents are ingested via `/ingest` endpoint
- Check `/stats` endpoint for indexed chunk count
- Query should match document content

### Build Issues
- Delete node_modules and package-lock.json, then `npm install`
- Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`
- Ensure Python 3.8+ and Node 18+

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Submit a pull request

---

**Disclaimer:** This is an educational tool. For actual legal advice, consult with a licensed attorney.
- **Frontend**: React + Vite
- **Backend**: FastAPI
- **LLM/RAG stack**: Retrieval-Augmented Generation with legal document chunks
- **Training pipeline**: Supervised fine-tuning (SFT) data preparation + LoRA training script template
- **Deployment**: Docker Compose skeleton

> ⚠️ Important: This is an educational engineering template, **not legal advice**. Keep a compliance review step with a licensed attorney before any real-world launch.

## 1) Recommended Architecture

1. **UI layer (React)**
   - Chat interface with conversation history
   - “Jurisdiction” and “Practice area” selectors
   - Display citations and confidence labels

2. **API layer (FastAPI)**
   - `/chat`: receives user query and metadata
   - `/ingest`: indexes legal documents
   - `/health`: readiness check

3. **Retrieval layer**
   - Chunk legal texts and create vector representations
   - Retrieve top-k relevant chunks for each user query
   - Return citations (document name + chunk id)

4. **Generation layer**
   - Prompt template with strict legal-safe policy
   - Use LLM to answer with “not legal advice” disclaimer
   - Refuse unsupported/high-risk requests

5. **Training layer**
   - Build instruction dataset from curated legal Q/A
   - Fine-tune with LoRA on instruction format
   - Evaluate with policy and hallucination tests

6. **Safety layer**
   - Jurisdiction gating and escalation to human counsel
   - Content filters (sensitive, illegal, harmful requests)
   - Logging + audit trails + model/card versioning

## 2) Tech Stack (Best Practical Choices)

### Frontend
- **React + TypeScript + Vite**: fast dev, clean component model
- **Tailwind CSS** (optional): rapid UI building
- **SWR/React Query**: robust API data handling

### Backend
- **FastAPI**: async, type-safe, excellent for AI APIs
- **Pydantic**: strict request/response schemas
- **Uvicorn/Gunicorn**: production serving

### Retrieval & Model
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2` for cheap baseline)
- **Vector DB**: FAISS (local), then move to pgvector/Pinecone/Weaviate in production
- **LLM options**:
  - Cloud: GPT-4.1/GPT-4o class models for quality
  - Self-hosted: Llama 3.x Instruct / Mistral Instruct with vLLM

### Training
- **Transformers + PEFT + TRL** for LoRA SFT
- **Datasets** for pipeline management
- **Weights & Biases** for experiment tracking

## 3) Legal Data Strategy (Critical)

- Use **licensed / permissive** datasets only.
- Include:
  - Statutes/regulations by jurisdiction
  - Case law summaries (where licensing allows)
  - Internal policy/procedure docs (if enterprise)
- Every source gets metadata:
  - `jurisdiction`, `practice_area`, `effective_date`, `source_url`, `version`

## 4) Model Training Plan (High Level)

1. Collect and clean domain Q/A + statute interpretation examples
2. Convert to instruction format (`system`, `user`, `assistant`)
3. Fine-tune with LoRA
4. Evaluate on:
   - factuality
   - citation correctness
   - refusal behavior
   - harmful prompt resistance
5. Add RAG grounding + policy prompts
6. Human legal review before release

## 5) Run the starter

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Training scripts
```bash
cd training
python prepare_dataset.py
python train_lora.py
```

## 6) Production checklist

- [ ] Prompt injection defenses
- [ ] Data access controls (RBAC)
- [ ] PII redaction pipeline
- [ ] Full observability (latency, token usage, retrieval hit quality)
- [ ] Human escalation workflow
- [ ] Region/jurisdiction-specific model routing
- [ ] Legal disclaimer and terms acceptance

