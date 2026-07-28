import React, { useState } from 'react';
import { Copy, Check, Play, FileCode, ChevronDown, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';

interface ArtifactCardProps {
  id: string;
  title: string;
  language?: string;
  code: string;
  onRun?: (code: string) => void;
}

export const ArtifactCard: React.FC<ArtifactCardProps> = ({
  title,
  language = 'typescript',
  code,
  onRun,
}) => {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lines = code.trim().split('\n');

  return (
    <div className="my-3 rounded-xl border border-white/10 bg-slate-950/80 overflow-hidden shadow-lg transition-all duration-150 hover:border-white/20">
      {/* Card Header */}
      <div className="flex items-center justify-between px-3.5 py-2.5 bg-slate-900/90 border-b border-white/5">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2 text-xs font-mono text-slate-300 hover:text-white transition-colors cursor-pointer"
        >
          {isExpanded ? (
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          ) : (
            <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
          )}
          <FileCode className="w-4 h-4 text-blue-400" />
          <span className="font-semibold">{title}</span>
          <span className="px-1.5 py-0.5 text-[10px] uppercase tracking-wider rounded bg-slate-800 text-slate-400 border border-white/5">
            {language}
          </span>
        </button>

        <div className="flex items-center gap-2">
          {onRun && (
            <button
              onClick={() => onRun(code)}
              className="flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-mono rounded-md bg-blue-600/20 text-blue-300 border border-blue-500/30 hover:bg-blue-600/40 active:scale-95 transition-all cursor-pointer"
            >
              <Play className="w-3 h-3 text-blue-400 fill-blue-400" />
              <span>Run</span>
            </button>
          )}
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-mono rounded-md bg-slate-800/80 text-slate-300 border border-white/10 hover:bg-slate-700 active:scale-95 transition-all cursor-pointer"
          >
            {copied ? (
              <>
                <Check className="w-3 h-3 text-emerald-400" />
                <span className="text-emerald-400">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3 h-3 text-slate-400" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Code Area */}
      {isExpanded && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="p-3 bg-slate-950 font-mono text-xs overflow-x-auto"
        >
          <table className="w-full border-collapse">
            <tbody>
              {lines.map((line, idx) => (
                <tr key={idx} className="hover:bg-slate-900/50">
                  <td className="w-10 select-none text-right pr-4 text-slate-600 text-[11px]">
                    {idx + 1}
                  </td>
                  <td className="text-slate-200 whitespace-pre font-normal leading-relaxed">
                    {line}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      )}
    </div>
  );
};
