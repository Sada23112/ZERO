"""Unit tests for Phase 6 Context & Awareness Engine."""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
from awareness.time_engine import TimeEngine
from awareness.calendar import CalendarAwareness
from awareness.environment import EnvironmentAwareness
from awareness.workspace import WorkspaceAwareness
from awareness.session_context import SessionContext
from awareness.activity import ActivityLogger
from awareness.experience import ExperienceEngine
from awareness.history import DailyMemoryStore
from awareness.context_manager import ContextManager
from brain.brain import Brain


def test_time_engine():
    engine = TimeEngine()
    now = engine.get_now()

    today_dt = engine.parse_expression("today")
    assert today_dt is not None
    assert today_dt.day == now.day

    yest_dt = engine.parse_expression("yesterday")
    assert yest_dt is not None
    assert yest_dt.date() == (now - timedelta(days=1)).date()

    morning_dt = engine.parse_expression("this morning")
    assert morning_dt is not None
    assert morning_dt.hour == 9

    two_days = engine.parse_expression("two days ago")
    assert two_days is not None
    assert two_days.date() == (now - timedelta(days=2)).date()


def test_calendar_awareness():
    info = CalendarAwareness.get_current_info()
    assert "current_time" in info
    assert "weekday" in info
    assert info["greeting"] in ["Good morning", "Good afternoon", "Good evening"]


def test_environment_and_workspace(tmp_path: Path):
    env_aware = EnvironmentAwareness()
    env_info = env_aware.get_environment_info()
    assert "os" in env_info
    assert "cpu_usage" in env_info

    ws_aware = WorkspaceAwareness(workspace_root=tmp_path)
    ws_info = ws_aware.get_workspace_info()
    assert ws_info["project_name"] == tmp_path.name


def test_session_and_activity():
    sess = SessionContext()
    sess.record_activity("test command")
    info = sess.get_session_info()
    assert info["executed_commands_count"] == 1

    logger = ActivityLogger()
    evt = logger.log_event("command", "pytest run")
    assert evt.event_type == "command"


def test_experience_engine(tmp_path: Path):
    exp_file = tmp_path / "experiences.json"
    exp = ExperienceEngine(storage_file=exp_file)
    exp.record_experience("Refactor Module", ["GitTool"], "success", "Refactored cleanly")
    ref = exp.get_reflections()
    assert "Refactored cleanly" in ref["recent_lessons"]


def test_daily_memory_and_context_manager(tmp_path: Path):
    mem_file = tmp_path / "daily_mem.json"
    mem = DailyMemoryStore(storage_file=mem_file)
    mem.save_snapshot("ZERO", "main", "Testing", ["main.py"], "Verified awareness engine")

    tod_sum = mem.get_todays_summary()
    assert "Today's Progress" in tod_sum

    cm = ContextManager(workspace_root=tmp_path)
    ctx = cm.assemble_context()
    assert ctx.calendar["greeting"] is not None
    assert ctx.to_system_prompt_str() is not None


@pytest.mark.asyncio
async def test_brain_awareness_triggers():
    brain = Brain()

    res1 = await brain.process("Good morning")
    assert any(g in res1 for g in ["Good morning", "Good afternoon", "Good evening"])

    res2 = await brain.process("What did we work on yesterday?")
    assert "Yesterday's Work" in res2 or "Recent Session Summary" in res2

    res3 = await brain.process("What have you learned recently?")
    assert "Recent Learning Insights" in res3

    res4 = await brain.process("Which generated tools are most reliable?")
    assert "Most Reliable Subsystems" in res4
