import React, { useState, useEffect } from 'react';
import { OverlayHeader } from './components/OverlayHeader';
import { ChatOverlay, ChatMessage } from './components/ChatOverlay';
import { SettingsView } from './components/SettingsView';

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
  const [currentView, setCurrentView] = useState<'chat' | 'settings'>('chat');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    if (window.zeroApi) {
      window.zeroApi.onNavigate((view) => {
        if (view === 'settings' || view === 'chat') {
          setCurrentView(view);
        }
      });
    }
  }, []);

  const handleSendMessage = (text: string) => {
    const userMsg: ChatMessage = {
      id: `msg_${Date.now()}`,
      sender: 'user',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsStreaming(true);

    setTimeout(() => {
      const zeroMsg: ChatMessage = {
        id: `msg_${Date.now() + 1}`,
        sender: 'zero',
        text: `Project ZERO received: "${text}". Memory & Model Router initializing.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, zeroMsg]);
      setIsStreaming(false);
    }, 600);
  };

  const handleHide = () => {
    if (window.zeroApi) {
      window.zeroApi.hideOverlay();
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        backgroundColor: '#0f172a',
        borderRadius: '12px',
        border: '1px solid #1e293b',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4)',
        overflow: 'hidden',
      }}
    >
      <OverlayHeader
        currentView={currentView}
        onViewChange={(view) => setCurrentView(view)}
        onHide={handleHide}
      />
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {currentView === 'chat' ? (
          <ChatOverlay
            messages={messages}
            onSendMessage={handleSendMessage}
            isStreaming={isStreaming}
          />
        ) : (
          <SettingsView />
        )}
      </div>
    </div>
  );
};

export default App;
