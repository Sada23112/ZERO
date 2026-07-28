import React, { useState, useEffect } from 'react';
import { LightGlassCard } from './components/LightGlassCard';
import { AdaptivePromptBar } from './components/AdaptivePromptBar';
import { ResearchWorkspace, SourceReference } from './components/ResearchWorkspace';
import { EngineeringWorkspace, WorkItem } from './components/EngineeringWorkspace';
import { KnowledgeWorkspace } from './components/KnowledgeWorkspace';
import { SettingsView } from './components/SettingsView';
import { StatusIndicator, StatusMode } from './components/StatusIndicator';
import { ContextChip } from './components/ContextChip';
import { Terminal, Search, Database, Settings, ShieldCheck, X, Sparkles } from 'lucide-react';
import { AnimatePresence } from 'framer-motion';

export type WorkspaceMode = 'prompt' | 'engineering' | 'research' | 'memory' | 'settings';

declare global {
  interface Window {
    zeroApi?: {
      getSettings: () => Promise<Record<string, unknown>>;
      saveSettings: (settings: Record<string, unknown>) => Promise<boolean>;
      fetchModels?: (apiKey?: string) => Promise<Array<{ id: string; name: string }>>;
      hideOverlay: () => Promise<void>;
      onNavigate: (callback: (view: string) => void) => void;
    };
  }
}

