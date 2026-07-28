import React from 'react';
import { Terminal, Search, Database, Settings, ShieldCheck, X } from 'lucide-react';
import { StatusIndicator, StatusMode } from './StatusIndicator';
import { ContextChip } from './ContextChip';

export type ViewMode = 'all' | 'engineering' | 'research' | 'memory' | 'settings';

interface ToolbarProps {
  activeView: ViewMode;
  onViewChange: (view: ViewMode) => void;
  statusMode: StatusMode;
  onClose?: () => void;
}

export const Toolbar: React.FC<ToolbarProps> = ({
  activeView,
  onViewChange,
  statusMode,
  onClose,
}) => {
  const views: Array<{ id: ViewMode; label: string; icon: React.ComponentType<{ className?: string }> }> = [
    { id: 'all', label: 'Command', icon: Search },
    { id: 'engineering', label: 'Code', icon: Terminal },
    { id: 'research', label: 'Research', icon: Search },
    { id: 'memory', label: 'Memory', icon: Database },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div
      className="flex items-center justify-between px-4 py-2.5 bg-slate-950/90 border-b border-white/10 select-none"
      style={{ WebkitAppRegion: 'drag' } as React.CSSProperties}
    >
      {/* Left Context & Status */}
      <div className="flex items-center gap-3" style={{ WebkitAppRegion: 'no-drag' } as React.CSSProperties}>
        <div className="flex items-center gap-1.5 font-mono font-bold text-xs tracking-wider text-slate-100">
          <ShieldCheck className="w-4 h-4 text-blue-400" />
          <span>ZERO</span>
        </div>
        <StatusIndicator mode={statusMode} />
        <ContextChip />
      </div>

      {/* Right Navigation & Window Controls */}
      <div className="flex items-center gap-2" style={{ WebkitAppRegion: 'no-drag' } as React.CSSProperties}>
        <div className="flex items-center p-0.5 rounded-lg bg-slate-900/80 border border-white/5">
          {views.map((v) => {
            const Icon = v.icon;
            const isActive = activeView === v.id;
            return (
              <button
                key={v.id}
                onClick={() => onViewChange(v.id)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium transition-all cursor-pointer ${
                  isActive
                    ? 'bg-blue-600/30 text-white border border-blue-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{v.label}</span>
              </button>
            );
          })}
        </div>

        {onClose && (
          <button
            onClick={onClose}
            className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800/80 transition-all cursor-pointer"
            title="Hide Overlay (Esc)"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};
