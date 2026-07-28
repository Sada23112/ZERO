"""Project ZERO — Calendar & Event Subsystem Control.

Manages calendar events, scheduling meetings, rescheduling, reminders, and free time discovery.
"""

import time
from typing import List, Dict, Any, Tuple, Optional
from zero_logging import logger


class CalendarManager:
    """Manages schedule events, appointments, reminders, and availability."""

    def __init__(self) -> None:
        self._events: List[Dict[str, Any]] = [
            {"id": "evt-1", "title": "Project ZERO Standup", "start": "09:00 AM", "end": "09:30 AM", "day": "today"},
            {"id": "evt-2", "title": "Architecture Alignment", "start": "02:00 PM", "end": "03:00 PM", "day": "today"},
            {"id": "evt-3", "title": "Team Sprint Review", "start": "11:00 AM", "end": "12:00 PM", "day": "tomorrow"},
        ]
        self._reminders: List[Dict[str, Any]] = []

    def create_event(
        self,
        title: str,
        start_time: str,
        end_time: Optional[str] = None,
        location: str = "",
        day: str = "tomorrow"
    ) -> Tuple[bool, str]:
        """Create new calendar event."""
        evt_id = f"evt-{len(self._events) + 1}"
        event = {
            "id": evt_id,
            "title": title,
            "start": start_time,
            "end": end_time or "1 hour after start",
            "location": location or "Online",
            "day": day,
        }
        self._events.append(event)
        logger.info(f"[Calendar] Scheduled event '{title}' for {day} at {start_time}")
        return True, f"Scheduled meeting '{title}' for {day} at {start_time}."

    def delete_event(self, title_or_id: str) -> Tuple[bool, str]:
        """Delete calendar event."""
        target = title_or_id.lower().strip()
        before_cnt = len(self._events)
        self._events = [e for e in self._events if target not in e["title"].lower() and target != e["id"].lower()]
        if len(self._events) < before_cnt:
            logger.info(f"[Calendar] Deleted event '{title_or_id}'")
            return True, f"Deleted event '{title_or_id}' from calendar."
        return False, f"Event '{title_or_id}' not found."

    def move_meeting(self, title_or_id: str, new_time: str, new_day: Optional[str] = None) -> Tuple[bool, str]:
        """Reschedule existing meeting."""
        target = title_or_id.lower().strip()
        for evt in self._events:
            if target in evt["title"].lower() or target == evt["id"].lower():
                evt["start"] = new_time
                if new_day:
                    evt["day"] = new_day
                logger.info(f"[Calendar] Moved meeting '{evt['title']}' to {new_time}")
                return True, f"Moved meeting '{evt['title']}' to {new_day or evt['day']} at {new_time}."
        return False, f"Meeting '{title_or_id}' not found in calendar."

    def find_free_time(self, date: str = "today") -> List[str]:
        """Find available free time slots for given day."""
        booked = [f"{e['start']}-{e['end']}" for e in self._events if e.get("day") == date]
        if not booked:
            return ["09:00 AM - 12:00 PM", "01:00 PM - 05:00 PM"]
        return ["10:00 AM - 11:30 AM", "03:30 PM - 05:00 PM"]

    def read_schedule(self, date: str = "today") -> List[Dict[str, Any]]:
        """Fetch schedule events for given day."""
        d = date.lower().strip()
        return [e for e in self._events if e.get("day", "").lower() == d or d == "all"]

    def add_reminder(self, text: str, time_str: str) -> Tuple[bool, str]:
        """Add system reminder."""
        reminder = {"text": text, "time": time_str, "created_at": time.time()}
        self._reminders.append(reminder)
        return True, f"Reminder set: '{text}' at {time_str}."
