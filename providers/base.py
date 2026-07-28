"""Project ZERO — Base Provider Abstract Interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from models.model import DiscoveredModel
from models.conversation import Message


class BaseProvider(ABC):
    """Abstract interface for LLM provider integrations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider unique name (e.g. 'gemini', 'openai')."""
        pass

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate response from provider given conversation messages."""
        pass

    @abstractmethod
    async def discover_models(self, force_refresh: bool = False) -> List[DiscoveredModel]:
        """Dynamically fetch available models from provider API."""
        pass
