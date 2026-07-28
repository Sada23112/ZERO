import React, { useState } from 'react';
import { GitCommit, Plus, Minus, ChevronDown, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';

export interface DiffLine {
  type: 'add' | 'delete' | 'normal';
  content: string;
}

interface DiffPreviewCardProps {
  filePath: string;
  lines: DiffLine[];
}

export const DiffPreviewCard: React.FC<DiffPreviewCardProps> = ({ filePath, lines }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const additions = lines.filter((l) => l.type === 'add').length;
  const deletions = lines.filter((l) => l.type === 'delete').length;

  return (
    <div className="my-3 rounded-xl border border-white/10 bg-slate-950/90 overflow-hidden shadow-lg">
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
          <GitCommit className="w-4 h-4 text-purple-400" />
          <span className="font-semibold text-slate-100">{filePath}</span>
        </button>

        <div className="flex items-center gap-2 text-[11px] font-mono">
          <span className="flex items-center text-emerald-400 font-medium">
            <Plus className="w-3 h-3" />
            {additions}
          </span>
          <span className="flex items-center text-rose-400 font-medium">
            <Minus className="w-3 h-3" />
            {deletions}
          </span>
        </div>
      </div>

      {isExpanded && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="p-2 bg-slate-950 font-mono text-xs overflow-x-auto leading-relaxed"
        >
          {lines.map((line, idx) => {
            const lineStyle =
              line.type === 'add'
                ? 'bg-emerald-950/30 text-emerald-300 border-l-2 border-emerald-500'
                : line.type === 'delete'
                ? 'bg-rose-950/30 text-rose-300 border-l-2 border-rose-500'
                : 'text-slate-400';

            const prefix = line.type === 'add' ? '+' : line.type === 'delete' ? '-' : ' ';

            return (
              <div key={idx} className={`px-2 py-0.5 whitespace-pre flex gap-2 ${lineStyle}`}>
                <span className="select-none text-slate-600 w-4 text-right">{prefix}</span>
                <span>{line.content}</span>
              </div>
            );
          })}
        </motion.div>
      )}
    </div>
  );
};
