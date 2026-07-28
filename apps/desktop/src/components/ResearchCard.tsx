import React, { useState } from 'react';
import { ExternalLink, Bookmark, Search, Check } from 'lucide-react';
import { motion } from 'framer-motion';

export interface SourceReference {
  title: string;
  url: string;
  snippet: string;
}

interface ResearchCardProps {
  query: string;
  summary: string;
  sources: SourceReference[];
}

export const ResearchCard: React.FC<ResearchCardProps> = ({ query, summary, sources }) => {
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="my-3 rounded-xl border border-white/10 bg-slate-950/80 overflow-hidden shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between px-3.5 py-2.5 bg-slate-900/90 border-b border-white/5">
        <div className="flex items-center gap-2 text-xs font-mono text-slate-200">
          <Search className="w-4 h-4 text-blue-400" />
          <span className="font-semibold text-slate-100">Research: {query}</span>
        </div>

        <button
          onClick={handleSave}
          className="flex items-center gap-1.5 px-2 py-1 text-[11px] font-mono rounded bg-slate-800 text-slate-300 border border-white/10 hover:bg-slate-700 active:scale-95 transition-all cursor-pointer"
        >
          {saved ? (
            <>
              <Check className="w-3 h-3 text-emerald-400" />
              <span className="text-emerald-400">Saved</span>
            </>
          ) : (
            <>
              <Bookmark className="w-3 h-3 text-slate-400" />
              <span>Save Reference</span>
            </>
          )}
        </button>
      </div>

      {/* Content Body */}
      <div className="p-4 space-y-4 text-xs leading-relaxed text-slate-300">
        <p className="text-slate-200 text-sm font-normal leading-relaxed">{summary}</p>

        {/* Source Cards */}
        {sources.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-white/5">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
              Cited References ({sources.length})
            </span>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {sources.map((src, idx) => (
                <motion.a
                  key={idx}
                  href={src.url}
                  target="_blank"
                  rel="noreferrer"
                  whileHover={{ scale: 1.01 }}
                  className="p-2.5 rounded-lg bg-slate-900/60 border border-white/5 hover:border-blue-500/30 transition-all flex flex-col justify-between gap-1 group text-decoration-none"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-medium text-slate-200 group-hover:text-blue-400 line-clamp-1">
                      {src.title}
                    </span>
                    <ExternalLink className="w-3 h-3 text-slate-500 group-hover:text-blue-400 shrink-0" />
                  </div>
                  <span className="text-[11px] text-slate-400 line-clamp-2 leading-normal">
                    {src.snippet}
                  </span>
                </motion.a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
