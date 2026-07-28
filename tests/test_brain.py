"""Unit and integration tests for Brain coordinator & ContextBuilder."""

import pytest
from pathlib import Path
from brain.brain import Brain
from brain.context import ContextBuilder
from memory.database import DatabaseManager
from memory.repository import MemoryRepository, ConversationRepository, MemoryCategory


@pytest.fixture
def temp_brain(tmp_path: Path):
    db_file = tmp_path / "brain_test.db"
    db_manager = DatabaseManager(str(db_file))
    return Brain(db_manager=db_manager)


@pytest.mark.asyncio
async def test_brain_remember_and_recall_memory(temp_brain: Brain):
    # Test memory store trigger: "remember that Canalib uses Flutter"
    res1 = await temp_brain.process("remember that Canalib uses Flutter")
    assert "Recorded memory" in res1
    assert "Canalib -> uses Flutter" in res1

    # Test memory recall trigger: "what framework does Canalib use?"
    res2 = await temp_brain.process("what framework does Canalib use?")
    assert "Canalib uses Flutter" in res2


@pytest.mark.asyncio
async def test_brain_list_and_search_memories(temp_brain: Brain):
    await temp_brain.process("remember that Project ZERO uses Python")
    
    res_list = await temp_brain.process("list my memories")
    assert "Project ZERO" in res_list

    res_search = await temp_brain.process("search memory Python")
    assert "Project ZERO" in res_search


def test_context_builder(tmp_path: Path):
    db_file = tmp_path / "ctx_test.db"
    db_manager = DatabaseManager(str(db_file))
    mem_repo = MemoryRepository(db_manager)
    conv_repo = ConversationRepository(db_manager)

    mem_repo.store("framework", "Python 3.13", category=MemoryCategory.PROJECT_FACT)

    builder = ContextBuilder(mem_repo, conv_repo, workspace_root=tmp_path)
    system_prompt = builder.build_system_instruction("Tell me about framework")

    assert "Project ZERO" in system_prompt
    assert "framework: Python 3.13" in system_prompt
