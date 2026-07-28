import React from 'react';

interface ActionChipProps {
  shortcut: string;
  label: string;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'accent';
}

export const ActionChip: React.FC<ActionChipProps> = ({
  shortcut,
  label,
  onClick,
  variant = 'secondary',
}) => {
  const bgStyles = {
    primary: 'bg-blue-600/20 text-blue-300 border-blue-500/30 hover:bg-blue-600/30',
    secondary: 'bg-slate-800/60 text-slate-300 border-white/10 hover:bg-slate-700/60',
    accent: 'bg-rose-500/20 text-rose-300 border-rose-500/30 hover:bg-rose-500/30',
  };

  return (
    <button
      onClick={onClick}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border text-xs transition-all duration-150 active:scale-95 cursor-pointer ${bgStyles[variant]}`}
    >
      <span className="text-[11px] text-slate-200">{label}</span>
      <kbd className="px-1 py-0.5 text-[10px] font-mono font-semibold rounded bg-black/40 text-slate-400 border border-white/10">
        {shortcut}
      </kbd>
    </button>
  );
};
