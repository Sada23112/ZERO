"""Project ZERO — Configuration System.

Loads and manages runtime environment settings using Pydantic.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import json
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ZeroSettings(BaseSettings):
    """Pydantic Settings model for Project ZERO runtime configuration."""

    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    default_provider: str = Field(default="gemini", validation_alias="DEFAULT_PROVIDER")
    default_model: str = Field(default="gemini-3.5-flash-lite", validation_alias="DEFAULT_MODEL")
    database_path: str = Field(default="data/zero.db", validation_alias="DATABASE_PATH")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )

    @classmethod
    def load(cls, base_dir: Optional[Path] = None) -> "ZeroSettings":
        """Load settings from .env file and zero-settings.json overrides."""
        root_dir = base_dir or Path.cwd()
        env_path = root_dir / ".env"
        json_path = root_dir / "data" / "zero-settings.json"

        # Load environment variables first
        instance = cls(_env_file=str(env_path) if env_path.exists() else None)

        # Merge JSON overrides if available
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data: Dict[str, Any] = json.load(f)
                    if "gemini_api_key" in data and not instance.gemini_api_key:
                        instance.gemini_api_key = data["gemini_api_key"]
                    if "default_model" in data and data["default_model"]:
                        instance.default_model = data["default_model"]
                    if "default_provider" in data and data["default_provider"]:
                        instance.default_provider = data["default_provider"]
            except Exception as e:
                print(f"Warning: Failed to parse zero-settings.json: {e}")

        return instance

    def save_to_env(self, env_path: Optional[Path] = None) -> bool:
        """Persist updated settings to .env file safely."""
        target_path = env_path or (Path.cwd() / ".env")
        try:
            lines = [
                "# Project ZERO Local Configuration\n",
                f"GEMINI_API_KEY={self.gemini_api_key}\n",
                f"DEFAULT_PROVIDER={self.default_provider}\n",
                f"DEFAULT_MODEL={self.default_model}\n",
                f"DATABASE_PATH={self.database_path}\n",
                f"LOG_LEVEL={self.log_level}\n",
                f"DEBUG={str(self.debug).lower()}\n",
            ]
            with open(target_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True
        except Exception as err:
            print(f"Error writing to .env: {err}")
            return False


# Global singleton settings loader
get_settings = ZeroSettings.load
