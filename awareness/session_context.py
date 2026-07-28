"""Project ZERO — Session Context & Metrics (Phase 6)."""

import time
from datetime import datetime
from typing import List, Dict, Any, Optional


class SessionContext:
    """Tracks active terminal session metrics, idle duration, & executed commands."""

    def __init__(self):
        self.session_start_time: datetime = datetime.now()
        self.last_activity_time: float = time.time()
        self.executed_commands_count: int = 0
        self.command_history: List[str] = []
        self.current_objective: Optional[str] = None

    def record_activity(self, prompt: str):
        """Update last activity timestamp and command history."""
        self.last_activity_time = time.time()
        self.executed_commands_count += 1
        self.command_history.append(prompt)

    def get_idle_duration_seconds(self) -> float:
        """Return seconds since last activity."""
        return time.time() - self.last_activity_time

    def get_session_info(self) -> Dict[str, Any]:
        """Return session state details."""
        return {
            "session_start_time": self.session_start_time.strftime("%I:%M:%S %p"),
            "idle_duration_seconds": round(self.get_idle_duration_seconds(), 1),
            "executed_commands_count": self.executed_commands_count,
            "recent_commands": self.command_history[-5:],
            "current_objective": self.current_objective or "General Engineering Operating Tasks"
        }
