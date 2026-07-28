export { GeminiClient, StreamCompletionOptions, ChatTurn } from './gemini-client.js';
export { ChatEngine, ChatEngineOptions } from './chat-engine.js';

export const ZERO_VERSION = '0.1.0-alpha';

export function getCoreInfo(): string {
  return `Project ZERO Core Engine v${ZERO_VERSION} (Gemini + Memory + Security Active)`;
}
