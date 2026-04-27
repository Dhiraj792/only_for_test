# Legal Advisor Chatbot (End-to-End Project Starter)

This repository is a production-style starter for a **legal advisor chatbot** with:

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

