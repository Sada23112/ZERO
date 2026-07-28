"""Project ZERO — Runtime Configuration Manager (Phase 4 Capability #21)."""

from pathlib import Path
from typing import Dict, Any, Optional
from config.settings import ZeroSettings
from zero_logging import logger


class RuntimeConfigManager:
    """Manages live runtime settings updates without restarting shell."""

    def __init__(self, settings: Optional[ZeroSettings] = None):
        self.settings = settings or ZeroSettings.load()

    def update_setting(self, key: str, value: Any) -> bool:
        """Update runtime configuration setting dynamically and save to .env."""
        key_lower = key.lower()

        if hasattr(self.settings, key_lower):
            setattr(self.settings, key_lower, value)
            saved = self.settings.save_to_env()
            logger.info(f"Updated runtime setting '{key}' -> {value} (saved={saved})")
            return saved
        else:
            logger.warning(f"Unknown setting key '{key}'.")
            return False