export const App: React.FC = () => {
  const [activeMode, setActiveMode] = useState<WorkspaceMode>('prompt');
  const [inputText, setInputText] = useState('');
  const [statusMode, setStatusMode] = useState<StatusMode>('idle');
  const [isStreaming, setIsStreaming] = useState(false);

  // Work items state
  const [workItems, setWorkItems] = useState<WorkItem[]>([]);
  const [researchData, setResearchData] = useState<{ query: string; summary: string; sources: SourceReference[] } | null>(null);

  useEffect(() => {
    if (window.zeroApi) {
      window.zeroApi.onNavigate((view) => {
        if (['prompt', 'engineering', 'research', 'memory', 'settings'].includes(view)) {
          setActiveMode(view as WorkspaceMode);
        }
      });
    }
  }, []);

  const handleDismiss = () => {
    if (window.zeroApi) {
      window.zeroApi.hideOverlay();
    }
  };

  const handleExecutePrompt = async (promptText: string) => {
    if (!promptText.trim()) return;

    setStatusMode('thinking');
    setIsStreaming(true);

    const lower = promptText.toLowerCase();

    setTimeout(() => {
      setStatusMode('executing');

      setTimeout(() => {
        if (lower.includes('research') || lower.includes('paper') || lower.includes('what is')) {
          setResearchData({
            query: promptText,
            summary: `Project ZERO Research Synthesis: Evaluated technical documentation and multi-query references. Context parsed via headless browser drivers.`,
            sources: [
              {
                title: 'Model Context Protocol Standards Specification',
                url: 'https://modelcontextprotocol.io',
                snippet: 'JSON-RPC 2.0 open protocol standard for tool integration.',
              },
              {
                title: 'Apple Human Interface Guidelines for macOS',
                url: 'https://developer.apple.com/design/human-interface-guidelines/',
                snippet: 'Frosted acrylic materials, dynamic typography scaling, and natural lighting.',
              },
            ],
          });
          setActiveMode('research');
        } else if (lower.includes('code') || lower.includes('diff') || lower.includes('run') || lower.includes('test')) {
          const item: WorkItem = {
            id: `art_${Date.now()}`,
            type: 'artifact',
            payload: {
              title: 'packages/core/src/model-discovery.ts',
              language: 'typescript',
              code: `export class ModelDiscoveryEngine {\n  async fetchAvailableModels(apiKey: string): Promise<DiscoveredModel[]> {\n    const response = await fetch(\`https://generativelanguage.googleapis.com/v1beta/models?key=\${apiKey}\`);\n    return (await response.json()).models;\n  }\n}`,
            },
            timestamp: new Date().toISOString(),
          };
          setWorkItems((prev) => [item, ...prev]);
          setActiveMode('engineering');
        } else {
          const textItem: WorkItem = {
            id: `text_${Date.now()}`,
            type: 'text',
            payload: { text: `Project ZERO Companion: Processed query "${promptText}". Response streaming active.` },
            timestamp: new Date().toISOString(),
          };
          setWorkItems((prev) => [textItem, ...prev]);
          setActiveMode('engineering');
        }

        setStatusMode('idle');
        setIsStreaming(false);
      }, 350);
    }, 250);
  };

  return (
    <div className="w-screen h-screen flex items-center justify-center p-4 select-none bg-transparent font-sans">
      <LightGlassCard className="w-full max-w-[760px] zero-light-glass">
        {/* Header Bar */}
        <div
          className="flex items-center justify-between px-4 py-2.5 bg-white/40 border-b border-black/[0.05]"
          style={{ WebkitAppRegion: 'drag' } as React.CSSProperties}
        >
          <div className="flex items-center gap-3" style={{ WebkitAppRegion: 'no-drag' } as React.CSSProperties}>
            <div className="flex items-center gap-1.5 font-sans font-bold text-xs tracking-tight text-slate-900">
              <ShieldCheck className="w-4 h-4 text-blue-600" />
              <span>ZERO</span>
            </div>
            <StatusIndicator mode={statusMode} />
            <ContextChip />
          </div>

          <div className="flex items-center gap-1.5" style={{ WebkitAppRegion: 'no-drag' } as React.CSSProperties}>
            {/* View Mode Buttons */}
            <div className="flex items-center p-0.5 rounded-lg bg-black/[0.04] border border-black/[0.04]">
              <button
                onClick={() => setActiveMode('prompt')}
                className={`p-1.5 rounded-md text-xs font-medium transition-all cursor-pointer ${
                  activeMode === 'prompt' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'
                }`}
                title="Prompt Bar"
              >
                <Sparkles className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setActiveMode('engineering')}
                className={`p-1.5 rounded-md text-xs font-medium transition-all cursor-pointer ${
                  activeMode === 'engineering' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'
                }`}
                title="Engineering Workspace"
              >
                <Terminal className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setActiveMode('research')}
                className={`p-1.5 rounded-md text-xs font-medium transition-all cursor-pointer ${
                  activeMode === 'research' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'
                }`}
                title="Research Workspace"
              >
                <Search className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setActiveMode('memory')}
                className={`p-1.5 rounded-md text-xs font-medium transition-all cursor-pointer ${
                  activeMode === 'memory' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'
                }`}
                title="Knowledge Memory"
              >
                <Database className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setActiveMode('settings')}
                className={`p-1.5 rounded-md text-xs font-medium transition-all cursor-pointer ${
                  activeMode === 'settings' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'
                }`}
                title="Settings"
              >
                <Settings className="w-3.5 h-3.5" />
              </button>
            </div>

            <button
              onClick={handleDismiss}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-800 hover:bg-slate-100 transition-colors cursor-pointer"
              title="Dismiss Overlay (Esc)"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Adaptive Prompt Input */}
        <AdaptivePromptBar
          value={inputText}
          onChange={setInputText}
          onSubmit={handleExecutePrompt}
          onDismiss={handleDismiss}
          isStreaming={isStreaming}
        />

        {/* Dynamic Expanding Content Views */}
        <AnimatePresence mode="wait">
          {activeMode === 'research' && researchData && (
            <ResearchWorkspace
              key="research"
              query={researchData.query}
              summary={researchData.summary}
              sources={researchData.sources}
            />
          )}

          {activeMode === 'engineering' && (
            <EngineeringWorkspace
              key="engineering"
              items={workItems}
              onExecuteCommand={(cmd) => handleExecutePrompt(`run ${cmd}`)}
            />
          )}

          {activeMode === 'memory' && (
            <KnowledgeWorkspace key="memory" memories={[]} />
          )}

          {activeMode === 'settings' && (
            <SettingsView key="settings" />
          )}
        </AnimatePresence>
      </LightGlassCard>
    </div>
  );
};

export default App;
