# Frontend Development Guide

## Overview

The Legal Advisor frontend is built with React 18, TypeScript, Tailwind CSS, and Vite. It features a modular component architecture with responsive design and persistent state management.

## Project Structure

```
frontend/src/
├── components/
│   ├── ChatInput.tsx        # User message input component
│   ├── ChatHistory.tsx      # Conversation history sidebar
│   ├── Filters.tsx          # Jurisdiction & practice area selectors
│   └── ResponseDisplay.tsx  # Answer & citations display
├── lib/
│   └── utils.ts             # Utility functions (classname merger)
├── App.tsx                  # Main application container
├── main.tsx                 # React entry point
├── globals.css              # Tailwind + design tokens
├── index.html               # HTML template
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies & scripts
```

## Component Architecture

### App.tsx (240 lines)
**Main container component** managing state and coordinating child components.

**State:**
- `jurisdiction`: Selected legal jurisdiction
- `practiceArea`: Selected practice area
- `response`: Current API response (answer + citations)
- `loading`: API request state
- `error`: Error message state
- `history`: Array of past chat messages
- `showHistory`: Toggle history sidebar
- `currentMessageId`: Track current message selection

**Features:**
- Persistent chat history (localStorage)
- Error handling with try-catch
- Layout: Header, Main content area, History sidebar (optional), Footer
- Responsive grid (1 col mobile, 3+1 on desktop)

### ChatInput.tsx (72 lines)
**Textarea input with smart features**

**Props:**
- `onSend(message: string)`: Callback when sending
- `disabled?: boolean`: Disable input
- `isLoading?: boolean`: Show loading spinner

**Features:**
- Auto-expanding textarea (grows with content)
- Ctrl+Enter submit keyboard shortcut
- Loading state with spinner
- Disabled state during API calls
- Accessibility: ARIA labels

```tsx
// Usage
<ChatInput onSend={handleSend} isLoading={loading} />
```

### ResponseDisplay.tsx (79 lines)
**Displays AI response with citations and disclaimer**

**Props:**
- `answer: string`: Main response text
- `citations: Citation[]`: Source references
- `disclaimer: string`: Legal disclaimer

**Features:**
- Syntax highlighting ready (prose classes)
- Citation numbering with relevance scores
- Highlighted disclaimer box with icon
- Fade-in animation

```tsx
// Usage
<ResponseDisplay 
  answer={response.answer}
  citations={response.citations}
  disclaimer={response.disclaimer}
/>
```

### Filters.tsx (91 lines)
**Jurisdiction and practice area selection**

**Props:**
- `jurisdiction: string`
- `onJurisdictionChange(value: string)`
- `practiceArea: string`
- `onPracticeAreaChange(value: string)`
- `disabled?: boolean`

**Available Options:**
- Jurisdictions: US, Canada, UK, Australia, International
- Practice Areas: General, Contract, Criminal, Family, Employment, Corporate, IP

```tsx
// Usage
<Filters
  jurisdiction={jurisdiction}
  onJurisdictionChange={setJurisdiction}
  practiceArea={practiceArea}
  onPracticeAreaChange={setPracticeArea}
  disabled={loading}
/>
```

### ChatHistory.tsx (71 lines)
**Persistent conversation history with local storage**

**Props:**
- `messages: ChatMessage[]`: History items
- `onSelectMessage(msg: ChatMessage)`: Restore message
- `onDeleteMessage(id: string)`: Remove from history
- `currentMessageId?: string`: Highlight selected

**Features:**
- Sortable (newest first)
- Max 3 visible items with scroll
- Quick delete button per item
- Empty state message

```tsx
// Usage
<ChatHistory
  messages={history}
  onSelectMessage={handleSelect}
  onDeleteMessage={handleDelete}
  currentMessageId={currentMessageId}
/>
```

## Styling System

### Design Tokens (globals.css)
CSS custom properties for consistent theming:

```css
:root {
  /* Colors */
  --background: 0 0% 100%;
  --foreground: 0 0% 3.6%;
  --primary: 0 84.2% 60.2%;
  --secondary: 0 0% 96.1%;
  --accent: 0 84.2% 60.2%;
  
  /* Typography */
  --radius: 0.5rem;
}

.dark {
  /* Dark mode overrides */
}
```

