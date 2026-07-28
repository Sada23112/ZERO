"""Project ZERO — Evolution Engine Package (Phase 5)."""

from evolution.metadata import CapabilityMetadata, EvolutionStepLog
from evolution.history import EvolutionHistoryStore, EvolutionHistoryRecord
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
from evolution.diagnostics import SelfImprovementDiagnostics, ImprovementSuggestion
from evolution.rollback import RollbackEngine
from evolution.engine import EvolutionEngine, EvolutionEngineResult

__all__ = [
    "CapabilityMetadata",
    "EvolutionStepLog",
    "EvolutionHistoryStore",
    "EvolutionHistoryRecord",
    "CapabilityRegistryStore",
    "CapabilityDetector",
    "CapabilityDetectionResult",
    "EvolutionPlanner",
    "EvolutionPlan",
    "ArchitecturalGenerator",
    "CapabilityArchitecturalSpec",
    "DependencyManager",
    "CodeGenerator",
    "TestGenerator",
    "ExecutionSandbox",
    "CapabilityValidator",
    "ValidationResult",
    "ChangeReviewer",
    "ChangeReview",
    "CapabilityInstaller",
    "SelfRepairEngine",
    "RepairReport",
    "SelfImprovementDiagnostics",
    "ImprovementSuggestion",
    "RollbackEngine",
    "EvolutionEngine",
    "EvolutionEngineResult",
]
