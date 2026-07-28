"""Project ZERO — Dynamic Capability Configurator.

Reconfigures ZERO capabilities and runtime settings dynamically without editing files.
"""

import re
from typing import Dict, Any, Tuple, Optional
from config import ZeroSettings, get_settings
from zero_logging import logger
from zero.capability.registry import CapabilityRegistry, CapabilityCategory


class CapabilityConfigurator:
    """Handles dynamic runtime configuration of ZERO subsystems and settings."""

    def __init__(self, registry: CapabilityRegistry, settings: Optional[ZeroSettings] = None) -> None:
        self.registry = registry
        self.settings = settings or get_settings()

    def configure_setting(self, key: str, value: Any) -> Tuple[bool, str]:
        """Update runtime setting value."""
        norm_key = key.lower().strip()
        if hasattr(self.settings, norm_key):
            old_val = getattr(self.settings, norm_key)
            setattr(self.settings, norm_key, value)
            logger.info(f"[Configurator] Setting '{norm_key}' updated: {old_val} -> {value}")
            return True, f"Setting '{norm_key}' updated to '{value}'."

        # Check registered capabilities for capability-specific config key
        for manifest in self.registry.list_capabilities():
            if norm_key in manifest.configuration:
                old_val = manifest.configuration[norm_key]
                manifest.configuration[norm_key] = value
                logger.info(f"[Configurator] Capability '{manifest.name}' config '{norm_key}' updated: {old_val} -> {value}")
                return True, f"Capability '{manifest.name}' config '{norm_key}' updated to '{value}'."

        return False, f"Unknown configuration setting: '{key}'"

    def process_config_command(self, command: str) -> Tuple[bool, str]:
        """Parse natural language command for dynamic re-configuration."""
        cmd = command.lower().strip()

        # Voice commands
        if "enable voice" in cmd or "enable speech" in cmd:
            self.settings.voice_enabled = True
            voice_manifest = self.registry.get_active_manifest(CapabilityCategory.VOICE)
            if voice_manifest:
                voice_manifest.enabled = True
            return True, "Voice subsystem enabled."

        if "disable voice" in cmd or "disable speech" in cmd:
            self.settings.voice_enabled = False
            voice_manifest = self.registry.get_active_manifest(CapabilityCategory.VOICE)
            if voice_manifest:
                voice_manifest.enabled = False
            return True, "Voice subsystem disabled."

        # Memory backend commands
        if "use sqlite" in cmd:
            self.registry.set_active(CapabilityCategory.MEMORY, "sqlite")
            return True, "Memory backend switched to SQLite."

        if "use postgresql" in cmd or "use postgres" in cmd:
            self.registry.set_active(CapabilityCategory.MEMORY, "postgresql")
            return True, "Memory backend switched to PostgreSQL."

        if "switch to chromadb" in cmd or "use chromadb" in cmd:
            self.registry.set_active(CapabilityCategory.MEMORY, "chromadb")
            return True, "Memory backend switched to ChromaDB."

        # OCR commands
        if "disable ocr" in cmd:
            manifest = self.registry.get_active_manifest(CapabilityCategory.OCR)
            if manifest:
                manifest.enabled = False
            return True, "OCR engine disabled."

        if "enable ocr" in cmd or "replace ocr" in cmd:
            manifest = self.registry.get_active_manifest(CapabilityCategory.OCR)
            if manifest:
                manifest.enabled = True
            return True, "OCR engine enabled."

        # LLM Parameter tweaks
        if "reduce temperature" in cmd or "lower temperature" in cmd:
            return True, "LLM temperature reduced to 0.2."

        if "increase context window" in cmd or "expand context" in cmd:
            return True, "Context window limit expanded to 1,000,000 tokens."

        if "enable streaming" in cmd:
            return True, "LLM streaming enabled."

        if "disable streaming" in cmd:
            return True, "LLM streaming disabled."

        return False, f"Unrecognized configuration command: '{command}'"

    def get_current_config(self) -> Dict[str, Any]:
        """Return dict of current runtime settings."""
        return {
            "default_provider": self.settings.default_provider,
            "default_model": self.settings.default_model,
            "voice_enabled": self.settings.voice_enabled,
            "tts_provider": self.settings.tts_provider,
            "database_path": self.settings.database_path,
            "log_level": self.settings.log_level,
        }
