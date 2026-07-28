"""Project ZERO — Base Connector Abstract Interface.

Every external service connector implements this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Optional


class BaseConnector(ABC):
    """Abstract interface for external service connectors."""

    @property
    @abstractmethod
    def service_type(self) -> str:
        """Service identifier (e.g. 'google_gmail', 'github', 'spotify')."""
        pass

    @abstractmethod
    def connect(self, credentials: Dict[str, Any]) -> Tuple[bool, str]:
        """Establish connection with credentials."""
        pass

    @abstractmethod
    def disconnect(self) -> Tuple[bool, str]:
        """Disconnect and revoke active session."""
        pass

    @abstractmethod
    def health_check(self) -> Tuple[bool, str]:
        """Verify API connectivity and credential validity."""
        pass

    @abstractmethod
    def supported_capabilities(self) -> List[str]:
        """List capabilities provided by connector."""
        pass
