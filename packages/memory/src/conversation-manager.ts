import { SQLiteDatabaseManager } from './sqlite-db.js';

export interface ChatSession {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface StoredMessage {
  id: string;
  chat_id: string;
  sender: 'user' | 'zero';
  text: string;
  timestamp: string;
}

export class ConversationManager {
  constructor(private dbManager: SQLiteDatabaseManager) {}

  createChat(title: string = 'New Conversation'): ChatSession {
    const db = this.dbManager.getDatabase();
    const id = `chat_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const now = new Date().toISOString();

    const stmt = db.prepare('INSERT INTO chats (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)');
    stmt.run(id, title, now, now);

    return { id, title, created_at: now, updated_at: now };
  }

  getChat(chatId: string): ChatSession | null {
    const db = this.dbManager.getDatabase();
    const stmt = db.prepare('SELECT * FROM chats WHERE id = ?');
    const res = stmt.get(chatId) as ChatSession | undefined;
    return res || null;
  }

  listChats(): ChatSession[] {
    const db = this.dbManager.getDatabase();
    const stmt = db.prepare('SELECT * FROM chats ORDER BY updated_at DESC');
    return stmt.all() as ChatSession[];
  }

  addMessage(chatId: string, sender: 'user' | 'zero', text: string): StoredMessage {
    const db = this.dbManager.getDatabase();
    const id = `msg_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const timestamp = new Date().toISOString();

    const insertMsg = db.prepare('INSERT INTO messages (id, chat_id, sender, text, timestamp) VALUES (?, ?, ?, ?, ?)');
    const updateChat = db.prepare('UPDATE chats SET updated_at = ? WHERE id = ?');

    db.transaction(() => {
      insertMsg.run(id, chatId, sender, text, timestamp);
      updateChat.run(timestamp, chatId);
    })();

    return { id, chat_id: chatId, sender, text, timestamp };
  }

  getMessages(chatId: string): StoredMessage[] {
    const db = this.dbManager.getDatabase();
    const stmt = db.prepare('SELECT * FROM messages WHERE chat_id = ? ORDER BY timestamp ASC');
    return stmt.all(chatId) as StoredMessage[];
  }

  deleteChat(chatId: string): boolean {
    const db = this.dbManager.getDatabase();
    const stmt = db.prepare('DELETE FROM chats WHERE id = ?');
    const res = stmt.run(chatId);
    return res.changes > 0;
  }
}
