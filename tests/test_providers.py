"""Unit tests for Provider abstraction & Gemini Provider."""

import pytest
from providers.gemini import GeminiProvider
from providers.registry import ProviderRegistry


def test_provider_registry():
    registry = ProviderRegistry()
    provider = GeminiProvider(api_key="test_key")
    registry.register_provider(provider)

    fetched = registry.get_provider("gemini")
    assert fetched is not None
    assert fetched.name == "gemini"
    assert "gemini" in registry.list_providers()


@pytest.mark.asyncio
async def test_gemini_provider_empty_key():
    provider = GeminiProvider(api_key="")
    models = await provider.discover_models()
    assert models == []
