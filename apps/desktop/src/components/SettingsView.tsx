import React, { useState, useEffect } from 'react';

export const SettingsView: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [modelName, setModelName] = useState('gemini-1.5-pro');
  const [autoLaunch, setAutoLaunch] = useState(false);
  const [savedMessage, setSavedMessage] = useState('');

  useEffect(() => {
    if (window.zeroApi) {
      window.zeroApi.getSettings().then((settings) => {
        if (settings) {
          setApiKey((settings.apiKey as string) || '');
          setModelName((settings.modelName as string) || 'gemini-1.5-pro');
          setAutoLaunch(Boolean(settings.autoLaunch));
        }
      });
    }
  }, []);

  const handleSave = async () => {
    if (window.zeroApi) {
      const success = await window.zeroApi.saveSettings({
        apiKey,
        modelName,
        autoLaunch,
      });
      if (success) {
        setSavedMessage('Settings saved successfully!');
        setTimeout(() => setSavedMessage(''), 3000);
      }
    }
  };

  return (
    <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <h3 style={{ fontSize: '15px', color: '#f3f4f6', margin: 0 }}>System Settings</h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <label style={{ fontSize: '12px', color: '#9ca3af' }}>Gemini API Key</label>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter your Gemini API key..."
          style={{
            background: '#1f2937',
            border: '1px solid #374151',
            borderRadius: '6px',
            color: '#f3f4f6',
            padding: '8px 12px',
            fontSize: '13px',
            outline: 'none',
          }}
        />
        <span style={{ fontSize: '11px', color: '#6b7280' }}>
          Stored locally in your user profile. Never shared externally.
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <label style={{ fontSize: '12px', color: '#9ca3af' }}>Default Model</label>
        <select
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          style={{
            background: '#1f2937',
            border: '1px solid #374151',
            borderRadius: '6px',
            color: '#f3f4f6',
            padding: '8px 12px',
            fontSize: '13px',
            outline: 'none',
          }}
        >
          <option value="gemini-1.5-pro">Gemini 1.5 Pro (Recommended)</option>
          <option value="gemini-1.5-flash">Gemini 1.5 Flash (Ultra Fast)</option>
          <option value="gemini-2.0-flash-exp">Gemini 2.0 Flash</option>
        </select>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <input
          type="checkbox"
          id="autoLaunch"
          checked={autoLaunch}
          onChange={(e) => setAutoLaunch(e.target.checked)}
          style={{ accentColor: '#3b82f6', width: '16px', height: '16px' }}
        />
        <label htmlFor="autoLaunch" style={{ fontSize: '13px', color: '#d1d5db', cursor: 'pointer' }}>
          Launch Project ZERO automatically with Windows
        </label>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '10px' }}>
        <button
          onClick={handleSave}
          style={{
            background: '#2563eb',
            color: '#ffffff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 16px',
            fontSize: '13px',
            fontWeight: 500,
            cursor: 'pointer',
          }}
        >
          Save Settings
        </button>
        {savedMessage && <span style={{ fontSize: '12px', color: '#10b981' }}>{savedMessage}</span>}
      </div>
    </div>
  );
};
