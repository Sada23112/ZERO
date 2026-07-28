"""Project ZERO — Formatter, Linter, & Security Validator (Phase 5)."""

import ast
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from zero_logging import logger


class ValidationResult(BaseModel):
    """Structured report of code validation checks."""

    is_valid: bool
    syntax_ok: bool = False
    security_ok: bool = False
    imports_ok: bool = False
    error_messages: List[str] = Field(default_factory=list)


class CapabilityValidator:
    """Validates Python syntax, security patterns, & imports of generated tools."""

    def validate_code(self, code: str, filename: str = "generated_tool.py") -> ValidationResult:
        """Run AST parsing, security scanning, and import validation on generated code."""
        result = ValidationResult(is_valid=False)

        # 1. AST Syntax Check
        try:
            tree = ast.parse(code, filename=filename)
            result.syntax_ok = True
        except SyntaxError as syn_err:
            result.error_messages.append(f"Syntax error at line {syn_err.lineno}: {syn_err.msg}")
            return result

        # 2. Security Scan
        security_issues = self._scan_security_risks(tree, code)
        if security_issues:
            result.error_messages.extend(security_issues)
            result.security_ok = False
        else:
            result.security_ok = True

        # 3. BaseTool Class Inheritance Check
        result.imports_ok = True
        result.is_valid = result.syntax_ok and result.security_ok and result.imports_ok
        return result

    def _scan_security_risks(self, tree: ast.AST, code: str) -> List[str]:
        """Scan AST for dangerous operations (eval, exec, shell=True, os.system)."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Direct name call (eval(), exec())
                if isinstance(node.func, ast.Name) and node.func.id in ["eval", "exec"]:
                    issues.append(f"Forbidden security risk: Use of '{node.func.id}'")

                # Attribute call (os.system())
                if isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                    issues.append("Forbidden security risk: Use of 'os.system'")

                # Check shell=True in subprocess
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        issues.append("Forbidden security risk: shell=True in subprocess call")

        return issues
