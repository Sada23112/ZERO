import React, { useState, useEffect } from 'react';
import { Key, Cpu, Power, Save, RefreshCw, CheckCircle2, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

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
          if (!modelName || !fetched.some((m) => m.id === modelName)) {
            setModelName(fetched[0].id);
          }
        }
      }
    } catch (err) {
      console.error('Failed to fetch dynamic models:', err);
    } finally {
      setIsFetchingModels(false);
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
        setSavedMessage('Preferences updated & saved to .env');
        setTimeout(() => setSavedMessage(''), 3000);
      }
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 space-y-5 max-h-[460px] overflow-y-auto font-sans"
    >
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-200/80">
        <div>
          <h2 className="text-base font-semibold text-slate-900 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-blue-600" />
            System Preferences
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Manage provider authentication, dynamic model discovery, and .env configuration.
          </p>
        </div>
      </div>

      {/* Group 1: Gemini API Authentication */}
      <div className="p-4 rounded-2xl zero-light-card space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-800 flex items-center gap-2">
            <Key className="w-4 h-4 text-amber-500" />
            Gemini API Authentication Key
          </label>
          <span className="text-[11px] text-slate-400 font-mono">Updates .env & zero-settings.json</span>
        </div>

        <div className="flex gap-2">
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter Gemini API Key..."
            className="zero-input flex-1 font-mono text-xs"
          />
          <button
            onClick={() => loadModels(apiKey)}
            disabled={isFetchingModels || !apiKey.trim()}
            className="px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50 transition-all flex items-center gap-1.5 shadow-sm cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${isFetchingModels ? 'animate-spin' : ''}`} />
            <span>Discover Models</span>
          </button>
        </div>
      </div>

      {/* Group 2: Dynamic Model Discovery Selector */}
      <div className="p-4 rounded-2xl zero-light-card space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-800 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-purple-600" />
            Dynamic Model Router Selection
          </label>
          {availableModels.length > 0 && (
            <span className="text-[11px] text-emerald-600 font-mono font-medium flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {availableModels.length} Models Discovered
            </span>
          )}
        </div>

        <select
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          className="zero-select w-full font-mono text-xs"
        >
          {availableModels.length > 0 ? (
            availableModels.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))
          ) : (
            <>
              <option value="gemini-2.0-flash">Gemini 2.0 Flash (Default / High Speed)</option>
              <option value="gemini-2.5-pro">Gemini 2.5 Pro (Deep Reasoning)</option>
              <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
              <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
            </>
          )}
        </select>
      </div>

      {/* Group 3: Windows Startup */}
      <div className="p-4 rounded-2xl zero-light-card flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Power className="w-4 h-4 text-blue-600" />
          <div>
            <span className="text-xs font-semibold text-slate-800 block">Launch with Windows Startup</span>
            <span className="text-[11px] text-slate-500">Run background daemon automatically on system boot.</span>
          </div>
        </div>

        <input
          type="checkbox"
          checked={autoLaunch}
          onChange={(e) => setAutoLaunch(e.target.checked)}
          className="zero-checkbox"
        />
      </div>

      {/* Action Footer */}
      <div className="flex items-center gap-3 pt-2">
        <button onClick={handleSave} className="zero-btn-primary flex items-center gap-2">
          <Save className="w-4 h-4" />
          <span>Save System Preferences</span>
        </button>
        {savedMessage && (
          <span className="text-xs text-emerald-600 font-mono flex items-center gap-1 font-medium">
            <CheckCircle2 className="w-3.5 h-3.5" />
            {savedMessage}
          </span>
        )}
      </div>
    </motion.div>
  );
};
