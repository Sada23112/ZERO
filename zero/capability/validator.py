"""Project ZERO — Capability & Code Validator.

Performs static syntax verification (AST), contract verification, and automated unit test execution
for newly generated or updated capabilities.
"""

import ast
import sys
import types
from dataclasses import dataclass, field
from typing import List, Optional, Any, Type
from zero_logging import logger
from zero.capability.registry import CapabilityCategory
from providers.base import BaseProvider


@dataclass
class ValidationResult:
    """Result object for capability validation."""

    success: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class CapabilityValidator:
    """Validator inspecting capability code syntax, class contracts, and executing unit tests."""

    @staticmethod
    def validate_code_syntax(code: str) -> ValidationResult:
        """Parse code into AST to check for Python syntax errors."""
        result = ValidationResult(success=True)
        try:
            ast.parse(code)
        except SyntaxError as e:
            result.success = False
            result.errors.append(f"SyntaxError on line {e.lineno}, col {e.offset}: {e.msg}")
        except Exception as e:
            result.success = False
            result.errors.append(f"AST Parsing Error: {e}")
        return result

    @staticmethod
    def validate_provider_contract(provider_cls: Type[Any]) -> ValidationResult:
        """Ensure class implements BaseProvider required interface."""
        result = ValidationResult(success=True)
        required_methods = ["generate_response", "stream_generate", "discover_models"]

        for method in required_methods:
            if not hasattr(provider_cls, method):
                result.success = False
                result.errors.append(f"Provider class '{provider_cls.__name__}' missing required method '{method}'")

        if not hasattr(provider_cls, "name"):
            result.success = False
            result.errors.append(f"Provider class '{provider_cls.__name__}' missing required property 'name'")

        return result

    @staticmethod
    def validate_instance_contract(category: CapabilityCategory, instance: Any) -> ValidationResult:
        """Validate live capability instance contracts."""
        result = ValidationResult(success=True)
        if instance is None:
            result.success = False
            result.errors.append("Capability instance is None")
            return result

        if category == CapabilityCategory.PROVIDER:
            if not isinstance(instance, BaseProvider) and not hasattr(instance, "generate_response"):
                result.success = False
                result.errors.append("Instance does not satisfy BaseProvider interface contract.")

        return result

    @staticmethod
    def run_tests(test_code: str, target_module: types.ModuleType) -> ValidationResult:
        """Execute dynamic test suite code against target module."""
        result = ValidationResult(success=True)
        try:
            test_globals = {"target": target_module, "__name__": "__dynamic_tests__"}
            exec(test_code, test_globals)

            # Look for test functions starting with test_
            test_funcs = [v for k, v in test_globals.items() if k.startswith("test_") and callable(v)]
            if not test_funcs:
                result.warnings.append("No test functions (test_*) found in test code.")

            for test_fn in test_funcs:
                try:
                    test_fn()
                    logger.debug(f"[Validator] Dynamic test passed: {test_fn.__name__}")
                except Exception as test_err:
                    result.success = False
                    result.errors.append(f"Test failure in '{test_fn.__name__}': {test_err}")

        except Exception as e:
            result.success = False
            result.errors.append(f"Failed to execute test suite: {e}")

        return result
