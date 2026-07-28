"""Unit tests for Project ZERO CLI shell subsystem."""

import pytest
from cli.shell import ZeroShell


def test_zero_shell_initialization():
    shell = ZeroShell()
    assert shell.brain is not None
    assert shell.brain.settings is not None
    assert shell.brain.conv_repo is not None


def test_zero_shell_cmd_config(capsys):
    shell = ZeroShell()
    shell.cmd_config()
    # Verified without exceptions


def test_zero_shell_cmd_memory(capsys):
    shell = ZeroShell()
    record = shell.brain.memory_repo.store("test_key", "test_value")
    fetched = shell.brain.memory_repo.get_memory_by_key("test_key")
    assert fetched is not None
    assert fetched.value == "test_value"
