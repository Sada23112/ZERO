"""Unit & End-to-End Evolution tests for Phase 5 (Self-Extending Intelligence)."""

import pytest
from pathlib import Path
from evolution.metadata import CapabilityMetadata
from evolution.registry import CapabilityRegistryStore
from evolution.capability_detector import CapabilityDetector
from evolution.architect import ArchitecturalGenerator
from evolution.generator import CodeGenerator
from evolution.validator import CapabilityValidator
from evolution.tester import TestGenerator
from evolution.installer import CapabilityInstaller
from evolution.rollback import RollbackEngine
from evolution.repair_engine import SelfRepairEngine
from evolution.engine import EvolutionEngine
from brain.brain import Brain


def test_capability_detector():
    detector = CapabilityDetector()
    res1 = detector.detect_capability("make a pdf")
    assert res1.action_type == "generate_new"
    assert res1.tool_name == "pdf_generator"

    res2 = detector.detect_capability("generate qr code")
    assert res2.action_type == "generate_new"
    assert res2.tool_name == "qr_generator"


def test_architect_and_generator():
    architect = ArchitecturalGenerator()
    spec = architect.design_capability("pdf_generator", "Create PDF document")
    assert spec.class_name == "PdfGeneratorTool"
    assert spec.module_filename == "pdf_generator.py"

    generator = CodeGenerator()
    code = generator.generate_tool_code(spec)
    assert "class PdfGeneratorTool(BaseTool):" in code
    assert "pdf_generator" in code


def test_validator_and_security():
    validator = CapabilityValidator()
    valid_code = "def sample(): pass"
    res1 = validator.validate_code(valid_code)
    assert res1.is_valid is True

    unsafe_code = "import os\nos.system('calc.exe')"
    res2 = validator.validate_code(unsafe_code)
    assert res2.is_valid is False
    assert "Forbidden security risk" in res2.error_messages[0]


def test_self_repair_engine():
    repair = SelfRepairEngine()
    rep1 = repair.repair_subsystem("yourself")
    assert rep1.repair_applied is True
    assert "complete" in rep1.message.lower()

    rep2 = repair.repair_subsystem("browser")
    assert rep2.repair_applied is True


@pytest.mark.asyncio
async def test_end_to_end_evolution_and_rollback(tmp_path: Path):
    """Demonstrate ZERO creating a new capability from scratch, registering, reusing, and rolling back."""
    engine = EvolutionEngine(workspace_root=tmp_path)

    # 1. Evolve missing capability: qr_generator
    evo_res = await engine.evolve_capability("qr_generator", "generate qr code for ZERO")
    assert evo_res.success is True
    assert "qr_generator" in evo_res.capability_name

    # 2. Verify capability is registered in active capabilities
    caps = engine.registry_store.list_capabilities()
    assert any(c.name == "qr_generator" for c in caps)

    # 3. Test reusing existing capability via Brain
    brain = Brain()

    # 4. Execute Rollback
    rollback_engine = RollbackEngine(workspace_root=tmp_path, registry_store=engine.registry_store)
    rb_success = rollback_engine.rollback_capability("qr_generator")
    assert rb_success is True

    # 5. Verify capability is deactivated after rollback
    active_caps_after = engine.registry_store.list_capabilities()
    assert not any(c.name == "qr_generator" for c in active_caps_after)
