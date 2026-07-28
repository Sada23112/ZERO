"""Project ZERO — Context & Awareness Package (Phase 6)."""

from awareness.time_engine import TimeEngine
from awareness.calendar import CalendarAwareness
from awareness.environment import EnvironmentAwareness
from awareness.workspace import WorkspaceAwareness
from awareness.session_context import SessionContext
from awareness.activity import ActivityLogger, ActivityEvent
from awareness.experience import ExperienceEngine, ExperienceRecord
from awareness.routine import RoutineLearner
from awareness.history import DailyMemoryStore, ContextSnapshot
from awareness.context_manager import ContextManager, SystemContext

__all__ = [
    "TimeEngine",
    "CalendarAwareness",
    "EnvironmentAwareness",
    "WorkspaceAwareness",
    "SessionContext",
    "ActivityLogger",
    "ActivityEvent",
    "ExperienceEngine",
    "ExperienceRecord",
    "RoutineLearner",
    "DailyMemoryStore",
    "ContextSnapshot",
    "ContextManager",
    "SystemContext",
]
