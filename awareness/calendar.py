"""Project ZERO — Calendar & Timezone Awareness (Phase 6)."""

import time
from datetime import datetime
from typing import Dict, Any, Optional


class CalendarAwareness:
    """Provides current time, date, weekday, timezone, & natural greeting awareness."""

    @staticmethod
    def get_greeting() -> str:
        """Return time-based natural greeting ('Good morning', 'Good afternoon', 'Good evening')."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    @staticmethod
    def get_current_info() -> Dict[str, Any]:
        """Return comprehensive calendar context information."""
        now = datetime.now()
        tz_name = time.tzname[time.daylight] if time.daylight else time.tzname[0]
        return {
            "current_time": now.strftime("%I:%M:%S %p"),
            "current_date": now.strftime("%Y-%m-%d"),
            "weekday": now.strftime("%A"),
            "month": now.strftime("%B"),
            "year": now.year,
            "timezone": tz_name,
            "greeting": CalendarAwareness.get_greeting()
        }
