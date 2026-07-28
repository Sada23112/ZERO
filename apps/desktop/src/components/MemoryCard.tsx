import React from 'react';
import { Database, Clock, Tag } from 'lucide-react';

export interface MemoryItem {
  id: string;
  key: string;
  value: string;
  category: string;
  created_at: string;
}

interface MemoryCardProps {
  memory: MemoryItem;
  onSelect?: (memory: MemoryItem) => void;
}

export const MemoryCard: React.FC<MemoryCardProps> = ({ memory, onSelect }) => {
  return (
    <div
      onClick={() => onSelect && onSelect(memory)}
      className="p-3 my-2 rounded-xl border border-white/10 bg-slate-950/80 hover:bg-slate-900/80 hover:border-white/20 transition-all cursor-pointer shadow-md group"
    >
      <div className="flex items-center justify-between gap-2 mb-1.5">
        <div className="flex items-center gap-2">
          <Database className="w-3.5 h-3.5 text-purple-400" />
          <span className="font-mono text-xs font-semibold text-slate-200 group-hover:text-purple-300">
            {memory.key}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-mono bg-purple-950/50 text-purple-300 border border-purple-800/40">
            <Tag className="w-2.5 h-2.5" />
            {memory.category}
          </span>
          <span className="inline-flex items-center gap-1 text-[10px] font-mono text-slate-500">
            <Clock className="w-2.5 h-2.5" />
            {new Date(memory.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      </div>
      <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed font-normal">
        {memory.value}
      </p>
    </div>
  );
};
