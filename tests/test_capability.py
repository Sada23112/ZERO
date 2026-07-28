"""Project ZERO — Unit Tests for Phase 8 Dynamic Capability & Runtime Reconfiguration."""

import pytest
import asyncio
from typing import List, Dict, Any

from zero.capability.registry import CapabilityRegistry, CapabilityCategory, CapabilityManifest
from zero.capability.dependency_graph import DependencyGraph
from zero.capability.runtime_loader import RuntimeLoader
from zero.capability.hot_reload import HotReloader
from zero.capability.plugin_loader import PluginLoader
from zero.capability.provider_factory import ProviderFactory, GenericOpenAICompatibleProvider
from zero.capability.validator import CapabilityValidator
from zero.capability.installer import CapabilityInstaller
from zero.capability.configurator import CapabilityConfigurator
from zero.capability.migration import CapabilityMigrationManager
from zero.capability.rollback import CapabilityRollbackEngine
from zero.capability.marketplace import CapabilityMarketplace
from zero.capability.capability_manager import CapabilityManager, capability_manager
from models.conversation import Message, MessageRole


def test_registry_and_manifest():
    registry = CapabilityRegistry()
    manifest = CapabilityManifest(
        name="test_provider",
        category=CapabilityCategory.PROVIDER,
        version="1.0.0",
        description="Test provider",
        instance="test_instance"
    )
    registry.register(manifest, instance="test_instance")

    assert registry.get_active("provider") == "test_instance"
    assert registry.get("provider", "test_provider") == "test_instance"
    assert registry.set_active("provider", "test_provider") is True
    assert len(registry.list_capabilities("provider")) == 1


def test_dependency_graph():
    graph = DependencyGraph()
    graph.add_capability("base_cap", version="1.0.0")

    can_inst, errors = graph.can_install("child_cap", dependencies=["base_cap"])
    assert can_inst is True
    assert len(errors) == 0

    graph.add_capability("child_cap", version="1.0.0", dependencies=["base_cap"])
    can_rem, rem_errors = graph.can_remove("base_cap")
    assert can_rem is False
    assert "relied upon" in rem_errors[0]

    valid, v_errors = graph.validate_graph()
    assert valid is True


def test_runtime_loader():
    code = """
class DynamicTestClass:
    def hello(self):
        return 'world'
"""
    module = RuntimeLoader.load_module_from_code(code, "test_dynamic_mod")
    cls = RuntimeLoader.load_class_from_module(module, "DynamicTestClass")
    instance = cls()
    assert instance.hello() == "world"


def test_validator():
    valid_code = "x = 1 + 2"
    res1 = CapabilityValidator.validate_code_syntax(valid_code)
    assert res1.success is True

    invalid_code = "x = (1 +"
    res2 = CapabilityValidator.validate_code_syntax(invalid_code)
    assert res2.success is False

    class GoodProvider:
        @property
        def name(self):
            return "good"
        async def generate_response(self, messages, **kwargs):
            return "ok"
        async def stream_generate(self, messages, **kwargs):
            yield "ok"
        async def discover_models(self, force_refresh=False):
            return []

    res3 = CapabilityValidator.validate_provider_contract(GoodProvider)
    assert res3.success is True


def test_provider_factory():
    providers = ["openai", "claude", "grok", "ollama", "lmstudio", "openrouter", "nvidia", "together", "deepseek"]
    for p_name in providers:
        p = ProviderFactory.create_provider(p_name)
        assert p.name == p_name

    assert len(ProviderFactory.get_known_providers()) >= 10


@pytest.mark.asyncio
async def test_dynamic_openai_provider_response():
    provider = GenericOpenAICompatibleProvider("mock_p", base_url="http://localhost:9999/v1", api_key="test")
    messages = [Message(role=MessageRole.USER, content="Hello", session_id="test_session")]
    resp = await provider.generate_response(messages)
    assert isinstance(resp, str)
    assert len(resp) > 0


def test_plugin_loader():
    registry = CapabilityRegistry()
    loader = PluginLoader(registry)
    manifest_dict = {
        "name": "sample_plugin",
        "category": "tool",
        "version": "1.0.0",
        "description": "Sample plugin",
        "entry_point": ""
    }
    manifest = loader.load_plugin_from_dict(manifest_dict)
    assert manifest.name == "sample_plugin"
    assert registry.get_manifest("tool", "sample_plugin") is not None


def test_configurator():
    registry = CapabilityRegistry()
    configurator = CapabilityConfigurator(registry)

    succ, msg = configurator.process_config_command("disable voice")
    assert succ is True
    assert configurator.settings.voice_enabled is False

    succ, msg = configurator.process_config_command("enable voice")
    assert succ is True
    assert configurator.settings.voice_enabled is True

    succ, msg = configurator.process_config_command("use sqlite")
    assert succ is True

    succ, msg = configurator.process_config_command("use postgresql")
    assert succ is True


def test_migration_manager():
    migrator = CapabilityMigrationManager()
    
    def mock_transformer(data):
        return True, {"migrated": True, "count": len(data) if data else 0}

    migrator.register_migration("sqlite", "postgresql", mock_transformer)
    success, msg = migrator.migrate("sqlite", "postgresql", data=[1, 2, 3])
    assert success is True
    assert "migrated successfully" in msg


def test_rollback_engine():
    registry = CapabilityRegistry()
    manifest1 = CapabilityManifest(name="gemini", category=CapabilityCategory.PROVIDER)
    manifest2 = CapabilityManifest(name="claude", category=CapabilityCategory.PROVIDER)
    registry.register(manifest1)
    registry.register(manifest2)

    rollback = CapabilityRollbackEngine(registry)
    rollback.save_checkpoint("initial_state")

    registry.set_active("provider", "claude")
    assert registry.get_active_manifest("provider").name == "claude"

    succ, msg = rollback.rollback_last_upgrade()
    assert succ is True
    assert registry.get_active_manifest("provider").name == "gemini"


def test_marketplace():
    marketplace = CapabilityMarketplace()
    items = marketplace.list_available("provider")
    assert len(items) >= 9

    search_res = marketplace.search("deepseek")
    assert len(search_res) >= 1
    assert search_res[0]["name"] == "deepseek"


@pytest.mark.asyncio
async def test_capability_manager_end_to_end():
    mgr = CapabilityManager()

    # 1. Switch existing baseline provider
    succ, msg = mgr.switch_provider("claude")
    assert succ is True
    assert mgr.get("provider").name == "claude"

    # 2. Switch back to Gemini
    succ, msg = mgr.switch_provider("gemini")
    assert succ is True
    assert mgr.get("provider").name == "gemini"

    # 3. Process natural language commands
    res1 = mgr.process_capability_command("Switch to OpenAI.")
    assert "[Phase 8 Provider Reconfiguration]" in res1

    res2 = mgr.process_capability_command("Disable voice.")
    assert "[Phase 8 Dynamic Config]" in res2

    res3 = mgr.process_capability_command("Rollback provider.")
    assert "[Phase 8 Rollback]" in res3
