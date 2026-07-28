"""Project ZERO — Conversation & Memory Repositories."""

import json
from typing import List, Optional, Dict, Any
from memory.database import DatabaseManager
from models.conversation import Message, Session, MessageRole
from models.memory import MemoryRecord, MemoryCategory


class ConversationRepository:
    """Repository operations for sessions and message transcript history."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_session(self, title: str = "New Session") -> Session:
        """Create a new conversation session."""
        session = Session(title=title)
        with self.db_manager.get_connection() as conn:
            conn.execute(
                "INSERT INTO sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (session.id, session.title, session.created_at, session.updated_at)
            )
            conn.commit()
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Fetch session by ID."""
        with self.db_manager.get_connection() as conn:
            row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if row:
                return Session(
                    id=row["id"],
                    title=row["title"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
        return None

    def list_sessions(self, limit: int = 20) -> List[Session]:
        """Fetch list of recent sessions."""
        with self.db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM sessions ORDER BY updated_at DESC LIMIT ?", (limit,)
            ).fetchall()
            return [
                Session(
                    id=r["id"],
                    title=r["title"],
                    created_at=r["created_at"],
                    updated_at=r["updated_at"]
                )
                for r in rows
            ]

    def add_message(self, message: Message) -> Message:
        """Persist message in session history."""
        with self.db_manager.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO messages (id, session_id, role, content, model, tokens, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    message.id,
                    message.session_id,
                    message.role.value if isinstance(message.role, MessageRole) else str(message.role),
                    message.content,
                    message.model,
                    message.tokens,
                    message.created_at,
                    json.dumps(message.metadata)
                )
            )
            conn.execute(
                "UPDATE sessions SET updated_at = ? WHERE id = ?",
                (message.created_at, message.session_id)
            )
            conn.commit()
        return message

    def get_session_messages(self, session_id: str, limit: Optional[int] = None) -> List[Message]:
        """Retrieve ordered history of messages for a session."""
        with self.db_manager.get_connection() as conn:
            query = "SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC"
            params: list = [session_id]
            if limit:
                query = "SELECT * FROM (SELECT * FROM messages WHERE session_id = ? ORDER BY created_at DESC LIMIT ?) ORDER BY created_at ASC"
                params = [session_id, limit]

            rows = conn.execute(query, tuple(params)).fetchall()
            return [
                Message(
                    id=r["id"],
                    session_id=r["session_id"],
                    role=MessageRole(r["role"]),
                    content=r["content"],
                    model=r["model"],
                    tokens=r["tokens"],
                    created_at=r["created_at"],
                    metadata=json.loads(r["metadata"]) if r["metadata"] else {}
                )
                for r in rows
            ]


class MemoryRepository:
    """Repository operations for cognitive key-value & categorical memory."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def store(
        self,
        key: str,
        value: str,
        category: MemoryCategory = MemoryCategory.GENERAL,
        tags: Optional[List[str]] = None
    ) -> MemoryRecord:
        """Store or update a cognitive memory record."""
        tags = tags or []
        existing = self.get_memory_by_key(key)

        if existing:
            record = MemoryRecord(
                id=existing.id,
                key=key,
                value=value,
                category=category,
                tags=tags,
                created_at=existing.created_at
            )
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    """
                    UPDATE memories SET value = ?, category = ?, tags = ?, updated_at = ?
                    WHERE key = ?
                    """,
                    (record.value, record.category.value, json.dumps(tags), record.updated_at, key)
                )
                conn.commit()
            return record

        record = MemoryRecord(key=key, value=value, category=category, tags=tags)
        with self.db_manager.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO memories (id, key, value, category, tags, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.key,
                    record.value,
                    record.category.value,
                    json.dumps(record.tags),
                    record.created_at,
                    record.updated_at,
                    json.dumps(record.metadata)
                )
            )
            conn.commit()
        return record

    def set_memory(self, key: str, value: str, category: MemoryCategory = MemoryCategory.GENERAL, tags: Optional[List[str]] = None) -> MemoryRecord:
        """Alias for store()."""
        return self.store(key, value, category, tags)

    def get_memory_by_key(self, key: str) -> Optional[MemoryRecord]:
        """Fetch memory record by key."""
        with self.db_manager.get_connection() as conn:
            row = conn.execute("SELECT * FROM memories WHERE key = ?", (key,)).fetchone()
            if row:
                return self._row_to_memory(row)
        return None

    def search(self, query: str, limit: int = 10) -> List[MemoryRecord]:
        """Perform keyword search across memory keys, values, and categories."""
        pattern = f"%{query}%"
        with self.db_manager.get_connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM memories
                WHERE key LIKE ? OR value LIKE ? OR category LIKE ? OR tags LIKE ?
                ORDER BY updated_at DESC LIMIT ?
                """,
                (pattern, pattern, pattern, pattern, limit)
            ).fetchall()
            return [self._row_to_memory(r) for r in rows]

    def recent(self, limit: int = 10) -> List[MemoryRecord]:
        """Fetch most recently updated memory records."""
        with self.db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM memories ORDER BY updated_at DESC LIMIT ?", (limit,)
            ).fetchall()
            return [self._row_to_memory(r) for r in rows]

    def forget(self, key: str) -> bool:
        """Delete a memory record by key."""
        with self.db_manager.get_connection() as conn:
            cursor = conn.execute("DELETE FROM memories WHERE key = ?", (key,))
            conn.commit()
            return cursor.rowcount > 0

    def list(self, category: Optional[MemoryCategory] = None, limit: int = 50) -> List[MemoryRecord]:
        """List memory records, optionally filtered by category."""
        with self.db_manager.get_connection() as conn:
            if category:
                rows = conn.execute(
                    "SELECT * FROM memories WHERE category = ? ORDER BY updated_at DESC LIMIT ?",
                    (category.value, limit)
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM memories ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()

            return [self._row_to_memory(r) for r in rows]

    def list_memories(self, category: Optional[MemoryCategory] = None) -> List[MemoryRecord]:
        """Alias for list()."""
        return self.list(category)

    def _row_to_memory(self, row: Any) -> MemoryRecord:
        return MemoryRecord(
            id=row["id"],
            key=row["key"],
            value=row["value"],
            category=MemoryCategory(row["category"]),
            tags=json.loads(row["tags"]) if row["tags"] else [],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
        )
