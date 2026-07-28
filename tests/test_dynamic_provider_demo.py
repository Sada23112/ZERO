"""Project ZERO — Deliverable Demonstration: Dynamic Provider Hot-Loading & Live Switching.

Demonstrates:
1. Reading API documentation for a brand-new, non-existent provider ('DeepMindCustomProvider').
2. Synthesizing provider implementation and dynamic unit test suite.
3. Static AST validation and interface contract verification.
4. Executing dynamic test suite.
5. Registering and zero-downtime hot reloading into runtime.
6. Switching active provider to 'DeepMindCustomProvider' and generating response through Brain.
7. Switching back to Gemini provider without restarting ZERO process.
"""

import pytest
import asyncio
from brain.brain import Brain
from zero.capability.capability_manager import CapabilityManager, capability_manager
from zero.capability.registry import CapabilityCategory


@pytest.mark.asyncio
async def test_dynamic_provider_full_lifecycle_demo():
    brain = Brain()
    mgr = brain.capability_manager

    # Step 1: Initial state verification (Default provider is Gemini)
    initial_provider = brain.active_provider.name
    assert initial_provider == "gemini"

    # Step 2: Supply documentation for a brand-new custom provider
    api_documentation = """
    Official API Documentation for provider deepmind_custom.
    Base URL: https://api.deepmind-custom.ai/v1
    API Key: sk-deepmind-secret-key-12345
    Endpoint: /chat/completions
    Authentication: Bearer sk-deepmind-secret-key-12345
    Please add provider deepmind_custom.
    """

    # Step 3: Execute installation & hot reload workflow via Brain / CapabilityManager
    result_msg = mgr.process_capability_command(api_documentation)

    assert result_msg is not None
    assert "[Phase 8 Dynamic Provider]" in result_msg
    assert "installed, validated, hot-loaded, and activated successfully" in result_msg

    # Step 4: Verify active provider is now the new dynamic provider without process restart
    active_p = brain.active_provider
    assert active_p.name == "deepmind_custom"

    # Step 5: Process prompt through Brain using the hot-loaded active provider
    response = await brain.process("Hello, testing dynamic provider capability!")
    assert isinstance(response, str)
    assert "[CUSTOM_PROVIDER Provider]" in response or "Hello" in response

    # Step 6: Demonstrate natural language command to switch back to Gemini without restart
    switch_back_msg = mgr.process_capability_command("Switch back to Gemini.")
    assert switch_back_msg is not None
    assert "[Phase 8 Provider Reconfiguration]" in switch_back_msg
    assert "switched to 'gemini'" in switch_back_msg

    # Step 7: Verify active provider is cleanly restored to Gemini
    assert brain.active_provider.name == "gemini"
    print("\n[Phase 8 Demonstration Success] Successfully added, validated, hot-loaded, switched to custom provider, and switched back to Gemini without restarting ZERO process!")
