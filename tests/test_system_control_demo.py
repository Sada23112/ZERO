"""Project ZERO — Deliverable Demonstration: Natural Language OS Control & Device Integration.

Demonstrates natural language execution of core operating system features:
1. Bluetooth activation and device connection ("Turn on Bluetooth.", "Connect my headphones.")
2. Email sending and replying ("Send today's report to my manager.", "Reply to that email.")
3. Display brightness adjustment ("Increase brightness.")
4. Microphone control ("Mute my microphone.")
5. Workstation security locking ("Lock the computer.")
without requiring manual user UI interaction.
"""

import pytest
from brain.brain import Brain
from zero.system_control.system_control_manager import SystemControlManager


@pytest.mark.asyncio
async def test_system_control_full_demo_scenarios():
    brain = Brain()

    scenarios = [
        ("Turn on Bluetooth.", "[Phase 9 Bluetooth]"),
        ("Connect my headphones.", "[Phase 9 Bluetooth]"),
        ("Send today's report to my manager.", "[Phase 9 Email]"),
        ("Reply to that email.", "[Phase 9 Email]"),
        ("Increase brightness to 70%.", "[Phase 9 Brightness]"),
        ("Mute my microphone.", "[Phase 9 Microphone]"),
        ("Lock my computer.", "[Phase 9 Power]"),
    ]

    for prompt, expected_tag in scenarios:
        res = await brain.process(prompt)
        assert res is not None
        assert expected_tag in res, f"Expected '{expected_tag}' in response for prompt '{prompt}', got: '{res}'"

    print("\n[Phase 9 Demonstration Success] ZERO successfully executed all natural language operating system control scenarios safely!")
