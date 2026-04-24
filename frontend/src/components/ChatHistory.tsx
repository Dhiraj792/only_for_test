import { Trash2, MessageCircle } from 'lucide-react';
import { cn } from '../lib/utils';

export interface ChatMessage {
  id: string;
  question: string;
  answer: string;
  timestamp: number;
  jurisdiction: string;
  practiceArea: string;
}

interface ChatHistoryProps {
  messages: ChatMessage[];
  onSelectMessage: (message: ChatMessage) => void;
  onDeleteMessage: (id: string) => void;
  currentMessageId?: string;
}

export function ChatHistory({
  messages,
  onSelectMessage,
  onDeleteMessage,
  currentMessageId,
}: ChatHistoryProps) {
  if (messages.length === 0) {
    return (
      <div className="text-center py-8">
        <MessageCircle className="w-8 h-8 mx-auto text-gray-400 mb-2" />
        <p className="text-sm text-gray-500">No chat history yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-2 max-h-96 overflow-y-auto">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={cn(
            "p-3 rounded-lg border cursor-pointer transition-all duration-200",
            currentMessageId === msg.id
              ? "border-primary bg-primary/10"
              : "border-border bg-secondary/30 hover:bg-secondary/50"
          )}
          onClick={() => onSelectMessage(msg)}
        >
          <p className="text-sm font-medium text-foreground truncate">
            {msg.question}
          </p>
          <div className="flex items-center justify-between mt-2">
            <p className="text-xs text-gray-500">
              {new Date(msg.timestamp).toLocaleDateString()} • {msg.jurisdiction}
            </p>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDeleteMessage(msg.id);
              }}
              className="p-1 rounded hover:bg-red-500/20 text-red-600 dark:text-red-400 transition-colors"
              aria-label="Delete message"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
