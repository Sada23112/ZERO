import React from 'react';

interface OverlayHeaderProps {
  currentView: 'chat' | 'settings';
  onViewChange: (view: 'chat' | 'settings') => void;
  onHide: () => void;
}

export const OverlayHeader: React.FC<OverlayHeaderProps> = ({
  currentView,
  onViewChange,
  onHide,
}) => {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '8px 16px',
        backgroundColor: '#111827',
        borderBottom: '1px solid #1f2937',
        borderTopLeftRadius: '12px',
        borderTopRightRadius: '12px',
        WebkitAppRegion: 'drag',
      } as React.CSSProperties}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <div
          style={{
            width: '10px',
            height: '10px',
            borderRadius: '50%',
            backgroundColor: '#3b82f6',
            boxShadow: '0 0 8px #3b82f6',
          }}
        />
        <span style={{ fontWeight: 600, fontSize: '13px', color: '#f3f4f6', letterSpacing: '0.5px' }}>
          PROJECT ZERO
        </span>
        <span style={{ fontSize: '10px', color: '#6b7280', paddingLeft: '4px' }}>v0.1</span>
      </div>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          WebkitAppRegion: 'no-drag',
        } as React.CSSProperties}
      >
        <button
          onClick={() => onViewChange('chat')}
          style={{
            background: currentView === 'chat' ? '#1f2937' : 'transparent',
            border: 'none',
            color: currentView === 'chat' ? '#60a5fa' : '#9ca3af',
            padding: '4px 10px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '12px',
            fontWeight: 500,
          }}
        >
          Assistant
        </button>
        <button
          onClick={() => onViewChange('settings')}
          style={{
            background: currentView === 'settings' ? '#1f2937' : 'transparent',
            border: 'none',
            color: currentView === 'settings' ? '#60a5fa' : '#9ca3af',
            padding: '4px 10px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '12px',
            fontWeight: 500,
          }}
        >
          Settings
        </button>
        <button
          onClick={onHide}
          title="Hide Overlay (Alt+Space)"
          style={{
            background: 'transparent',
            border: 'none',
            color: '#6b7280',
            fontSize: '14px',
            cursor: 'pointer',
            padding: '4px 8px',
            borderRadius: '4px',
          }}
        >
          ✕
        </button>
      </div>
    </div>
  );
};
