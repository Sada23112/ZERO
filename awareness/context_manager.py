"""Project ZERO — Unified Context Manager (Phase 6)."""

from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from awareness.time_engine import TimeEngine
from awareness.calendar import CalendarAwareness
from awareness.environment import EnvironmentAwareness
from awareness.workspace import WorkspaceAwareness
from awareness.session_context import SessionContext
from awareness.activity import ActivityLogger
from awareness.experience import ExperienceEngine
from awareness.routine import RoutineLearner
from awareness.history import DailyMemoryStore


class SystemContext(BaseModel):
    """Unified system context object consumed directly by Brain."""

    calendar: Dict[str, Any] = Field(default_factory=dict)
    environment: Dict[str, Any] = Field(default_factory=dict)
    workspace: Dict[str, Any] = Field(default_factory=dict)
    session: Dict[str, Any] = Field(default_factory=dict)
    experience: Dict[str, Any] = Field(default_factory=dict)
    routines: list = Field(default_factory=list)
    daily_summary: str = ""

    def to_system_prompt_str(self) -> str:
        """Format unified context into system prompt block for LLM reasoning."""
        cal = self.calendar
        env = self.environment
        ws = self.workspace
        sess = self.session

        return (
            f"=== CURRENT SYSTEM & AWARENESS CONTEXT ===\n"
            f"- Date & Time: {cal.get('current_date')} {cal.get('current_time')} ({cal.get('weekday')}, {cal.get('timezone')})\n"
            f"- Greeting Context: {cal.get('greeting')}\n"
            f"- Active Workspace: {ws.get('project_name')} (Branch: {ws.get('git_branch')})\n"
            f"- Recently Modified Files: {', '.join(ws.get('recently_modified_files', [])[:3])}\n"
            f"- System Hardware: OS={env.get('os')}, CPU={env.get('cpu_usage')}, RAM={env.get('ram_usage')}, Battery={env.get('battery')}\n"
            f"- Active Session: Start={sess.get('session_start_time')}, Commands Run={sess.get('executed_commands_count')}\n"
            f"- Current Objective: {sess.get('current_objective')}\n"
            f"=========================================="
        )


class ContextManager:
    """Synthesizes all awareness engines into a unified SystemContext object."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

        self.time_engine = TimeEngine()
        self.calendar_awareness = CalendarAwareness()
        self.environment_awareness = EnvironmentAwareness()
        self.workspace_awareness = WorkspaceAwareness(self.workspace_root)
        self.session_context = SessionContext()
        self.activity_logger = ActivityLogger()
        self.experience_engine = ExperienceEngine()
        self.routine_learner = RoutineLearner()
        self.daily_memory = DailyMemoryStore()

    def assemble_context(self) -> SystemContext:
        """Gather all context inputs into unified SystemContext."""
        cal_info = self.calendar_awareness.get_current_info()
        env_info = self.environment_awareness.get_environment_info()
        ws_info = self.workspace_awareness.get_workspace_info()
        sess_info = self.session_context.get_session_info()
        exp_info = self.experience_engine.get_reflections()
        routines = self.routine_learner.get_learned_routines()

        return SystemContext(
            calendar=cal_info,
            environment=env_info,
            workspace=ws_info,
            session=sess_info,
            experience=exp_info,
            routines=routines,
            daily_summary=self.daily_memory.get_todays_summary()
        )
