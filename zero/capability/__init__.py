"""Project ZERO — Capability Package.

Provides dynamic capability architecture, runtime loading, hot reloading, provider factory,
self-installer, dynamic configuration, migrations, rollback, and runtime API.
"""

from zero.capability.registry import CapabilityRegistry, CapabilityCategory, CapabilityManifest
from zero.capability.dependency_graph import DependencyGraph
from zero.capability.runtime_loader import RuntimeLoader
from zero.capability.hot_reload import HotReloader
from zero.capability.plugin_loader import PluginLoader
from zero.capability.provider_factory import ProviderFactory
from zero.capability.validator import CapabilityValidator, ValidationResult
from zero.capability.installer import CapabilityInstaller
from zero.capability.configurator import CapabilityConfigurator
from zero.capability.migration import CapabilityMigrationManager
from zero.capability.rollback import CapabilityRollbackEngine
from zero.capability.marketplace import CapabilityMarketplace
from zero.capability.capability_manager import CapabilityManager, capability_manager

__all__ = [
    "CapabilityCategory",
    "CapabilityManifest",
    "CapabilityRegistry",
    "DependencyGraph",
    "RuntimeLoader",
    "HotReloader",
    "PluginLoader",
    "ProviderFactory",
    "CapabilityValidator",
    "ValidationResult",
    "CapabilityInstaller",
    "CapabilityConfigurator",
    "CapabilityMigrationManager",
    "CapabilityRollbackEngine",
    "CapabilityMarketplace",
    "CapabilityManager",
    "capability_manager",
]
