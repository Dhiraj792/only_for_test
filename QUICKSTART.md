# Quick Start Guide - Legal Advisor

Get the Legal Advisor chatbot running in 2 minutes!

## Prerequisites

- Node.js 18+ installed
- Python 3.8+ installed
- Git installed

## Quick Start (2 terminals)

### Terminal 1: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the server
python start.py
```

You should see output like:
```
╔════════════════════════════════════════════════════════════╗
║           Legal Advisor - Backend Server                   ║
║                                                            ║
║   Starting FastAPI server with pre-loaded legal docs      ║
║   API Documentation: http://localhost:8000/docs           ║
║   Health Check: http://localhost:8000/health              ║
╚════════════════════════════════════════════════════════════╝

[INFO] Loading sample legal documents...
✓ Loaded us-contract-law
✓ Loaded us-employment-law
✓ Loaded us-property-law
✓ Loaded us-criminal-procedure
✓ Loaded contract-templates
[INFO] RAG System Ready: 175 chunks indexed
```

The backend is now running at **http://localhost:8000**

### Terminal 2: Start the Frontend

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

You should see output like:
```
  VITE v5.4.11  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

## Access the App

Open your browser to: **http://localhost:5173**

You should see:
- ✓ Legal Advisor header with "Connected" status badge
- ✓ Jurisdiction selector (default: United States)
- ✓ Practice area selector (default: General)
- ✓ Chat input box
- ✓ Empty state message

## Test It Out

Try asking these sample questions:

1. **"What are the key elements of a valid contract?"**
   - Should return information from the contract law document

2. **"What is wrongful termination?"**
   - Should return information from employment law

3. **"What is adverse possession?"**
   - Should return information about property law

4. **"What are Miranda rights?"**
   - Should return information from criminal procedure

## What Just Happened

1. **Backend** started FastAPI server with 5 pre-loaded legal documents
2. **RAG System** automatically split documents into 175 chunks and indexed them
3. **Frontend** connected to backend and verified connection
4. **Sample Data** is ready for Q&A

## Troubleshooting

### "Cannot connect to backend server"
- Make sure Terminal 1 (backend) is running
- Backend should be at http://localhost:8000
- Check firewall settings if needed

### "No answers being returned"
- Verify backend shows "RAG System Ready" in startup logs
- Check browser console (F12) for errors
- Make sure you're asking questions related to the sample documents

### Port Already in Use
If port 8000 or 5173 is already in use:

**Backend (change port):**
```bash
API_PORT=8001 python start.py
```

**Frontend (vite will auto-change):** Vite handles this automatically

### Module Not Found (Python)
```bash
cd backend
pip install --upgrade -r requirements.txt
```

### Module Not Found (Node)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

After verifying it works:

1. **Add More Legal Documents** - Put text files in backend and ingest them via `/ingest` endpoint
2. **Customize Styling** - Edit `/frontend/src/globals.css` or tailwind.config.js
3. **Deploy** - See BACKEND.md and FRONTEND.md for deployment instructions
4. **Integrate APIs** - Connect to external legal document sources

## API Documentation

While the backend is running, you can access:

- **OpenAPI Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## File Structure

```
legal-advisor/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app with sample docs
│   │   └── rag.py           # RAG system
│   ├── start.py             # Run this to start server
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main app with API integration
│   │   ├── main.tsx         # Entry point
│   │   └── globals.css      # Styling
│   ├── vite.config.ts       # Vite config (includes API proxy)
│   └── package.json         # npm dependencies
│
└── README.md                # Full documentation
```

## Sample Questions by Practice Area

### Contract Law
- "What is consideration in a contract?"
- "Can I terminate a contract?"
- "What makes a contract valid?"

### Employment Law
- "What is wrongful termination?"
- "Are there any discrimination protections?"
- "What is harassment in the workplace?"

### Property Law
- "What is adverse possession?"
- "What are tenant rights?"
- "How do easements work?"

### Criminal Procedure
- "What are Miranda rights?"
- "When can police search my property?"
- "What is double jeopardy?"

### Contract Templates
- "What should be in a payment terms clause?"
- "What is a confidentiality agreement?"
- "What does limitation of liability mean?"

## Performance Tips

- Keep backend and frontend in separate terminals
- Don't close Terminal 1 while using the app
- For production, use `python start.py` with environment variables
- For high traffic, consider Redis caching (see BACKEND.md)

## Getting Help

1. Check the logs in both Terminal 1 (backend) and Terminal 2 (frontend)
2. Open browser DevTools (F12) to see frontend errors
3. Visit http://localhost:8000/docs for API documentation
4. See BACKEND.md and FRONTEND.md for detailed documentation

---

**Ready to go!** If both terminals are running and you see "Connected" in the UI, you're all set. 🎉
