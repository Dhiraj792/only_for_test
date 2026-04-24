# How to Run the Legal Advisor Project

This guide walks you through running the complete Legal Advisor application.

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

## Quick Start (2 Minutes)

### Step 1: Start Backend (Terminal 1)

```bash
cd backend
python start.py
```

Expected output:
```
╔════════════════════════════════════════════════════════════╗
║           Legal Advisor - Backend Server                   ║
║                                                            ║
║   Starting FastAPI server with pre-loaded legal docs      ║
║   API Documentation: http://localhost:8000/docs           ║
║   Health Check: http://localhost:8000/health              ║
╚════════════════════════════════════════════════════════════╝

[INIT] Loading sample legal documents...
      ✓ us-contract-law
      ✓ us-employment-law
      ✓ us-property-law
      ✓ us-criminal-procedure
      ✓ contract-templates
[INIT] Ready: 175 chunks indexed from 5 documents

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend
npm install  # Only first time
npm run dev
```

Expected output:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

### Step 3: Open Browser

Visit: http://localhost:5173

You should see:
- Green "Connected" badge in the header
- Chat interface enabled
- Ready to ask legal questions

## How to Use

1. **Select jurisdiction** (top dropdown, default: US)
2. **Select practice area** (contract, employment, property, criminal, general)
3. **Type your legal question** in the text area
4. **Press Enter or click Send**
5. **View answer** with citations and relevance scores

## Example Questions to Try

- "What are the key elements of a valid contract?"
- "What is wrongful termination?"
- "What is adverse possession in property law?"
- "What are Miranda rights?"
- "What does a landlord-tenant relationship entail?"

## Troubleshooting

### Backend Connection Issues

**Problem:** Frontend shows "Disconnected" badge
**Solution:** 
1. Ensure backend is running (Terminal 1)
2. Check no other service uses port 8000
3. Wait 3 seconds for reconnection attempt
4. Check console for error messages

**Try:** `curl http://localhost:8000/health`

Expected response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "chunks_indexed": 175,
  "documents_loaded": 5
}
```

### Frontend Not Loading

**Problem:** Blank page or errors
**Solution:**
1. Ensure frontend process is running (Terminal 2)
2. Check no other service uses port 5173
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try a different browser

### API Documentation

Access Swagger UI at: http://localhost:8000/docs

### Stopping the Servers

- Backend: Press Ctrl+C in Terminal 1
- Frontend: Press Ctrl+C in Terminal 2

## What's Pre-Loaded

The system automatically loads 5 legal documents on startup:

1. **Contract Law** - Offer, acceptance, consideration, capacity, legality
2. **Employment Law** - At-will employment, wrongful termination, discrimination
3. **Property Law** - Real/personal property, landlord-tenant, titles, easements
4. **Criminal Procedure** - Arrest, searches, Miranda rights, trials
5. **Contract Templates** - Payment terms, termination clauses, indemnification

Total: ~175 indexed chunks for RAG retrieval

## Architecture

```
Browser (localhost:5173)
    ↓ (HTTP via Vite Proxy)
Frontend (React + Tailwind)
    ↓ (/api/* routes)
Vite Dev Server (port 5173)
    ↓ (Proxy rewrite)
Backend FastAPI (localhost:8000)
    ↓
RAG System (TF-IDF search)
    ↓
Pre-loaded Legal Documents
```

## Production Deployment

For production, build the frontend:

```bash
cd frontend
npm run build
# Output in dist/
```

Deploy `dist/` to any static hosting and update API endpoint in app.

## Next Steps

- Add more legal documents via `/ingest` endpoint
- Customize UI colors in `frontend/src/globals.css`
- Modify RAG parameters in `backend/app/rag.py`
- Add authentication for production
- Deploy to cloud (Vercel, AWS, GCP)

## Support

Check the following files for more details:
- README.md - Full project documentation
- BACKEND.md - Backend architecture
- FRONTEND.md - Frontend components
- backend/app/rag.py - RAG system details
