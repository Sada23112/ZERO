import React from 'react';
import { motion } from 'framer-motion';

export type StatusMode = 'idle' | 'thinking' | 'streaming' | 'executing' | 'error';

interface StatusIndicatorProps {
  mode: StatusMode;
  label?: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ mode, label }) => {
  const statusConfig = {
    idle: { color: 'bg-emerald-500', glow: 'shadow-emerald-500/50', defaultLabel: 'Ready' },
    thinking: { color: 'bg-amber-400', glow: 'shadow-amber-400/50', defaultLabel: 'Thinking...' },
    streaming: { color: 'bg-blue-500', glow: 'shadow-blue-500/50', defaultLabel: 'Streaming' },
    executing: { color: 'bg-indigo-500', glow: 'shadow-indigo-500/50', defaultLabel: 'Executing Tool' },
    error: { color: 'bg-rose-500', glow: 'shadow-rose-500/50', defaultLabel: 'Error' },
  };

  const config = statusConfig[mode];

  return (
    <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-slate-900/80 border border-white/10 text-xs font-medium text-slate-300">
      <div className="relative flex h-2 w-2 items-center justify-center">
        {mode !== 'idle' && (
          <motion.span
            animate={{ scale: [1, 1.8, 1], opacity: [0.7, 0, 0.7] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
            className={`absolute inline-flex h-full w-full rounded-full ${config.color}`}
          />
        )}
        <span className={`relative inline-flex h-2 w-2 rounded-full ${config.color} ${config.glow}`} />
      </div>
      <span className="text-[11px] font-mono tracking-tight text-slate-300">
        {label || config.defaultLabel}
      </span>
    </div>
  );
};
