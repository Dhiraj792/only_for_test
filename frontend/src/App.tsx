import { useState, useEffect } from 'react';
import { Scale, Trash2, History } from 'lucide-react';
import { ChatInput } from './components/ChatInput';
import { ResponseDisplay } from './components/ResponseDisplay';
import { Filters } from './components/Filters';
import { ChatHistory, ChatMessage } from './components/ChatHistory';
import { cn } from './lib/utils';

interface ChatResponse {
  answer: string;
  citations: Array<{ doc_id: string; chunk_id: number; score: number }>;
  disclaimer: string;
}

function App() {
  const [jurisdiction, setJurisdiction] = useState('US');
  const [practiceArea, setPracticeArea] = useState('general');
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<ChatMessage[]>([]);
  const [currentMessageId, setCurrentMessageId] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);

  // Load history from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  // Save history to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(history));
  }, [history]);

  const handleSendMessage = async (message: string) => {
    setLoading(true);
    setError(null);
    setCurrentMessageId(null);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          jurisdiction,
          practice_area: practiceArea,
        }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.statusText}`);
      }

      const data = (await res.json()) as ChatResponse;
      setResponse(data);

      // Add to history
      const newMessage: ChatMessage = {
        id: Date.now().toString(),
        question: message,
        answer: data.answer,
        timestamp: Date.now(),
        jurisdiction,
        practiceArea,
      };
      setHistory([newMessage, ...history]);
      setCurrentMessageId(newMessage.id);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get response';
      setError(errorMessage);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectMessage = (msg: ChatMessage) => {
    setResponse({
      answer: msg.answer,
      citations: [],
      disclaimer: 'This is a message from your history.',
    });
    setJurisdiction(msg.jurisdiction);
    setPracticeArea(msg.practiceArea);
    setCurrentMessageId(msg.id);
  };

  const handleDeleteMessage = (id: string) => {
    setHistory(history.filter((msg) => msg.id !== id));
    if (currentMessageId === id) {
      setCurrentMessageId(null);
      setResponse(null);
    }
  };

  const handleClearHistory = () => {
    setHistory([]);
    setCurrentMessageId(null);
    setResponse(null);
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border bg-secondary/30 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/20">
                <Scale className="w-6 h-6 text-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Legal Advisor</h1>
                <p className="text-sm text-gray-500">AI-Powered Legal Consultation</p>
              </div>
            </div>
            <button
              onClick={() => setShowHistory(!showHistory)}
              className={cn(
                'p-2 rounded-lg transition-colors duration-200',
                showHistory
                  ? 'bg-primary/20 text-primary'
                  : 'hover:bg-secondary text-gray-600 dark:text-gray-400'
              )}
              aria-label="Toggle history"
            >
              <History className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Content */}
          <main className="lg:col-span-3 space-y-6">
            {/* Filters */}
            <div className="rounded-lg border border-border bg-secondary/50 p-4 sm:p-6">
              <Filters
                jurisdiction={jurisdiction}
                onJurisdictionChange={setJurisdiction}
                practiceArea={practiceArea}
                onPracticeAreaChange={setPracticeArea}
                disabled={loading}
              />
            </div>

            {/* Chat Input */}
            <div className="rounded-lg border border-border bg-secondary/50 p-4 sm:p-6">
              <ChatInput
                onSend={handleSendMessage}
                disabled={loading}
                isLoading={loading}
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="rounded-lg border border-red-500 bg-red-50 dark:bg-red-950/20 p-4">
                <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
              </div>
            )}

            {/* Response */}
            {response && (
              <ResponseDisplay
                answer={response.answer}
                citations={response.citations}
                disclaimer={response.disclaimer}
              />
            )}

            {/* Empty State */}
            {!response && !error && (
              <div className="rounded-lg border border-border bg-secondary/30 p-12 text-center">
                <Scale className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                <h2 className="text-lg font-semibold text-foreground mb-2">
                  Ask a Legal Question
                </h2>
                <p className="text-gray-500 max-w-md mx-auto">
                  Select your jurisdiction and practice area, then ask your legal question. We&apos;ll provide an answer with supporting references.
                </p>
              </div>
            )}
          </main>

          {/* Sidebar - History */}
          {showHistory && (
            <aside className="lg:col-span-1">
              <div className="rounded-lg border border-border bg-secondary/50 p-4 h-fit sticky top-20">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-semibold text-foreground flex items-center gap-2">
                    <History className="w-4 h-4" />
                    History
                  </h2>
                  {history.length > 0 && (
                    <button
                      onClick={handleClearHistory}
                      className="p-1 rounded hover:bg-red-500/20 text-red-600 dark:text-red-400 transition-colors"
                      aria-label="Clear history"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <ChatHistory
                  messages={history}
                  onSelectMessage={handleSelectMessage}
                  onDeleteMessage={handleDeleteMessage}
                  currentMessageId={currentMessageId}
                />
              </div>
            </aside>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-border bg-secondary/30 mt-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
          <div className="text-center text-sm text-gray-500">
            <p>
              This is an educational tool. Always consult with a qualified legal professional for real legal advice.
            </p>
            <p className="mt-2">
              Built with React, Tailwind CSS, and TypeScript
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
