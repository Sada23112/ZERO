"""Unit tests for ConversationManager."""

import pytest
from pathlib import Path
from memory.database import DatabaseManager
from memory.repository import ConversationRepository
from brain.conversation import ConversationManager
from models.conversation import MessageRole


@pytest.fixture
def temp_conv_manager(tmp_path: Path):
    db_file = tmp_path / "conv_test.db"
    db_manager = DatabaseManager(str(db_file))
    repo = ConversationRepository(db_manager)
    return ConversationManager(repo)


def test_conversation_manager_session_lifecycle(temp_conv_manager: ConversationManager):
    session1 = temp_conv_manager.active_session
    assert session1.id is not None

    session2 = temp_conv_manager.new_session("Secondary Session")
    assert session2.id != session1.id
    assert session2.title == "Secondary Session"


def test_conversation_manager_append_and_load(temp_conv_manager: ConversationManager):
    msg1 = temp_conv_manager.append_message(role=MessageRole.USER, content="Test Prompt 1")
    assert msg1.content == "Test Prompt 1"

    msg2 = temp_conv_manager.append_message(role=MessageRole.ASSISTANT, content="Test Response 1")
    assert msg2.content == "Test Response 1"

    history = temp_conv_manager.load_history()
    assert len(history) == 2
    assert history[0].content == "Test Prompt 1"
    assert history[1].content == "Test Response 1"

    summary = temp_conv_manager.summarize_long_conversation()
    assert "2 turns" in summary
