import { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { cn } from '../lib/utils';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  isLoading?: boolean;
}

export function ChatInput({ onSend, disabled = false, isLoading = false }: ChatInputProps) {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [value]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim() && !disabled && !isLoading) {
      onSend(value.trim());
      setValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ask your legal question..."
        disabled={disabled || isLoading}
        className={cn(
          "flex-1 px-4 py-3 rounded-lg border border-border bg-background text-foreground",
          "placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary",
          "resize-none overflow-y-auto max-h-48 font-sans",
          "transition-all duration-200",
          (disabled || isLoading) && "opacity-50 cursor-not-allowed"
        )}
        rows={1}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && e.ctrlKey) {
            handleSubmit(e as any);
          }
        }}
      />
      <button
        type="submit"
        disabled={!value.trim() || disabled || isLoading}
        className={cn(
          "px-4 py-3 rounded-lg bg-primary text-primary-foreground font-semibold",
          "hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-primary",
          "transition-all duration-200 flex items-center gap-2 self-end",
          (!value.trim() || disabled || isLoading) && "opacity-50 cursor-not-allowed"
        )}
      >
        {isLoading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <Send className="w-4 h-4" />
        )}
        <span className="hidden sm:inline">Send</span>
      </button>
    </form>
  );
}
