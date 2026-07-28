import React, { useState } from 'react';
import { Terminal, CheckCircle2, XCircle, Clock, ChevronDown, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';

interface ExecutionCardProps {
  command: string;
  exitCode: number;
  stdout: string;
  stderr?: string;
  durationMs?: number;
}

export const ExecutionCard: React.FC<ExecutionCardProps> = ({
  command,
  exitCode,
  stdout,
  stderr,
  durationMs = 120,
}) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const isSuccess = exitCode === 0;

  return (
    <div className="my-3 rounded-xl border border-white/10 bg-slate-950/90 overflow-hidden shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between px-3.5 py-2.5 bg-slate-900/90 border-b border-white/5">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2.5 text-xs font-mono text-slate-200 hover:text-white transition-colors cursor-pointer"
        >
          {isExpanded ? (
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          ) : (
            <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
          )}
          <Terminal className="w-4 h-4 text-emerald-400" />
          <span className="font-semibold text-slate-100">{command}</span>
        </button>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1 text-[11px] text-slate-400 font-mono">
            <Clock className="w-3 h-3 text-slate-500" />
            <span>{durationMs}ms</span>
          </div>

          <div
            className={`flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-mono border ${
              isSuccess
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
            }`}
          >
            {isSuccess ? (
              <>
                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                <span>Exit 0</span>
              </>
            ) : (
              <>
                <XCircle className="w-3 h-3 text-rose-400" />
                <span>Exit {exitCode}</span>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Output Console */}
      {isExpanded && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="p-3 bg-black/90 font-mono text-xs text-slate-300 max-h-60 overflow-y-auto leading-relaxed"
        >
          {stdout && <pre className="whitespace-pre-wrap text-emerald-300/90">{stdout}</pre>}
          {stderr && <pre className="whitespace-pre-wrap text-rose-400/90 mt-1">{stderr}</pre>}
          {!stdout && !stderr && (
            <span className="text-slate-500 italic">[Command executed cleanly with no output]</span>
          )}
        </motion.div>
      )}
    </div>
  );
};
