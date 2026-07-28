import { SQLiteDatabaseManager } from './sqlite-db.js';

export interface SearchResult {
  id: string;
  chat_id: string;
  sender: string;
  text: string;
  timestamp: string;
}

export interface MemoryRecord {
  id: string;
  key: string;
  value: string;
  category: string;
  created_at: string;
}

export class MemoryRetrievalEngine {
  constructor(private dbManager: SQLiteDatabaseManager) {}

  searchFullText(query: string, limit: number = 10): SearchResult[] {
    if (!query || !query.trim()) return [];

    const db = this.dbManager.getDatabase();
    const stmt = db.prepare(
      'SELECT id, chat_id, sender, text, timestamp FROM messages WHERE text LIKE ? ORDER BY timestamp DESC LIMIT ?'
    );
    return stmt.all(`%${query}%`, limit) as SearchResult[];
  }

  saveMemory(key: string, value: string, category: string = 'general'): MemoryRecord {
    const db = this.dbManager.getDatabase();
    const id = `mem_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const now = new Date().toISOString();

    const stmt = db.prepare(`
      INSERT INTO memories (id, key, value, category, created_at)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(key) DO UPDATE SET value=excluded.value, created_at=excluded.created_at
    `);

    stmt.run(id, key, value, category, now);
    return { id, key, value, category, created_at: now };
  }

  getMemory(key: string): MemoryRecord | null {
    const db = this.dbManager.getDatabase();
    const stmt = db.prepare('SELECT * FROM memories WHERE key = ?');
    const res = stmt.get(key) as MemoryRecord | undefined;
    return res || null;
  }

  listMemories(category?: string): MemoryRecord[] {
    const db = this.dbManager.getDatabase();
    if (category) {
      const stmt = db.prepare('SELECT * FROM memories WHERE category = ? ORDER BY created_at DESC');
      return stmt.all(category) as MemoryRecord[];
    }
    const stmt = db.prepare('SELECT * FROM memories ORDER BY created_at DESC');
    return stmt.all() as MemoryRecord[];
  }
}
