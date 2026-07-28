import { GeminiClient } from './gemini-client.js';
import { ConversationManager, MemoryRetrievalEngine, StoredMessage } from '@zero/memory';
import { PermissionGatekeeper } from '@zero/security';

export interface ChatEngineOptions {
  convManager: ConversationManager;
  retrievalEngine: MemoryRetrievalEngine;
  gatekeeper: PermissionGatekeeper;
  geminiClient: GeminiClient;
}

export class ChatEngine {
  constructor(private options: ChatEngineOptions) {}

  async processUserMessage(
    chatId: string,
    userText: string,
    apiKey: string,
    onChunk: (chunk: string) => void
  ): Promise<{ message: StoredMessage; retrievedMemories: string[] }> {
    const { convManager, retrievalEngine, geminiClient } = this.options;

    // 1. Save user message to memory
    convManager.addMessage(chatId, 'user', userText);

    // 2. Retrieve relevant memory context
    const searchResults = retrievalEngine.searchFullText(userText, 3);
    const retrievedMemories = searchResults.map((r) => r.text);

    // 3. Assemble system instruction & history
    const allMessages = convManager.getMessages(chatId);
    const history = allMessages.slice(0, -1).map((m) => ({
      role: (m.sender === 'user' ? 'user' : 'model') as 'user' | 'model',
      parts: [{ text: m.text }],
    }));

    const systemInstruction = `You are Project ZERO—a personal autonomous intelligence platform and lifelong engineering partner.
Be concise, accurate, technically rigorous, calm, and honest.
${retrievedMemories.length > 0 ? `Relevant Past Memories:\n- ${retrievedMemories.join('\n- ')}` : ''}`;

    // 4. Stream response from Gemini
    const fullText = await geminiClient.streamCompletion({
      apiKey,
      prompt: userText,
      history,
      systemInstruction,
      onChunk,
    });

    // 5. Save ZERO response to memory
    const zeroMsg = convManager.addMessage(chatId, 'zero', fullText);

    return { message: zeroMsg, retrievedMemories };
  }
}
