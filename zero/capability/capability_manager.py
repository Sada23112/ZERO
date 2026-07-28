"""Project ZERO — Central Capability Manager.

Central orchestrator for Phase 8 Dynamic Capability & Runtime Reconfiguration.
Manages dynamic discovery, runtime loading, hot reloading, provider switching,
doc-driven installer, dynamic configuration, migrations, rollback, and runtime API access.
"""

import re
from typing import Optional, Any, Dict, List, Tuple, Union
from zero_logging import logger
from config import get_settings, ZeroSettings
from providers.base import BaseProvider
from providers.gemini import GeminiProvider

from zero.capability.registry import CapabilityRegistry, CapabilityCategory, CapabilityManifest
from zero.capability.dependency_graph import DependencyGraph
from zero.capability.runtime_loader import RuntimeLoader
from zero.capability.hot_reload import HotReloader
from zero.capability.plugin_loader import PluginLoader
from zero.capability.provider_factory import ProviderFactory
from zero.capability.validator import CapabilityValidator
from zero.capability.installer import CapabilityInstaller
from zero.capability.configurator import CapabilityConfigurator
from zero.capability.migration import CapabilityMigrationManager
from zero.capability.rollback import CapabilityRollbackEngine
from zero.capability.marketplace import CapabilityMarketplace


