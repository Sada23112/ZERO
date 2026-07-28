import React, { useRef, useEffect } from 'react';
import { Search } from 'lucide-react';
import { ActionChip } from './ActionChip';

interface CommandInputProps {
  value: string;
  onChange: (val: string) => void;
  onSubmit: (val: string) => void;
  onDismiss?: () => void;
  placeholder?: string;
  isStreaming?: boolean;
}

export const CommandInput: React.FC<CommandInputProps> = ({
  value,
  onChange,
  onSubmit,
  onDismiss,
  placeholder = 'Ask ZERO or run an engineering command...',
  isStreaming = false,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim()) {
        onSubmit(value.trim());
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      if (onDismiss) {
        onDismiss();
      }
    }
  };

  return (
    <div className="relative flex items-center gap-3 px-4 py-3.5 bg-slate-950/90 border-b border-white/10 shadow-inner">
      <Search className="w-5 h-5 text-blue-400 shrink-0" />

      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={isStreaming}
        className="flex-1 bg-transparent border-none text-slate-100 text-sm font-normal placeholder-slate-500 focus:outline-none focus:ring-0 leading-relaxed font-sans"
      />

      <div className="flex items-center gap-2 shrink-0">
        <ActionChip shortcut="↵" label="Execute" onClick={() => value.trim() && onSubmit(value.trim())} variant="primary" />
        <ActionChip shortcut="Esc" label="Dismiss" onClick={onDismiss} variant="secondary" />
      </div>
    </div>
  );
};
