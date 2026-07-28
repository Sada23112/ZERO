import React, { useState, useEffect } from 'react';
import { Key, Cpu, Power, Save, RefreshCw, CheckCircle2, Shield } from 'lucide-react';
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
        setSavedMessage('Settings saved cleanly');
        setTimeout(() => setSavedMessage(''), 3000);
      }
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-5 space-y-5 max-h-[460px] overflow-y-auto font-sans"
    >
      <div className="flex items-center justify-between pb-3 border-b border-white/10">
        <div>
          <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <Shield className="w-4 h-4 text-blue-400" />
            System Preferences
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Configure model routing, API tokens, and Windows startup preferences.
          </p>
        </div>
      </div>

      {/* Group 1: Gemini API Key */}
      <div className="p-4 rounded-xl bg-slate-950/60 border border-white/10 space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-medium text-slate-200 flex items-center gap-2">
            <Key className="w-4 h-4 text-amber-400" />
            Gemini API Authentication
          </label>
          <span className="text-[11px] text-slate-500 font-mono">Stored in zero-settings.json</span>
        </div>

        <div className="flex gap-2">
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter Gemini API Key..."
            className="flex-1 bg-slate-900/90 border border-white/10 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500/50 font-mono"
          />
          <button
            onClick={() => loadModels(apiKey)}
            disabled={isFetchingModels || !apiKey.trim()}
            className="px-3 py-2 rounded-lg bg-slate-800 border border-white/10 text-xs font-medium text-slate-200 hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-1.5 cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isFetchingModels ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Group 2: Dynamic Model Selector */}
      <div className="p-4 rounded-xl bg-slate-950/60 border border-white/10 space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-medium text-slate-200 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-purple-400" />
            Model Router Selection
          </label>
          {availableModels.length > 0 && (
            <span className="text-[11px] text-emerald-400 font-mono font-medium flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" />
              {availableModels.length} Models Available
            </span>
          )}
        </div>

        <select
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          className="w-full bg-slate-900/90 border border-white/10 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-purple-500/50 font-mono"
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
              <option value="gemini-2.5-pro">Gemini 2.5 Pro (High Reasoning)</option>
              <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
              <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
            </>
          )}
        </select>
      </div>

      {/* Group 3: Startup Integration */}
      <div className="p-4 rounded-xl bg-slate-950/60 border border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Power className="w-4 h-4 text-blue-400" />
          <div>
            <span className="text-xs font-medium text-slate-200 block">Launch on Windows Startup</span>
            <span className="text-[11px] text-slate-400">Run background daemon automatically when computer starts.</span>
          </div>
        </div>

        <input
          type="checkbox"
          checked={autoLaunch}
          onChange={(e) => setAutoLaunch(e.target.checked)}
          className="w-4 h-4 accent-blue-500 rounded cursor-pointer"
        />
      </div>

      {/* Action Footer */}
      <div className="flex items-center gap-3 pt-2">
        <button
          onClick={handleSave}
          className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition-all shadow-md active:scale-95 flex items-center gap-2 cursor-pointer"
        >
          <Save className="w-4 h-4" />
          <span>Save Preferences</span>
        </button>
        {savedMessage && (
          <span className="text-xs text-emerald-400 font-mono flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            {savedMessage}
          </span>
        )}
      </div>
    </motion.div>
  );
};
