"""Project ZERO — Provider Registry System."""

from typing import Dict, Optional, List
from providers.base import BaseProvider
from zero_logging import logger


class ProviderRegistry:
    """Registry managing LLM providers."""

    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {}

    def register_provider(self, provider: BaseProvider) -> None:
        """Register a provider instance."""
        self._providers[provider.name.lower()] = provider
        logger.debug(f"Registered provider: {provider.name}")

    def get_provider(self, name: str) -> Optional[BaseProvider]:
        """Fetch provider by name."""
        return self._providers.get(name.lower())

    def list_providers(self) -> List[str]:
        """List registered provider names."""
        return list(self._providers.keys())


# Singleton Provider Registry instance
provider_registry = ProviderRegistry()
