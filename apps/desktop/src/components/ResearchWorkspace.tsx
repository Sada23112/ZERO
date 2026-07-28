import React from 'react';
import { ExternalLink, Bookmark, Search, BookOpen } from 'lucide-react';
import { motion } from 'framer-motion';

export interface SourceReference {
  title: string;
  url: string;
  snippet: string;
}

interface ResearchWorkspaceProps {
  query: string;
  summary: string;
  sources: SourceReference[];
}

export const ResearchWorkspace: React.FC<ResearchWorkspaceProps> = ({
  query,
  summary,
  sources,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="grid grid-cols-1 md:grid-cols-12 gap-4 p-5 max-h-[460px] overflow-y-auto"
    >
      {/* Left Column: Query & Executive Summary */}
      <div className="md:col-span-7 space-y-3">
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-600 uppercase tracking-wider">
          <Search className="w-3.5 h-3.5" />
          <span>Research Synthesis</span>
        </div>

        <h3 className="text-base font-semibold text-slate-900 leading-snug">{query}</h3>

        <div className="p-4 rounded-xl bg-white/70 border border-slate-200/60 shadow-sm text-xs leading-relaxed text-slate-700 font-sans space-y-2">
          <p className="whitespace-pre-wrap">{summary}</p>
        </div>
      </div>

      {/* Right Column: References & Open Actions */}
      <div className="md:col-span-5 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Sources ({sources.length})</span>
          </span>
          <button className="text-[11px] font-medium text-blue-600 hover:underline flex items-center gap-1">
            <Bookmark className="w-3 h-3" />
            <span>Save All</span>
          </button>
        </div>

        <div className="space-y-2.5">
          {sources.map((src, idx) => (
            <motion.a
              key={idx}
              href={src.url}
              target="_blank"
              rel="noreferrer"
              whileHover={{ x: 2 }}
              className="block p-3 rounded-xl bg-white/80 border border-slate-200/80 hover:border-blue-400/60 hover:shadow-md transition-all group text-decoration-none"
            >
              <div className="flex items-center justify-between gap-2 mb-1">
                <span className="font-medium text-xs text-slate-900 group-hover:text-blue-600 line-clamp-1">
                  {src.title}
                </span>
                <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600 shrink-0" />
              </div>
              <p className="text-[11px] text-slate-500 line-clamp-2 leading-relaxed">
                {src.snippet}
              </p>
            </motion.a>
          ))}
        </div>
      </div>
    </motion.div>
  );
};
