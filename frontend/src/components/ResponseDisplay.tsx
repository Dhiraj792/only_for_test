import { BookOpen, AlertCircle } from 'lucide-react';
import { cn } from '../lib/utils';

interface Citation {
  doc_id: string;
  chunk_id: number;
  score: number;
}

interface ResponseDisplayProps {
  answer: string;
  citations: Citation[];
  disclaimer: string;
}

export function ResponseDisplay({ answer, citations, disclaimer }: ResponseDisplayProps) {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Answer Section */}
      <div className="rounded-lg border border-border bg-secondary/50 p-6">
        <h3 className="text-lg font-semibold text-foreground mb-3 flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-primary" />
          Answer
        </h3>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <p className="text-foreground whitespace-pre-wrap leading-relaxed">
            {answer}
          </p>
        </div>
      </div>

      {/* Citations Section */}
      {citations.length > 0 && (
        <div className="rounded-lg border border-border bg-secondary/30 p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">
            Supporting References ({citations.length})
          </h3>
          <div className="space-y-2">
            {citations.map((citation, idx) => (
              <div
                key={`${citation.doc_id}-${idx}`}
                className="flex items-start gap-3 p-3 rounded bg-background/50 border border-border/50 hover:bg-background transition-colors"
              >
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center">
                  <span className="text-xs font-semibold text-primary">{idx + 1}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground break-words">
                    {citation.doc_id}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Chunk {citation.chunk_id} • Relevance: {(citation.score * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Disclaimer Section */}
      <div className={cn(
        "rounded-lg border-l-4 border-l-yellow-500 bg-yellow-50/50 dark:bg-yellow-950/20 p-4",
        "flex gap-3"
      )}>
        <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-500 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-sm font-semibold text-yellow-900 dark:text-yellow-200 mb-1">
            Important Disclaimer
          </p>
          <p className="text-sm text-yellow-800 dark:text-yellow-300">
            {disclaimer}
          </p>
        </div>
      </div>
    </div>
  );
}
