# Setup Verification Checklist

Use this checklist to verify your Legal Advisor installation is working correctly.

## Pre-Setup Checklist

- [ ] Node.js 18+ installed: `node --version`
- [ ] Python 3.8+ installed: `python --version`
- [ ] Git installed: `git --version`
- [ ] Have 2 terminal windows open or tabs ready

## Backend Setup Verification

### Step 1: Navigate to Backend
```bash
cd backend
```
- [ ] Successfully navigated to backend directory

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
Expected output:
- [ ] Shows "Successfully installed" for: fastapi, uvicorn, pydantic, scikit-learn, numpy, python-dotenv
- [ ] No errors about incompatible versions
- [ ] Completes without warnings (warnings are OK)

### Step 3: Start Backend Server
```bash
python start.py
```

Expected output in terminal:
```
╔════════════════════════════════════════════════════════════╗
║           Legal Advisor - Backend Server                   ║
║                                                            ║
║   Starting FastAPI server with pre-loaded legal docs      ║
║   API Documentation: http://localhost:8000/docs           ║
║   Health Check: http://localhost:8000/health              ║
╚════════════════════════════════════════════════════════════╝

INFO:     Uvicorn running on http://0.0.0.0:8000
```

Verification:
- [ ] Backend starts without errors
- [ ] Shows "Uvicorn running on" message
- [ ] Terminal shows "Loading sample legal documents..."
- [ ] You see checkmarks (✓) for all 5 documents:
  - [ ] ✓ Loaded us-contract-law
  - [ ] ✓ Loaded us-employment-law
  - [ ] ✓ Loaded us-property-law
  - [ ] ✓ Loaded us-criminal-procedure
  - [ ] ✓ Loaded contract-templates
- [ ] Terminal shows "RAG System Ready: 175 chunks indexed" (or similar)
- [ ] Terminal is waiting for requests (not erroring)

### Step 4: Test Backend Health (in a 3rd terminal)
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"ok","version":"1.0.0","chunks_indexed":175}
```

Verification:
- [ ] Returns JSON with "status": "ok"
- [ ] Shows chunks_indexed count > 0
- [ ] No error messages

### Step 5: View API Documentation
Open in browser: http://localhost:8000/docs

Verification:
- [ ] Swagger UI loads
- [ ] Shows 5 endpoints: /health, /ingest, /chat, /stats, /docs
- [ ] Can expand each endpoint to see documentation

## Frontend Setup Verification

### Step 1: Navigate to Frontend (in Terminal 2)
```bash
cd frontend
```
- [ ] Successfully navigated to frontend directory

### Step 2: Install Dependencies
```bash
npm install
```

Expected output:
- [ ] Shows "added X packages"
- [ ] Completes with "found 0 vulnerabilities" or "X vulnerabilities"
- [ ] No fatal errors (warnings are OK)

Verification:
- [ ] node_modules/ folder created
- [ ] package-lock.json created or updated

### Step 3: Start Development Server
```bash
npm run dev
```

Expected output:
```
  VITE v5.4.11  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Verification:
- [ ] Vite server starts
- [ ] Shows Local URL: http://localhost:5173/
- [ ] Terminal is waiting (not erroring)

## Application Access Verification

### Step 1: Open Browser
Navigate to: http://localhost:5173

### Step 2: Check Visual Elements
On the page you should see:

Header:
- [ ] Legal Advisor title visible
- [ ] "AI-Powered Legal Consultation" subtitle visible
- [ ] History icon (clock) in top right
- [ ] Status badge showing "Connected" (green with checkmark)

Filters Section:
- [ ] "Jurisdiction" dropdown with "United States" selected
- [ ] "Practice Area" dropdown with "General" selected
- [ ] Both dropdowns are clickable

Chat Section:
- [ ] Text input box with placeholder "Ask your legal question..."
- [ ] Send button (paper airplane icon)
- [ ] Input is enabled (not grayed out)

Empty State:
- [ ] Scale (balance) icon shown
- [ ] "Ask a Legal Question" heading
- [ ] Helper text visible
- [ ] Sample question suggestion shown

## End-to-End Test

### Test 1: Ask About Contracts
1. Leave filters as default (US, General)
2. Type in chat box: "What are the key elements of a valid contract?"
3. Click Send button or press Ctrl+Enter
4. Wait for response...

