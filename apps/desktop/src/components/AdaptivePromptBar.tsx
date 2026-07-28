import React, { useRef, useEffect } from 'react';
import { Sparkles, Mic, ArrowUpRight } from 'lucide-react';
import { motion } from 'framer-motion';

interface AdaptivePromptBarProps {
  value: string;
  onChange: (val: string) => void;
  onSubmit: (val: string) => void;
  onDismiss?: () => void;
  isStreaming?: boolean;
}

export const AdaptivePromptBar: React.FC<AdaptivePromptBarProps> = ({
  value,
  onChange,
  onSubmit,
  onDismiss,
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
    <div className="relative px-5 py-4 flex items-center gap-3 bg-white/70 backdrop-blur-xl border-b border-black/[0.05]">
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 border border-blue-100 text-blue-600 shadow-sm shrink-0">
        <Sparkles className="w-5 h-5" />
      </div>

      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="What are we engineering today?"
        disabled={isStreaming}
        className="flex-1 bg-transparent border-none text-slate-900 text-base font-normal placeholder-slate-400 focus:outline-none focus:ring-0 leading-relaxed font-sans"
      />

      <div className="flex items-center gap-2 shrink-0">
        <button
          type="button"
          className="p-2 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100/80 transition-colors cursor-pointer"
          title="Voice Command"
        >
          <Mic className="w-4 h-4" />
        </button>

        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={() => value.trim() && onSubmit(value.trim())}
          disabled={!value.trim() || isStreaming}
          className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium shadow-sm disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center gap-1 cursor-pointer"
        >
          <span>Run</span>
          <ArrowUpRight className="w-3.5 h-3.5" />
        </motion.button>
      </div>
    </div>
  );
};