### Tailwind Config
Extends Tailwind with design tokens:

```js
theme: {
  extend: {
    colors: {
      background: "hsl(var(--background))",
      primary: "hsl(var(--primary))",
      // ...
    }
  }
}
```

### Color Palette
- **Primary**: Red (#dc2626) - Actions, highlights
- **Background**: White/Black - Page background
- **Secondary**: Light gray - Card backgrounds
- **Accent**: Red - Interactive elements

## State Management

### Persistent Storage
Chat history saved to localStorage:

```tsx
// Auto-save on change
useEffect(() => {
  localStorage.setItem('chatHistory', JSON.stringify(history));
}, [history]);

// Load on mount
useEffect(() => {
  const saved = localStorage.getItem('chatHistory');
  if (saved) setHistory(JSON.parse(saved));
}, []);
```

### API Integration
Fetch wrapper with error handling:

```tsx
const handleSendMessage = async (message: string) => {
  setLoading(true);
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, jurisdiction, practice_area: practiceArea })
    });
    
    if (!res.ok) throw new Error(`${res.statusText}`);
    const data = await res.json();
    setResponse(data);
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Error');
  } finally {
    setLoading(false);
  }
};
```

## Development Workflow

### Setup
```bash
cd frontend
npm install
npm run dev
```

### Scripts
- `npm run dev` - Start dev server with HMR
- `npm run build` - Production build
- `npm run preview` - Preview production build

### Environment Variables
Frontend uses `/api` proxy to backend:

```ts
// vite.config.ts
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ''),
  }
}
```

## Best Practices

### Performance
- Memoize expensive computations with useMemo
- Lazy load components with React.lazy()
- Use virtual scrolling for long lists (future enhancement)

### Accessibility
- All buttons have `aria-label`
- Form inputs have associated labels
- Semantic HTML: `<main>`, `<header>`, `<footer>`
- Color contrast meets WCAG AA standards

### Code Quality
- Type safety: strict TypeScript mode
- Component props validated with TypeScript interfaces
- Error boundaries for graceful error handling
- Console logging for debugging

### Styling
- Utility-first with Tailwind
- Responsive design mobile-first
- Consistent spacing with Tailwind scale
- Color themes via CSS custom properties

## Adding New Components

1. Create file in `src/components/YourComponent.tsx`
2. Define TypeScript interface for props
3. Use `cn()` utility for conditional classes
4. Export and import in App.tsx

```tsx
// components/YourComponent.tsx
interface YourComponentProps {
  title: string;
  onAction: () => void;
}

export function YourComponent({ title, onAction }: YourComponentProps) {
  return (
    <div className="rounded-lg border border-border p-4">
      <h2>{title}</h2>
      <button onClick={onAction} className="px-4 py-2 bg-primary">
        Action
      </button>
    </div>
  );
}
```

## Debugging

### Console Logging
```tsx
console.log("[v0] User input:", value);
console.log("[v0] API response:", data);
console.log("[v0] State updated:", newState);
```

### React DevTools
- Inspect component props and state
- Track re-renders with Profiler
- Jump to component source

### Network Tab
- Monitor API calls
- Check request/response payloads
- View CORS headers

## Deployment

### Production Build
```bash
npm run build
# Creates dist/ folder with optimized assets
```

### Static Hosting
Deploy `dist/` folder to:
- Vercel
- Netlify
- AWS S3
- GitHub Pages
- Any static CDN

### Environment Configuration
Set backend URL for production:

```tsx
// Could be configured via environment variables
const API_URL = process.env.REACT_APP_API_URL || '/api';
```

## Testing (Future)

Add testing with:
- **Vitest** - Unit tests
- **React Testing Library** - Component tests
- **Cypress** - E2E tests

```bash
npm install --save-dev vitest @testing-library/react
```

## Troubleshooting

### CORS Errors
- Verify backend CORS headers
- Check vite.config.ts proxy settings
- Test with `curl` to isolate frontend

### Styling Issues
- Clear Tailwind cache: `npx tailwindcss -c tailwind.config.js -i ./src/globals.css -o ./dist/output.css`
- Verify class names are in content config
- Check browser DevTools for specificity conflicts

### Performance
- Use Lighthouse audit
- Profile with React DevTools Profiler
- Analyze bundle size: `npm install -D webpack-bundle-analyzer`
