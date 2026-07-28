"""Project ZERO — Routine Learning & Preference Engine (Phase 6)."""

from typing import List, Dict, Any


class RoutineLearner:
    """Identifies recurring user behaviors and preferences."""

    def __init__(self):
        self.observed_routines: List[str] = [
            "Runs pytest after code changes",
            "Commits to Git after passing test suite",
            "Scans codebase entry points before building new modules"
        ]

    def get_learned_routines(self) -> List[str]:
        """Return list of identified routine patterns."""
        return self.observed_routines