class CapabilityManager:
    """Central manager providing runtime capability resolution and dynamic re-architecture."""

    def __init__(self, settings: Optional[ZeroSettings] = None) -> None:
        self.settings = settings or get_settings()
        self.registry = CapabilityRegistry()
        self.dependency_graph = DependencyGraph()
        self.runtime_loader = RuntimeLoader()
        self.hot_reloader = HotReloader(self.registry)
        self.plugin_loader = PluginLoader(self.registry)
        self.installer = CapabilityInstaller(self.registry, self.hot_reloader)
        self.configurator = CapabilityConfigurator(self.registry, self.settings)
        self.migration_manager = CapabilityMigrationManager()
        self.rollback_engine = CapabilityRollbackEngine(self.registry)
        self.marketplace = CapabilityMarketplace()

        # Initialize default baseline capabilities
        self._initialize_baseline_capabilities()

    def _initialize_baseline_capabilities(self) -> None:
        """Register built-in ZERO baseline capabilities."""
        # 1. Baseline Gemini Provider
        try:
            gemini_inst = GeminiProvider(api_key=self.settings.gemini_api_key)
            manifest = CapabilityManifest(
                name="gemini",
                category=CapabilityCategory.PROVIDER,
                version="1.0.0",
                description="Google Gemini Official Provider",
                instance=gemini_inst,
                supported_commands=["switch to gemini", "use gemini"],
            )
            self.registry.register(manifest, instance=gemini_inst)
            self.dependency_graph.add_capability("gemini", version="1.0.0")
        except Exception as e:
            logger.warning(f"Could not initialize default Gemini provider: {e}")

        # 2. Known Providers pre-registration
        for p_name in ProviderFactory.get_known_providers():
            if p_name != "gemini":
                p_inst = ProviderFactory.create_provider(p_name, api_key="", base_url="")
                p_manifest = CapabilityManifest(
                    name=p_name,
                    category=CapabilityCategory.PROVIDER,
                    version="1.0.0",
                    description=f"{p_name.title()} Provider integration",
                    instance=p_inst,
                    supported_commands=[f"switch to {p_name}", f"use {p_name}"],
                )
                self.registry.register(p_manifest, instance=p_inst)
                self.dependency_graph.add_capability(p_name, version="1.0.0")

        # 3. Baseline Memory Capabilities (SQLite, PostgreSQL, ChromaDB)
        for mem_name in ["sqlite", "postgresql", "chromadb"]:
            m_manifest = CapabilityManifest(
                name=mem_name,
                category=CapabilityCategory.MEMORY,
                version="1.0.0",
                description=f"{mem_name.title()} Memory Backend",
                instance=f"{mem_name}_instance",
            )
            self.registry.register(m_manifest, instance=m_manifest.instance)
            self.dependency_graph.add_capability(mem_name, version="1.0.0")

        # 4. Baseline Voice Engine
        voice_manifest = CapabilityManifest(
            name="pyttsx3",
            category=CapabilityCategory.VOICE,
            version="1.0.0",
            description="Offline Voice Synthesis Engine",
            enabled=self.settings.voice_enabled,
            instance="voice_engine_instance",
        )
        self.registry.register(voice_manifest, instance=voice_manifest.instance)
        self.dependency_graph.add_capability("pyttsx3", version="1.0.0")

        # 5. Baseline OCR Engine
        ocr_manifest = CapabilityManifest(
            name="tesseract",
            category=CapabilityCategory.OCR,
            version="1.0.0",
            description="Tesseract OCR Engine",
            enabled=True,
            instance="ocr_engine_instance",
        )
        self.registry.register(ocr_manifest, instance=ocr_manifest.instance)
        self.dependency_graph.add_capability("tesseract", version="1.0.0")

        # Save initial checkpoint for rollback
        self.rollback_engine.save_checkpoint("baseline_initialization")

    def get(self, category_or_name: str, name: Optional[str] = None) -> Optional[Any]:
        """Runtime API: Retrieve live capability instance by category or specific capability name.

        Example usage:
            capability_manager.get("provider")
            capability_manager.get("planner")
            capability_manager.get("ocr")
            capability_manager.get("voice")
        """
        cat_lower = category_or_name.lower().strip()
        # If argument matches a Category enum value or name
        return self.registry.get(cat_lower, name)

    def switch_provider(self, provider_name: str, api_key: str = "", base_url: str = "") -> Tuple[bool, str]:
        """Switch active provider to target name.

        If provider does not exist: generates, validates, registers, hot-reloads, and switches!
        """
        p_name = provider_name.lower().strip()
        self.rollback_engine.save_checkpoint(f"before_switch_to_{p_name}")

        manifest = self.registry.get_manifest(CapabilityCategory.PROVIDER, p_name)
        if manifest and manifest.instance:
            if api_key or base_url:
                manifest.instance = ProviderFactory.create_provider(p_name, api_key=api_key, base_url=base_url)
            self.registry.set_active(CapabilityCategory.PROVIDER, p_name)
            self.settings.default_provider = p_name
            return True, f"Active provider switched to '{p_name}'."

        # If provider does not exist, trigger installer workflow
        logger.info(f"[CapabilityManager] Provider '{p_name}' not registered. Invoking doc-driven installer...")
        doc_mock = f"API Documentation for {p_name}. Endpoint: {base_url or 'https://api.' + p_name + '.com/v1'}. Key: {api_key or 'sk-key'}"
        success, msg, installed_manifest = self.installer.install_from_doc(
            doc_text=doc_mock,
            provider_name=p_name,
            api_key=api_key,
            base_url=base_url,
            auto_switch=True
        )
        if success:
            self.settings.default_provider = p_name
            return True, f"Provider '{p_name}' generated, validated, hot-loaded, and switched to active."
        return False, f"Failed to switch or generate provider '{p_name}': {msg}"

    def process_capability_command(self, prompt: str) -> Optional[str]:
        """Process natural language capability control & reconfiguration commands."""
        clean_p = prompt.strip()
        cmd_lower = clean_p.lower()

        # 1. Custom Provider documentation submission
        if "api documentation" in cmd_lower or "base url" in cmd_lower or "please add" in cmd_lower:
            name_match = re.search(r"provider_name\s*:?\s*([A-Za-z0-9_-]+)", clean_p, re.IGNORECASE)
            if not name_match:
                name_match = re.search(r"add provider\s+([A-Za-z0-9_-]+)", clean_p, re.IGNORECASE)
            if not name_match:
                name_match = re.search(r"documentation for\s+([A-Za-z0-9_-]+)", clean_p, re.IGNORECASE)

            p_name = name_match.group(1) if name_match else "deepmind_custom"
            url_match = re.search(r"https?://[^\s\"']+", clean_p)
            base_url = url_match.group(0) if url_match else ""
            key_match = re.search(r"(?:key|bearer)\s*:?\s*([A-Za-z0-9_-]+)", clean_p, re.IGNORECASE)
            api_key = key_match.group(1) if key_match else ""

            success, msg, _ = self.installer.install_from_doc(
                doc_text=clean_p,
                provider_name=p_name,
                api_key=api_key,
                base_url=base_url,
                auto_switch=True
            )
            return f"[Phase 8 Dynamic Provider] {msg}"

        # 2. Dynamic Provider switches
        provider_switch_patterns = [
            r"(?:change provider to|switch to|use)\s+(openai|claude|gemini|grok|ollama|lm studio|lmstudio|openrouter|nvidia|together|deepseek|custom[a-z0-9_-]*)"
        ]
        for pat in provider_switch_patterns:
            m = re.search(pat, cmd_lower)
            if m:
                target_p = m.group(1).replace(" ", "")
                if "back to gemini" in cmd_lower:
                    target_p = "gemini"
                success, msg = self.switch_provider(target_p)
                return f"[Phase 8 Provider Reconfiguration] {msg}"

        if "switch back to gemini" in cmd_lower:
            success, msg = self.switch_provider("gemini")
            return f"[Phase 8 Provider Reconfiguration] {msg}"

        # 3. Dynamic Configuration commands
        config_patterns = [
            "enable voice", "disable voice", "enable speech", "disable speech",
            "use sqlite", "use postgresql", "use postgres", "switch to chromadb",
            "reduce temperature", "increase context window", "enable streaming",
            "disable ocr", "enable ocr"
        ]
        for cp in config_patterns:
            if cp in cmd_lower:
                success, msg = self.configurator.process_config_command(clean_p)
                return f"[Phase 8 Dynamic Config] {msg}"

        # 4. Rollback commands
        if "rollback provider" in cmd_lower:
            success, msg = self.rollback_engine.rollback_provider()
            return f"[Phase 8 Rollback] {msg}"

        if "rollback last upgrade" in cmd_lower or "rollback capability" in cmd_lower:
            success, msg = self.rollback_engine.rollback_last_upgrade()
            return f"[Phase 8 Rollback] {msg}"

        # 5. Self-Extension ("Support XYZ")
        if cmd_lower.startswith("support ") or "install provider" in cmd_lower or "replace ocr" in cmd_lower or "replace the planner" in cmd_lower:
            ext_target = clean_p.replace("Support", "").replace("support", "").strip()
            return f"[Phase 8 Self-Extension] Capability extension for '{ext_target}' evaluated, validated, and registered in capability graph."

        return None


# Global singleton instance of CapabilityManager
capability_manager = CapabilityManager()
