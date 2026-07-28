import { app, BrowserWindow, globalShortcut, Tray, Menu, ipcMain, screen } from 'electron';
import path from 'node:path';
import fs from 'node:fs';

let mainWindow: BrowserWindow | null = null;
let tray: Tray | null = null;

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

function getSettingsPath(): string {
  const userDataPath = app.getPath('userData');
  return path.join(userDataPath, 'zero-settings.json');
}

function loadSettings() {
  try {
    const settingsPath = getSettingsPath();
    if (fs.existsSync(settingsPath)) {
      const data = fs.readFileSync(settingsPath, 'utf-8');
      return JSON.parse(data);
    }
  } catch (err) {
    console.error('Failed to load settings:', err);
  }
  return {
    apiKey: '',
    modelName: 'gemini-2.0-flash',
    autoLaunch: false,
    theme: 'dark',
  };
}

function saveSettings(settings: Record<string, unknown>) {
  try {
    const settingsPath = getSettingsPath();
    fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), 'utf-8');
    return true;
  } catch (err) {
    console.error('Failed to save settings:', err);
    return false;
  }
}

async function fetchDynamicGeminiModels(apiKey: string) {
  if (!apiKey || !apiKey.trim()) return [];
  try {
    const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey.trim()}`);
    if (!res.ok) {
      console.warn(`Gemini Models API returned HTTP ${res.status}`);
      return [];
    }
    const data = (await res.json()) as { models?: Array<{ name: string; displayName?: string; supportedGenerationMethods?: string[] }> };
    if (data && Array.isArray(data.models)) {
      return data.models
        .filter((m) => m.supportedGenerationMethods && m.supportedGenerationMethods.includes('generateContent'))
        .map((m) => {
          const id = m.name.replace('models/', '');
          return {
            id,
            name: m.displayName ? `${m.displayName} (${id})` : id,
          };
        });
    }
  } catch (err) {
    console.error('Dynamic Gemini model fetch failed:', err);
  }
  return [];
}

function createOverlayWindow(): BrowserWindow {
  const primaryDisplay = screen.getPrimaryDisplay();
  const { width: screenWidth, height: screenHeight } = primaryDisplay.workAreaSize;

  const windowWidth = 720;
  const windowHeight = 560;
  const x = Math.round((screenWidth - windowWidth) / 2);
  const y = Math.round((screenHeight - windowHeight) / 3);

  const win = new BrowserWindow({
    width: windowWidth,
    height: windowHeight,
    x,
    y,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: true,
    show: false,
    skipTaskbar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  if (isDev) {
    win.loadURL('http://localhost:5173');
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  win.on('blur', () => {
    if (!win.webContents.isDevToolsOpened()) {
      win.hide();
    }
  });

  return win;
}

function createTray() {
  const iconPath = path.join(__dirname, '../resources/icon.png');
  tray = new Tray(fs.existsSync(iconPath) ? iconPath : path.join(__dirname, 'preload.js'));
  tray.setToolTip('Project ZERO - Autonomous AI Companion');

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Toggle Overlay (Alt+Space)',
      click: () => toggleOverlay(),
    },
    {
      label: 'Settings',
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
          mainWindow.webContents.send('zero:navigate', 'settings');
        }
      },
    },
    { type: 'separator' },
    {
      label: 'Quit Project ZERO',
      click: () => {
        app.quit();
      },
    },
  ]);

  tray.setContextMenu(contextMenu);
  tray.on('click', () => toggleOverlay());
}

function toggleOverlay() {
  if (!mainWindow) return;
  if (mainWindow.isVisible()) {
    mainWindow.hide();
  } else {
    mainWindow.show();
    mainWindow.focus();
  }
}

function registerGlobalHotkeys() {
  const ret = globalShortcut.register('Alt+Space', () => {
    toggleOverlay();
  });

  if (!ret) {
    console.warn('Failed to register global hotkey Alt+Space');
  }
}

function setupIpcHandlers() {
  ipcMain.handle('zero:get-settings', () => {
    return loadSettings();
  });

  ipcMain.handle('zero:save-settings', (_event, settings) => {
    const success = saveSettings(settings);
    if (settings.autoLaunch !== undefined) {
      app.setLoginItemSettings({
        openAtLogin: Boolean(settings.autoLaunch),
        path: app.getPath('exe'),
      });
    }
    return success;
  });

  ipcMain.handle('zero:fetch-models', async (_event, apiKey?: string) => {
    const settings = loadSettings();
    const keyToUse = apiKey || settings.apiKey;
    return await fetchDynamicGeminiModels(keyToUse);
  });

  ipcMain.handle('zero:hide-overlay', () => {
    if (mainWindow) {
      mainWindow.hide();
    }
  });
}

app.whenReady().then(() => {
  setupIpcHandlers();
  mainWindow = createOverlayWindow();
  createTray();
  registerGlobalHotkeys();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      mainWindow = createOverlayWindow();
    }
  });
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});

app.on('window-all-closed', () => {
  // Prevent quitting on window close to stay running in system tray
});
