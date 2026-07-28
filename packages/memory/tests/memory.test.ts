import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { SQLiteDatabaseManager, ConversationManager, MemoryRetrievalEngine } from '../src/index.js';
import fs from 'node:fs';
import path from 'node:path';

describe('Milestones 10-12: Memory Subsystem (SQLite, History & Retrieval)', () => {
  let dbPath: string;
  let dbManager: SQLiteDatabaseManager;
  let convManager: ConversationManager;
  let retrievalEngine: MemoryRetrievalEngine;

  beforeEach(() => {
    dbPath = path.join(process.cwd(), `test_zero_${Date.now()}_${Math.random().toString(36).substring(2, 6)}.db`);
    dbManager = new SQLiteDatabaseManager(dbPath);
    convManager = new ConversationManager(dbManager);
    retrievalEngine = new MemoryRetrievalEngine(dbManager);
  });

  afterEach(() => {
    dbManager.close();
    if (fs.existsSync(dbPath)) {
      fs.unlinkSync(dbPath);
    }
  });

  it('Milestone 10: Should initialize SQLite DB & create tables', () => {
    const db = dbManager.getDatabase();
    const res = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as { name: string }[];
    const names = res.map((r) => r.name);
    expect(names).toContain('chats');
    expect(names).toContain('messages');
    expect(names).toContain('memories');
  });

  it('Milestone 11: Should perform CRUD on conversation history', () => {
    const chat = convManager.createChat('Test Conversation');
    expect(chat.id).toBeDefined();
    expect(chat.title).toBe('Test Conversation');

    convManager.addMessage(chat.id, 'user', 'Hello Project ZERO');
    convManager.addMessage(chat.id, 'zero', 'Hello Human Engineer');

    const history = convManager.getMessages(chat.id);
    expect(history.length).toBe(2);
    expect(history[0].text).toBe('Hello Project ZERO');
    expect(history[1].text).toBe('Hello Human Engineer');
  });

  it('Milestone 12: Should execute memory retrieval & key-value storage', () => {
    const chat = convManager.createChat('Search Test');
    convManager.addMessage(chat.id, 'user', 'How do I implement microkernel syscalls?');
    convManager.addMessage(chat.id, 'zero', 'You implement syscalls using typed Rust traits.');

    const searchResults = retrievalEngine.searchFullText('syscalls');
    expect(searchResults.length).toBeGreaterThan(0);
    expect(searchResults[0].text).toContain('syscalls');

    retrievalEngine.saveMemory('user_preferred_language', 'TypeScript', 'preferences');
    const mem = retrievalEngine.getMemory('user_preferred_language');
    expect(mem).not.toBeNull();
    expect(mem?.value).toBe('TypeScript');
  });
});