Expected:
- [ ] Loading spinner appears briefly
- [ ] Response appears in 1-3 seconds
- [ ] Answer mentions: Offer, Acceptance, Consideration, Mutual Intent, Capacity, Legality
- [ ] Citations appear below answer
- [ ] Disclaimer visible at bottom
- [ ] Question appears in history sidebar (if visible)

### Test 2: Ask About Employment
1. Type: "What is wrongful termination?"
2. Click Send

Expected:
- [ ] Response appears mentioning illegal reasons for termination
- [ ] References to discrimination and whistleblower protection
- [ ] Citations show "us-employment-law"

### Test 3: Ask About Property Law
1. Type: "What is adverse possession?"
2. Click Send

Expected:
- [ ] Response mentions occupation period and ownership intent
- [ ] References property law document

### Test 4: Ask About Criminal Procedure
1. Type: "What are Miranda rights?"
2. Click Send

Expected:
- [ ] Response mentions right to remain silent, right to attorney
- [ ] References criminal procedure document

### Test 5: Check History
1. Click history icon (clock) in top right
2. History sidebar appears on right

Expected:
- [ ] Previous questions are listed
- [ ] Can click any question to reload its answer
- [ ] Delete button appears on hover
- [ ] Clear all button (trash icon) available

## Connection Status Verification

### Normal Operation (Connected)
- [ ] Status badge shows "Connected" with green dot
- [ ] Chat input is enabled
- [ ] Filters are enabled
- [ ] Send button works

### Backend Disconnected
Stop backend server (Ctrl+C in backend terminal)

Expected:
- [ ] Status badge changes to "Disconnected" with red pulsing dot
- [ ] Chat input becomes disabled (grayed out)
- [ ] Error banner appears with instructions
- [ ] Error message says: "Backend Connection Required"
- [ ] Shows command to run: `cd backend && python start.py`

Restart backend:
- [ ] Backend restarts and loads documents again
- [ ] Status returns to "Connected"
- [ ] Chat becomes enabled again

## Browser Console Verification

1. Press F12 to open DevTools
2. Click Console tab
3. You should see debug logs like:
   - [ ] "[v0] API health check passed: {...}"
   - [ ] "[v0] Sending chat request: {...}"
   - [ ] "[v0] Chat response received: {...}"
   - [ ] NO error messages (warnings are OK)

## Performance Verification

### Response Times
- [ ] First question: < 2 seconds
- [ ] Subsequent questions: < 1 second
- [ ] No timeout errors

### File Size
- [ ] Frontend: npm run build should create dist/ folder < 500KB
- [ ] Backend: responses < 10KB each

## Error Scenarios (Optional)

### Test: Wrong Backend URL
Edit `vite.config.ts` and change proxy target to invalid URL

Expected:
- [ ] Status shows "Disconnected"
- [ ] Error banner appears
- [ ] Error message is helpful

Revert the change after testing.

## Production Readiness Checks

- [ ] CORS properly configured (for production, restrict origins)
- [ ] Error handling works for edge cases
- [ ] Chat history persists in localStorage
- [ ] No sensitive data in URLs
- [ ] All endpoints respond with proper status codes
- [ ] API documentation complete (http://localhost:8000/docs)

## Cleanup & Next Steps

After verification passes:

1. **Optional**: Try ingesting custom legal documents via the `/ingest` endpoint
2. **Optional**: Modify styling in `/frontend/src/globals.css`
3. **Optional**: Add more practice areas in Filters component
4. **Deploy**: See BACKEND.md and FRONTEND.md for deployment instructions
5. **Integrate**: Connect to external legal document APIs

## Common Issues & Solutions

### Issue: "Cannot GET /api/chat"
**Solution**: Vite proxy not working
- Verify vite.config.ts has proxy configuration
- Restart frontend server

### Issue: "Connection refused" to backend
**Solution**: Backend not running
- Start backend with: `cd backend && python start.py`
- Verify port 8000 is not already in use

### Issue: "No chunks indexed"
**Solution**: Documents didn't load
- Check backend startup logs
- Look for error messages about loading
- Try running: `python -c "from app.rag import InMemoryLegalRAG; r = InMemoryLegalRAG()"`

### Issue: Empty response from chat
**Solution**: RAG not finding matches
- Ask different question with key terms from documents
- Check /stats endpoint to verify chunks exist
- Try: "contract", "employment", "property"

## Summary

If all checkboxes are marked, your Legal Advisor is fully functional! 

**Status: ✓ PRODUCTION READY**

You can now:
1. Deploy to production (see deployment guides)
2. Add more legal documents
3. Customize UI/styling
4. Integrate with external services
