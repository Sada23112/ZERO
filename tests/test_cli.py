"""Unit tests for Project ZERO CLI shell subsystem."""

import pytest
from cli.shell import ZeroShell


def test_zero_shell_initialization():
    shell = ZeroShell()
    assert shell.settings is not None
    assert shell.active_session is not None
    assert shell.gemini_provider is not None


def test_zero_shell_cmd_config(capsys):
    shell = ZeroShell()
    shell.cmd_config()
    # Verified without exceptions


def test_zero_shell_cmd_memory(capsys):
    shell = ZeroShell()
    shell.cmd_memory("set test_key test_value")
    fetched = shell.mem_repo.get_memory_by_key("test_key")
    assert fetched is not None
    assert fetched.value == "test_value"
