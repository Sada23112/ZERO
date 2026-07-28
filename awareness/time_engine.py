"""Project ZERO — Temporal Expression Parser & Time Engine (Phase 6)."""

import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class TimeEngine:
    """Parses natural language temporal expressions into concrete datetime objects."""

    @staticmethod
    def get_now() -> datetime:
        """Return current local datetime."""
        return datetime.now()

    def parse_expression(self, expression: str) -> Optional[datetime]:
        """Resolve expressions like 'today', 'yesterday', 'this morning', 'two days ago', etc."""
        expr = expression.lower().strip()
        now = self.get_now()

        if expr in ["today", "now"]:
            return now

        if expr in ["yesterday"]:
            return now - timedelta(days=1)

        if expr in ["tomorrow"]:
            return now + timedelta(days=1)

        if expr in ["this morning"]:
            return now.replace(hour=9, minute=0, second=0, microsecond=0)

        if expr in ["this afternoon"]:
            return now.replace(hour=14, minute=0, second=0, microsecond=0)

        if expr in ["this evening"]:
            return now.replace(hour=19, minute=0, second=0, microsecond=0)

        if expr in ["last night"]:
            yesterday = now - timedelta(days=1)
            return yesterday.replace(hour=21, minute=0, second=0, microsecond=0)

        if expr in ["end of day"]:
            return now.replace(hour=23, minute=59, second=59, microsecond=0)

        if expr in ["beginning of month"]:
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Handle 'X days ago'
        match_days_ago = re.search(r"(\d+|two|three|four|five)\s+days?\s+ago", expr)
        if match_days_ago:
            val_str = match_days_ago.group(1)
            num_map = {"two": 2, "three": 3, "four": 4, "five": 5}
            num = num_map.get(val_str, int(val_str) if val_str.isdigit() else 1)
            return now - timedelta(days=num)

        # Handle 'X hours ago'
        match_hours_ago = re.search(r"(\d+|one|two|three)\s+hours?\s+ago", expr)
        if match_hours_ago:
            val_str = match_hours_ago.group(1)
            num_map = {"one": 1, "two": 2, "three": 3}
            num = num_map.get(val_str, int(val_str) if val_str.isdigit() else 1)
            return now - timedelta(hours=num)

        # Handle 'in X minutes'
        match_in_mins = re.search(r"in\s+(\d+|ten|twenty|thirty)\s+minutes?", expr)
        if match_in_mins:
            val_str = match_in_mins.group(1)
            num_map = {"ten": 10, "twenty": 20, "thirty": 30}
            num = num_map.get(val_str, int(val_str) if val_str.isdigit() else 10)
            return now + timedelta(minutes=num)

        if expr in ["last week"]:
            return now - timedelta(weeks=1)

        if expr in ["last month"]:
            return now - timedelta(days=30)

        if expr in ["last year"]:
            return now - timedelta(days=365)

        return None
