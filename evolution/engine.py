"""Project ZERO — Central Evolution Engine (Phase 5)."""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from evolution.metadata import CapabilityMetadata
from evolution.history import EvolutionHistoryStore
from evolution.registry import CapabilityRegistryStore
from evolution.capability_detector import CapabilityDetector, CapabilityDetectionResult
from evolution.planner import EvolutionPlanner, EvolutionPlan
from evolution.architect import ArchitecturalGenerator, CapabilityArchitecturalSpec
from evolution.dependency_manager import DependencyManager
from evolution.generator import CodeGenerator
from evolution.tester import TestGenerator
from evolution.sandbox import ExecutionSandbox
from evolution.validator import CapabilityValidator, ValidationResult
from evolution.reviewer import ChangeReviewer, ChangeReview
from evolution.installer import CapabilityInstaller
from evolution.repair_engine import SelfRepairEngine, RepairReport
from evolution.rollback import RollbackEngine
from zero_logging import logger


class EvolutionEngineResult:
    """Outcome of Evolution Engine pipeline execution."""

    def __init__(self, success: bool, capability_name: str, message: str = "", output: str = ""):
        self.success = success
        self.capability_name = capability_name
        self.message = message
        self.output = output


class EvolutionEngine:
    """Central Pipeline Coordinator for controlled self-extending and self-repairing intelligence."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

        self.history_store = EvolutionHistoryStore()
        self.registry_store = CapabilityRegistryStore()

        self.detector = CapabilityDetector(self.registry_store)
        self.planner = EvolutionPlanner()
        self.architect = ArchitecturalGenerator()
        self.dependency_manager = DependencyManager(self.workspace_root)
        self.code_generator = CodeGenerator()
        self.test_generator = TestGenerator()
        self.sandbox = ExecutionSandbox()
        self.validator = CapabilityValidator()
        self.reviewer = ChangeReviewer()
        self.installer = CapabilityInstaller(self.workspace_root, self.registry_store)
        self.repair_engine = SelfRepairEngine(self.workspace_root)
        self.rollback_engine = RollbackEngine(self.workspace_root, self.registry_store)

    async def evolve_capability(self, capability_name: str, user_prompt: str) -> EvolutionEngineResult:
        """Run complete 12-stage Evolution Pipeline to generate, validate, install, & execute new capability."""
        logger.info(f"Initiating Evolution Pipeline for missing capability: {capability_name}")

        try:
            # 1. Architectural Design
            spec: CapabilityArchitecturalSpec = self.architect.design_capability(capability_name, user_prompt)

            # 2. Evolution Plan
            plan: EvolutionPlan = self.planner.create_plan(spec)

            # 3. Resolve Dependencies
            for dep in spec.required_dependencies:
                installed = await self.dependency_manager.install_package(dep)
                if not installed:
                    return EvolutionEngineResult(
                        success=False,
                        capability_name=capability_name,
                        message=f"Dependency resolution failed for required package '{dep}'"
                    )

            # 4. Generate Code & Tests
            tool_code = self.code_generator.generate_tool_code(spec)
            test_code = self.test_generator.generate_test_code(spec)

            # 5. Sandbox Workspace Execution & Validation
            sandbox_path = self.sandbox.create_sandbox(capability_name)
            self.sandbox.write_sandbox_file(spec.module_filename, tool_code)
            self.sandbox.write_sandbox_file(f"test_{spec.module_filename}", test_code)

            # 6. Validate Syntax & Security Scan
            val_res: ValidationResult = self.validator.validate_code(tool_code, spec.module_filename)
            if not val_res.is_valid:
                self.sandbox.cleanup()
                errs = ", ".join(val_res.error_messages)
                return EvolutionEngineResult(
                    success=False,
                    capability_name=capability_name,
                    message=f"Validation failed in sandbox: {errs}"
                )

            # 7. Run Sandbox Tests
            tests_passed = await self.test_generator.run_sandbox_tests(sandbox_path)
            if not tests_passed:
                self.sandbox.cleanup()
                return EvolutionEngineResult(
                    success=False,
                    capability_name=capability_name,
                    message="Sandbox unit tests failed. Aborting installation."
                )

            # 8. Clean up sandbox
            self.sandbox.cleanup()

            # 9. Installation & Registration
            meta: Optional[CapabilityMetadata] = self.installer.install_capability(
                capability_name=spec.capability_name,
                class_name=spec.class_name,
                code_content=tool_code,
                dependencies=spec.required_dependencies,
                reason=user_prompt
            )

            if not meta:
                return EvolutionEngineResult(
                    success=False,
                    capability_name=capability_name,
                    message="Installation failed during module import."
                )

            # 10. Record Evolution History Audit
            self.history_store.add_record(
                action_type="generate",
                capability_name=spec.capability_name,
                user_prompt=user_prompt,
                status="success",
                metadata=meta
            )

            # 11. Immediately Execute Capability to Fulfill Request
            from tools.registry import tool_registry
            exec_res = await tool_registry.execute_tool("evo_call_1", spec.capability_name, {"input_text": user_prompt})

            output_str = exec_res.output if exec_res.success else f"Error: {exec_res.error}"
            return EvolutionEngineResult(
                success=True,
                capability_name=spec.capability_name,
                message=f"Successfully evolved capability '{spec.capability_name}' v{meta.version}",
                output=output_str
            )

        except Exception as err:
            logger.error(f"Evolution Pipeline exception for '{capability_name}': {err}")
            return EvolutionEngineResult(
                success=False,
                capability_name=capability_name,
                message=f"Pipeline exception: {err}"
            )
