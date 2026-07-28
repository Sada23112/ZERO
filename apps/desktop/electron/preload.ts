import { contextBridge, ipcRenderer } from 'electron';

export interface ZeroApi {
  getSettings: () => Promise<Record<string, unknown>>;
  saveSettings: (settings: Record<string, unknown>) => Promise<boolean>;
  fetchModels: (apiKey?: string) => Promise<Array<{ id: string; name: string }>>;
  hideOverlay: () => Promise<void>;
  onNavigate: (callback: (view: string) => void) => void;
}

const api: ZeroApi = {
  getSettings: () => ipcRenderer.invoke('zero:get-settings'),
  saveSettings: (settings) => ipcRenderer.invoke('zero:save-settings', settings),
  fetchModels: (apiKey?: string) => ipcRenderer.invoke('zero:fetch-models', apiKey),
  hideOverlay: () => ipcRenderer.invoke('zero:hide-overlay'),
  onNavigate: (callback) => {
    ipcRenderer.on('zero:navigate', (_event, view) => callback(view));
  },
};

contextBridge.exposeInMainWorld('zeroApi', api);
