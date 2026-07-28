import { GoogleGenAI, GenerateContentParameters } from '@google/genai';

export interface ChatTurn {
  role: 'user' | 'model';
  parts: Array<{ text: string }>;
}

export interface StreamCompletionOptions {
  apiKey: string;
  modelName?: string;
  systemInstruction?: string;
  history?: ChatTurn[];
  prompt: string;
  onChunk: (chunkText: string) => void;
}

export class GeminiClient {
  private defaultModel = 'gemini-2.0-flash';

  async streamCompletion(options: StreamCompletionOptions): Promise<string> {
    const { apiKey, modelName = this.defaultModel, systemInstruction, history = [], prompt, onChunk } = options;

    if (!apiKey) {
      throw new Error('Gemini API key is required. Please set it in Project ZERO Settings.');
    }

    const ai = new GoogleGenAI({ apiKey });
    let fullResponseText = '';

    try {
      const contents: ChatTurn[] = [
        ...history,
        { role: 'user', parts: [{ text: prompt }] },
      ];

      const params: GenerateContentParameters = {
        model: modelName,
        contents,
      };

      if (systemInstruction) {
        params.config = {
          systemInstruction: {
            parts: [{ text: systemInstruction }],
          },
        };
      }

      const responseStream = await ai.models.generateContentStream(params);

      for await (const chunk of responseStream) {
        const text = chunk.text;
        if (text) {
          fullResponseText += text;
          onChunk(text);
        }
      }

      return fullResponseText;
    } catch (error) {
      console.error('Gemini API Streaming Error:', error);
      throw new Error(`Gemini API call failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
}
