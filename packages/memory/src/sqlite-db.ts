import Database from 'better-sqlite3';
import path from 'node:path';
import fs from 'node:fs';

export class SQLiteDatabaseManager {
  private db: Database.Database;

  constructor(dbPath?: string) {
    const finalPath = dbPath || this.getDefaultDbPath();
    fs.mkdirSync(path.dirname(finalPath), { recursive: true });

    this.db = new Database(finalPath);
    this.configurePragmas();
    this.runMigrations();
  }

  private getDefaultDbPath(): string {
    const homeDir = process.env.USERPROFILE || process.env.HOME || '.';
    return path.join(homeDir, '.zero', 'zero.db');
  }

  private configurePragmas(): void {
    this.db.pragma('journal_mode = WAL');
    this.db.pragma('synchronous = NORMAL');
    this.db.pragma('foreign_keys = ON');
  }

  private runMigrations(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS chats (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        chat_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        text TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (chat_id) REFERENCES chats (id) ON DELETE CASCADE
      );

      CREATE TABLE IF NOT EXISTS memories (
        id TEXT PRIMARY KEY,
        key TEXT NOT NULL UNIQUE,
        value TEXT NOT NULL,
        category TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
    `);
  }

  getDatabase(): Database.Database {
    return this.db;
  }

  close(): void {
    this.db.close();
  }
}
