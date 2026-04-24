# Project Verification Checklist

## Pre-Launch Verification

### Frontend Setup
- [ ] Run `npm install` in frontend folder
- [ ] Verify no installation errors
- [ ] `npm run dev` starts without errors
- [ ] Vite dev server running on http://localhost:5173
- [ ] Application loads in browser
- [ ] Tailwind styles are applied (colors, spacing, fonts)
- [ ] No console errors in browser DevTools

### Backend Setup
- [ ] Run `pip install -r requirements.txt` 
- [ ] Verify Python 3.8+ installed
- [ ] `python run.py` starts without errors
- [ ] FastAPI server running on http://localhost:8000
- [ ] Health check: `curl http://localhost:8000/health` returns 200
- [ ] Swagger UI accessible at http://localhost:8000/docs

### Integration Testing
- [ ] CORS error not appearing in browser console
- [ ] API proxy configured (check network tab)
- [ ] Sample document ingestion via API works
- [ ] Chat query returns response with citations
- [ ] Chat history saves and loads from localStorage
- [ ] Dark mode toggle works
- [ ] Mobile responsiveness (check with DevTools)

### Component Testing

#### ChatInput
- [ ] Input field visible and editable
- [ ] Placeholder text displays
- [ ] Send button enabled when text present
- [ ] Ctrl+Enter submits message
- [ ] Loading spinner shows during request
- [ ] Button disabled while loading

#### Filters
- [ ] Jurisdiction dropdown works
- [ ] Practice area dropdown works
- [ ] Selected values persist during queries
- [ ] Dropdowns disabled during loading

#### ResponseDisplay
- [ ] Answer text displays correctly
- [ ] Citations show with numbering
- [ ] Relevance scores display
- [ ] Disclaimer box visible and styled
- [ ] Response animates on appear

#### ChatHistory
- [ ] History appears in sidebar
- [ ] Can click to restore message
- [ ] Delete button removes item
- [ ] Clear all button works
- [ ] Items sorted newest first
- [ ] Shows empty state when no history

### Error Handling
- [ ] Type invalid jurisdiction in URL search params
- [ ] API down error displays gracefully
- [ ] Network error shows user message (not technical error)
- [ ] Invalid chat message validates on frontend
- [ ] Backend validation errors display

### Performance
- [ ] First page load < 3 seconds
- [ ] Chat response < 2 seconds
- [ ] No console warnings about unused imports
- [ ] No memory leaks in DevTools
- [ ] Scrolling is smooth
- [ ] No layout shift during loading

### Accessibility
- [ ] Tab navigation works through all buttons
- [ ] Form inputs have labels
- [ ] Buttons have aria-labels
- [ ] Color contrast is sufficient (WCAG AA)
- [ ] Semantic HTML used (header, main, footer)
- [ ] Screen reader can identify interactive elements

### Documentation
- [ ] README.md exists and is current
- [ ] FRONTEND.md describes all components
- [ ] BACKEND.md explains architecture
- [ ] MODERNIZATION.md summarizes changes
- [ ] .env.example has all config options
- [ ] Code comments explain complex logic

### Configuration
- [ ] .env.example in backend folder
- [ ] vite.config.ts has API proxy
- [ ] tailwind.config.js configured
- [ ] postcss.config.js has autoprefixer
- [ ] tsconfig.json has strict mode
- [ ] package.json has all scripts

### Build & Production
- [ ] `npm run build` completes without errors
- [ ] Build output in dist/ folder
- [ ] dist/ can be served as static files
- [ ] Backend can run with gunicorn: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
- [ ] All secrets are in .env, not committed
- [ ] .gitignore excludes node_modules, __pycache__, .env

## Post-Deployment

### Production Checklist
- [ ] CORS_ORIGINS configured for actual domain
- [ ] API_DEBUG set to false
- [ ] All environment variables set
- [ ] Database/persistence strategy implemented
- [ ] Rate limiting configured
- [ ] Authentication/authorization implemented
- [ ] HTTPS enabled
- [ ] Error logging configured
- [ ] Monitoring/alerting set up
- [ ] Backup strategy in place

### Security Review
- [ ] No API keys in code
- [ ] CORS not overly permissive
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (if using DB)
- [ ] XSS prevention (React escaping)
- [ ] CSRF tokens (if needed)
- [ ] Password hashing (if needed)
- [ ] SSL/TLS certificates valid

### Performance Review
- [ ] Lighthouse score > 80
- [ ] Page load time < 2s
- [ ] API response time < 1s
- [ ] Bundle size < 500KB (gzipped)
- [ ] Database queries optimized
- [ ] Caching strategy implemented

### User Testing
- [ ] Sample users can ingest documents
- [ ] Queries return relevant results
- [ ] No crashes or crashes handled gracefully
- [ ] UI is intuitive and responsive
- [ ] Mobile experience is good
- [ ] Dark mode works on all pages

## Common Issues & Solutions

### Frontend Issues
**Problem**: Tailwind styles not applying
- Solution: Ensure content path in tailwind.config.js is correct
- Check: `content: ["./src/**/*.{js,ts,jsx,tsx}"]`

**Problem**: CORS errors in console
- Solution: Verify backend CORS middleware is enabled
- Check: vite.config.ts proxy settings

**Problem**: Chat history not persisting
- Solution: Check browser localStorage is enabled
- Check: No errors in DevTools console

### Backend Issues
**Problem**: Import errors when running
- Solution: Ensure Python virtual environment activated
- Solution: Run `pip install -r requirements.txt`

**Problem**: Port 8000 already in use
- Solution: Kill process: `lsof -ti:8000 | xargs kill -9`
- Alternative: Change PORT in .env

**Problem**: No search results
- Solution: Verify documents ingested with `/stats` endpoint
- Solution: Document content should match query terms

## Quick Commands

```bash
# Frontend
cd frontend
npm install                # Install dependencies
npm run dev               # Start dev server
npm run build            # Build for production
npm run preview          # Preview production build

# Backend
cd backend
pip install -r requirements.txt  # Install dependencies
python run.py                     # Start server
python -m pytest                  # Run tests
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app  # Production
```

## Support Resources

- Frontend docs: FRONTEND.md
- Backend docs: BACKEND.md
- Main README: README.md
- Modernization summary: MODERNIZATION.md
- FastAPI docs: http://localhost:8000/docs
- React docs: https://react.dev
- Tailwind docs: https://tailwindcss.com

## Final Sign-Off

- [ ] All checklist items completed
- [ ] No critical bugs remain
- [ ] Documentation is up to date
- [ ] Ready for production deployment
- [ ] Team onboarded on new architecture

---

**Date Completed**: _______________
**Verified By**: ___________________
**Notes**: _________________________
