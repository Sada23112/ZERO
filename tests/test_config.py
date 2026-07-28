"""Unit tests for config settings management."""

import os
from pathlib import Path
from config import ZeroSettings


def test_zero_settings_defaults():
    settings = ZeroSettings()
    assert settings.default_provider == "gemini"
    assert settings.default_model == "gemini-2.0-flash"
    assert settings.log_level == "INFO"
    assert settings.debug is False


def test_zero_settings_save_to_env(tmp_path: Path):
    env_file = tmp_path / ".env"
    settings = ZeroSettings(
        gemini_api_key="test_api_key_123",
        default_provider="gemini",
        default_model="gemini-2.5-pro",
        database_path="data/test.db",
        debug=True
    )
    
    saved = settings.save_to_env(env_file)
    assert saved is True
    assert env_file.exists()

    content = env_file.read_text(encoding="utf-8")
    assert "GEMINI_API_KEY=test_api_key_123" in content
    assert "DEFAULT_MODEL=gemini-2.5-pro" in content
    assert "DEBUG=true" in content
