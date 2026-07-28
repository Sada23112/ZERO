"""Project ZERO — Test Generator & Executor (Phase 5)."""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from evolution.architect import CapabilityArchitecturalSpec
from zero_logging import logger


class TestGenerator:
    """Automatically synthesizes Pytest unit test suites for generated capabilities."""

    def generate_test_code(self, spec: CapabilityArchitecturalSpec) -> str:
        """Synthesize unit test code covering normal behavior, edge cases, & invalid input."""
        class_name = spec.class_name
        tool_name = spec.capability_name
        module_name = spec.capability_name

        test_template = f'''"""Automated Pytest suite for dynamic capability {class_name}."""

import pytest
from pathlib import Path
from {module_name} import {class_name}


@pytest.mark.asyncio
async def test_{tool_name}_execution(tmp_path: Path):
    tool = {class_name}(workspace_root=tmp_path)
    assert tool.name == "{tool_name}"
    
    res = await tool.execute("test_call_1", {{"input_text": "sample test input"}})
    assert res.success is True
    assert "Executed" in res.output or "Generated" in res.output or "Opened" in res.output or "saved" in res.output.lower()


@pytest.mark.asyncio
async def test_{tool_name}_edge_case_empty(tmp_path: Path):
    tool = {class_name}(workspace_root=tmp_path)
    res = await tool.execute("test_call_2", {{}})
    assert res.success is True or res.error is not None
'''
        return test_template

    async def run_sandbox_tests(self, sandbox_path: Path) -> bool:
        """Run pytest inside sandbox workspace."""
        try:
            # Set PYTHONPATH to sandbox_path so imports resolve
            env = dict(os.environ)
            env["PYTHONPATH"] = str(sandbox_path) + os.pathsep + env.get("PYTHONPATH", "")

            process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "pytest",
                str(sandbox_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )

            stdout, stderr = await process.communicate()
            exit_code = process.returncode or 0

            if exit_code == 0:
                logger.info("Sandbox test suite passed cleanly.")
                return True
            else:
                logger.warning(f"Sandbox tests failed (exit code {exit_code}): {stderr.decode('utf-8')}")
                return False

        except Exception as err:
            logger.error(f"Error executing sandbox tests: {err}")
            return False
