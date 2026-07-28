"""Project ZERO — Self Diagnostics & System Health Checker (Phase 4 Capability #20)."""

import os
from pathlib import Path
from typing import Dict, Any, List
from config import get_settings
from memory.database import DatabaseManager
from providers.registry import provider_registry
from tools.registry import tool_registry
from pydantic import BaseModel, Field


class DiagnosticReport(BaseModel):
    """Structured report of system health and diagnostic checks."""

    database_healthy: bool = False
    provider_healthy: bool = False
    registered_tools_count: int = 0
    workspace_readable: bool = False
    workspace_writable: bool = False
    issues_found: List[str] = Field(default_factory=list)


class SelfDiagnostics:
    """Performs system health audits across database, providers, tools, and workspace permissions."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def run_health_check(self) -> DiagnosticReport:
        """Run full system health audit."""
        report = DiagnosticReport()

        # 1. Database Check
        try:
            settings = get_settings()
            db = DatabaseManager(settings.database_path)
            conn = db.get_connection()
            conn.execute("SELECT 1")
            report.database_healthy = True
        except Exception as err:
            report.issues_found.append(f"Database health check failed: {err}")

        # 2. Provider Check
        try:
            if provider_registry.get_provider("gemini"):
                report.provider_healthy = True
        except Exception as err:
            report.issues_found.append(f"Provider health check failed: {err}")

        # 3. Tools Check
        report.registered_tools_count = len(tool_registry.list_tools())

        # 4. Workspace Permission Check
        report.workspace_readable = os.access(self.workspace_root, os.R_OK)
        report.workspace_writable = os.access(self.workspace_root, os.W_OK)

        if not report.workspace_writable:
            report.issues_found.append(f"Workspace directory {self.workspace_root} is not writable.")

        return report
