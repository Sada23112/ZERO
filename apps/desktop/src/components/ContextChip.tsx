import React from 'react';
import { FolderGit2, Cpu } from 'lucide-react';

interface ContextChipProps {
  workspace?: string;
  model?: string;
}

export const ContextChip: React.FC<ContextChipProps> = ({
  workspace = 'zero/workspace',
  model = 'Gemini 2.0',
}) => {
  return (
    <div className="inline-flex items-center gap-3 text-xs text-slate-400 font-mono">
      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-900/60 border border-white/5">
        <FolderGit2 className="w-3.5 h-3.5 text-blue-400" />
        <span className="text-[11px] text-slate-300">{workspace}</span>
      </div>
      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-900/60 border border-white/5">
        <Cpu className="w-3.5 h-3.5 text-purple-400" />
        <span className="text-[11px] text-slate-300">{model}</span>
      </div>
    </div>
  );
};
