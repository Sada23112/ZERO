import React from 'react';
import { motion } from 'framer-motion';
import { ArtifactCard } from './ArtifactCard';
import { ExecutionCard } from './ExecutionCard';
import { DiffPreviewCard } from './DiffPreviewCard';

export interface WorkItem {
  id: string;
  type: 'text' | 'artifact' | 'execution' | 'diff' | 'research' | 'memory';
  payload: any;
  timestamp: string;
}

interface EngineeringWorkspaceProps {
  items: WorkItem[];
  onExecuteCommand?: (cmd: string) => void;
}

export const EngineeringWorkspace: React.FC<EngineeringWorkspaceProps> = ({
  items,
  onExecuteCommand,
}) => {
  const engItems = items.filter((i) => ['artifact', 'execution', 'diff'].includes(i.type));

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-5 space-y-4 max-h-[460px] overflow-y-auto"
    >
      <div className="flex items-center justify-between p-3 rounded-xl bg-white/70 border border-slate-200/60 shadow-sm text-xs font-mono text-slate-600">
        <span>Engineering Mode: Active Workspace Context</span>
        <span className="text-blue-600 font-semibold">@zero/core</span>
      </div>

      {engItems.length === 0 ? (
        <div className="py-10 text-center text-xs text-slate-400 font-mono">
          No active code artifacts or terminal executions yet. Enter an engineering prompt.
        </div>
      ) : (
        engItems.map((item) => {
          if (item.type === 'artifact') {
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
          }
          if (item.type === 'execution') {
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
          }
          if (item.type === 'diff') {
            return (
              <DiffPreviewCard
                key={item.id}
                filePath={item.payload.filePath || 'src/index.ts'}
                lines={item.payload.lines || []}
              />
            );
          }
          return null;
        })
      )}
    </motion.div>
  );
};
