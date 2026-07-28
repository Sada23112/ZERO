"""Unit tests for SQLite WAL memory subsystem."""

import pytest
from pathlib import Path
from memory.database import DatabaseManager
from memory.repository import ConversationRepository, MemoryRepository
from models.conversation import Message, MessageRole
from models.memory import MemoryCategory


@pytest.fixture
def temp_db(tmp_path: Path):
    db_file = tmp_path / "test_zero.db"
    return DatabaseManager(str(db_file))


def test_sqlite_wal_init(temp_db: DatabaseManager):
    conn = temp_db.get_connection()
    row = conn.execute("PRAGMA journal_mode;").fetchone()
    assert row[0].lower() == "wal"


def test_conversation_repository(temp_db: DatabaseManager):
    repo = ConversationRepository(temp_db)
    session = repo.create_session("Test Session")
    assert session.id is not None
    assert session.title == "Test Session"

    msg = Message(
        session_id=session.id,
        role=MessageRole.USER,
        content="Hello Project ZERO"
    )
    repo.add_message(msg)

    messages = repo.get_session_messages(session.id)
    assert len(messages) == 1
    assert messages[0].content == "Hello Project ZERO"
    assert messages[0].role == MessageRole.USER


def test_memory_repository(temp_db: DatabaseManager):
    repo = MemoryRepository(temp_db)
    record = repo.set_memory(
        key="user_name",
        value="Developer",
        category=MemoryCategory.USER_PREFERENCE,
        tags=["profile"]
    )
    assert record.key == "user_name"
    assert record.value == "Developer"

    fetched = repo.get_memory_by_key("user_name")
    assert fetched is not None
    assert fetched.value == "Developer"
    assert "profile" in fetched.tags
