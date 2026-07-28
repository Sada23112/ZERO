"""Project ZERO — Connected Account Preferences.

Manages user rules and preferences for selecting default accounts for professional,
personal, or academic contexts.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any
from zero_logging import logger

PREFERENCES_FILE = Path("data/account_preferences.json")


class AccountPreferences:
    """Manages user account preferences and category mappings."""

    def __init__(self) -> None:
        self._prefs: Dict[str, str] = {
            "work": "",
            "personal": "",
            "college": "",
            "default_google": "",
            "default_microsoft": "",
            "default_github": "",
        }
        self._load()

    def _load(self) -> None:
        if PREFERENCES_FILE.exists():
            try:
                with open(PREFERENCES_FILE, "r", encoding="utf-8") as f:
                    self._prefs.update(json.load(f))
            except Exception as e:
                logger.warning(f"[AccountPreferences] Failed to load preferences: {e}")

    def _save(self) -> None:
        try:
            PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(PREFERENCES_FILE, "w", encoding="utf-8") as f:
                json.dump(self._prefs, f, indent=2)
        except Exception as e:
            logger.error(f"[AccountPreferences] Failed to save preferences: {e}")

    def set_preference(self, category_or_key: str, account_id_or_email: str) -> None:
        """Set default preferred account for key (e.g. 'work' -> 'work@gmail.com')."""
        k = category_or_key.lower().strip()
        v = account_id_or_email.lower().strip()
        self._prefs[k] = v
        self._save()
        logger.info(f"[AccountPreferences] Saved preference '{k}' -> '{v}'")

    def get_preference(self, category_or_key: str) -> Optional[str]:
        """Fetch preferred account for key."""
        val = self._prefs.get(category_or_key.lower().strip())
        return val if val else None

    def clear_preferences(self) -> None:
        """Reset all saved preferences."""
        self._prefs = {
            "work": "",
            "personal": "",
            "college": "",
            "default_google": "",
            "default_microsoft": "",
            "default_github": "",
        }
        self._save()

    def get_all_preferences(self) -> Dict[str, str]:
        """Return dict of active preferences."""
        return dict(self._prefs)
