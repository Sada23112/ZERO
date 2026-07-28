import React, { useState, useEffect } from 'react';

interface DynamicModel {
  id: string;
  name: string;
}

export const SettingsView: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [modelName, setModelName] = useState('gemini-2.0-flash');
  const [availableModels, setAvailableModels] = useState<DynamicModel[]>([]);
  const [autoLaunch, setAutoLaunch] = useState(false);
  const [isFetchingModels, setIsFetchingModels] = useState(false);
  const [savedMessage, setSavedMessage] = useState('');

  useEffect(() => {
    if (window.zeroApi) {
      window.zeroApi.getSettings().then((settings) => {
        if (settings) {
          const key = (settings.apiKey as string) || '';
          const model = (settings.modelName as string) || 'gemini-2.0-flash';
          setApiKey(key);
          setModelName(model);
          setAutoLaunch(Boolean(settings.autoLaunch));
          if (key) {
            loadModels(key);
          }
        }
      });
    }
  }, []);

  const loadModels = async (keyToUse: string) => {
    if (!keyToUse.trim()) return;
    setIsFetchingModels(true);
    try {
      if (window.zeroApi && window.zeroApi.fetchModels) {
        const fetched = await window.zeroApi.fetchModels(keyToUse);
        if (fetched && fetched.length > 0) {
          setAvailableModels(fetched);
          if (!modelName || !fetched.some((m: DynamicModel) => m.id === modelName)) {
            setModelName(fetched[0].id);
          }
        }
      } else {
        // Fallback for browser direct dev
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${keyToUse.trim()}`);
        if (res.ok) {
          const data = (await res.json()) as { models?: Array<{ name: string; displayName?: string; supportedGenerationMethods?: string[] }> };
          if (data.models && Array.isArray(data.models)) {
            const models: DynamicModel[] = data.models
              .filter((m) => m.supportedGenerationMethods && m.supportedGenerationMethods.includes('generateContent'))
              .map((m) => {
                const id = m.name.replace('models/', '');
                return { id, name: m.displayName ? `${m.displayName} (${id})` : id };
              });
            setAvailableModels(models);
          }
        }
      }
    } catch (err) {
      console.error('Failed to fetch dynamic models:', err);
    } finally {
      setIsFetchingModels(false);
    }
  };

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setApiKey(val);
    if (val.length > 20) {
      loadModels(val);
    }
  };

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
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            type="password"
            value={apiKey}
            onChange={handleApiKeyChange}
            placeholder="Enter your Gemini API key..."
            style={{
              flex: 1,
              background: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '6px',
              color: '#f3f4f6',
              padding: '8px 12px',
              fontSize: '13px',
              outline: 'none',
            }}
          />
          <button
            onClick={() => loadModels(apiKey)}
            disabled={isFetchingModels || !apiKey.trim()}
            style={{
              background: '#374151',
              color: '#f3f4f6',
              border: 'none',
              borderRadius: '6px',
              padding: '0 12px',
              fontSize: '12px',
              cursor: isFetchingModels || !apiKey.trim() ? 'not-allowed' : 'pointer',
            }}
          >
            {isFetchingModels ? 'Fetching...' : 'Refresh Models'}
          </button>
        </div>
        <span style={{ fontSize: '11px', color: '#6b7280' }}>
          Stored locally in your profile (`zero-settings.json`). Never shared externally.
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <label style={{ fontSize: '12px', color: '#9ca3af' }}>Dynamic Model Router Selection</label>
          {availableModels.length > 0 && (
            <span style={{ fontSize: '11px', color: '#10b981' }}>
              ✓ {availableModels.length} Latest Gemini Models Available
            </span>
          )}
        </div>

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
          {availableModels.length > 0 ? (
            availableModels.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))
          ) : (
            <>
              <option value="gemini-2.0-flash">Gemini 2.0 Flash (Recommended / Default)</option>
              <option value="gemini-2.5-pro">Gemini 2.5 Pro (Latest Architecture)</option>
              <option value="gemini-2.5-flash">Gemini 2.5 Flash (Ultra Fast)</option>
              <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
              <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
            </>
          )}
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
          Launch Project ZERO automatically with Windows startup
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
