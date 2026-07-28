import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ViewMode } from './Toolbar';
import { ArtifactCard } from './ArtifactCard';
import { ExecutionCard } from './ExecutionCard';
import { DiffPreviewCard } from './DiffPreviewCard';
import { ResearchCard } from './ResearchCard';
import { MemoryCard, MemoryItem } from './MemoryCard';

export interface WorkItem {
  id: string;
  type: 'text' | 'artifact' | 'execution' | 'diff' | 'research' | 'memory';
  payload: any;
  timestamp: string;
}

interface WorkspaceProps {
  activeView: ViewMode;
  items: WorkItem[];
  memories?: MemoryItem[];
  onExecuteCommand?: (cmd: string) => void;
}

export const Workspace: React.FC<WorkspaceProps> = ({
  activeView,
  items,
  memories = [],
  onExecuteCommand,
}) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[460px] scroll-smooth">
      <AnimatePresence mode="popLayout">
        {activeView === 'all' && (
          <motion.div
            key="all-view"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.15 }}
            className="space-y-4"
          >
            {items.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-center text-slate-500">
                <p className="text-sm font-mono">Press Alt + Space anytime to trigger Project ZERO.</p>
                <p className="text-xs text-slate-600 mt-1">Autonomous operating companion ready for execution.</p>
              </div>
            ) : (
              items.map((item) => renderWorkItem(item, onExecuteCommand))
            )}
          </motion.div>
        )}

        {activeView === 'engineering' && (
          <motion.div
            key="engineering-view"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.15 }}
            className="space-y-4"
          >
            <div className="p-3 rounded-xl bg-slate-950/60 border border-white/5 text-xs text-slate-400 font-mono flex items-center justify-between">
              <span>Engineering Mode: Inspecting Workspace Code & Command Execution</span>
              <span className="text-blue-400 font-semibold">Active Context</span>
            </div>
            {items
              .filter((i) => ['artifact', 'execution', 'diff'].includes(i.type))
              .map((item) => renderWorkItem(item, onExecuteCommand))}
          </motion.div>
        )}

        {activeView === 'research' && (
          <motion.div
            key="research-view"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.15 }}
            className="space-y-4"
          >
            <ResearchCard
              query="Deep Research & Technical Literature Analysis"
              summary="Project ZERO is configured with multi-query synthesis. External web documentation and API references are parsed automatically via Playwright & Tavily search drivers."
              sources={[
                {
                  title: 'Model Context Protocol Specification',
                  url: 'https://modelcontextprotocol.io',
                  snippet: 'JSON-RPC 2.0 standard protocol for open tool interoperability.',
                },
                {
                  title: 'Raycast Developer Ergonomics Study',
                  url: 'https://raycast.com',
                  snippet: 'Keyboard-first command palette heuristics for developer flow state.',
                },
              ]}
            />
          </motion.div>
        )}

        {activeView === 'memory' && (
          <motion.div
            key="memory-view"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.15 }}
            className="space-y-3"
          >
            <div className="p-3 rounded-xl bg-slate-950/60 border border-white/5 text-xs text-slate-400 font-mono flex items-center justify-between">
              <span>Cognitive Episodic & Key-Value Memory Store</span>
              <span className="text-purple-400 font-semibold">zero.db (WAL Mode)</span>
            </div>
            {memories.length > 0 ? (
              memories.map((mem) => <MemoryCard key={mem.id} memory={mem} />)
            ) : (
              <div className="py-8 text-center text-xs text-slate-500 font-mono">
                No saved memory entries yet. Conversations & preferences are saved automatically.
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

function renderWorkItem(item: WorkItem, onExecuteCommand?: (cmd: string) => void) {
  switch (item.type) {
    case 'artifact':
      return (
        <ArtifactCard
          key={item.id}
          id={item.id}
          title={item.payload.title || 'Code Artifact'}
          language={item.payload.language || 'typescript'}
          code={item.payload.code || ''}
          onRun={onExecuteCommand}
        />
      );

    case 'execution':
      return (
        <ExecutionCard
          key={item.id}
          command={item.payload.command || 'pnpm test'}
          exitCode={item.payload.exitCode ?? 0}
          stdout={item.payload.stdout || ''}
          stderr={item.payload.stderr}
          durationMs={item.payload.durationMs || 140}
        />
      );

    case 'diff':
      return (
        <DiffPreviewCard
          key={item.id}
          filePath={item.payload.filePath || 'src/index.ts'}
          lines={item.payload.lines || []}
        />
      );

    case 'research':
      return (
        <ResearchCard
          key={item.id}
          query={item.payload.query || 'Research Query'}
          summary={item.payload.summary || ''}
          sources={item.payload.sources || []}
        />
      );

    case 'text':
    default:
      return (
        <div key={item.id} className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5 text-xs leading-relaxed text-slate-200">
          <span className="font-mono text-[10px] text-blue-400 block mb-1">ZERO Companion</span>
          <p className="whitespace-pre-wrap">{item.payload.text || String(item.payload)}</p>
        </div>
      );
  }
}
