export { SQLiteDatabaseManager } from './sqlite-db.js';
export { ConversationManager, ChatSession, StoredMessage } from './conversation-manager.js';
export { MemoryRetrievalEngine, SearchResult, MemoryRecord } from './memory-retrieval.js';

export function getMemoryInfo(): string {
  return 'Project ZERO Memory Subsystem (SQLite WAL + FTS5 Retrieval) Active';
}
