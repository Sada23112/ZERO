import fs from 'node:fs';
import path from 'node:path';

export interface ZeroConfig {
  geminiApiKey: string;
  defaultProvider: string;
  defaultModel: string;
  autoLaunch: boolean;
  debug: boolean;
}

export class ConfigManager {
  private envPath: string;
  private settingsPath: string;

  constructor(baseDir: string = process.cwd(), userDataDir?: string) {
    this.envPath = path.join(baseDir, '.env');
    this.settingsPath = userDataDir
      ? path.join(userDataDir, 'zero-settings.json')
      : path.join(baseDir, 'zero-settings.json');
  }

  getConfig(): ZeroConfig {
    const envVars = this.readEnv();
    const settings = this.readSettings();

    return {
      geminiApiKey: envVars.GEMINI_API_KEY || (settings.apiKey as string) || '',
      defaultProvider: envVars.DEFAULT_PROVIDER || (settings.provider as string) || 'gemini',
      defaultModel: envVars.DEFAULT_MODEL || (settings.modelName as string) || 'gemini-2.0-flash',
      autoLaunch: Boolean(settings.autoLaunch ?? false),
      debug: (envVars.DEBUG === 'true') || Boolean(settings.debug ?? false),
    };
  }

  updateConfig(updates: Partial<ZeroConfig>): boolean {
    try {
      const currentConfig = this.getConfig();
      const updatedConfig: ZeroConfig = { ...currentConfig, ...updates };

      // Update .env
      const envLines: string[] = [
        `# Project ZERO Local Configuration`,
        `GEMINI_API_KEY=${updatedConfig.geminiApiKey}`,
        `DEFAULT_PROVIDER=${updatedConfig.defaultProvider}`,
        `DEFAULT_MODEL=${updatedConfig.defaultModel}`,
        `DEBUG=${updatedConfig.debug}`,
      ];
      fs.writeFileSync(this.envPath, envLines.join('\n'), 'utf-8');

      // Update zero-settings.json
      const settingsPayload = {
        apiKey: updatedConfig.geminiApiKey,
        provider: updatedConfig.defaultProvider,
        modelName: updatedConfig.defaultModel,
        autoLaunch: updatedConfig.autoLaunch,
        debug: updatedConfig.debug,
      };
      fs.mkdirSync(path.dirname(this.settingsPath), { recursive: true });
      fs.writeFileSync(this.settingsPath, JSON.stringify(settingsPayload, null, 2), 'utf-8');

      return true;
    } catch (err) {
      console.error('Failed to update Zero Config:', err);
      return false;
    }
  }

  private readEnv(): Record<string, string> {
    const result: Record<string, string> = {};
    try {
      if (fs.existsSync(this.envPath)) {
        const content = fs.readFileSync(this.envPath, 'utf-8');
        content.split('\n').forEach((line) => {
          const trimmed = line.trim();
          if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
            const [key, ...rest] = trimmed.split('=');
            result[key.trim()] = rest.join('=').trim();
          }
        });
      }
    } catch (err) {
      console.warn('Could not read .env:', err);
    }
    return result;
  }

  private readSettings(): Record<string, unknown> {
    try {
      if (fs.existsSync(this.settingsPath)) {
        const data = fs.readFileSync(this.settingsPath, 'utf-8');
        return JSON.parse(data);
      }
    } catch (err) {
      console.warn('Could not read settings JSON:', err);
    }
    return {};
  }
}
