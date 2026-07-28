import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Database, FileText } from 'lucide-react';
import { MemoryCard, MemoryItem } from './MemoryCard';

interface KnowledgeWorkspaceProps {
  memories: MemoryItem[];
}

export const KnowledgeWorkspace: React.FC<KnowledgeWorkspaceProps> = ({ memories }) => {
  const [filterQuery, setFilterQuery] = useState('');

  const filtered = memories.filter(
    (m) =>
      m.key.toLowerCase().includes(filterQuery.toLowerCase()) ||
      m.value.toLowerCase().includes(filterQuery.toLowerCase()) ||
      m.category.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-5 space-y-4 max-h-[460px] overflow-y-auto"
    >
      {/* Search Header */}
      <div className="relative flex items-center gap-2 px-3.5 py-2.5 rounded-xl bg-white/80 border border-slate-200/80 shadow-sm">
        <Search className="w-4 h-4 text-slate-400 shrink-0" />
        <input
          type="text"
          value={filterQuery}
          onChange={(e) => setFilterQuery(e.target.value)}
          placeholder="Search cognitive memory & specs..."
          className="flex-1 bg-transparent border-none text-xs text-slate-900 placeholder-slate-400 focus:outline-none font-sans"
        />
        <div className="flex items-center gap-1 text-[11px] font-mono text-slate-400">
          <Database className="w-3.5 h-3.5 text-purple-500" />
          <span>zero.db</span>
        </div>
      </div>

      {/* Memory List */}
      <div className="space-y-2">
        {filtered.length > 0 ? (
          filtered.map((mem) => <MemoryCard key={mem.id} memory={mem} />)
        ) : (
          <div className="py-12 text-center text-xs text-slate-400 font-mono space-y-1">
            <FileText className="w-8 h-8 text-slate-300 mx-auto mb-2" />
            <p>No matching cognitive memory entries found.</p>
            <p className="text-[11px] text-slate-400">Memory entries are indexed automatically from conversations.</p>
          </div>
        )}
      </div>
    </motion.div>
  );
};
