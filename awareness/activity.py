"""Project ZERO — Activity Logger & Event Tracker (Phase 6)."""

import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ActivityEvent(BaseModel):
    """Event log record of user or agent activity."""

    event_id: str
    event_type: str  # 'command', 'tool_execution', 'evolution', 'repair'
    description: str
    timestamp: str = ""
    status: str = "success"


class ActivityLogger:
    """Tracks session and project activity events."""

    def __init__(self):
        self.events: List[ActivityEvent] = []

    def log_event(self, event_type: str, description: str, status: str = "success") -> ActivityEvent:
        """Record an activity event."""
        import time
        evt = ActivityEvent(
            event_id=f"evt_{len(self.events) + 1}",
            event_type=event_type,
            description=description,
            timestamp=time.strftime("%I:%M:%S %p"),
            status=status
        )
        self.events.append(evt)
        return evt

    def get_recent_events(self, limit: int = 10) -> List[ActivityEvent]:
        """Fetch recent activity logs."""
        return self.events[-limit:]
