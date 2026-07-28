import React, { useState, useEffect } from 'react';
import { GlassPanel } from './components/GlassPanel';
import { Toolbar, ViewMode } from './components/Toolbar';
import { CommandInput } from './components/CommandInput';
import { Workspace, WorkItem } from './components/Workspace';
import { SettingsView } from './components/SettingsView';
import { StatusMode } from './components/StatusIndicator';

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
  const [activeView, setActiveView] = useState<ViewMode>('all');
  const [inputText, setInputText] = useState('');
  const [statusMode, setStatusMode] = useState<StatusMode>('idle');
  const [isStreaming, setIsStreaming] = useState(false);

  // Work items state (structured artifacts)
  const [workItems, setWorkItems] = useState<WorkItem[]>([
    {
      id: 'init_1',
      type: 'text',
      payload: { text: 'Project ZERO Operating Companion initialized. Press Alt + Space to toggle.' },
      timestamp: new Date().toISOString(),
    },
  ]);

  useEffect(() => {
    if (window.zeroApi) {
      window.zeroApi.onNavigate((view) => {
        if (['all', 'engineering', 'research', 'memory', 'settings'].includes(view)) {
          setActiveView(view as ViewMode);
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

    // 1. Append user prompt as work item
    const userItem: WorkItem = {
      id: `prompt_${Date.now()}`,
      type: 'text',
      payload: { text: `Query: ${promptText}` },
      timestamp: new Date().toISOString(),
    };

    setWorkItems((prev) => [userItem, ...prev]);
    setInputText('');
    setStatusMode('thinking');
    setIsStreaming(true);

    // 2. Determine execution flow or simulate response structured artifact
    setTimeout(() => {
      setStatusMode('executing');

      setTimeout(() => {
        let responseItem: WorkItem;

        if (promptText.toLowerCase().includes('code') || promptText.toLowerCase().includes('run') || promptText.toLowerCase().includes('test')) {
          responseItem = {
            id: `art_${Date.now()}`,
            type: 'artifact',
            payload: {
              title: 'packages/core/src/chat-engine.ts',
              language: 'typescript',
              code: `export class ChatEngine {\n  constructor(private options: ChatEngineOptions) {}\n\n  async processUserMessage(chatId: string, userText: string): Promise<void> {\n    // Structured response streaming logic\n  }\n}`,
            },
            timestamp: new Date().toISOString(),
          };
        } else if (promptText.toLowerCase().includes('git') || promptText.toLowerCase().includes('diff')) {
          responseItem = {
            id: `diff_${Date.now()}`,
            type: 'diff',
            payload: {
              filePath: 'apps/desktop/src/components/Workspace.tsx',
              lines: [
                { type: 'normal', content: 'export const Workspace = () => {' },
                { type: 'delete', content: '  return <div className="old-dashboard" />' },
                { type: 'add', content: '  return <GlassPanel className="expanded-workspace" />' },
                { type: 'normal', content: '};' },
              ],
            },
            timestamp: new Date().toISOString(),
          };
        } else {
          responseItem = {
            id: `text_${Date.now()}`,
            type: 'text',
            payload: { text: `Project ZERO executed query: "${promptText}". Response streaming active.` },
            timestamp: new Date().toISOString(),
          };
        }

        setWorkItems((prev) => [responseItem, ...prev]);
        setStatusMode('idle');
        setIsStreaming(false);
      }, 400);
    }, 300);
  };

  return (
    <div className="w-screen h-screen flex items-center justify-center p-3 select-none bg-transparent">
      <GlassPanel className="w-full max-w-[760px] flex flex-col overflow-hidden shadow-2xl border border-white/10">
        {/* Navigation & Status Header */}
        <Toolbar
          activeView={activeView}
          onViewChange={setActiveView}
          statusMode={statusMode}
          onClose={handleDismiss}
        />

        {/* Command Search Bar */}
        <CommandInput
          value={inputText}
          onChange={setInputText}
          onSubmit={handleExecutePrompt}
          onDismiss={handleDismiss}
          isStreaming={isStreaming}
        />

        {/* Dynamic Workspace Container */}
        {activeView === 'settings' ? (
          <SettingsView />
        ) : (
          <Workspace
            activeView={activeView}
            items={workItems}
            onExecuteCommand={(cmd) => handleExecutePrompt(`run ${cmd}`)}
          />
        )}
      </GlassPanel>
    </div>
  );
};

export default App;
