import React, { useState, useRef, useEffect } from 'react';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'zero';
  text: string;
  timestamp: string;
}

interface ChatOverlayProps {
  messages: ChatMessage[];
  onSendMessage: (text: string) => void;
  isStreaming: boolean;
}

export const ChatOverlay: React.FC<ChatOverlayProps> = ({
  messages,
  onSendMessage,
  isStreaming,
}) => {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isStreaming]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || isStreaming) return;
    onSendMessage(inputText);
    setInputText('');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', backgroundColor: '#0f172a' }}>
      {/* Message List */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
        }}
      >
        {messages.length === 0 ? (
          <div
            style={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#64748b',
              textAlign: 'center',
              gap: '8px',
            }}
          >
            <div style={{ fontSize: '24px' }}>⚡</div>
            <div style={{ fontSize: '14px', fontWeight: 500, color: '#94a3b8' }}>
              Project ZERO Cognitive Assistant
            </div>
            <div style={{ fontSize: '12px', maxWidth: '360px' }}>
              Press <kbd style={{ background: '#1e293b', padding: '2px 6px', borderRadius: '4px', border: '1px solid #334155' }}>Alt + Space</kbd> anytime to toggle overlay.
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              style={{
                alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '85%',
                display: 'flex',
                flexDirection: 'column',
                gap: '4px',
              }}
            >
              <div
                style={{
                  backgroundColor: msg.sender === 'user' ? '#2563eb' : '#1e293b',
                  color: '#f8fafc',
                  padding: '10px 14px',
                  borderRadius: msg.sender === 'user' ? '12px 12px 2px 12px' : '12px 12px 12px 2px',
                  fontSize: '13px',
                  lineHeight: '1.5',
                  wordBreak: 'break-word',
                  whiteSpace: 'pre-wrap',
                  border: msg.sender === 'zero' ? '1px solid #334155' : 'none',
                }}
              >
                {msg.text}
              </div>
              <span
                style={{
                  fontSize: '10px',
                  color: '#64748b',
                  alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  padding: '0 4px',
                }}
              >
                {msg.timestamp}
              </span>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form
        onSubmit={handleSubmit}
        style={{
          padding: '12px 16px',
          borderTop: '1px solid #1e293b',
          backgroundColor: '#0f172a',
          display: 'flex',
          gap: '8px',
        }}
      >
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={isStreaming ? 'ZERO is thinking...' : 'Ask ZERO anything or command workspace...'}
          disabled={isStreaming}
          style={{
            flex: 1,
            backgroundColor: '#1e293b',
            border: '1px solid #334155',
            borderRadius: '8px',
            color: '#f8fafc',
            padding: '10px 14px',
            fontSize: '13px',
            outline: 'none',
          }}
        />
        <button
          type="submit"
          disabled={isStreaming || !inputText.trim()}
          style={{
            backgroundColor: isStreaming || !inputText.trim() ? '#334155' : '#2563eb',
            color: '#ffffff',
            border: 'none',
            borderRadius: '8px',
            padding: '0 16px',
            fontSize: '13px',
            fontWeight: 600,
            cursor: isStreaming || !inputText.trim() ? 'not-allowed' : 'pointer',
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};
