"""Project ZERO — SQLite Database Connection & Migration Manager."""

from pathlib import Path
import sqlite3
from typing import Optional
from zero_logging import logger


class DatabaseManager:
    """Manages SQLite database connections, WAL mode enablement, and schema initialization."""

    def __init__(self, db_path: str = "data/zero.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a configured SQLite connection with WAL mode enabled."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def init_database(self) -> None:
        """Create required database tables if they do not exist."""
        with self.get_connection() as conn:
            # Sessions Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)

            # Messages Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    model TEXT,
                    tokens INTEGER,
                    created_at TEXT NOT NULL,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
                );
            """)

            # Memories Table (Key-Value & Categories)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    category TEXT NOT NULL,
                    tags TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT
                );
            """)

            # Command Audit Execution Logs Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id TEXT PRIMARY KEY,
                    command TEXT NOT NULL,
                    output TEXT,
                    exit_code INTEGER,
                    executed_at TEXT NOT NULL
                );
            """)
            conn.commit()
            logger.debug(f"SQLite database initialized cleanly at {self.db_path}")
