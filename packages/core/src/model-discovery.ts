export interface DiscoveredModel {
  id: string;
  displayName: string;
  version: string;
  description?: string;
  inputTokenLimit?: number;
  outputTokenLimit?: number;
  supportedMethods: string[];
}

export class ModelDiscoveryEngine {
  private cache: Map<string, DiscoveredModel[]> = new Map();

  async fetchAvailableModels(apiKey: string, forceRefresh: boolean = false): Promise<DiscoveredModel[]> {
    if (!apiKey || !apiKey.trim()) {
      return [];
    }

    const trimmedKey = apiKey.trim();

    if (!forceRefresh && this.cache.has(trimmedKey)) {
      return this.cache.get(trimmedKey)!;
    }

    try {
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${trimmedKey}`);
      if (!response.ok) {
        console.warn(`Gemini Model Discovery returned HTTP ${response.status}`);
        return [];
      }

      const data = (await response.json()) as {
        models?: Array<{
          name: string;
          displayName?: string;
          version?: string;
          description?: string;
          inputTokenLimit?: number;
          outputTokenLimit?: number;
          supportedGenerationMethods?: string[];
        }>;
      };

      if (data && Array.isArray(data.models)) {
        const models: DiscoveredModel[] = data.models
          .filter((m) => m.supportedGenerationMethods && m.supportedGenerationMethods.includes('generateContent'))
          .map((m) => {
            const id = m.name.replace('models/', '');
            return {
              id,
              displayName: m.displayName || id,
              version: m.version || 'latest',
              description: m.description,
              inputTokenLimit: m.inputTokenLimit,
              outputTokenLimit: m.outputTokenLimit,
              supportedMethods: m.supportedGenerationMethods || [],
            };
          });

        this.cache.set(trimmedKey, models);
        return models;
      }
    } catch (err) {
      console.error('Failed to discover Gemini models dynamically:', err);
    }

    return [];
  }

  clearCache() {
    this.cache.clear();
  }
}
