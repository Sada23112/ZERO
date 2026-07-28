"""Unit tests for Phase 4 Capability Expansion subsystems and tools."""

import subprocess
import pytest
from pathlib import Path
from tools.git_tool import GitTool
from tools.document import DocumentReaderTool
from tools.process import ProcessManagerTool
from intelligence.codebase import CodebaseIntelligence
from intelligence.search import SemanticSearchEngine
from memory.knowledge_graph import CognitiveKnowledgeGraph
from planner.task_manager import TaskManager
from security.failsafe import FailsafeSystem
from cli.diagnostics import SelfDiagnostics


@pytest.mark.asyncio
async def test_git_tool(tmp_path: Path):
    # Initialize a dummy git repository in tmp_path
    subprocess.run(["git", "init"], cwd=str(tmp_path), capture_output=True)

    tool = GitTool(workspace_root=tmp_path)
    res = await tool.execute("call_g1", {"subcommand": "status"})
    assert res.success is True
    assert "On branch" in res.output or "No commits yet" in res.output or "master" in res.output or "main" in res.output


def test_codebase_intelligence(tmp_path: Path):
    (tmp_path / "main.py").write_text("print('hello')", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("pytest", encoding="utf-8")

    intel = CodebaseIntelligence(workspace_root=tmp_path)
    analysis = intel.analyze_project()
    assert "Python" in analysis.languages
    assert "main.py" in analysis.entry_points
    assert "pip / uv" in analysis.package_managers


def test_semantic_search_engine(tmp_path: Path):
    (tmp_path / "sample.py").write_text("# TODO: Refactor test module\ndef test_fn(): pass", encoding="utf-8")

    engine = SemanticSearchEngine(workspace_root=tmp_path)
    todos = engine.search_todos()
    assert len(todos) >= 1
    assert "TODO: Refactor" in todos[0].line_content


@pytest.mark.asyncio
async def test_document_reader_tool(tmp_path: Path):
    json_file = tmp_path / "test.json"
    json_file.write_text('{"name": "ZERO", "version": 1}', encoding="utf-8")

    reader = DocumentReaderTool(workspace_root=tmp_path)
    res = await reader.execute("call_doc1", {"path": str(json_file)})
    assert res.success is True
    assert "ZERO" in res.output


@pytest.mark.asyncio
async def test_process_manager_tool():
    tool = ProcessManagerTool()
    res = await tool.execute("call_p1", {"action": "metrics"})
    assert res.success is True
    assert "CPU Usage" in res.output
    assert "RAM Usage" in res.output


def test_knowledge_graph(tmp_path: Path):
    kg_file = tmp_path / "kg.json"
    kg = CognitiveKnowledgeGraph(storage_file=kg_file)
    kg.add_relation("Flutter", "uses", "Canalib")

    query_res = kg.query_entity("Flutter")
    assert len(query_res["relationships"]) >= 1
    assert "Flutter --[uses]--> Canalib" in query_res["relationships"][0]


def test_task_manager(tmp_path: Path):
    tm_file = tmp_path / "tasks.json"
    tm = TaskManager(storage_file=tm_file)
    task = tm.create_task("Test Task", priority="high")
    assert task.title == "Test Task"

    completed = tm.complete_task(task.id)
    assert completed is True
    assert tm.list_tasks(status="completed")[0].title == "Test Task"


def test_self_diagnostics(tmp_path: Path):
    diag = SelfDiagnostics(workspace_root=tmp_path)
    report = diag.run_health_check()
    assert report.database_healthy is True
    assert report.workspace_writable is True


def test_failsafe_system(tmp_path: Path):
    failsafe = FailsafeSystem(backup_dir=tmp_path / "backups")
    sample_file = tmp_path / "file.txt"
    sample_file.write_text("original content", encoding="utf-8")

    backup = failsafe.create_safety_backup(sample_file)
    assert backup is not None
    assert backup.exists()
    assert backup.read_text(encoding="utf-8") == "original content"
